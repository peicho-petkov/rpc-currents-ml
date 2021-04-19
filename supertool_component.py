from db_tools import * 
from z_analysis_tools import analyse_for_period_and_active_method
from z_prediction_tools import predict_for_period_and_active_method 
from datetime import datetime
from datetime import timedelta
import time

def periodic_evaluation(timeinseconds):
    end_date = datetime.now() 
    start_date = end_date - timedelta(seconds=timeinseconds)

    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Time interval is: {start_date} , {end_date}")
    predict_for_period_and_active_method.perform_prediction(start_date, end_date)
    analyse_for_period_and_active_method.perform_analysis(start_date, end_date)

    time.sleep(timeinseconds)    
    
if __name__ == "__main__":
    while True:
        periodic_evaluation(200000)



