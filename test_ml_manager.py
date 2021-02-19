import db_tools.base as dbase
import db_tools.db_tables as tables
import TrainerModule.MLModelManager as ml_mod_manager
import TrainerModule.DataManager as data_manager
import TrainerModule.Trainer as trainer
import TrainerModule.MLModelInput as ml_input

if __name__ == '__main__':
    rpccurrml = dbase.mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')

    training_table = tables.TrainingDataTable()
    
    trng_manager = data_manager.Extractor_MySql(training_table.tablename,rpccurrml)
    trng_manager.set_FLAG(56)
    
    mlconf = tables.MLModelsConf()
    mlmods = tables.MLModels()
    
    query = mlconf.get_myqsl_create_query()
    print(query)
    
    query = mlmods.get_myqsl_create_query()
    print(query)
    
    mconf = ml_mod_manager.MLModelConf()
    mconf_manager = ml_mod_manager.MLModelsConfManager(rpccurrml,mlconf)
    model1 = ml_mod_manager.MLModel()
    
  
    mconf.name = "initial_test"
    mconf.mlclass = "GLM_V2"
    mconf.input_cols = ",".join([training_table.vmon,training_table.uxcP,training_table.uxcT,training_table.instant_lumi,training_table.integrated_lumi,training_table.hours_without_lumi])
    mconf.output_cols = training_table.imon
    mconf.train_from = "2016-05-01"
    mconf.train_to = "2016-06-01"
    mconf.test_from = "2017-06-01"
    mconf.test_to = "2017-07-01"
    
    mconf_id = mconf_manager.RegisterMLModelConf(mconf)
    print ("mc_id", mconf_id)
    mconf = mconf_manager.get_by_name(mconf.name)

    dpid = 315
    trng_manager.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(','))
    trng_manager.set_time_widow(mconf.train_from,mconf.train_to)
    trng_manager.set_DPID(dpid)
    
    trnr = trainer.Trainer(mconf)
    
    query = trng_manager.get_data_by_dpid_flag_query()

    data = rpccurrml.fetchall_for_query_self(query)

    model_315 = trnr.train_model_for_dpid(trng_manager._DPID,data)    
    
    