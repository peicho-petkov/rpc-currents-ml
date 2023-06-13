from tensorflow import keras
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.callbacks import TensorBoard

# with open('test.csv') as indata:
#     header = True
#     for line in indata:
#         if header:
#             header = not header
#             continue
#         line = line.split(',')
#         line = map(lambda x : float(x),line[:-2])
#         print(list(line))

# indata = np.loadtxt('test.csv',skiprows=1,delimiter=',',
#                     usecols=[x for x in range(480)],
#                     max_rows=200000)

array_file = open('array.npy', 'rb')
indata = np.load(array_file)
array_file.close()

x_train = indata[:150000]
x_test  = indata[150000:200000]

print(x_train.shape)
print(x_test.shape)

input_img = keras.Input(shape=(x_train.shape[-1],))
encoded = layers.Dense(512, activation='relu')(input_img)
encoded = layers.Dense(128, activation='relu')(encoded)
encoded = layers.Dense(64, activation='relu')(encoded)
#encoded = layers.Dense(8, activation='relu')(encoded)

decoded = layers.Dense(128, activation='relu')(encoded)
decoded = layers.Dense(512, activation='relu')(decoded)
#decoded = layers.Dense(64, activation='relu')(decoded)
decoded = layers.Dense(x_train.shape[-1], activation='relu')(decoded)

loss_fn = keras.losses.MeanSquaredError()

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss=loss_fn)

autoencoder.summary()

autoencoder.fit(x_train, x_train,
                epochs=300,
                batch_size=1024,
                shuffle=True,
                validation_data=(x_test, x_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])

autoencoder.save('saved_model/512_128_64')
