#!/usr/bin/env python3

from optparse import OptionParser
from db_tools import table_mlmodelsconf, table_training, rpccurrml, table_autoencoderData
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
    oparser.add_option("--test-from", action="store", type="string", dest="test_from",default='',
                       help="the begining of the validation period [yyyy-mm-dd]")
    oparser.add_option("--test-to", action="store", type="string", dest="test_to",default='',
                       help="the end of the validation period [yyyy-mm-dd]")
    oparser.add_option("--mlclass", action="store", type="string", dest="mlclass",default='GLM_V2',
                       help="accepts supported ml classes only: 'GLM_V1','GLM_V2','GLM_V3','GLM_V4','GLM_V5','GLM_V6','GLM_V7' and 'AUTOENC_V1'")

    (options, args) = oparser.parse_args()
    
    mconf = MLModelConf()
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf.name = options.conf_name
    mconf.mlclass = options.mlclass

    mconf.output_cols = table_training.imon

    if mconf.mlclass == 'GLM_V4':
        mconf.input_cols = ",".join([table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    elif mconf.mlclass == 'AUTOENC_V1':
        mconf.input_cols = ",".join(table_autoencoderData.dpids)
        mconf.output_cols = ",".join(table_autoencoderData.dpids)
    else:
        mconf.input_cols = ",".join([table_training.vmon,table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])

    
    mconf.train_from = options.train_from
    mconf.train_to = options.train_to

    if options.test_from=='':
        mconf.test_from = options.train_from
    else:
        mconf.test_from = options.test_from
    
    if options.test_to=='':
        mconf.test_to = options.train_to
    else:
        mconf.test_to = options.test_to

    mconf_id = mconf_manager.RegisterMLModelConf(mconf)

    if mconf_id == -1:
        print("modelconf already registered...")
    elif mconf_id == -2:
        print('modelconf registration failed...')
    else:
        print(f"The model configuration registered successfully with modelconf_id {mconf_id}")
