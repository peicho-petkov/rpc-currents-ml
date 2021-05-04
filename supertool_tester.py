from z_analysis_tools import analyse_for_period_and_active_method
from z_prediction_tools import predict_for_period_and_active_method 
from datetime import datetime, timedelta
import time
import h2o

emul_datenow = datetime(2018,10,3,8,15)
emul_enddate = emul_datenow + timedelta(hours=12)

while emul_datenow <= emul_enddate:
    h2o.init()
    h2o.remove_all()
    print(f"datetime now: {emul_datenow}")
    t0 = datetime.now()
    print(f"prediction step started...")
    predict_for_period_and_active_method.perform_prediction(emul_datenow - timedelta(minutes=15), emul_datenow)
    print(f"prediction step ended... elapsed time: {datetime.now()-t0}")
    #time.sleep(3)
    t0 = datetime.now()
    print(f"analysis step started...")
    analyse_for_period_and_active_method.perform_analysis(emul_datenow - timedelta(minutes=30), emul_datenow)
    print(f"analysis step ended... elapsed time: {datetime.now()-t0}")
    #time.sleep(3)
    emul_datenow = emul_datenow + timedelta(minutes=15)




