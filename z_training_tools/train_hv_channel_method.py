import RPCHVChannelModel
import h2o

def train(model_conf_name, dpid, flag, mojopath, modelpath):
    conf_name = model_conf_name
    
    # h2o.init()
    
    RPCHVChannelModel.init(model_conf_name=conf_name,mojofiles_path=mojopath,mlmodels_path=modelpath)
    
    if 'AUTOENC' in RPCHVChannelModel.mconf.mlclass:
        model_id = RPCHVChannelModel.train_and_register_autoencoder(True)      
        
    if 'GLM' in RPCHVChannelModel.mconf.mlclass:
        model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag,True)
    
    if model_id == -1:
        print(f"A model configuration with name {conf_name} already registered for DPID {dpid}...")
    elif model_id == -2:
        print(f"No data for DPID {dpid} and model configuration {conf_name}")
    elif model_id >= 0:
        print(f"An ML model with model_id {model_id} with configuration name {conf_name} for DPID {dpid} was registered successfully...")
    