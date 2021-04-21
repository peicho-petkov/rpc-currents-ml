from db_tools import table_predicted_current, table_training, table_mlmodels, table_mlmodelsconf, table_configuration
from db_tools import base as dbase 
from db_tools import rpccurrml
from Configuration import Configuration
from optparse import OptionParser
from z_analysis_tools import analyse_for_period
from datetime import datetime

def perform_analysis(start_date, end_date):
    start_date = options.start_date
    end_date = options.end_date

    query = table_mlmodels.get_get_active_model_ids_and_dpids_query()
    print(query)
    active_model_ids = rpccurrml.fetchall_for_query_self(query)
    active_model_ids = [(i[0],i[1]) for i in active_model_ids]
    print(active_model_ids)
    conf = Configuration(rpccurrml)
    flag = conf.GetParameter("flag")

    for model_id, dpid in active_model_ids:
        print(f"The dpid is: {dpid}")
        try:
            print(f"Search for warnings/errors in this prediction period begins for model_id {model_id}")
            analyse_for_period.analyse_prediction(model_id, dpid, start_date, end_date, rpccurrml)
            print(f"Warning/error analysis ended for this prediction period for model_id {model_id}")
        except Exception as e:
            print(e)
            continue

