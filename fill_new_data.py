from TrainerModule.DataManager import Extractor_Oracle, DataPopulator, Extractor_MySql
from db_tools import table_training, table_uxcenv, table_lumi, rpccurrml, omds
from dateutil.relativedelta import relativedelta


class FillTrainingTable:
    ''' A class whose methods use the Oracle extractor class to
        fill the Training Data table '''

    def __init__(self, mysql_conn, oracle_conn, dpids, sdate, edate):
        self.dpids = dpids
        self.start_date = sdate
        self.end_date = edate
        self.oracle_connect = oracle_conn
        self.mysql_connect = mysql_conn


    def fill_imon_vmon_data(self, time_step):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(self.mysql_connect)
    
        flag=56
        
        for dpid in self.dpids:
            dpid = dpid.strip()
            fromdate = self.start_date
            while fromdate < self.end_date: 
                todate = fromdate + relativedelta(seconds = time_step)
                ce.set_time_widow(fromdate,todate)
                fromdate = todate
                # print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
                for rpc_data in ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS", dpid, flag, ["DPID","CHANGE_DATE","IMON","VMON","FLAG"]):
                    dp.insert_imon_record(rpccurr_table=table_training.tablename, dpid_col_name="DPID", ichange_col_name="CHANGE_DATE", imon_col_name="IMON", vmon_col_name="VMON", flag_col_name="FLAG", rpccurr_data=rpc_data)
    
                dp.commit_inserted_records()

    def fill_inst_lumi_table(self, time_step):
        ce = Extractor_Oracle(self.oracle_connect)
        dp = DataPopulator(self.mysql_connect)

        fromdate = self.start_date
        while fromdate < self.end_date: 
            todate = fromdate + relativedelta(months = time_step)
            ce.set_time_widow(fromdate,todate)
            fromdate = todate
            # print(ce._startdate,ce._enddate)

            for instlumidata in ce.get_inst_lumi_data("cms_runtime_logger.lumi_sections",
                                                    "STARTTIME",["STARTTIME","STOPTIME","INSTLUMI"]):
                dp.insert_inst_lumi_record(table_lumi.tablename, "STARTTIME", "STOPTIME", "INSTLUMI", instlumidata)
    
            dp.commit_inserted_records()  

    def update_uxc_data(self, time_step):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(rpccurrml)

        flag=56
        fromdate = self.start_date 
        old_data=[]
        while fromdate < self.end_date: 
            todate = fromdate + relativedelta(days = time_step)
            ce.set_time_widow(fromdate,todate)
            fromdate = todate
            # print("start date ", ce._startdate," enddate ", ce._enddate)
            
            for uxc_data in ce.get_uxc_env_data("cms_rpc_pvss_test.UXC_ENVIRONMENT",["CHANGE_DATE","PRESSURE","TEMPERATURE","RELATIVE_HUMIDITY","DEWPOINT"]):
                if old_data[1:4] != uxc_data[1:4] and len(old_data) == 5:
                    # print("sending to db: different old ",old_data," new ", uxc_data)
                    dp.update_env_parameters(uxc_table=table_uxcenv.tablename, uxc_press_col_name='uxcPressure', uxc_temp_col_name='uxcTemperature', uxc_rh_col_name='uxcRH', change_date_col='CHANGE_DATE', until_col_name='NEXT_CHANGE_DATE', uxc_data=old_data, until_timestamp=uxc_data[0])
                    old_data = uxc_data[:]
                if (len(old_data) < 5):
                    old_data = uxc_data[:]
            
            dp.commit_inserted_records()

    def insert_integrated_lumi(self, time_step):
        dp = DataPopulator(self.mysql_connect)
        
        sdate = dp.get_min_colname_cond(tablename = table_lumi.tablename, col_name = "STARTTIME", condition = "where INTEGRATED IS NULL")
        edate = self.end_date
        fromdate = sdate
        intlumi = dp.get_max_colname(tablename = table_lumi.tablename, col_name = "INTEGRATED")
        if intlumi is None:
            intlumi = 0.0
        while fromdate < edate: 
            todate = fromdate + relativedelta(months = time_step)
            # print(fromdate,todate,intlumi)
            for lumirecid,instlumi in dp.get_inst_lumi_data(table_lumi.tablename, lstart_col_name="STARTTIME", select_col_list=['rec_id','INSTLUMI'], startdate=fromdate, enddate=todate):
                intlumi = float(intlumi) + float(instlumi)
                dp.update_integrated_lumi_record(table_lumi.tablename, "INTEGRATED", lumirecid, intlumi)
                # print("recid",lumirecid,"inst lumi",instlumi,"integr",intlumi)
            dp.commit_inserted_records()
            fromdate = todate

    def fill_imon_vmon_uxc_data_old(self, time_step):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(self.mysql_connect)
         
        for dpid in self.dpids:
            dpid = dpid.strip()
            VmonLast=0.0
            fromdate=self.start_date
            VmonXt=0.0
            dt_last=0
            R=0.0
            T=0.0
            RH=0.0

            q = table_training.get_latest_HoursWithoutLumi_query(dpid)
            q_res = self.mysql_connect.fetchall_for_query_self(q)
            VmonAvg=0.0
            if len(q_res) == 1:
                VmonAvg = float(q_res[0][0])
            
            while fromdate < self.end_date: 
                todate = fromdate + relativedelta(days = time_step)
                ce.set_time_widow(fromdate, todate)
                # print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
                ll = 0
                hvidata = ce.get_rpccurrents_data_anyflag("cms_rpc_pvss_test.RPCCURRENTS", dpid, ["DPID", "CHANGE_DATE", "IMON", "VMON", "FLAG"])
                uxcdata = dp.get_inst_lumi_data(table_uxcenv.tablename, lstart_col_name = table_uxcenv.change_date, select_col_list = [table_uxcenv.change_date, table_uxcenv.next_change_date, table_uxcenv.pressure, table_uxcenv.temperature, table_uxcenv.relative_humidity], startdate = fromdate, enddate = todate)
                lumidata = []
                if len(hvidata) > 0:
                    lumidata = dp.get_inst_lumi_data(table_lumi.tablename, lstart_col_name = table_lumi.ls_start, select_col_list = [table_lumi.ls_start, table_lumi.ls_stop, table_lumi.inst_lumi, table_lumi.integrated_lumi], startdate = fromdate, enddate = todate)
                
                for rpc_data in hvidata:
                    _dpid = rpc_data[0]
                    ch_date = rpc_data[1]
                    imon = rpc_data[2]
                    vmon = rpc_data[3]
                    flag = rpc_data[4]
                    dt = ch_date - fromdate
                    dt = dt.total_seconds()

                    for uxcrec in uxcdata:
                        uxc_ch_date = uxcrec[0]
                        uxc_next_ch_date = uxcrec[1]
                        if (uxc_ch_date < ch_date or uxc_ch_date == ch_date) and ( ch_date == uxc_next_ch_date or ch_date < uxc_next_ch_date):
                            P = uxcrec[2]
                            T = uxcrec[3]
                            RH = uxcrec[4]
                        elif uxc_next_ch_date > ch_date:
                            break

                    if not flag==56:
                        VmonXt = VmonXt + VmonLast*dt
                    
                    VmonLast = vmon 

                    if (vmon < 6400):
                        continue
                    if not flag == 56:
                        continue

                    # print("", _dpid,ch_date,imon,vmon,flag,dt,VmonAvg )                    
                    InstLumi=0
                    instbuf=0.0
                    intebuf=0.0
                    nbuf=0
                    for lumirec in lumidata:
                        lb = lumirec[0]
                        le = lumirec[1]
                        inst = lumirec[2]
                        inte = lumirec[3]
                        if (lb < ch_date or lb == ch_date) and ( ch_date == le or ch_date < le):
                            #                            print("chdate lb le",ch_date,lb,le)
                            instbuf = inst
                            intebuf = inte
                            nbuf = nbuf + 1
                        elif le > ch_date:
                            break

                            
                    if nbuf > 0:
                        instbuf = instbuf/nbuf
                        intebuf = intebuf/nbuf

                    rpccurrml.execute_query_self(table_training.get_insert_data_query(ch_date, imon, vmon, dpid, flag, instbuf, P, T, RH, intebuf, VmonAvg))
                
                rpccurrml.execute_commit_self()
                dt = todate - fromdate
                dt = dt.total_seconds()
                VmonAvg = VmonAvg + VmonXt / dt / 1000.0
                VmonXt = 0.0
                fromdate = todate

    def fill_imon_vmon_uxc_data_for_DPIDs_old(self, time_step):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(self.mysql_connect)

        for dpid in self.dpids:
            dpid = dpid.strip()
            VmonLast = 0.0
            fromdate = self.start_date
            VmonXt = 0.0
            dt_last = 0
            VmonAvg = 0.0
            R = 0.0
            T = 0.0
            RH = 0.0
            while fromdate < self.end_date: 
                todate = fromdate + relativedelta(days = time_step)
                ce.set_time_widow(fromdate, todate)
                # print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
                ll = 0
                hvidata = ce.get_rpccurrents_data_anyflag("cms_rpc_pvss_test.RPCCURRENTS", dpid, ["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
                uxcdata = dp.get_inst_lumi_data(table_uxcenv.tablename, lstart_col_name = table_uxcenv.change_date, select_col_list = [table_uxcenv.change_date, table_uxcenv.next_change_date, table_uxcenv.pressure, table_uxcenv.temperature, table_uxcenv.relative_humidity], startdate = fromdate, enddate = todate)
                lumidata = []
                if len(hvidata) > 0:
                    lumidata = dp.get_inst_lumi_data(table_lumi.tablename, lstart_col_name = table_lumi.ls_start, select_col_list = [table_lumi.ls_start, table_lumi.ls_stop, table_lumi.inst_lumi, table_lumi.integrated_lumi], startdate = fromdate, enddate = todate)
                
                for rpc_data in hvidata:
                    _dpid = rpc_data[0]
                    ch_date = rpc_data[1]
                    imon = rpc_data[2]
                    vmon = rpc_data[3]
                    flag = rpc_data[4]
                    dt = ch_date - fromdate
                    dt = dt.total_seconds()

                    for uxcrec in uxcdata:
                        uxc_ch_date = uxcrec[0]
                        uxc_next_ch_date = uxcrec[1]
                        if (uxc_ch_date < ch_date or uxc_ch_date == ch_date) and ( ch_date == uxc_next_ch_date or ch_date < uxc_next_ch_date):
                            P = uxcrec[2]
                            T = uxcrec[3]
                            RH = uxcrec[4]
                        elif uxc_next_ch_date > ch_date:
                            break
                
                    if not flag == 56:
                        VmonXt = VmonXt + VmonLast*dt
                    
                    VmonLast = vmon 

                    if (vmon < 6400):
                        continue
                    if not flag == 56:
                        continue

                    InstLumi = 0
                    instbuf = 0.0
                    intebuf = 0.0
                    nbuf = 0
                    for lumirec in lumidata:
                        lb = lumirec[0]
                        le = lumirec[1]
                        inst = lumirec[2]
                        inte = lumirec[3]
                        if (lb < ch_date or lb == ch_date) and ( ch_date == le or ch_date < le):
                            instbuf = inst
                            intebuf = inte
                            nbuf = nbuf + 1
                            break
                        elif le > ch_date:
                            break

                            
                    if nbuf > 0:
                        instbuf = instbuf/nbuf
                        intebuf = intebuf/nbuf
                        query = table_training.get_insert_data_query(ch_date, imon, vmon, dpid, flag, instbuf, P, T, RH, intebuf, VmonAvg)
                        rpccurrml.execute_query_self(query)
                
                rpccurrml.execute_commit_self()
                dt = todate - fromdate
                dt = dt.total_seconds()
                VmonAvg = VmonAvg + VmonXt / dt / 1000.0
                VmonXt = 0.0
                fromdate = todate

    def fill_imon_vmon_uxc_data(self, time_step_days=1):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(self.mysql_connect)
         
        for dpid in self.dpids:
            dpid = dpid.strip()
            fromdate=self.start_date
            last_vmon=0.0
            last_vmon_timestamp=self.start_date
            P=0.0
            T=0.0
            RH=0.0

            q = table_training.get_latest_HoursWithoutLumi_query(dpid)
            q_res = self.mysql_connect.fetchall_for_query_self(q)
            HwoL=0.0
            if len(q_res) == 1:
                HwoL = float(q_res[0][0])
            
            while fromdate < self.end_date: 
                todate = fromdate + relativedelta(days = time_step_days)
                ce.set_time_widow(fromdate, todate)
                # print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
                ll = 0
                hvidata = ce.get_rpccurrents_data_anyflag("cms_rpc_pvss_test.RPCCURRENTS", dpid, ["DPID", "CHANGE_DATE", "IMON", "VMON", "FLAG"])
                uxcdata = dp.get_inst_lumi_data(table_uxcenv.tablename, lstart_col_name = table_uxcenv.change_date, select_col_list = [table_uxcenv.change_date, table_uxcenv.next_change_date, table_uxcenv.pressure, table_uxcenv.temperature, table_uxcenv.relative_humidity], startdate = fromdate, enddate = todate)
                lumidata = []
                if len(hvidata) > 0:
                    lumidata = dp.get_inst_lumi_data(table_lumi.tablename, lstart_col_name = table_lumi.ls_start, select_col_list = [table_lumi.ls_start, table_lumi.ls_stop, table_lumi.inst_lumi, table_lumi.integrated_lumi], startdate = fromdate, enddate = todate)
                
                for rpc_data in hvidata:
                    _dpid = rpc_data[0]
                    ch_date = rpc_data[1]
                    imon = rpc_data[2]
                    vmon = rpc_data[3]
                    flag = rpc_data[4]
                    
                    dt = ch_date - last_vmon_timestamp
                    dt = dt.total_seconds()
                    
                    if last_vmon > 8500 and not flag == 56:
                        HwoL = HwoL + dt

                    last_vmon = vmon
                    last_vmon_timestamp = ch_date

                    for uxcrec in uxcdata:
                        uxc_ch_date = uxcrec[0]
                        uxc_next_ch_date = uxcrec[1]
                        if (uxc_ch_date < ch_date or uxc_ch_date == ch_date) and ( ch_date == uxc_next_ch_date or ch_date < uxc_next_ch_date):
                            P = uxcrec[2]
                            T = uxcrec[3]
                            RH = uxcrec[4]
                        elif uxc_next_ch_date > ch_date:
                            break

                    if (vmon < 6400):
                        continue
                    if not flag == 56:
                        continue

                    # print("", _dpid,ch_date,imon,vmon,flag,dt,VmonAvg )                    
                    InstLumi=0
                    instbuf=0.0
                    intebuf=0.0
                    nbuf=0
                    for lumirec in lumidata:
                        lb = lumirec[0]
                        le = lumirec[1]
                        inst = lumirec[2]
                        inte = lumirec[3]
                        if (lb < ch_date or lb == ch_date) and ( ch_date == le or ch_date < le):
                            #                            print("chdate lb le",ch_date,lb,le)
                            instbuf = inst
                            intebuf = inte
                            nbuf = nbuf + 1
                        elif le > ch_date:
                            break

                            
                    if nbuf > 0:
                        instbuf = instbuf/nbuf
                        intebuf = intebuf/nbuf

                    rpccurrml.execute_query_self(table_training.get_insert_data_query(ch_date, imon, vmon, dpid, flag, instbuf, P, T, RH, intebuf, HwoL))
                
                rpccurrml.execute_commit_self()
                fromdate = todate
                
    def fill_imon_vmon_uxc_data_for_DPIDs(self, time_step_days=1):
        ce = Extractor_Oracle(self.oracle_connect)
        ce.set_flag_col_name("FLAG")
        ce.set_timestamp_col_name("CHANGE_DATE")
        ce.set_dpid_col_name("DPID")

        dp = DataPopulator(self.mysql_connect)

        for dpid in self.dpids:
            dpid = dpid.strip()
            fromdate=self.start_date
            last_vmon=0.0
            last_vmon_timestamp=self.start_date
            P=0.0
            T=0.0
            RH=0.0

            q = table_training.get_latest_HoursWithoutLumi_query(dpid)
            q_res = self.mysql_connect.fetchall_for_query_self(q)
            HwoL=0.0
            if len(q_res) == 1:
                HwoL = float(q_res[0][0])
            
            while fromdate < self.end_date: 
                todate = fromdate + relativedelta(days = time_step_days)
                ce.set_time_widow(fromdate, todate)
                # print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
                ll = 0
                hvidata = ce.get_rpccurrents_data_anyflag("cms_rpc_pvss_test.RPCCURRENTS", dpid, ["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
                uxcdata = dp.get_inst_lumi_data(table_uxcenv.tablename, lstart_col_name = table_uxcenv.change_date, select_col_list = [table_uxcenv.change_date, table_uxcenv.next_change_date, table_uxcenv.pressure, table_uxcenv.temperature, table_uxcenv.relative_humidity], startdate = fromdate, enddate = todate)
                lumidata = []
                if len(hvidata) > 0:
                    lumidata = dp.get_inst_lumi_data(table_lumi.tablename, lstart_col_name = table_lumi.ls_start, select_col_list = [table_lumi.ls_start, table_lumi.ls_stop, table_lumi.inst_lumi, table_lumi.integrated_lumi], startdate = fromdate, enddate = todate)
                
                for rpc_data in hvidata:
                    _dpid = rpc_data[0]
                    ch_date = rpc_data[1]
                    imon = rpc_data[2]
                    vmon = rpc_data[3]
                    flag = rpc_data[4]

                    dt = ch_date - last_vmon_timestamp
                    dt = dt.total_seconds()
                    
                    last_vmon = vmon
                    last_vmon_timestamp = ch_date

                    for uxcrec in uxcdata:
                        uxc_ch_date = uxcrec[0]
                        uxc_next_ch_date = uxcrec[1]
                        if (uxc_ch_date < ch_date or uxc_ch_date == ch_date) and ( ch_date == uxc_next_ch_date or ch_date < uxc_next_ch_date):
                            P = uxcrec[2]
                            T = uxcrec[3]
                            RH = uxcrec[4]
                        elif uxc_next_ch_date > ch_date:
                            break

                    if not flag == 56 and not P == 0:
                        HwoL = HwoL + (vmon/P)*dt

                    if (vmon < 6400):
                        continue
                    if not flag == 56:
                        continue

                    InstLumi = 0
                    instbuf = 0.0
                    intebuf = 0.0
                    nbuf = 0
                    for lumirec in lumidata:
                        lb = lumirec[0]
                        le = lumirec[1]
                        inst = lumirec[2]
                        inte = lumirec[3]
                        if (lb < ch_date or lb == ch_date) and ( ch_date == le or ch_date < le):
                            instbuf = inst
                            intebuf = inte
                            nbuf = nbuf + 1
                            break
                        elif le > ch_date:
                            break

                            
                    if nbuf > 0:
                        instbuf = instbuf/nbuf
                        intebuf = intebuf/nbuf
                        query = table_training.get_insert_data_query(ch_date, imon, vmon, dpid, flag, instbuf, P, T, RH, intebuf, HwoL)
                        rpccurrml.execute_query_self(query)
                
                rpccurrml.execute_commit_self()
                fromdate = todate
