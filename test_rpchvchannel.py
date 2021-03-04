import h2o
import RPCHVChannelModel

    h2o.init()
    RPCHVChannelModel.init('initial_test')
    dpid = 315
    flag = 56
    model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag)
