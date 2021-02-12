import db_tools.base as dbase
import db_tools.db_tables as tables
import Trainer.MLModelManager as ml_mod_manager
if __name__ == '__main__':
    rpccurrml = dbase.mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    
    training_table = tables.TrainingDataTable()
    mlconf = tables.MLModelsConf()
    mlmods = tables.MLModels()
    
    query = mlconf.get_myqsl_create_query()
    print(query)
    
    query = mlmods.get_myqsl_create_query()
    print(query)
    
    mc = ml_mod_manager.MLModelConf()
    mcm = ml_mod_manager.MLModelsConfManager()
    
    mc.name = "test1"
    mc.mlclass = "GLM"
    mc.input_cols = ",".join([training_table.vmon,training_table.uxcP,training_table.uxcT,training_table.instant_lumi,training_table.integrated_lumi,training_table.hours_without_lumi])
    mc.output_cols = training_table.imon
    mc.train_from = "2016-05-01"
    mc.train_to = "2016-06-01"
    mc.test_from = "2017-05-01"
    mc.test_to = "2017-06-01"
    
    mc_id = mcm.RegisterMLModelConf(mc)
    print ("mc_id", mc_id)
    
    