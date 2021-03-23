#!/usr/bin/env python3

from optparse import OptionParser
from db_tools import table_mlmodelsconf, table_training
from db_tools import base as dbase
from TrainerModule import MLModelConf,MLModelsConfManager

if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-conf-name", action="store",
                       type="string", dest="conf_name")
    oparser.add_option("--train-from", action="store", type="string", dest="train_from",
                       help="the begining of the training period [yyyy-mm-dd]")
    oparser.add_option("--train-to", action="store", type="string", dest="train_to",
                       help="the end of the training period [yyyy-mm-dd]")
    oparser.add_option("--mlclass", action="store", type="string", dest="mlclass",default='GLM_V2',
                       help="accepts supported ml classes only. accepts 'GLM_V2', currently.")

    (options, args) = oparser.parse_args()
    
    rpccurrml = dbase.mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')
    
    mconf = MLModelConf()
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf.name = options.conf_name
    mconf.mlclass = options.mlclass
    mconf.input_cols = ",".join([table_training.vmon,table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    mconf.output_cols = table_training.imon
    mconf.train_from = options.train_from
    mconf.train_to = options.train_to
    # TODO: implement test period
    mconf.test_from = options.train_from
    mconf.test_to = options.train_to

    mconf_id = mconf_manager.RegisterMLModelConf(mconf)

    if mconf_id == -1:
        print("modelconf already registered...")
    elif mconf_id == -2:
        print('modelconf registration failed...')
    else:
        print(f"The model configuration registered successfully with modelconf_id {mconf_id}")
