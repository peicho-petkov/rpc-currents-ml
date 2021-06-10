from TrainerModule import DataManager
import fill_new_data
from db_tools import rpccurrml, omds
from datetime import datetime
import csv
import sys
# DataManager.fill_imon_vmon_uxc_data_for_DPIDs([420])

# print("Start: ",sys.argv[1])
# print("Stop: ",sys.argv[2])
# fromDpid = int(sys.argv[1])
# toDpid   = int(sys.argv[2])

# inpfile = open("/afs/cern.ch/user/e/eshumka/rpc-currents-ml/new_dpids.csv", "r")
# thedpids = inpfile.readlines()
# dpids = []

# for ent in thedpids:
#     ent = ent.replace("\n", "")
#     dpids.append(ent)

# dpids = list( dict.fromkeys(dpids) )
# dpids.sort(reverse=False, key=int)
# dpids = dpids[fromDpid:toDpid]
# print(dpids)
# print(len(dpids))
dpids = ['316']
startdate = datetime(2016,5,5)
enddate = datetime(2018,12,3)
ftt = fill_new_data.FillTrainingTable(rpccurrml, omds, dpids, startdate, enddate)
#ftt.fill_inst_lumi_table(time_step = 1)  # time step in months
#ftt.insert_integrated_lumi(time_step = 1)  # time step in months
ftt.fill_imon_vmon_uxc_data_for_DPIDs(time_step_days = 1)  # time step in days
#ftt.update_uxc_data(1)
