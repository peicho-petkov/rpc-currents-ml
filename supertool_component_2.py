from z_analysis_tools import analyse_for_period_and_active_method
from z_prediction_tools import predict_for_period_and_active_method 
from datetime import datetime
from datetime import timedelta
import time
from Misc import datetime_to_string

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
  
    while end_date + timedelta(seconds=predict_interval) < datetime.now():
        # TODO: do something else meanwhile (like uploading new data), 
        # that has execution time < predict_interval
        time.sleep(0.5)    
    
if __name__ == "__main__":
    while True:
        periodic_evaluation(200000)



