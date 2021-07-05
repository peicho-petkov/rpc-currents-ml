#!/usr/bin/env python3

import RPCHVChannelModel
import h2o
from optparse import OptionParser

if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-conf-name", action="store",
                       type="string", dest="conf_name")
    oparser.add_option("--dpid", action="store", type="int", dest="dpid")
    oparser.add_option("--flag", action="store",
                       type="int", dest="flag", default=56)
    oparser.add_option("--scale-sd", action="store",
                       type="float", dest="scale_sd", default=5.0)

    (options, args) = oparser.parse_args()

    conf_name=options.conf_name
    dpid = options.dpid
    flag = options.flag
    scale_sd = options.scale_sd
    mojopath="."
    modelpath="."
    print(f"conf_name {conf_name}")
    print(f"dpid {dpid}")
    print(f"flag {flag}")
    print(f"scale-sd {scale_sd}")
    h2o.init()
    
    RPCHVChannelModel.init(model_conf_name=conf_name,mojofiles_path=mojopath,mlmodels_path=modelpath)
    
    model_id = RPCHVChannelModel.train_refined_and_register_for_dpid(dpid,flag,scale_sd=scale_sd,forceupdate=True)
    if model_id < 0:
        print(f"a model configuration with name {conf_name} already registered for DPID {dpid}...")
    else:
        print(f"An ML model with model_id {model_id} with configuration name {conf_name} for DPID {dpid} was registered successfully...")