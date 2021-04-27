
from TrainerModule import DataManager
import fill_new_data
from db_tools import rpccurrml, omds
from datetime import datetime

# DataManager.fill_imon_vmon_uxc_data_for_DPIDs([420])

dpids = [399]
startdate = datetime(2018,5,1)
endate = datetime(2018,12,12)
ftt = fill_new_data.FillTrainingTable(rpccurrml, omds, dpids, startdate, endate)
ftt.fill_imon_vmon_uxc_data_for_DPIDs(time_step = 1)
