from db_tools import table_predicted_current
from db_tools import base as dbase
from datetime import datetime

class PredictionsManager:
    def __init__(self, db_conn, model_id, dpid):
        self.model_id = model_id
        self.dpid = dpid
        self.db_conn = db_conn
        #self.db_conn.self_cursor_mode()
        
    def insert_record(self,prediction_datetime,prediction, prediction_err, measured_val):
        query = table_predicted_current.get_insert_query(self.model_id,self.dpid,prediction_datetime,prediction,prediction_err,measured_val)
        print(query)
        #self.db_conn.execute_query_self(query)
        
    def commit_records(self):
        #self.db_conn.execute_commit_self()
        pass
        

if __name__ == '__main__':
    rpccurrml = dbase.mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML') 
      
    pm = PredictionsManager(rpccurrml,-777,-315)
    pm.insert_record(datetime(2018,7,17,15,33,21),-15,-4,-5)
    
    pm.commit_records()
