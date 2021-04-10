from db_tools import table_notifications, table_predicted_current
from NotificationModule import NotificationManager
from TrainerModule import DataManager
from db_tools import rpccurrml
from db_tools import base as dbase
from datetime import datetime

rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
rpccurrml.connect_to_db('RPCCURRML')
rpccurrml.self_cursor_mode()


extractor_pred_curr_table = DataManager.Extractor_MySql(table_predicted_current.tablename, rpccurrml)
extractor_pred_curr_table.set_column_name_list(["predicted_for", "predicted_value", "measured_value"])
extractor_pred_curr_table.set_timestamp_col('predicted_for')
extractor_pred_curr_table.set_dpid_col_name('dpid')
extractor_pred_curr_table.set_DPID(317)
extractor_pred_curr_table.set_model_id_col_name('model_id')
extractor_pred_curr_table.set_model_id(4)
start_date=datetime.strptime('2016-05-06','%Y-%m-%d')
end_date=datetime.strptime('2016-06-30','%Y-%m-%d')
extractor_pred_curr_table.set_time_widow(start_date,end_date)

query=extractor_pred_curr_table.get_data_by_model_id_query()
data=rpccurrml.fetchall_for_query_self(query)

notmanager = NotificationManager.NotificationManager(rpccurrml,table_predicted_current,10)
notmanager.set_soft_limit(1)
notmanager.set_hard_limit(3)
notmanager.set_persistence_time(100)
notmanager.load_data(data)
# notmanager.analyse()
for message, timestamp, avgdiff in notmanager.analyse():    
    myquery=table_notifications.get_insert_notification_query(317,4,message,timestamp,avgdiff,1,0,0)
    rpccurrml.execute_commit_query_self(myquery)

