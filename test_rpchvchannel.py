import h2o
import RPCHVChannelModel
import Configuration
from db_tools import base as dbase

    rpccurrml = dbase.mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')
    conf = Configuration.Configuration(rpccurrml)

    model_path = conf.GetParameter('MODEL_PATH')
    mojo_path = conf.GetParameter('MOJO_PATH')

    conf.AddParameter("int_list_example","1,2,6,9","int_list")
    
    par = conf.GetParameter("int_list_example")
    print(par)
    
    # h2o.init()
    # RPCHVChannelModel.init('initial_test',model_path,mojo_path)
    # flag = 56
    
    # for dpid in [315, 316, 317, 378, 379 ]: 
    #     model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag)
