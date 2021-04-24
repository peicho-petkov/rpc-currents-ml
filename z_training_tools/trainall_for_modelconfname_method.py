from db_tools import table_mlmodelsconf, table_mlmodels, table_training, table_configuration
from db_tools import rpccurrml
from TrainerModule import MLModelManager
import train_hv_channel_method
from Configuration import Configuration
import h2o

def trainall(modelconf_name):
    modelconfmanager = MLModelManager.MLModelsConfManager(rpccurrml, table_mlmodelsconf)
    model_conf = modelconfmanager.get_by_name(modelconf_name)

    train_start_date = model_conf.train_from            
    train_end_date = model_conf.train_to               

    conf = Configuration(rpccurrml)
    mojopath = conf.GetParameter("mojopath") 
    modelpath = conf.GetParameter("modelpath") 
    flag = int(conf.GetParameter("flag"))

    query = table_training.get_get_all_dpids_query()  # Maybe select only some dpids
    dpids = rpccurrml.fetchall_for_query_self(query)
    dpids = [i[0] for i in dpids] 

    h2o.init()

    for dpid in dpids:
        train_hv_channel_method.train(modelconf_name, dpid, flag, mojopath, modelpath)
