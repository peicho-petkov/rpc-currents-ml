from db_tools import table_predicted_current, table_training, table_mlmodels, table_mlmodelsconf, table_configuration
from db_tools import base as dbase 
from db_tools import rpccurrml
from TrainerModule import MLModelManager 
from Configuration import Configuration
from optparse import OptionParser
import predict_for_hv_channel_method
import analyse_for_period
from datetime import datetime
import h2o

def perform_prediction(start_date, end_date):
    query = table_mlmodels.get_get_active_model_ids_query()
    print(query)
    active_model_ids = rpccurrml.fetchall_for_query_self(query)
    active_model_ids = [i[0] for i in active_model_ids]
    print(active_model_ids)
    conf = Configuration(rpccurrml)
    flag = conf.GetParameter("flag")

    h2o.init()

    for model_id in active_model_ids:
        ok = predict_for_hv_channel_method.predict(model_id, flag, start_date, end_date)
        if not ok:
            print(f"No data for {model_id} in period {start_date} to {end_date}")
            continue
