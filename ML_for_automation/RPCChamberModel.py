import h2o
from db_tools import table_training, table_mlmodelsconf, table_mlmodels, automation_db
from db_tools import base as dbase
from TrainerModule import MLTrainer, DataManager
from TrainerModule.MLTrainer import MLTrainer
from TrainerModule.MLModelManager import MLModelsManager, MLModelsConfManager
  
extractor_table_training = DataManager.Extractor_Oracle(table_training.tablename, automation_db)
extractor_table_training.set_flag_col_name(table_training.flag)
extractor_table_training.set_chid_col_name(table_training.chid)

mconf_manager = MLModelsConfManager(automation_db,table_mlmodelsconf)
model_manager = MLModelsManager(automation_db,table_mlmodels)
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
        extractor_table_training.set_select_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+extra_cols_list)
    else:
        extractor_table_training.set_select_column_name_list(str(mconf.input_cols).split(',')+str(mconf.output_cols).split(',')) 
    extractor_table_training.set_time_widow(mconf.train_from,mconf.train_to)

def get_for_chid(chid,flag):
    extractor_table_training.set_CHID(chid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_chid_flag_query()
    data = automation_db.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1:
        return None
    model = trainer.train_model_for_chid(extractor_table_training._CHID,data)
    return model

def get_refined_for_chid(chid,flag,scale_sd=5.0):
    extractor_table_training.set_CHID(chid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_chid_flag_query()
    data = automation_db.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1:
        return None
    model = trainer.train_and_refine_model_for_chid(extractor_table_training._CHID,data,scale_sd=scale_sd)
    return model


def validate_get_for_chid(chid,flag):
    extractor_table_training.set_CHID(chid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_chid_flag_query()
    data = automation_db.fetchall_for_query_self(query)
    print(mconf.test_from,mconf.test_to)
    extractor_table_training.set_time_widow(mconf.test_from,mconf.test_to)
    query = extractor_table_training.get_data_by_chid_flag_query()
    test_data = automation_db.fetchall_for_query_self(query)
    # check if len data > 0
    if len(data) < 1 and len(test_data) < 1:
        return None
    model = trainer.train_and_test_model_for_chid(extractor_table_training._CHID,data,test_data)
    return model

def train_and_register_for_chid(chid,flag,forceupdate=False):
    model = get_for_chid(chid,flag)
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

def train_refined_and_register_for_chid(chid,flag,scale_sd=5.0,forceupdate=False):
    model = get_refined_for_chid(chid,flag,scale_sd=scale_sd)
    print("model type ", type(model))
    if model is None:
        return -2
    model_id = model_manager.RegisterMLModel(model)
    if model_id < 0 and forceupdate:
        model_id = model_manager.UpdateRegistedMLModel(model)
    return model_id

def train_validate_and_register_for_chid(chid,flag,forceupdate=False):
    model = validate_get_for_chid(chid,flag)
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
    model_ids = []

    chids = [int(vv) for vv in mconf.output_cols.replace('chid','').split(',')]

    for chid in chids:
        model.chid = chid
        model_id = model_manager.RegisterMLModel(model)
        if model_id < 0 and forceupdate:
            model_id = model_manager.UpdateRegistedMLModel(model)
        model_ids.append(model_id)

    return model_ids[:],chids[:]

if __name__ == '__main__':
    h2o.init()
    init('initial_test')
    chid = 315
    flag = 56
    model_id = train_and_register_for_chid(chid,flag,True)
    if model_id < 0:
        print(f"a model configuration with name {mconf.name} already registered for CHID {chid}...")

