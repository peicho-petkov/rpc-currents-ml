import datetime
from dateutil.relativedelta import relativedelta
from db_tools.base import mysql_dbConnector
from db_tools.base import oracle_dbConnector
class Extractor_MySql:
    ''' Selects and gets the RPC imon and vmon datapoints
        for a given time window with a given flag
        startdate and enddate members are of class datetime.date
    '''
    def __init__(self,tablename,mysql_dbcon=None):
        self.set_mysql_dbcon(mysql_dbcon)
        self._tablename = tablename
        
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
        
    def set_mysql_dbcon(self,dbcon):
        assert(isinstance(dbcon,mysql_dbConnector))
        self._dbcon = dbcon
        
    def set_column_name_list(self,cnamelist):
        self._column_names = cnamelist[:]

    def get_data(self):       
        query = "SELECT {0} FROM {1}".format(self._tablename, ",".join(self._column_names))
        print(query)

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

    def insert_imon_record(self,rpccurr_table,dpid_col_name,ichange_col_name,imon_col_name,vmon_col_name,flag_col_name,rpccurr_data):
        query="INSERT INTO {table} ({dpid_col}, {ichange_col}, {imon_col}, {vmon_col}, {flag_col}) VALUES ('{dpid}','{ichange}','{imon}','{vmon}','{flag}')".format(table=rpccurr_table,
            dpid_col=dpid_col_name, ichange_col=ichange_col_name, imon_col=imon_col_name, vmon_col=vmon_col_name,flag_col=flag_col_name,
            dpid=rpccurr_data[0], ichange=rpccurr_data[1], imon=rpccurr_data[2], vmon=rpccurr_data[3], flag=rpccurr_data[4])
        self._dbcon.execute_query_self(query)

    def insert_imon_many(self,rpccurr_table,dpid_col_name,ichange_col_name,imon_col_name,vmon_col_name,flag_col_name,rpccurr_data):
        query="INSERT INTO {table} ({dpid_col}, {ichange_col}, {imon_col}, {vmon_col}, {flag_col}) VALUES (%s,%s,%s,%s,%s)".format(table=rpccurr_table,
            dpid_col=dpid_col_name, ichange_col=ichange_col_name, imon_col=imon_col_name, vmon_col=vmon_col_name,flag_col=flag_col_name)
        self._dbcon._cursor.executemany(query,rpccurr_data)

    def update_env_parameters(self,rpccurr_table,ichange_col_name,uxc_press_col_name,uxc_temp_col_name,uxc_rh_col_name,uxc_dp_colname,uxc_data):
        query="UPDATE {table} SET {press_col}={press}, {temp_col}={temp}, {rh_col}={rh}, {dp_col}={dp} WHERE {press_col}==NULL and {temp_col}==NULL and {rh_col}==NULL and {ichagne_col}<={uxc_change_time}".format(table=rpccurr_table, ichange_col=ichange_col_name,press_col=uxc_press_col_name,temp_col=uxc_temp_col_name,rh_col=uxc_rh_col_name,dp_col=uxc_dp_colname,uxc_change_time=uxc_data[0],press=uxc_data[1],temp=uxc_data[2],rh=uxc_data[3],dp=uxc_data[4])
        self._dbcon.execute_query_self(query)


def fill_inst_lumi_table():
    omds = oracle_dbConnector(user='CMS_RPC_R',password='rpcr34d3r')
    omds.connect_to_db('cms_omds_adg')

    rpccurrml = mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')

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

    rpccurrml = mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')

    ce = Extractor_Oracle(omds)

    ce.set_flag_col_name("FLAG")
    ce.set_timestamp_col_name("CHANGE_DATE")
    ce.set_dpid_col_name("DPID")

    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,1,1)
    edate=datetime.datetime(2018,12,12)

    flag=56

    dpids=open("/afs/cern.ch/user/p/ppetkov/work/public/dpids")
    
    for dpid in dpids:
        dpid=dpid.strip()

        fromdate=sdate
        while fromdate<edate: 
            todate=fromdate+relativedelta(months=1)
            ce.set_time_widow(fromdate,todate)
            fromdate=todate

            print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
            
            # rpcdata = ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS",dpid,flag,["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
            # dp.insert_imon_many(rpccurr_table="TrainingData",dpid_col_name="DPID",ichange_col_name="CHANGE_DATE", imon_col_name="IMON",vmon_col_name="VMON",flag_col_name="FLAG",rpccurr_data=rpcdata)
            # dp.commit_inserted_records()
            
            for rpc_data in ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS",dpid,flag,["DPID","CHANGE_DATE","IMON","VMON","FLAG"]):
                dp.insert_imon_record(rpccurr_table="TrainingData",dpid_col_name="DPID",ichange_col_name="CHANGE_DATE", imon_col_name="IMON",vmon_col_name="VMON",flag_col_name="FLAG",rpccurr_data=rpc_data)
  
            dp.commit_inserted_records()

if __name__ == "__main__":
    print("stating...")
    omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
    omds.connect_to_db('cman_int2r')

    rpccurrml = mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
    rpccurrml.connect_to_db('RPCCURRML')

    ce = Extractor_Oracle(omds)

    ce.set_flag_col_name("FLAG")
    ce.set_timestamp_col_name("CHANGE_DATE")
    ce.set_dpid_col_name("DPID")

    
    dp = DataPopulator(rpccurrml)
    
    sdate=datetime.datetime(2016,1,1)
    edate=datetime.datetime(2018,12,12)

    flag=56

    dpids=open("/afs/cern.ch/user/p/ppetkov/work/public/dpids")
    
    for dpid in dpids:
        dpid=dpid.strip()

        fromdate=sdate
        while fromdate<edate: 
            todate=fromdate+relativedelta(months=1)
            ce.set_time_widow(fromdate,todate)
            fromdate=todate

            print("dpid ",dpid, "start date ", ce._startdate," enddate ", ce._enddate)
            
            # rpcdata = ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS",dpid,flag,["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
            # dp.insert_imon_many(rpccurr_table="TrainingData",dpid_col_name="DPID",ichange_col_name="CHANGE_DATE", imon_col_name="IMON",vmon_col_name="VMON",flag_col_name="FLAG",rpccurr_data=rpcdata)
            # dp.commit_inserted_records()
            
            for uxc_data in ce.get_uxc_env_data("cms_rpc_pvss_test.UXC_ENVIRONMENT",["CHANGE_DATE","PRESSURE","TEMPERATURE","RELATIVE_HUMIDITY","DEWPOINT"]):
                dp.insert_imon_record(rpccurr_table="TrainingData",ichange_col_name='CHANGE_DATE',uxc_press_col_name='uxcPressure',uxc_temp_col_name='uxcTemperature',uxc_rh_col_name='uxcRH',uxc_dp_colname='uxcDPoint',uxc_data)
  
            dp.commit_inserted_records()

    # ce.set_time_widow(datetime.datetime(2018,10,10),datetime.datetime(2018,11,3))
    # print(ce._startdate)
    # print(ce._enddate)
    # ce.set_flag_col_name("FLAG")
    # ce.set_timestamp_col_name("CHANGE_DATE")
    # ce.set_dpid_col_name("DPID")
    # ce.get_rpccurrents_data("cms_rpc_pvss_test.RPCCURRENTS",315,56,["DPID","CHANGE_DATE","IMON","VMON","FLAG"])
    # ce.get_uxc_env_data("cms_rpc_pvss_test.UXC_ENVIRONMENT",["CHANGE_DATE","PRESSURE","TEMPERATURE","RELATIVE_HUMIDITY","DEWPOINT"])

    print("done...")
