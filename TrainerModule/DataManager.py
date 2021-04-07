import datetime
from dateutil.relativedelta import relativedelta
from db_tools.base import mysql_dbConnector
from db_tools.base import oracle_dbConnector
from db_tools import table_training, table_uxcenv, table_lumi, rpccurrml

class Extractor_MySql:
    ''' Selects and gets the RPC imon and vmon datapoints
        for a given time window with a given flag
        startdate and enddate members are of class datetime.date
    '''
    def __init__(self,tablename,mysql_dbcon=None):
        self.set_mysql_dbcon(mysql_dbcon)
        self._tablename = tablename
        self.set_flag_col_name()
        self.set_dpid_col_name()
        self.set_flag_col_name()
        self.set_timestamp_col()

    def set_startdate(self, startdate):
        assert(isinstance(startdate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._startdate = startdate
    
    def set_enddate(self, enddate):
        assert(isinstance(enddate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._enddate = enddate
    
    def set_time_widow(self,startdate,enddate):
        self.set_startdate(startdate)
        self.set_enddate(enddate)
        
    def set_timestamp_col(self,col_name='CHANGE_DATE'):
        self._timestamp_col=col_name
    
    def set_flag_col_name(self,flagcolname='FLAG'):
        self._flag_col_name = flagcolname

    def set_dpid_col_name(self,dpidcolname='DPID'):
        self._dpid_col_name = dpidcolname
                
    def set_model_id_col_name(self,modelidcolname='model_id'):
        self._model_id_col_name = modelidcolname          
    
    def set_model_id(self, modelid):
        self._model_id = modelid
    
    def set_DPID(self,dpid):
        self._DPID = dpid

    def set_FLAG(self,flag):
        self._FLAG=flag
        
    def set_mysql_dbcon(self,dbcon):
        assert(isinstance(dbcon,mysql_dbConnector))
        self._dbcon = dbcon
        self._dbcon.self_cursor_mode()
        
    def set_column_name_list(self,cnamelist):
        self._column_names = cnamelist[:]

    def get_data_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}'"
        return query

    def get_data_by_dpid_flag_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._flag_col_name} = '{self._FLAG}' and {self._dpid_col_name} = '{self._DPID}'"
        return query
    
    def get_data_by_model_id_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._model_id_col_name} = '{self._model_id}'"
        return query
    
    def get_data_by_dpid_only_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._dpid_col_name} = '{self._DPID}'"
        return query

class Extractor_Oracle:
    ''' Selects and gets the RPC imon and vmon datapoints
        for a given time window with a given flag
        startdate and enddate members are of class datetime.date
    '''
    def __init__(self,oracle_dbcon=None):
        self.set_oracle_dbcon(oracle_dbcon)
        self._dbcon.self_cursor_mode()
        pass
    def set_startdate(self, startdate):
        assert(isinstance(startdate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._startdate = startdate
    
    def set_enddate(self, enddate):
        assert(isinstance(enddate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._enddate = enddate
    
    def set_time_widow(self,startdate,enddate):
        self.set_startdate(startdate)
        self.set_enddate(enddate)
        
    def set_DPID(self,dpid):
        self._DPID = dpid
    
    def set_FLAG(self,flag):
        self._FLAG=flag
        
    def set_oracle_dbcon(self,dbcon):
        assert(isinstance(dbcon,(oracle_dbConnector,mysql_dbConnector)))
        self._dbcon = dbcon

    def set_tablename(self,tablename):
        self._tablename = tablename
        
    def set_select_column_name_list(self,cnamelist):
        self._column_names = cnamelist[:]

    def set_timestamp_col_name(self,ichange):
        self._ichange_col_name = ichange
    
    def set_flag_col_name(self,flagcolname):
        self._flag_col_name = flagcolname

    def set_dpid_col_name(self,dpidcolname):
        self._dpid_col_name = dpidcolname

    def get_rpccurrents_data(self,tablename,dpid,flag,select_col_list):
        self.set_DPID(dpid)
        self.set_tablename(tablename)
        self.set_FLAG(flag)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{dpid_col}={dpid} and BITAND(t.{flag_col},{flag})={flag} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            dpid_col=self._dpid_col_name, dpid=self._DPID,
            flag_col=self._flag_col_name, flag=self._FLAG,
            ichange=self._ichange_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def get_rpccurrents_data_anyflag(self,tablename,dpid,select_col_list):
        self.set_DPID(dpid)
        self.set_tablename(tablename)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{dpid_col}={dpid} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            dpid_col=self._dpid_col_name, dpid=self._DPID,
            flag_col=self._flag_col_name,
            ichange=self._ichange_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def get_uxc_env_data(self,tablename,select_col_list):
        self.set_tablename(tablename)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            ichange=self._ichange_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def get_inst_lumi_data(self,tablename,lstart_col_name,select_col_list):
        self.set_tablename(tablename)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{lstart} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{lstart} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            lstart=lstart_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    

class DataPopulator:
    def __init__(self,mysql_dbcon=None):
        self.set_mysql_dbcon(mysql_dbcon)
        self._dbcon.self_cursor_mode()


    def set_mysql_dbcon(self,dbcon):
        assert(isinstance(dbcon,mysql_dbConnector))
        self._dbcon = dbcon

    def commit_inserted_records(self):
        self._dbcon.execute_commit_self()

    def insert_inst_lumi_record(self,instlumi_table,starttime_col_name,stoptime_col_name,instlumi_col_name,inst_lumi_data):
        query="INSERT INTO {table} ({start_col}, {stop_col}, {instlumi_col}) VALUES ('{starttime}', '{stoptime}', '{instlumi}')".format(table=instlumi_table,
            start_col=starttime_col_name,stop_col=stoptime_col_name,instlumi_col=instlumi_col_name,
            starttime=inst_lumi_data[0], stoptime=inst_lumi_data[1],instlumi=inst_lumi_data[2]
        )
        self._dbcon.execute_query_self(query)

    def get_max_colname(self,tablename,col_name):
        query="SELECT MAX({col}) from {table}".format(col=col_name,table=tablename)
        intlumi=self._dbcon.fetchall_for_query_self(query)
        return intlumi[0][0]

    def get_min_colname_cond(self,tablename,col_name, condition):
        query="SELECT min({col}) from {table} {where}".format(col=col_name,table=tablename,where=condition)
        intlumi=self._dbcon.fetchall_for_query_self(query)
        return intlumi[0][0]

    def update_integrated_lumi_record(self,instlumi_table,integrated_lumi_col_name,rec_id,integrated_lumi):
        query="UPDATE {table_name} SET {set_colname}={set_data} WHERE rec_id={rec}".format(table_name=instlumi_table,set_colname=integrated_lumi_col_name,set_data=integrated_lumi,rec=rec_id)
        #print(query)
        self._dbcon.execute_query_self(query)

    def get_inst_lumi_data(self,tablename,lstart_col_name,select_col_list,startdate,enddate):
        query = "SELECT {collist} FROM {table} where {lstart} BETWEEN '{startdate}' and '{enddate}' order by {lstart} asc".format(
            table=tablename, collist=",".join(select_col_list),
            lstart=lstart_col_name,
            startdate=startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def insert_imon_record(self,rpccurr_table,dpid_col_name,ichange_col_name,imon_col_name,vmon_col_name,flag_col_name,rpccurr_data):
        query="INSERT INTO {table} ({dpid_col}, {ichange_col}, {imon_col}, {vmon_col}, {flag_col}) VALUES ('{dpid}','{ichange}','{imon}','{vmon}','{flag}')".format(table=rpccurr_table,
            dpid_col=dpid_col_name, ichange_col=ichange_col_name, imon_col=imon_col_name, vmon_col=vmon_col_name,flag_col=flag_col_name,
            dpid=rpccurr_data[0], ichange=rpccurr_data[1], imon=rpccurr_data[2], vmon=rpccurr_data[3], flag=rpccurr_data[4])
        self._dbcon.execute_query_self(query)

    def insert_imon_many(self,rpccurr_table,dpid_col_name,ichange_col_name,imon_col_name,vmon_col_name,flag_col_name,rpccurr_data):
        query="INSERT INTO {table} ({dpid_col}, {ichange_col}, {imon_col}, {vmon_col}, {flag_col}) VALUES (%s,%s,%s,%s,%s)".format(table=rpccurr_table,
            dpid_col=dpid_col_name, ichange_col=ichange_col_name, imon_col=imon_col_name, vmon_col=vmon_col_name,flag_col=flag_col_name)
        self._dbcon._cursor.executemany(query,rpccurr_data)

    def update_env_parameters(self, uxc_table, uxc_press_col_name,uxc_temp_col_name,uxc_rh_col_name,change_date_col,until_col_name,uxc_data,until_timestamp):

        query="INSERT INTO {table} ({press_col}, {temp_col}, {rh_col}, {change_date_col}, {until_col}) VALUES ('{press}', '{temp}', '{rh}', '{change_date}','{until}')".format(table=uxc_table, change_date_col=change_date_col,press_col=uxc_press_col_name,temp_col=uxc_temp_col_name,rh_col=uxc_rh_col_name,until_col=until_col_name,change_date=uxc_data[0],press=uxc_data[1],temp=uxc_data[2],rh=uxc_data[3],until=until_timestamp)
        self._dbcon.execute_query_self(query)

def insert_integrated_lumi():
    dp = DataPopulator(rpccurrml)
    
    sdate=dp.get_min_colname_cond(tablename='LUMI_DATA',col_name="STARTTIME",condition="where INTEGRATED IS NULL")
    edate=datetime.datetime(2018,12,12)
    fromdate=sdate
    intlumi = dp.get_max_colname(tablename='LUMI_DATA',col_name="INTEGRATED")
    if intlumi is None:
        intlumi=0.0
    while fromdate<edate: 
        todate=fromdate+relativedelta(months=1)
        print(fromdate,todate,intlumi)
        for lumirecid,instlumi in dp.get_inst_lumi_data('LUMI_DATA',lstart_col_name="STARTTIME",select_col_list=['rec_id','INSTLUMI'],startdate=fromdate,enddate=todate):
            intlumi = float(intlumi) + float(instlumi)
            dp.update_integrated_lumi_record('LUMI_DATA',"INTEGRATED",lumirecid,intlumi)
            #print("recid",lumirecid,"inst lumi",instlumi,"integr",intlumi)
        dp.commit_inserted_records()
        fromdate=todate

def fill_inst_lumi_table():
    omds = oracle_dbConnector(user='CMS_RPC_R',password='rpcr34d3r')
    omds.connect_to_db('cms_omds_adg')

    ce = Extractor_Oracle(omds)
    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,1,1)
    edate=datetime.datetime(2018,12,12)

    fromdate=sdate

    while fromdate<edate: 
        todate=fromdate+relativedelta(months=1)
        ce.set_time_widow(fromdate,todate)
        fromdate=todate

        print(ce._startdate,ce._enddate)

        for instlumidata in ce.get_inst_lumi_data("cms_runtime_logger.lumi_sections",
                                                  "STARTTIME",["STARTTIME","STOPTIME","INSTLUMI"]):
            dp.insert_inst_lumi_record('LUMI_DATA',"STARTTIME","STOPTIME","INSTLUMI",instlumidata)
   
        dp.commit_inserted_records()  

def fill_imon_vmon_data():
    omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
    omds.connect_to_db('cman_int2r')

    ce = Extractor_Oracle(omds)

    ce.set_flag_col_name("FLAG")
    ce.set_timestamp_col_name("CHANGE_DATE")
    ce.set_dpid_col_name("DPID")

    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,1,1)
    edate=datetime.datetime(2018,12,12)
    
    flag=56

    dpids=open("/afs/cern.ch/user/p/ppetkov/work/public/dpids-sample")
    
    for dpid in dpids:
        dpid=dpid.strip()

        fromdate=sdate
        while fromdate<edate: 
            todate=fromdate+relativedelta(months=1)
            ce.set_time_widow(fromdate,todate)
            fromdate=todate

            print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
            
            for rpc_data in ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS",dpid,flag,["DPID","CHANGE_DATE","IMON","VMON","FLAG"]):
                dp.insert_imon_record(rpccurr_table="TrainingData",dpid_col_name="DPID",ichange_col_name="CHANGE_DATE", imon_col_name="IMON",vmon_col_name="VMON",flag_col_name="FLAG",rpccurr_data=rpc_data)
  
            dp.commit_inserted_records()

def update_uxc_data():
    print("stating...")
    omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
    omds.connect_to_db('cman_int2r')

    ce = Extractor_Oracle(omds)

    ce.set_flag_col_name("FLAG")
    ce.set_timestamp_col_name("CHANGE_DATE")
    ce.set_dpid_col_name("DPID")

    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,1,1)
    edate=datetime.datetime(2018,12,12)

    flag=56
    fromdate=sdate
    old_data=[]
    while fromdate<edate: 
        todate=fromdate+relativedelta(days=1)
        ce.set_time_widow(fromdate,todate)
        fromdate=todate
        
        print("start date ", ce._startdate," enddate ", ce._enddate)
        
        for uxc_data in ce.get_uxc_env_data("cms_rpc_pvss_test.UXC_ENVIRONMENT",["CHANGE_DATE","PRESSURE","TEMPERATURE","RELATIVE_HUMIDITY","DEWPOINT"]):
            if old_data[1:4]!=uxc_data[1:4] and len(old_data)==5:
                print("sending to db: different old ",old_data," new ", uxc_data)
                dp.update_env_parameters(uxc_table="UXC_ENV",uxc_press_col_name='uxcPressure',uxc_temp_col_name='uxcTemperature',uxc_rh_col_name='uxcRH',change_date_col='CHANGE_DATE',until_col_name='NEXT_CHANGE_DATE',uxc_data=old_data,until_timestamp=uxc_data[0])
                old_data=uxc_data[:]
            if(len(old_data)<5):
                old_data=uxc_data[:]
        
        dp.commit_inserted_records()

    print("done...")

def test():

    uxc_data = rpccurrml.fetchall_for_query_self("select CHANGE_DATE,NEXT_CHANGE_DATE,uxcPressure,uxcTemperature,uxcRH from UXC_ENV")

    for rr in uxc_data[1500:]:
 #       uxc_rec = rpccurrml.fetchall_for_query_self("select  from UXC_ENV")
        print(rr)
        recids = rpccurrml.fetchall_for_query_self("select rec_id from TrainingData where CHANGE_DATE between '{start_date}' and '{stop_date}'".format(start_date=rr[0],stop_date=rr[1]))
        print(recids)
        for trec in recids:
            rpccurrml.execute_query_self("UPDATE TrainingData SET uxcPressure={press}, uxcTemperature={temp}, uxcRH={rh}  WHERE rec_id={rec}".format(press=rr[2],temp=rr[3],rh=rr[4],rec=trec[0]))
        rpccurrml.execute_commit_self()

def fill_imon_vmon_uxc_data():
    omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
    omds.connect_to_db('cman_int2r')

    ce = Extractor_Oracle(omds)

    ce.set_flag_col_name("FLAG")
    ce.set_timestamp_col_name("CHANGE_DATE")
    ce.set_dpid_col_name("DPID")

    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,5,1)
    edate=datetime.datetime(2018,12,12)

    dpids=open("/afs/cern.ch/user/p/ppetkov/work/public/dpids-sample")
    
    for dpid in dpids:
        dpid=dpid.strip()
        VmonLast=0.0
        fromdate=sdate
        VmonXt=0.0
        dt_last=0
        VmonAvg=0.0
        R=0.0
        T=0.0
        RH=0.0
        while fromdate<edate: 
            todate=fromdate+relativedelta(days=1)
            ce.set_time_widow(fromdate,todate)
            print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
            ll = 0
            hvidata=ce.get_rpccurrents_data_anyflag("cms_rpc_pvss_test.RPCCURRENTS",dpid,["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
            uxcdata=dp.get_inst_lumi_data(table_uxcenv.tablename,lstart_col_name=table_uxcenv.change_date,select_col_list=[table_uxcenv.change_date,table_uxcenv.next_change_date,table_uxcenv.pressure,table_uxcenv.temperature,table_uxcenv.relative_humidity],startdate=fromdate,enddate=todate)
            lumidata = []
            if len(hvidata)>0:
                lumidata=dp.get_inst_lumi_data(table_lumi.tablename,lstart_col_name=table_lumi.ls_start,select_col_list=[table_lumi.ls_start,table_lumi.ls_stop,table_lumi.inst_lumi,table_lumi.integrated_lumi],startdate=fromdate,enddate=todate)
            
            for rpc_data in hvidata:
                _dpid=rpc_data[0]
                ch_date=rpc_data[1]
                imon=rpc_data[2]
                vmon=rpc_data[3]
                flag=rpc_data[4]
                dt = ch_date-fromdate
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
                # print("============")
                # print("P T RH",P , T, RH)
                # print(rpccurrml.fetchall_for_query_self(table_uxcenv.get_data_query(ch_date)))
                # print("============")
                if not flag==56:
                    VmonXt = VmonXt + VmonLast*dt
                
                VmonLast = vmon 

#                table_lumi.get_inst_int_lumi_query(ch_date)

                if (vmon<6400):
                    continue
                if not flag==56:
                    continue

                print("", _dpid,ch_date,imon,vmon,flag,dt,VmonAvg )
                
                InstLumi=0

                print('______________________')
                #                   print(table_lumi.get_inst_int_lumi_query(ch_date))
                #                   print(rpccurrml.fetchall_for_query_self(table_lumi.get_inst_int_lumi_query(ch_date)))
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
                    instbuf=instbuf/nbuf
                    intebuf=intebuf/nbuf
                print(table_training.get_insert_data_query(ch_date,imon,vmon,dpid,flag,instbuf,P,T,RH,intebuf,VmonAvg))
                rpccurrml.execute_query_self(table_training.get_insert_data_query(ch_date,imon,vmon,dpid,flag,instbuf,P,T,RH,intebuf,VmonAvg))
                print('^^^^^^^^^^^^^^^^^^^^^^')
            
            rpccurrml.execute_commit_self()
            dt = todate-fromdate
            dt = dt.total_seconds()
            VmonAvg= VmonAvg + VmonXt / dt / 1000.0
            VmonXt = 0.0
            fromdate=todate
 
def test_mysql_extractor():

    TrainingTable_extractor = Extractor_MySql(table_training.tablename,rpccurrml)
    
    TrainingTable_extractor.set_startdate(datetime.datetime(2016,5,29))
    TrainingTable_extractor.set_enddate(datetime.datetime(2016,5,31))
    
    TrainingTable_extractor.set_column_name_list([table_training.imon,table_training.vmon])
    
    TrainingTable_extractor.set_FLAG(56)
    TrainingTable_extractor.set_DPID(315)
    
    print(TrainingTable_extractor.get_data())
            
if __name__=='__main__':
#    fill_imon_vmon_data()
#    update_uxc_data()
#    insert_integrated_lumi()
#    fill_imon_vmon_uxc_data()
    test_mysql_extractor()