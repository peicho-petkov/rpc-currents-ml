from db_tools import table_predicted_current, table_notifications
from NotificationModule import NotificationManager
from TrainerModule import DataManager
from Configuration import Configuration
from db_tools import base as dbase
from datetime import datetime

def analyse_prediction(model_id, dpid, start_date, end_date, rpccurrml):
    if type(start_date) is str:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if type(end_date) is str:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    extractor_pred_curr_table = DataManager.Extractor_MySql(table_predicted_current.tablename, rpccurrml)
    extractor_pred_curr_table.set_column_name_list(["predicted_for", "predicted_value", "measured_value"])
    extractor_pred_curr_table.set_timestamp_col('predicted_for')
    extractor_pred_curr_table.set_dpid_col_name('dpid')
    extractor_pred_curr_table.set_DPID(dpid)
    extractor_pred_curr_table.set_model_id_col_name('model_id')
    extractor_pred_curr_table.set_model_id(model_id)
    extractor_pred_curr_table.set_time_widow(start_date, end_date)

    query=extractor_pred_curr_table.get_data_by_model_id_query()
    data=rpccurrml.fetchall_for_query_self(query)

    conf = Configuration(rpccurrml)
    rolling_window = int(conf.GetParameter("rolling_window"))
    persistence_time = int(conf.GetParameter("persistence_time"))
    soft_limit = float(conf.GetParameter("soft_limit"))
    hard_limit = float(conf.GetParameter("hard_limit"))
    print(f"\n The rolling window is: {rolling_window}")
    print(f"\n The persistence time is: {persistence_time}")
    print(f"\n The soft limit is: {soft_limit}")
    print(f"\n The hard limit is: {hard_limit}") 
 
    notmanager = NotificationManager.NotificationManager(rpccurrml, rolling_window)
    notmanager.set_soft_limit(soft_limit)
    notmanager.set_hard_limit(hard_limit)
    notmanager.set_persistence_time(persistence_time)
    notmanager.load_data(data)
    
    for message, timestamp, avgdiff in notmanager.analyse():    
        myquery=table_notifications.get_insert_notification_query(dpid,model_id, message, timestamp, avgdiff,1 ,0 ,0)
        rpccurrml.execute_commit_query_self(myquery)

