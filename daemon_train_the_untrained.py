from db_tools import table_training, table_mlmodels, table_mlmodelsconf, table_dpidstate
from db_tools import base as dbase
import time
import train_hv_channel_method
from Configuration import Configuration
from TrainerModule import MLModelManager
from db_tools import rpccurrml


while True:
    print("\n ++++++++++ NEW CYCLE BEGINS ++++++++++ \n")

    query = table_mlmodels.get_get_active_modelconf_id_query()
    active_confs = rpccurrml.fetchall_for_query_self(query)
    active_confs = [i[0] for i in active_confs]

    for active_conf in active_confs:         
        query = table_mlmodelsconf.get_select_modelconfname_by_modelconfid_query(active_conf)
        conf_name = rpccurrml.fetchall_for_query_self(query)[0][0]
            
        modelconfmanager = MLModelManager.MLModelsConfManager(rpccurrml, table_mlmodelsconf)
        model_conf = modelconfmanager.get_by_name(conf_name)
        start_date = model_conf.train_from  
        end_date = model_conf.train_to 

        query = table_training.get_get_all_dpids_query()
        dpids = rpccurrml.fetchall_for_query_self(query)
        dpids = [i[0] for i in dpids]
        c = 0     
        print(f"The active modelconf_id is: {active_conf} \n")

        for dpid in dpids:

            print(f"Doing a check on dpid: {dpid} \n")
            newquery = table_mlmodels.get_count_for_conf_id_dpid_query(active_conf, dpid)
            result = rpccurrml.fetchall_for_query_self(newquery)[0][0]
            print(f"The number of models with that dpid and modelconf_id are: {result} \n")

            query = table_dpidstate.get_get_state_for_dpid_and_conf_query(dpid, conf_name)
            state = rpccurrml.fetchall_for_query_self(query)[0][0]
            if (result == 0 and state == 1):
                thequery = table_training.get_get_number_of_rows_for_dpid_in_period_query(dpid, start_date, end_date)
                count = rpccurrml.fetchall_for_query_self(thequery)[0][0]
                print(f"Number of rows is {count}")
                if count < 1:
                    print(f"No data for dpid {dpid} in period {start_date} to {end_date}")
                    continue

                conf = Configuration(rpccurrml)
                flag = int(conf.GetParameter("flag"))
                mojo_path = conf.GetParameter("mojopath")
                model_path = conf.GetParameter("modelpath")
                train_hv_channel_method.train(conf_name, dpid, flag, mojo_path, model_path)
                print("\n Finished Training \n")  
                aquery = table_mlmodels.get_set_active_query(1, active_conf, dpid)
                rpccurrml.execute_commit_query_self(aquery)
                print(f"The newly trained model for dpid {dpid} with modelconf_id {active_conf} was set to active")
                # else:
                #    print(f"The newly trained model for dpid {dpid} with modelconf_id {active_conf} was NOT set to active")
                
                c = c + 1
            else:
                # time.sleep(2)
                continue 

    print(f"In this cycle, {c} models were trained")
    time.sleep(180)
