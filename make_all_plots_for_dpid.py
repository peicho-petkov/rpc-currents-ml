#!/usr/bin/env python3

import RPCHVChannelModel
import h2o
from optparse import OptionParser
from EstimatorModule import PredictionsManager, Estimator
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training, rpccurrml, base as dbase
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd

if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-conf-name", action="store",
                       type="string", dest="conf_name")
    oparser.add_option("--dpid", action="store", type="int", dest="dpid")
    oparser.add_option("--flag", action="store",
                       type="int", dest="flag", default=56)
    
    oparser.add_option("--predict-from", action="store", type="string", dest="predict_from",
                       help="the beginning of the prediction period [yyyy-mm-dd]")
    oparser.add_option("--predict-to", action="store", type="string", dest="predict_to",
                       help="the end of the prediction period [yyyy-mm-dd]")

    oparser.add_option("--file-for-plots", action="store", type="string", dest="filename",
                        default="", help="Enter the file name where you want the plots stored")

    (options, args) = oparser.parse_args()

    conf_name=options.conf_name
    dpid = options.dpid
    flag = options.flag

    predict_from = datetime.strptime(options.predict_from,'%Y-%m-%d')
    predict_to = datetime.strptime(options.predict_to,'%Y-%m-%d')

    filename = options.filename

    print(f'current prediction for DPID {dpid} from {predict_from} to {predict_to}') 

    print(f"conf_name {conf_name}")
    print(f"dpid {dpid}")
    print(f"flag {flag}")
    
    h2o.init()
    
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf = mconf_manager.get_by_name(conf_name)
    
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)
    
    model = model_manager.get_by_modelconf_id_dpid(mconf.modelconf_id,dpid)
    
    hv_curr_estimator = Estimator.Estimator(model)
    
    extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)

    if mconf.mlclass == 'GLM_V4':
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.vmon,table_training.change_date])
    else:
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.change_date])

    extractor_table_training.set_time_widow(predict_from,predict_to)
    extractor_table_training.set_DPID(dpid)
    extractor_table_training.set_FLAG(flag)
    
    query = extractor_table_training.get_data_by_dpid_flag_query()
    data = rpccurrml.fetchall_for_query_self(query)

    mlinput = MLModelInput.ModelInput(mconf)
    if mconf.mlclass == 'GLM_V4':
        incols, outcol, dataset = mlinput.get_input_for_dataset(data,[table_training.vmon,table_training.change_date])
    else:
        incols, outcol, dataset = mlinput.get_input_for_dataset(data,[table_training.change_date])

    pf = dataset[table_training.change_date].as_data_frame()

    pf['predicted'], pred_err = hv_curr_estimator.predict_for_dataframe(dataset)

    del hv_curr_estimator
    
    print("prediction done...")

    pf[table_training.imon] = dataset[table_training.imon].as_data_frame()
    pf[table_training.change_date] = pd.to_datetime(pf[table_training.change_date].to_list(),unit='ms')
    print(pf)

    difference = pf[table_training.imon] - pf['predicted']
    pf['difference'] = difference
    newpf = pf[[table_training.change_date, 'difference']].copy()
    pf = pf.drop(['difference'], axis=1)
    newpf.set_index([table_training.change_date], inplace=True)
    rolling = newpf.rolling(100).mean()
    newpf['rolling'] = rolling    
    newpf = newpf.drop(['difference'], axis=1)    

    fig0 = plt.figure()
    pf.set_index([table_training.change_date], inplace=True)
    pf.plot(legend=True, xlabel="date", ylabel="Current [uA]", use_index=True)    
    plt.title(f"{dpid} {conf_name}")
    plt.xticks(rotation=45)

    if filename == "":
        plt.show()
    else:
        plt.savefig(filename)

    fig1 = plt.figure()
    plt.hist(difference, bins=40, orientation='vertical')
    plt.xlabel('Current difference')
    plt.title(f'diff-hist-{dpid}-{conf_name}')

    if filename == "":
        plt.show()
    else:
        plt.savefig(f'diff-hist-{filename}')

    fig2 = plt.figure()
    newpf.plot(legend=True, xlabel="date", ylabel="rolling_avg", use_index=True)
    plt.title(f"roll_avg_{dpid}_{conf_name}")
    plt.xticks(rotation=45)
 
    if filename == "":
        plt.show()
    else:
        plt.savefig(f'roll-avg-{filename}')

   
    print("plotting done...")
    
