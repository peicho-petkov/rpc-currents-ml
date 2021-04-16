from db_tools import table_training, table_mlmodels, table_mlmodelsconf
from db_tools import base as dbase
import time
import train_hv_channel_method
from Configuration import Configuration

rpccurrml = dbase.mysql_dbConnector(host="rpccurdevml", user="ppetkov", password="cmsrpc")
rpccurrml.connect_to_db("RPCCURRML")
rpccurrml.self_cursor_mode()

while True:
    query = table_training.get_get_all_dpids_query()
    dpids = rpccurrml.fetchall_for_query_self(query)
    dpids = [i[0] for i in dpids]

    for dpid in dpids:
        query = table_mlmodels.get_get_active_modelconf_id_query()
        active_conf = rpccurrml.fetchall_for_query_self(query)[0][0]
        newquery = table_mlmodels.get_count_for_conf_id_dpid_query(active_conf, dpid)
        result = rpccurrml.fetchall_for_query_self(newquery)
        if result == 0:
            # train for that dpid and modelconf_id
            query = table_mlmodelsconf.get_select_modelconfname_by_modelconfid_query(active_conf)
            conf_name = rpccurrml.fetchall_for_query_self(query)[0][0]
            conf = Configuration()
            flag = int(conf.GetParameter("flag"))
            mojo_path = conf.GetParameter("mojopath")
            model_path = conf.GetParameter("modelpath")
            train_hv_channel_method.train(conf_name, dpid, flag, mojo_path, model_path)
        else:
            continue 

    time.sleep(3600)