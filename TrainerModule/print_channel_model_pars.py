import h2o
from EstimatorModule import PredictionsManager, Estimator
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training
from db_tools import rpccurrml
from db_tools import base as dbase
from datetime import datetime

def print_pars(conf_name,dpid):
    
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf = mconf_manager.get_by_name(conf_name)
    
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)
    
    model = model_manager.get_by_modelconf_id_dpid(mconf.modelconf_id,dpid)
    
    hv_curr_estimator = Estimator.Estimator(model)
    
    h2o_model = hv_curr_estimator.h2omodel

    print(h2o_model._model_json['output']['coefficients_table'])

    return True

