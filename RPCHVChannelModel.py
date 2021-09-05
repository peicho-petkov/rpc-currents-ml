from z_training_tools.train_hv_channel_method import train
import h2o
from db_tools import table_training, table_mlmodelsconf, table_mlmodels, rpccurrml
from db_tools import base as dbase
from TrainerModule import MLTrainer, DataManager, MLModelsManager, MLModelsConfManager
  
extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)

mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
model_manager = MLModelsManager(rpccurrml,table_mlmodels)
print(type(table_mlmodels))

def init(model_conf_name,mlmodels_path=".",mojofiles_path="."):
    global trainer
    global mconf
   
    mconf = mconf_manager.get_by_name(model_conf_name)
    
    extra_cols_list = None
    if mconf.mlclass == 'GLM_V4':
        extra_cols_list = [table_training.vmon]
    
    trainer = MLTrainer(mconf,mlmodels_path,mojofiles_path,extra_cols_list)
    
    if mconf is None:
        raise Exception(f"ML Configuration {model_conf_name} is not registered...")
    if extra_cols_list is not None:
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+extra_cols_list)
    else:
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')) 
    extractor_table_training.set_time_widow(mconf.train_from,mconf.train_to)

def get_for_dpid(dpid,flag):
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1:
        return None
    model = trainer.train_model_for_dpid(extractor_table_training._DPID,data)
    return model

def get_refined_for_dpid(dpid,flag,scale_sd=5.0):
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1:
        return None
    model = trainer.train_and_refine_model_for_dpid(extractor_table_training._DPID,data,scale_sd=scale_sd)
    return model


def validate_get_for_dpid(dpid,flag):
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)
    print(mconf.test_from,mconf.test_to)
    extractor_table_training.set_time_widow(mconf.test_from,mconf.test_to)
    query = extractor_table_training.get_data_by_dpid_flag_query()
    test_data = rpccurrml.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1 and len(test_data) < 1:
        return None
    model = trainer.train_and_test_model_for_dpid(extractor_table_training._DPID,data,test_data)
    return model

def train_and_register_for_dpid(dpid,flag,forceupdate=False):
    model = get_for_dpid(dpid,flag)
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

def train_refined_and_register_for_dpid(dpid,flag,scale_sd=5.0,forceupdate=False):
    model = get_refined_for_dpid(dpid,flag,scale_sd=scale_sd)
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

def train_validate_and_register_for_dpid(dpid,flag,forceupdate=False):
    model = validate_get_for_dpid(dpid,flag)
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

def train_and_register_autoencoder(forceupdate=False):
    model = trainer.train_autoencoder()
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

if __name__ == '__main__':
    h2o.init()
    init('initial_test')
    dpid = 315
    flag = 56
    model_id = train_and_register_for_dpid(dpid,flag,True)
    if model_id < 0:
        print(f"a model configuration with name {mconf.name} already registered for DPID {dpid}...")

