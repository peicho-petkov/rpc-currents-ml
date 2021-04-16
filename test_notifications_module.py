#!/usr/bin/env python3
from db_tools import table_notifications, table_predicted_current, rpccurrml
from NotificationModule import NotificationManager
from TrainerModule import DataManager
from db_tools import rpccurrml
from Configuration import Configuration
from db_tools import base as dbase
from datetime import datetime
from optparse import OptionParser

if __name__ == "__main__":
    oparser = OptionParser()
    oparser.add_option("--model-id", action="store", type="int", dest="model_id", default=-1,
                        help="The model_id of the model you want to analyse, integer")
    oparser.add_option("--dpid", action="store", type="int", dest="dpid",
                        help="The dpid of the hv channel you want to analyse, integer")
    oparser.add_option("--start-date", action="store", type="string", dest="start_date", 
                        help="The starting date of the period you want to analyse")
    oparser.add_option("--end-date", action="store", type="string", dest="end_date", 
                        help="The end date of the period you want to analyse")
    
    (options, args) = oparser.parse_args()
    model_id = options.model_id
    dpid = options.dpid
    start_date = datetime.strptime(options.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(options.end_date, '%Y-%m-%d')

    rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
    rpccurrml.connect_to_db('RPCCURRML')
    rpccurrml.self_cursor_mode()


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

