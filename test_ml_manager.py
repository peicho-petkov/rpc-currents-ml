from .db_tools import table_training, table_mlmodelsconf, table_mlmodels, rpccurrml
from .db_tools import base as dbase

from TrainerModule import MLTrainer, DataManager, MLModel, MLModelConf, MLModelManager, MLModelsConfManager

if __name__ == '__main__':    
    
    extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)
    extractor_table_training.set_FLAG(56)

    
    query = table_mlmodelsconf.get_myqsl_create_query()
    print(query)
    
    query = table_mlmodels.get_myqsl_create_query()
    print(query)
    
    mconf = MLModelConf()
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    model1 = MLModel()
    
    mconf.name = "initial_test"
    mconf.mlclass = "GLM_V2"
    mconf.input_cols = ",".join([table_training.vmon,table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    mconf.output_cols = table_training.imon
    mconf.train_from = "2016-05-01"
    mconf.train_to = "2016-06-01"
    mconf.test_from = "2017-06-01"
    mconf.test_to = "2017-07-01"
    
    mconf_id = mconf_manager.RegisterMLModelConf(mconf)
    if mconf_id < 0:
        mconf = mconf_manager.get_by_name(mconf.name)

    dpid = 315
    extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(','))
    extractor_table_training.set_time_widow(mconf.train_from,mconf.train_to)
    extractor_table_training.set_DPID(dpid)
    
    trainer = MLTrainer(mconf)
    
    query = extractor_table_training.get_data_by_dpid_flag_query()

    data = rpccurrml.fetchall_for_query_self(query)

    model_315 = trainer.train_model_for_dpid(extractor_table_training._DPID,data)
    
    
    
    