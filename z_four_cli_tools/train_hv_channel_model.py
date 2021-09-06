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

    (options, args) = oparser.parse_args()

    conf_name=options.conf_name
    dpid = options.dpid
    flag = options.flag
    mojopath="."
    modelpath="."
    print(f"conf_name {conf_name}")
    print(f"dpid {dpid}")
    print(f"flag {flag}")
    
    RPCHVChannelModel.init(model_conf_name=conf_name,mojofiles_path=mojopath,mlmodels_path=modelpath)

    if "AUTOENC" in RPCHVChannelModel.mconf.mlclass:
        model_ids,dpids = RPCHVChannelModel.train_and_register_autoencoder(True)
        for kv in len(model_ids):
            if model_ids[kv] < 0:
                print(f"a model configuration with name {conf_name} already registered for DPID {dpids[kv]}...")
            else:
                print(f"An ML model with model_id {model_ids[kv]} with configuration name {conf_name} for DPID {dpids[kv]} was registered successfully...")    
    else:    
        h2o.init()
        model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag,True)
    
        if model_id < 0:
            print(f"a model configuration with name {conf_name} already registered for DPID {dpid}...")
        else:
            print(f"An ML model with model_id {model_id} with configuration name {conf_name} for DPID {dpid} was registered successfully...")