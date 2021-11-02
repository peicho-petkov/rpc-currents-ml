#!/usr/bin/env python3

from db_tools import table_mlmodelsconf, table_predicted_current, table_mlmodels, table_training, table_configuration, rpccurrml
from db_tools import base as dbase
from TrainerModule import DataManager
from TrainerModule import MLModelManager
from optparse import OptionParser
import train_hv_channel_method
from Configuration import Configuration
import h2o

if __name__ == "__main__":
    oparser = OptionParser()
    oparser.add_option("--modelconf-name", action="store", type="string", dest="modelconf_name",
                        help="The modelconfname of the models you want to train")

    (options, args) = oparser.parse_args()
    modelconf_name = options.modelconf_name
    
    # rpccurrml = dbase.mysql_dbConnector(host="rpccurdevml", user="ppetkov", password="cmsrpc")
    # rpccurrml.connect_to_db("RPCCURRML")
    # rpccurrml.self_cursor_mode()

    # modelmanager = MLModelManager.MLModelsManager(rpccurrml, table_mlmodels)
    # model_conf_obj_and_ids = modelmanager.set_mlmodels_active_state(table_mlmodelsconf, modelconf_name)
    # model_conf = model_conf_obj_and_ids[0]
    # model_ids = model_conf_obj_and_ids[1]
    
    modelconfmanager = MLModelManager.MLModelsConfManager(rpccurrml, table_mlmodelsconf)
    model_conf = modelconfmanager.get_by_name(modelconf_name)

    train_start_date = model_conf.train_from            # options.change_date_start
    train_end_date = model_conf.train_to                # options.change_date_end

    conf = Configuration(rpccurrml)
    mojopath = conf.GetParameter("mojopath") 
    modelpath = conf.GetParameter("modelpath") 
    flag = int(conf.GetParameter("flag"))

    if "AUTOENC" in model_conf.mlclass:
        train_hv_channel_method.train(modelconf_name, -1, flag, mojopath, modelpath)
    else:
        query = table_training.get_get_all_dpids_query()
        dpids = rpccurrml.fetchall_for_query_self(query)
        dpids = [i[0] for i in dpids] 

        h2o.init()

        for dpid in dpids:
            train_hv_channel_method.train(modelconf_name, dpid, flag, mojopath, modelpath)
