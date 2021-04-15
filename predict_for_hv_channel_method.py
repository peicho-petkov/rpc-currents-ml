import h2o
from EstimatorModule import PredictionsManager, Estimator
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training
from db_tools import rpccurrml
from db_tools import base as dbase
from datetime import datetime

def predict(model_id, flag, predict_from, predict_to):
    rpccurrml = dbase.mysql_dbConnector(host="rpccurdevml", user="ppetkov", password="cmsrpc")
    rpccurrml.connect_to_db("RPCCURRML")
    rpccurrml.self_cursor_mode()

    thequery = table_mlmodels.get_get_confname_dpid_for_mid_query(model_id)
    (modelconf_id, dpid) = rpccurrml.fetchall_for_query_self(thequery)
    newquery = table_mlmodelsconf.get_select_modelconfname_by_modelconfid_query(modelconf_id)
    conf_name = rpccurrml.fetchall_for_query_self(newquery)

    predict_from = datetime.strptime(predict_from,'%Y-%m-%d')
    predict_to = datetime.strptime(predict_to,'%Y-%m-%d')
        
    h2o.init()
    
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf = mconf_manager.get_by_name(conf_name)
    
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)
    
    model = model_manager.get_by_modelconf_id_dpid(mconf.modelconf_id,dpid)
    
    hv_curr_estimator = Estimator.Estimator(model)
    
    extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)
    extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.change_date])
    extractor_table_training.set_time_widow(predict_from,predict_to)
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)

    mlinput = MLModelInput.ModelInput(mconf)
        
    incols, outcol, dataset = mlinput.get_input_for_dataset(data,[table_training.change_date])
    
    pred, pred_err = hv_curr_estimator.predict_for_dataframe(dataset)

    del hv_curr_estimator
    
    n = len(pred)
    
    pm = PredictionsManager.PredictionsManager(rpccurrml,model.model_id,dpid)

    imon = dataset.as_data_frame()[table_training.imon].tolist()

    print("pred:",pred)
    print("dataset.names:",dataset.names)
    print("dataset.types:",dataset.types)

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