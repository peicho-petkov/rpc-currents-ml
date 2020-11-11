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
    def __init__(self, host, user, password, database):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._db = database

    def connect_to_db(self, database=''):
        assert (database=='' and self._db==''), "Database name not set!"
        dbname=self._db
        if database!='':
            dbname=database
        self._db=mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=dbname
                )
        return self._db

    def get_cursor(self):
        return self._db.cursor()

    def execute_commit_query(self,cursor,query):
        cursor.execute(query)
        cursor.commit()

    def fetchall_for_query(self,cursor,query):
        cursor.execute(query)
        return cursor.fetchall()
