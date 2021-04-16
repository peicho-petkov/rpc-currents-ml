from db_tables import table_predicted_current
from NotificationModule import NotificationManager
from TrainerModule import DataManager
from Configuration import Configuration
from db_tools import base as dbase
from datetime import datetime

def analyse_predictions(model_id, dpid, start_date, end_date, rpccurrml):
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
    rolling_window = conf.GetParameter("rolling_window")
    persistence_time = conf.GetParameter("persistence_time")
    soft_limit = conf.GetParameter("soft_limit")
    hard_limit = conf.GetParameter("hard_limit")
  
    notmanager = NotificationManager.NotificationManager(rpccurrml, rolling_window)
    notmanager.set_soft_limit(soft_limit)
    notmanager.set_hard_limit(hard_limit)
    notmanager.set_persistence_time(persistence_time)
    notmanager.load_data(data)
    
    for message, timestamp, avgdiff in notmanager.analyse():    
        myquery=table_notifications.get_insert_notification_query(dpid,model_id, message, timestamp, avgdiff,1 ,0 ,0)
        rpccurrml.execute_commit_query_self(myquery)

