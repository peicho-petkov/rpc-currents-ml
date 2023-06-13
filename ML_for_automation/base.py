import datetime

class dbConnector:
	''' Baseclass that holds host, username, password, database (if applicable) 
	and db conneciton object.
	the function get_cursor returns a cursor object '''
	def __init__(self, host, user, password, database=''):
		self._host = host
		self._user = user
		self._password = password
		self._database = database
		self._db = None

	def connect_to_db(self, database=''):
		raise NotImplementedError()

	def get_cursor(self):
		raise NotImplementedError()

	def execute_commit_query(self,cursor,query):
		raise NotImplementedError()

	def fetchall_for_query(self,cursor,query):
		raise NotImplementedError()


import cx_Oracle
class oracle_dbConnector(dbConnector):

	''' Oracle client wrapper '''
	def __init__(self, user, password, database=None, dsn_tns=None):
		self._user = user
		self._password = password
		self._database = database
		self._dsn_tns = dsn_tns
		self._db = None
		self._cursor = None

	def __del__(self):
		if self._cursor is not None:
			self._cursor.close() 
		if self._db is not None:
			self._db.close()

	def get_cursor(self):
		if self._cursor is not None:
	    		self._cursor.close()
		return self._db.cursor()

	def self_cursor_mode(self):
		self._cursor=self.get_cursor()

	def connect_to_db(self, database=None, dsn_tns=None):
		dbname=self._database
		dsn=self._dsn_tns
		if database!=None:
			dbname=database
		if dsn_tns!=None:
			dsn=dsn_tns
		print(f"dbname={dbname}")
		print(f"dsn={dsn}")

		assert (dbname is not None or dsn is not None), "either database name or dsn has to be set!"
		if dsn is not None:
			self._db = cx_Oracle.connect(self._user,self._password,dsn=dsn)
		if dbname is not None:
		    	self._db = cx_Oracle.connect(self._user,self._password,dbname)
		return self._db

	def connect_to_db_and_get_cursor(self, database=None, dsn_tns=None):
		self.connect_to_db(database,dsn_tns)      
		if self._db is not None:
			self._cursor=self.get_cursor()
		return self._cursor

	def execute_commit_query(self,cursor,query):
		cursor.execute(query)
		self._db.commit()

	def execute_query(self,cursor,query):
		cursor.execute(query)

	def execute_commit(self):
		self._db.commit()

	def execute_query_self(self,query):
		self.execute_query(self._cursor,query)

	def execute_commit_self(self):
		self.execute_commit()

	def fetchall_for_query(self,cursor,query):
		cursor.execute(query)
		return cursor.fetchall()

	def execute_commit_query_self(self,query):
		self.execute_commit_query(self._cursor,query)

	def fetchall_for_query_self(self,query):
		return self.fetchall_for_query(self._cursor,query)

class Extractor_Oracle:
	def __init__(self, oracle_dbcon=None):
		self.set_oracle_dbcon(oracle_dbcon)
		self._dbcon.self_cursor_mode()

	def set_startdate(self, startdate):
	        assert(isinstance(startdate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
	        self._startdate = startdate

	def set_enddate(self, enddate):
	        assert(isinstance(enddate, (datetime.datetime, datetime.date))), "startdate has to be of type datetime"
	        self._enddate = enddate

	def set_time_window(self, startdate, enddate):
	        self.set_startdate(startdate)
	        self.set_enddate(enddate)
	
	def set_chamber_ID(self, chid):
	        self._CHID = chid

	def set_FLAG(self, flag):
	        self._FLAG=flag

	def set_oracle_dbcon(self, dbcon):
		assert(isinstance(dbcon, oracle_dbConnector)), "dbcon is not of type oracle_dbConnector"
		self._dbcon = dbcon
	
	def set_tablename(self, tablename):
        	self._tablename = tablename
		
	def set_select_column_name_list(self, cnamelist):
        	self._column_names = cnamelist[:]

	def set_timestamp_col_name(self, ichange):
        	self._ichange_col_name = ichange
		
	def set_flag_col_name(self, flagcolname):
		self._flag_col_name = flagcolname
		
	def set_chamber_id_col_name(self, chidcolname):
            	self._chid_col_name = chidcolname
		
	def get_rpccurrents_data(self, tablename, chid, flag, select_col_list):
		self.set_chamber_ID(chid)
		self.set_tablename(tablename)
		self.set_FLAG(flag)
		self.set_select_column_name_list(select_col_list)
		query = "SELECT t.{collist} FROM {table} t where t.{chid_col}={chid} and BITAND(t.{flag_col},{flag})={flag} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
			table=self._tablename, collist=",t.".join(self._column_names),
		    	chid_col=self._chid_col_name, chid=self._CHID,
			flag_col=self._flag_col_name, flag=self._FLAG,
			ichange=self._ichange_col_name,
			startdate=self._startdate.strftime("%Y-%m-%d %H:%M:%S"),enddate=self._enddate.strftime("%Y-%m-%d %H:%M:%S"))
		print(query)
		return self._dbcon.fetchall_for_query_self(query)
	
	def get_rpccurrents_data_anyflag(self,tablename,chid,select_col_list):
		self.set_chamber_ID(chid)
		self.set_tablename(tablename)
		self.set_select_column_name_list(select_col_list)
		query = "SELECT t.{collist} FROM {table} t where t.{chid_col}={chid} and t.{ichange} BETWEEN TO_TIMESTAMP('{startdate}', 'YYYY-MM-DD HH24:MI:SS') and TO_TIMESTAMP('{enddate}', 'YYYY-MM-DD HH24:MI:SS') order by t.{ichange} asc".format(
			table=self._tablename, collist=",t.".join(self._column_names),
			chid_col=self._chid_col_name, chid=self._CHID,
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


