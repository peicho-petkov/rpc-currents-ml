#!/usr/bin/env python3
from optparse import OptionParser
from db_tools import base as dbase
from datetime import datetime
from db_tools import table_predicted_current, rpccurrml
from TrainerModule import DataManager 
import pandas as pd 
from Misc import plotter


if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-id", action="store", type="int", dest="model_id", default=-1,
                        help="The model_id of the model used to make the prediction, integer")
    oparser.add_option("--model-conf-name", action="store", type="string", dest="conf_name",
                        default="", help="Select model by model configuration name")
    oparser.add_option("--dpid", action="store", type="int", dest="DPID",
                        default=-1, help="Select model by dpid")
    oparser.add_option("--pred-start-date", action="store", type="string", dest="start_date",
                        help="The beginning of the prediction period you want to plot [yyyy-mm-dd]")
    oparser.add_option("--pred-end-date", action="store", type="string", dest="finish_date", 
                        help="The end of the prediction period you want to plot [yyyy-mm-dd]") 
    oparser.add_option("--file-for-plots", action="store", type="string", dest="filename",
                        default="", help="Enter the file name where you want the plots stored")

    (options, args) = oparser.parse_args()

    model_id = options.model_id
    modelconf_name = options.conf_name
    dpid = options.DPID 
    start_date = datetime.strptime(options.start_date, '%Y-%m-%d')
    finish_date = datetime.strptime(options.finish_date, '%Y-%m-%d')
    filename = options.filename

    if dpid < 0 and modelconf_name == "" and model_id < 0:
        print("To choose a model, specify --dpid and --modelconf_id or --model_id!")

    if model_id < 0:
        query = f" select MLModels.model_id from MLModels, MLModelsConf where MLModels.MODELCONF_ID=MLModelsConf.modelconf_id and MLModelsConf.NAME='{modelconf_name}' and MLModels.dpid={dpid}"
        print(query)
        model_id = rpccurrml.fetchall_for_query_self(query)
        if len(model_id) > 1:
            print(f"************************************************************")
            print(f"* ERROR: More than 1 model_ids found... Probably a bug!... *")
            print(f"************************************************************")
            exit(1)
        if len(model_id) == 0:
            
            print(f'''*************************************************************
* ERROR: No suitable models found for                       *   
* conf name {modelconf_name:24} and dpid {dpid:10}!...*
*************************************************************''')
            
            exit(1)
        model_id = model_id[0][0]

    extractor_pred_curr_table = DataManager.Extractor_MySql(table_predicted_current.tablename, rpccurrml)
    extractor_pred_curr_table.set_column_name_list(["predicted_for", "predicted_value", "measured_value"])
    extractor_pred_curr_table.set_timestamp_col('predicted_for')
    extractor_pred_curr_table.set_time_widow(start_date, finish_date)
    extractor_pred_curr_table.set_model_id_col_name()
    extractor_pred_curr_table.set_model_id(model_id)
    extractor_pred_curr_table.set_dpid_col_name('dpid')
    extractor_pred_curr_table.set_DPID(dpid)
   

    query = extractor_pred_curr_table.get_data_by_model_id_query()
    print(query)
    data = rpccurrml.fetchall_for_query_self(query)

    if len(data) == 0:
        print("**************************************")
        print("* ERROR: no prediction data found... *")
        print("**************************************")
        exit(1)

    plotter = plotter.simple_plotter({0:"predicted_for",1:"predicted_value",2:"measured_value"},data)
    plotter.plot_diff_opt(filename="diff-"+filename)
    plotter.plot_run_avg(filename="run-avg-"+filename)
    plotter.plot_it(filename=filename)
    
