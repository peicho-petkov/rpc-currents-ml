from z_analysis_tools import analyse_for_period_and_active_method
from z_prediction_tools import predict_for_period_and_active_method 
from db_tools import table_dpidstates
from db_tools import rpccurrml, omds
from datetime import datetime
from datetime import timedelta
import time
from Misc import datetime_to_string
import fill_new_data

def periodic_evaluation(predict_interval, analyse_interval=None):
    end_date = datetime.now() 
    start_date = end_date - timedelta(seconds=predict_interval)

    # end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
    # start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Time interval is: {datetime_to_string(start_date)} , {datetime_to_string(end_date)}")
    
    predict_for_period_and_active_method.perform_prediction(start_date, end_date)
    if analyse_interval is not None:
        analyse_for_period_and_active_method.perform_analysis(end_date - timedelta(seconds=analyse_interval), end_date)
    else:
        analyse_for_period_and_active_method.perform_analysis(start_date, end_date)
    
    query = table_dpidstates.get_get_all_dpids_query()
    dpids = rpccurrml.fetchall_for_query_self(query)
    dpids = [i[0] for i in dpids]
    # time_for_task = has tbd
    while end_date + timedelta(seconds=predict_interval) > datetime.now():
        time.sleep(0.5)
        sdate = end_date
        end_date = datetime.now()
        ftt = fill_new_data.FillTrainingTable(rpccurrml, omds, dpids, sdate, edate)
        ftt.fill_inst_lumi_table(20)
        ftt.insert_integrated_lumi(20)
        ftt.update_uxc_data(20)
        ftt.fill_imon_vmon_uxc_data_for_DPIDs(20)
        time.sleep(0.5)    
    
if __name__ == "__main__":
    while True:
        periodic_evaluation(200000)



