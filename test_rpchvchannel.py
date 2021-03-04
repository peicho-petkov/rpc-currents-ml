import h2o
import RPCHVChannelModel

    h2o.init()
    RPCHVChannelModel.init('initial_test')
    flag = 56
    
    for dpid in [315, 316, 317, 378, 379 ]: 
        model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag)
