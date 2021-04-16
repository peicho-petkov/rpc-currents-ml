#!/usr/bin/env python3

from db_tools import table_predicted_current, table_training, table_mlmodels, table_mlmodelsconf, table_configuration
from db_tools import base as dbase 
from TrainerModule import MLModelManager 
from Configuration import Configuration
from optparse import OptionParser
import predict_for_hv_channel_method
import analyse_for_period
from datetime import datetime

if __name__ == "__main__":
    oparser = OptionParser()
    oparser.add_option("--pred-start-date", action="store", type="string", dest="start_date",
                        help="Specify the beginning of the prediction period")
    oparser.add_option("--pred-end-date", action="store", type="string", dest="end_date", 
                        help="Specify the end of the prediction period")

    (options, args) = oparser.parse_args()
    start_date = options.start_date
    end_date = options.end_date
    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date = datetime.strptime(end_date, '%Y-%m-%d')

    rpccurrml = dbase.mysql_dbConnector(host="rpccurdevml", user="ppetkov", password="cmsrpc")
    rpccurrml.connect_to_db("RPCCURRML")
    rpccurrml.self_cursor_mode()

    query = table_mlmodels.get_get_active_model_ids_query()
    print(query)
    active_model_ids = rpccurrml.fetchall_for_query_self(query)
    active_model_ids = [i[0] for i in active_model_ids]
    print(active_model_ids)
    conf = Configuration(rpccurrml)
    flag = conf.GetParameter("flag")

    for model_id in active_model_ids:
        newquery = table_mlmodels.get_get_dpid_by_model_id_query(model_id)
        print(newquery)
        dpid = rpccurrml.fetchall_for_query_self(newquery)[0][0]
        print(f"The dpid is: {dpid}")
        thequery = table_training.get_get_number_of_rows_for_dpid_in_period_query(dpid, start_date, end_date)
        count = rpccurrml.fetchall_for_query_self(thequery)[0][0]
        print(f"number of rows is {count}")
        if count < 1:
            print(f"No data for dpid {dpid} in period {start_date} to {end_date}")
            continue
        predict_for_hv_channel_method.predict(model_id, flag, start_date, end_date)

    # for model_id in active_model_ids:
        # try:
            # print(f"Search for warnings/errors in this prediction period begins for model_id {model_id}")
            # analyse_for_period.analyse_prediction(model_id, dpid, start_date, end_date, rpccurrml)
            # print(f"Warning/error analysis ended for this prediction period for model_id {model_id}")
        # except Exception as e:
            # print(e)
            # continue
