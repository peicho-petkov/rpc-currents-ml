#!/usr/bin/env python3
from optparse import OptionParser
from db_tools import base as dbase
from datetime import datetime
from db_tools import table_predicted_current
from TrainerModule import DataManager 
import pandas as pd 
from Misc import plotter


if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-id", action="store", type="int", dest="model_id", 
                        help="The model_id of the model used to make the prediction, integer")
    oparser.add_option("--pred-start-date", action="store", type="string", dest="start_date",\
                        help="The beginning of the prediction period you want to plot [yyyy-mm-dd]")
    oparser.add_option("--pred_finish-date", action="store", type="string", dest="finish_date", 
                        help="The end of the prediction period you want to plot [yyyy-mm-dd]") 
    
    (options, args) = oparser.parse_args()

    model_id = options.model_id
    start_date = datetime.strptime(options.start_date, '%Y-%m-%d')
    finish_date = datetime.strptime(options.finish_date, '%Y-%m-%d')

    rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
    rpccurrml.connect_to_db('RPCCURRML')

    extractor_pred_curr_table = DataManager.Extractor_MySql(table_predicted_current.tablename, rpccurrml)
    extractor_pred_curr_table.set_column_name_list("predicted_for", "predicted_value", "measured_value")
    extractor_pred_curr_table.set_timestamp_col('predicted_for')
    extractor_pred_curr_table.set_time_widow(start_date, finish_date)

    query = extractor_pred_curr_table.get_data_query()
    data = rpccurrml.fetchall_for_query_self(query)

    plotter = plotter.simple_plotter({0:"predicted_for",1:"predicted_value",2:"measured_value"},data)
    plotter.plot_it()










