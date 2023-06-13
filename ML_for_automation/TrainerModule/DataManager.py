import datetime
from dateutil.relativedelta import relativedelta
from db_tools.base import mysql_dbConnector
from db_tools.base import oracle_dbConnector
from db_tools import table_training, table_uxcenv, table_lumi

class Extractor_MySql:
    ''' Selects and gets the RPC imon and vmon datapoints
        for a given time window with a given flag
        startdate and enddate members are of class datetime.date
    '''
    def __init__(self,tablename,mysql_dbcon=None):
        self.set_mysql_dbcon(mysql_dbcon)
        self._tablename = tablename
        self.set_flag_col_name()
        self.set_chid_col_name()
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

    def set_chid_col_name(self,chidcolname='CHAMBER_ID'):
        self._chid_col_name = chidcolname
        
    def set_model_id_col_name(self,modelidcolname='model_id'):
        self._model_id_col_name = modelidcolname          
        
    def set_model_id(self, modelid):
        self._model_id = modelid
        
    def set_CHID(self,chid):
        self._CHID = chid

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

    def get_data_by_chid_flag_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._flag_col_name} = '{self._FLAG}' and {self._chid_col_name} = '{self._CHID}'"
        return query
        
    def get_data_by_model_id_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._model_id_col_name} = '{self._model_id}'"
        return query
        
    def get_data_by_chid_only_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between '{startdate_str}' and '{enddate_str}' and {self._chid_col_name} = '{self._CHID}'"
        return query

class Extractor_Oracle:
    ''' Selects and gets the RPC imon and vmon datapoints
        for a given time window with a given flag
        startdate and enddate members are of class datetime.date
    '''
    def __init__(self, tablename="CMS_RPC_PVSS_TEST.MLTRAININGDATA", oracle_dbcon=None):
        self.set_tablename(tablename)
        self.set_oracle_dbcon(oracle_dbcon)
        self._dbcon.self_cursor_mode()
        self.set_timestamp_col()
        #pass

    def set_startdate(self, startdate):
        assert(isinstance(startdate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._startdate = startdate
        
    def set_enddate(self, enddate):
        assert(isinstance(enddate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
        self._enddate = enddate
        
    def set_time_widow(self,startdate,enddate):
        self.set_startdate(startdate)
        self.set_enddate(enddate)
        
    def set_CHID(self,chid):
        self._CHID = chid
        
    def set_FLAG(self,flag):
        self._FLAG=flag
        
    def set_oracle_dbcon(self,dbcon):
        assert(isinstance(dbcon,(oracle_dbConnector,mysql_dbConnector)))
        self._dbcon = dbcon

    def set_tablename(self,tablename):
        self._tablename = tablename
        
    def set_select_column_name_list(self,cnamelist):
        self._column_names = cnamelist[:]

    #def set_timestamp_col_name(self,ichange):
    #    self._ichange_col_name = ichange
        
    def set_timestamp_col(self,col_name='CHANGE_DATE'):
        self._timestamp_col=col_name
    
    def set_flag_col_name(self,flagcolname):
        self._flag_col_name = flagcolname

    def set_chid_col_name(self,chidcolname):
        self._chid_col_name = chidcolname

    def get_rpccurrents_data(self,tablename,chid,flag,select_col_list):
        self.set_CHID(chid)
        self.set_tablename(tablename)
        self.set_FLAG(flag)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{chid_col}={chid} and BITAND(t.{flag_col},{flag})={flag} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            chid_col=self._chid_col_name, chid=self._CHID,
            flag_col=self._flag_col_name, flag=self._FLAG,
            ichange=self._ichange_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def get_rpccurrents_data_anyflag(self,tablename,chid,select_col_list):
        self.set_CHID(chid)
        self.set_tablename(tablename)
        self.set_select_column_name_list(select_col_list)
        query = "SELECT t.{collist} FROM {table} t where t.{chid_col}={chid} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
            table=self._tablename, collist=",t.".join(self._column_names),
            chid_col=self._chid_col_name, chid=self._CHID,
            flag_col=self._flag_col_name,
            ichange=self._ichange_col_name,
            startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
        return self._dbcon.fetchall_for_query_self(query)

    def get_data_by_chid_flag_query(self):
        collist = ",".join(self._column_names)
        startdate_str = self._startdate.strftime("%Y-%m-%d %H:%M:%S")
        enddate_str = self._enddate.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT {collist} FROM {self._tablename} where {self._timestamp_col} between TO_TIMESTAMP('{startdate_str}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate_str}', 'YYYY-MM-DD HH24:MI:SS') and {self._flag_col_name} = '{self._FLAG}' and {self._chid_col_name} = '{self._CHID}'"
        return query
    
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

