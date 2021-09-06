from db_tools import table_predicted_current, table_training, table_mlmodels, table_mlmodelsconf, table_configuration
from db_tools import base as dbase 
from db_tools import rpccurrml
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from TrainerModule import MLModelManager 
from Configuration import Configuration
from optparse import OptionParser
from z_prediction_tools import predict_for_hv_channel_method
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

    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)

    autoenc_models_dict = {}

    for model_id in active_model_ids:
        model = model_manager.get_by_model_id(model_id=model_id)
            
        mconf = mconf_manager.get_by_modelconf_id(model.modelconf_id)

        if 'AUTOENC' in mconf.mlclass:
            if not (mconf.modelconf_id in autoenc_models_dict):
                autoenc_models_dict[mconf.modelconf_id] = []
            autoenc_models_dict[mconf.modelconf_id].append((model)
        else:
            ok = predict_for_hv_channel_method.predict(model_id, flag, start_date, end_date)
            if not ok:
                print(f"No data for {model_id} in period {start_date} to {end_date}")
                continue

    for mconf_id in autoenc_models_dict:
        models = autoenc_models_dict[mconf_id]
        ok = predict_for_hv_channel_method.predict_autoencoder(models, flag, start_date, end_date):
        if not ok:
            print(f"No data for model conf id {mconf_id} in period {start_date} to {end_date}")
            continue 