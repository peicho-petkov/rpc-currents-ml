import datetime
from db_tools.base import mysql_dbConnector

class Currents_Extractor:
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
        
    def set_mysql_dbcon(self,dbcon):
        assert(isinstance(dbcon,mysql_dbConnector))
        self._dbcon = dbcon
        
    def set_column_name_list(self,cnamelist):
        self._column_names = cnamelist[:]

    def get_data(self):       
        query = "SELECT {0} FROM {1}".format(self._tablename, ",".join(self._column_names))
        print(query)
         
if __name__ == "__main__":
    print("stating...")
    ce = Currents_Extractor()
    ce.set_enddate(datetime.datetime(2018,10,10))
    ce.set_time_widow(datetime.datetime(2017,10,10),datetime.datetime(2018,1,1))
    print(ce._startdate)
    print(ce._enddate)
    ce.set_column_name_list(["aaaaa",'kkkkk',"vvvvv"])
    ce.get_data("RPCCURRTRAINING")
    print("done...")