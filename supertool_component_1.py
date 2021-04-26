from db_tools import rpccurrml, table_mlmodelsconf, table_training, table_dpidstates
from TrainerModule import MLModelConf, MLModelsConfManager
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def register_new_model_configuration(flag="56", mlclass="GLM_V2"):
    train_to = datetime.now()
    train_from = train_to - relativedelta(months=+14)

    train_from = train_from.strftime("%Y-%m-%d")
    train_to = train_to.strftime("%Y-%m-%d")

    modelconf_name = f"{train_from[5:7]}-{train_from[0:4]}-{train_to[5:7]}-{train_to[0:4]}-f{flag}-v2"

    print(f"The training and testing interval for model configuration with name {modelconf_name} is: {train_from} to {train_to}")

    mconf = MLModelConf()
    mconf_manager = MLModelsConfManager(rpccurrml, table_mlmodelsconf)

    mconf.name = modelconf_name
    mconf.mlclass = mlclass
    mconf.input_cols = ",".join([table_training.vmon,table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    mconf.output_cols = table_training.imon
    mconf.train_from = train_from
    mconf.train_to = train_to 
    mconf.test_from = train_from
    mconf.test_to = train_to

    mconf_id = mconf_manager.RegisterMLModelConf(mconf) 

    if mconf_id == -1:
        print("modelconf already registered...")
    elif mconf_id == -2:
        print('modelconf registration failed...')
    else:
        print(f"The model configuration registered successfully with modelconf_id {mconf_id}")

    # A loop to write in dpidStates table
    query = table_training.get_get_all_dpids_query()
    dpids = rpccurrml.fetchall_for_query_self(query)
    dpids = [i[0] for i in dpids]
    for dpid in dpids:
        zquery = table_dpidstates.get_insert_entry_query(dpid=dpid, chambers="", conf_name=mconf.name, state=0)
        rpccurrml.execute_commit_query_self(zquery)
    print("\n ++++ Done writing to dpidStatesTable ++++ \n ")

    return mconf.name       

if __name__ == "__main__":
    register_new_model_configuration()
