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


import mysql.connector
class mysql_dbConnector(dbConnector):
    ''' mysql client wrapper '''
    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password
        self._database = None
        self._db = None
        self._cursor = None

    def __del__(self):
        if self._db is not None:
            self._db.close()


    def connect_to_db(self, database=None):
        dbname=self._database

        if database is not None:
            dbname=database

#        assert (dbname==None), "Database name not set!"
        
        self._db=mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=dbname
                )
        return self._db

    def connect_to_db_and_get_cursor(self, database=None):
        self.connect_to_db(database)      
        if self._db is not None:
            self._cursor=self.get_cursor()
        return self._db


    def get_cursor(self):
        if self._cursor is not None:
            self._cursor.close()
        return self._db.cursor()

    def self_cursor_mode(self):
        self._cursor=self.get_cursor()

    def execute_commit_query(self,cursor,query):
        cursor.execute(query)
        self._db.commit()

    def fetchall_for_query(self,cursor,query):
        cursor.execute(query)
        return cursor.fetchall()
    
    def execute_commit_query_self(self,query):
        self.execute_commit_query(self._cursor,query)
        
    def fetchall_for_query_self(self,query):
        return self.fetchall_for_query(self._cursor,query)
    
    def execute_query(self,cursor,query):
        cursor.execute(query)
    
    def execute_commit(self):
        self._db.commit()
    
    def execute_query_self(self,query):
        self.execute_query(self._cursor,query)
    
    def execute_commit_self(self):
        self.execute_commit()


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

        assert (dbname is None or dsn is None), "either database name or dsn has to be set!"
        if dsn is not None:
            self._db = cx_Oracle.connect (self._user,self._password,dsn=dsn)
        if dbname is not None:
            self._db = cx_Oracle.connect (self._user,self._password,dbname)
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
