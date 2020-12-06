class dbTable:
    def __init__(self,tablename):
        self.tablename=str(tablename)
        self.colls={}
    
    def add_coll(self,colname,coltype):
        self.colls[str(colname)]=str(coltype)
    
    def del_coll(self,colname):
        del self.colls[str(colname)]
    
    def get_myqsl_create_query(self):
        query='CREATE TABLE {} ('.format(self.tablename)
        isFirst=True
        for colname, coltype in self.colls.items():
            if isFirst:
                query = "{} {} {}".format(query,colname,coltype)
                isFirst=False
            else:
                query = "{}, {} {}".format(query,colname,coltype)
        query=query+')'
        return query
    
    def get_notnull_coll_names(self):
        collnames=[]
        for colname, coltype in self.colls.items():
            if "not null" in str(coltype).to_lower():
                collnames.append(conname)
        return collnames
    
from base import mysql_dbConnector

if __name__ == "__main__":
    print("creating...")

    TrainingData = dbTable("TrainingData")
    TrainingData.add_coll("rec_id","bigint auto_increment primary key")
    
    TrainingData.add_coll("DPID","mediumint not null")
    TrainingData.add_coll("CHANGE_DATE","timestamp not null")
    TrainingData.add_coll("IMON","float not null")
    TrainingData.add_coll("VMON","float not null")
    TrainingData.add_coll("FLAG","smallint not null")

    TrainingData.add_coll("InstLumi","float default null")

    TrainingData.add_coll("uxcPressure","float default null")
    TrainingData.add_coll("uxcTemperature","float default null")
    TrainingData.add_coll("uxcRH","float default null")
    TrainingData.add_coll("uxcDPoint","float default null")

    TrainingData.add_coll("IntegratedLumi","float default null")

    TrainingData.add_coll("HoursWithoutLumi","int default null")

    Lumidata = dbTable("LUMI_DATA")
    Lumidata.add_coll("rec_id","bigint auto_increment primary key")
    Lumidata.add_coll("lastupdate","TIMESTAMP default CURRENT_TIMESTAMP")
    Lumidata.add_coll("STARTTIME","TIMESTAMP not null")
    Lumidata.add_coll("STOPTIME","TIMESTAMP not null")
    Lumidata.add_coll("INSTLUMI","FLOAT not null")
    Lumidata.add_coll("INTEGRATED","FLOAT default null")

    print(TrainingData.get_myqsl_create_query())
    print(Lumidata.get_myqsl_create_query())

