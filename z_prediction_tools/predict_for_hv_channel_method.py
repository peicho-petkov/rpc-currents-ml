import h2o
from tf import autoencoder_rpc
from EstimatorModule import PredictionsManager, Estimator, EstimatorTF
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training, table_lumi, table_autoencoderData
from db_tools import rpccurrml
from db_tools import base as dbase
from datetime import datetime
import numpy as np

def predict(model_id, flag, predict_from, predict_to):

    thequery = table_mlmodels.get_get_confid_dpid_for_mid_query(model_id)
    result = rpccurrml.fetchall_for_query_self(thequery)
    print(f"The query returns {result}")
    modelconf_id = result[0][0]
    print(f"Modelconfid is {modelconf_id}")
    dpid = result[0][1]
    print(f"dpid is {dpid}")
    newquery = table_mlmodelsconf.get_select_modelconfname_by_modelconfid_query(modelconf_id)
    conf_name = rpccurrml.fetchall_for_query_self(newquery)[0][0]

    if type(predict_from) is str:
        predict_from = datetime.strptime(predict_from,'%Y-%m-%d %H:%M:%S')
    if type(predict_to) is str:
        predict_to = datetime.strptime(predict_to,'%Y-%m-%d %H:%M:%S')
        
    # h2o.init()
    
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf = mconf_manager.get_by_name(conf_name)
    
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)
    
    model = model_manager.get_by_modelconf_id_dpid(mconf.modelconf_id,dpid)
    
    hv_curr_estimator = Estimator.Estimator(model)
    
    extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)

    if mconf.mlclass == 'GLM_V4':
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.change_date,table_training.vmon])
    else:
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.change_date])

    extractor_table_training.set_time_widow(predict_from,predict_to)
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)

    # check if len data > 0
    if len(data) < 1:
        return False

    mlinput = MLModelInput.ModelInput(mconf)
        
    incols, outcol, dataset = mlinput.get_input_for_dataset(data,[table_training.change_date])
    
    pred, pred_err = hv_curr_estimator.predict_for_dataframe(dataset)

    del hv_curr_estimator

    if pred is None:
        return False
    
    n = len(pred)
    
    pm = PredictionsManager.PredictionsManager(rpccurrml,model.model_id,dpid)

    imon = dataset.as_data_frame()[table_training.imon].tolist()

    # print("pred:",pred)
    # print("dataset.names:",dataset.names)
    # print("dataset.types:",dataset.types)

    for i in range(n):
        pred_curr = pred[i]
        pred_curr_err = pred_err[i]
        pred_datetime = data[i][-1] #dataset[i,table_training.change_date]
#        print('i',i,pred_curr,pred_curr_err,pred_datetime,imon)
        pm.insert_record(pred_datetime,pred_curr, pred_curr_err, imon[i])
        if i%10000 == 0:
            pm.commit_records()
            print(f"{i/float(n)*100.:.1f}% records committed")
    
    pm.commit_records()
    print("prediction done...")

    return True

def predict_autoencoder(models, flag, predict_from, predict_to):

    if type(predict_from) is str:
        predict_from = datetime.strptime(predict_from,'%Y-%m-%d %H:%M:%S')
    if type(predict_to) is str:
        predict_to = datetime.strptime(predict_to,'%Y-%m-%d %H:%M:%S')
        
    if len(models) < 1:
        return False

    model = models[0]

    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    mconf = mconf_manager.get_by_modelconf_id(model.modelconf_id)
    
    model_output_dpids = [int(x) for x in mconf.output_cols.replace('dpid','').split(',')]

    print(f"Model output dpids length is: {len(model_output_dpids)}")
    print(f"+++++++++++++++++++++++++++++=+++++++++++++=+++++++++++")
    dpids = [int(m.dpid) for m in models]
    
    models_dict = {}
    for m in models:
        models_dict[int(m.dpid)] = m

    index_dpid_dict = {}

    for ii in range(len(dpids)):
        index_dpid_dict[dpids[ii]] = ii

    pm = PredictionsManager.PredictionsManager(rpccurrml,model.model_id,model.dpid)
    hv_curr_estimator = EstimatorTF.EstimatorTF(model)
    ok = False
    ae_extract = autoencoder_rpc.AE_DataManager()
    ae_extract.set_time_window(predict_from, predict_to)
    for currents, currents_timestamp in ae_extract.get_dataframe():
        print(f"The currents list length is: {len(currents)}")
        print(f"Currents shape: {currents.shape}")                 # (2-days worth of points, 774) shaped array  while timestamp array is (2dwop, 1) shaped
        predicted_currents = hv_curr_estimator.predict_for_dataframe(currents)  # (n_points, 774) shaped array
        print(f"The predicted currents list length is {len(predicted_currents)}")
        print(f"Predicted current shape: {predicted_currents.shape}")
        for ii in range(len(currents)):
            print(f"Inserting predictions for {currents_timestamp[ii]}")
            for index_dpid in dpids:
                ok = True
                pm.dpid = index_dpid
                pm.model_id = models_dict[index_dpid].model_id
                kk = index_dpid_dict[index_dpid]
                #print(f"The values to be inserted are: timestamp {currents_timestamp[kk]}, predicted_current {predicted_currents[ii, kk]}, measured current {currents[ii, kk]} ")
                pm.insert_record(currents_timestamp[ii],predicted_currents[ii, kk],0,currents[ii, kk])
                
#            for kk in range(len(currents[ii])):
#                index_dpid = model_output_dpids[kk]
#                if index_dpid in dpids:
#                    ok = True
#                    pm.dpid = index_dpid
#                    pm.model_id = models_dict[index_dpid].model_id
#                    #print(f"The values to be inserted are: timestamp {currents_timestamp[kk]}, predicted_current {predicted_currents[ii, kk]}, measured current {currents[ii, kk]} ")
#                    pm.insert_record(currents_timestamp[kk],predicted_currents[ii, kk],0,currents[ii, kk])
            print("Before commit")
            pm.commit_records()
            print("After commit")
        
    return ok       

def predict_hybrid(glm_mconfname, autoenc_mconfname,flag, predict_from, predict_to):

    if type(predict_from) is str:
        predict_from = datetime.strptime(predict_from,'%Y-%m-%d %H:%M:%S')
    if type(predict_to) is str:
        predict_to = datetime.strptime(predict_to,'%Y-%m-%d %H:%M:%S')
        
    # if len(models) < 1:
    #     return False

    # model = models[0]

    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    glm_mconf = mconf_manager.get_by_name(glm_mconfname)
    autoenc_mconf = mconf_manager.get_by_name(autoenc_mconfname)
    
    models_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)
    
    glm_models = models_manager.get_models_by_modelconf_id(glm_mconf.modelconf_id)
    autoenc_models = models_manager.get_models_by_modelconf_id(autoenc_mconf.modelconf_id)
    autoenc_model = autoenc_models[0]
    
    model_output_dpids = [int(x) for x in autoenc_mconf.output_cols.replace('dpid','').split(',')]

    # print(f"Model output dpids length is: {len(model_output_dpids)}")
    # print(f"+++++++++++++++++++++++++++++=+++++++++++++=+++++++++++")
    
    glm_dpids = [int(m.dpid) for m in glm_models]
    
    autoenc_dpids = [int(m.dpid) for m in autoenc_models]
    
    glm_models_dict = {}
    for m in glm_models:
        glm_models_dict[int(m.dpid)] = m

    glm_index_dpid_dict = {}

    for ii in range(len(glm_dpids)):
        glm_index_dpid_dict[glm_dpids[ii]] = ii

    autoenc_models_dict = {}
    for m in autoenc_models:
        autoenc_models_dict[int(m.dpid)] = m

    autoenc_index_dpid_dict = {}

    for ii in range(len(autoenc_dpids)):
        autoenc_index_dpid_dict[autoenc_dpids[ii]] = ii


    pm = PredictionsManager.PredictionsManager(rpccurrml,autoenc_model.model_id,autoenc_model.dpid)
    
    autoenc_curr_estimator = EstimatorTF.EstimatorTF(autoenc_model)
    
    glm_curr_estimator_dict = {}
    
    for glm_model in glm_models:
        glm_curr_estimator_dict[glm_model.dpid] = Estimator.Estimator(glm_model)
    
    ok = False
    ae_extract = autoencoder_rpc.AE_DataManager()
    ae_extract.set_time_window(predict_from, predict_to)
    
    glm_input = MLModelInput.ModelInput(glm_mconf)
    
    for currents, currents_timestamp in ae_extract.get_dataframe():
        print(f"The currents list length is: {len(currents)}")
        print(f"The shapes of currents and currents_timestamp are respectively: {currents.shape} and {currents_timestamp.shape} ")
        glm_currents = []
        for ii in range(len(currents_timestamp)):
            glm_predictions = []
            for dpid in autoenc_dpids:
                print(f"The counter ii has value: {ii}")
                print(f"dpid is: {dpid}, current timestamp {currents_timestamp[ii]}")
                at_datetime = currents_timestamp[ii].astype(datetime).strftime("%Y-%m-%d %H:%M:%S")
                query = table_training.get_for_dpid_the_record_before_query(dpid,at_datetime,
                                                                            glm_mconf.input_cols.split(',')+[table_training.imon])
                data = rpccurrml.fetchall_for_query_self(query)
                incol, outcol, input_for_dpid = glm_input.get_input_for_dataset(data)
                glm_prediction = -0.5
                if dpid in glm_curr_estimator_dict:
                    glm_prediction,glm_predicion_err = glm_curr_estimator_dict[dpid].predict_for_dataframe(input_for_dpid)
                glm_predictions.append(glm_prediction)     
            glm_currents.append(glm_predictions)
            
        predicted_currents = autoenc_curr_estimator.predict_for_dataframe(np.asarray(glm_currents).astype(np.float32)) 
        
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("ENTERING THE PREDICTION MANAGER LOOP WHERE WE COMMIT")
        for ii in range(len(predicted_currents)):
            print(f"Inserting predictions for {currents_timestamp[ii]}")
            for index_dpid in autoenc_dpids:
                ok = True
                pm.dpid = index_dpid
                pm.model_id = -autoenc_models_dict[index_dpid].model_id
                kk = autoenc_index_dpid_dict[index_dpid]
                pm.insert_record(currents_timestamp[ii],predicted_currents[ii, kk],0,currents[ii, kk])
            print("Before commit")
            pm.commit_records()
            print("After commit")
        
    return ok       
