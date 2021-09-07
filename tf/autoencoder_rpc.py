from db_tools import table_autoencoderData, rpccurrml
from datetime import datetime, timedelta
from tensorflow import keras
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.callbacks import TensorBoard

def mysql_buffer_to_float_np_array(buffer):
    array = np.array(buffer,dtype=np.float)
    return array

def mysql_buffer_to_datetime_np_array(buffer):
    array = np.array(buffer,dtype='datetime64')
    return array

class AE_DataManager:
    def __init__(self, dbcon = rpccurrml):
        self.dbcon = dbcon
        self.dbcon.self_cursor_mode()
        self.from_datetime = None
        self.to_datetime = None
        
    def set_time_window(self, from_datetime, to_datetime):
        if type(from_datetime) is str:
            from_datetime = datetime.strptime(from_datetime, '%Y-%m-%d %H:%M:%S')
        if type(to_datetime) is str:
            to_datetime = datetime.strptime(to_datetime, '%Y-%m-%d %H:%M:%S')
        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        
    def get_dataframe(self,tdelta_days=2):
        if self.from_datetime is None or self.to_datetime is None:
            raise Exception("AE_DataManger: calling get_dataframe without setting the time_window. Call set_time_window before getting data.")
        start_date = self.from_datetime
        
        while start_date + timedelta(days=tdelta_days) < self.to_datetime:
            end_date = start_date + timedelta(days=tdelta_days)
            q = table_autoencoderData.get_data_for_timeperiod_query(start_date,end_date)
            start_date = end_date
            dataset = self.dbcon.fetchall_for_query_self(q)
            array = None
            date_array = None
            for rec in dataset:
                if array is None:
                    array = mysql_buffer_to_float_np_array([rec[1:]])
                    date_array = mysql_buffer_to_datetime_np_array([rec[0]]) 
                else:
                    array = np.append(array,mysql_buffer_to_float_np_array([rec[1:]]),axis=0)
                    date_array = np.append(date_array,mysql_buffer_to_datetime_np_array([rec[0]]),axis=0)
                #yield array, date_array
            if array is None:
                continue
            print(f"yield {len(dataset)} array len {len(array)} array shape {array.shape} date array shape {date_array.shape} last date {date_array[-1]}")
            yield array, date_array
            
        q = table_autoencoderData.get_data_for_timeperiod_query(start_date,self.to_datetime)
        dataset = self.dbcon.fetchall_for_query_self(q)
        array = None
        date_array = None
        for rec in dataset:
            if array is None:
                array = mysql_buffer_to_float_np_array([rec[1:]])
                date_array = mysql_buffer_to_datetime_np_array([rec[0]]) 
            else:
                array = np.append(array,mysql_buffer_to_float_np_array([rec[1:]]),axis=0)
                date_array = np.append(date_array,mysql_buffer_to_datetime_np_array([rec[0]]),axis=0)
                #yield array, date_array
        if array is not None:
            print(f"yield {len(dataset)} array len {len(array)} array shape {array.shape}  last date {date_array[-1]}")
            yield array, date_array
        
class RPCAutoencoder:
    def __init__(self, n_inputs):
        self.n_inputs = n_inputs
        input_img = keras.Input(shape=(self.n_inputs,))
        encoded = layers.Dense(512, activation='relu')(input_img)
        encoded = layers.Dense(128, activation='relu')(encoded)
        encoded = layers.Dense(64,  activation='relu')(encoded)

        decoded = layers.Dense(128, activation='relu')(encoded)
        decoded = layers.Dense(512, activation='relu')(decoded)
        
        decoded = layers.Dense(self.n_inputs, activation='relu')(decoded)

        loss_fn = keras.losses.MeanSquaredError()

        self.autoencoder = keras.Model(input_img, decoded)
        self.autoencoder.compile(optimizer='adam', loss=loss_fn)

        self.autoencoder.summary()

    def train(self,training_dataset,validation_dataset):
        # self.autoencoder.fit(training_dataset, training_dataset,
        #         epochs=300,
        #         #batch_size=1024,
        #         #shuffle=True,
        #         validation_data=(validation_dataset, validation_dataset),
        #         callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])
        self.autoencoder.fit(training_dataset, training_dataset,
                             epochs=100)



if __name__ == '__main__':
    ae = AE_DataManager()
    ae.set_time_window(datetime(2018,6,1),datetime(2018,8,15))
    for ds,dateds in ae.get_dataframe():
        print(f'ds {len(ds)}')
