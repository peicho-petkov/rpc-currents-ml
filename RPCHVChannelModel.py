import h2o
from db_tools import table_training, table_mlmodelsconf, table_mlmodels
from db_tools import base as dbase
from TrainerModule import MLTrainer, DataManager, MLModelsManager, MLModelsConfManager

rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
rpccurrml.connect_to_db('RPCCURRML')    
extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)

mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
model_manager = MLModelsManager(rpccurrml,table_mlmodels)
print(type(table_mlmodels))

def init(model_conf_name,mlmodels_path=".",mojofiles_path="."):
    global trainer
    global mconf
    mconf = mconf_manager.get_by_name(model_conf_name)
    trainer = MLTrainer(mconf,mlmodels_path,mojofiles_path)
    if mconf is None:
        raise Exception(f"ML Configuration {model_conf_name} is not registered...")
    extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(','))
    extractor_table_training.set_time_widow(mconf.train_from,mconf.train_to)

def get_for_dpid(dpid,flag):
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)
    model = trainer.train_model_for_dpid(extractor_table_training._DPID,data)
    return model


def train_and_register_for_dpid(dpid,flag,forceupdate=False):
    model = get_for_dpid(dpid,flag)
    print("model type ", type(model))
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

