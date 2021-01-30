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

class TrainigDataTable(dbTable):
    def __init__(self,tablename='TrainigData'):
        super().__init__(tablename)
        self.add_call("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_change_date_col()
        self.set_iom_col()
        self.set_vom_col()
        self.set_pdid_col()
        self.set_flag_col()
        self.set_inst_lumi_col()
        self.set_uxc_p()
        self.set_uxc_t()
        self.set_uxc_rh()
        self.set_uxc_dp()
        self.set_integrated_lumi()
        self.set_hours_without_lumi()
        
        
    def set_iom_col(self,name='IMON',type="float not null"):
        self.imon=name
        self.add_coll(name,type)

    def set_vom_col(self,name='VMON',type="float not null"):
        self.vmon=name
        self.add_coll(name,type)
    
    def set_pdid_col(self,name='DPID',type="mediumint not null"):
        self.dpid=name
        self.add_coll(name,type)

    def set_change_date_col(self,name="CHANGE_DATE",type="timestamp not null"):
        self.change_date=name
        self.add_coll(name,type)

    def set_flag_col(self,name="FLAG",type="smallint not null"):
        self.flag=name
        self.add_coll(name,type)

    def set_inst_lumi_col(self,name="InstLumi",type="loat default null"):
        self.instant_lumi=name
        self.add_coll(name,type)
    
    def set_uxc_p(self,name="uxcPressure",type="float default null"):
        self.uxcP=name
        self.add_coll(name,type)

    def set_uxc_t(self,name="uxcTemperature",type="float default null"):
        self.uxcT=name
        self.add_coll(name,type)

    def set_uxc_rh(self,name="uxcRH",type="float default null"):
        self.uxcRH=name
        self.add_coll(name,type)
	    
    def set_uxc_dp(self,name="uxcDPoint",type="float default null"):
        self.uxcDP=name
        self.add_coll(name,type)

    def set_integrated_lumi(self,name="IntegratedLumi",type="float default null"):
        self.interated_lumi=name
        self.add_coll(name,type)

    def set_hours_without_lumi(self,name="HoursWithoutLumi",type="float default null"):
        self.hours_without_lumi=name
        self.add_coll(name,type)

class LumiDataTable(dbTable):
    def __init__(self, tablename):
        super().__init__(tablename)
        self.add_call("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_ls_start_col()
        self.set_ls_stop_col()
        self.set_inst_lumi()
        self.set_integrated_lumi()

    def set_ls_start_col(name="STARTTIME",type="TIMESTAMP not null"):
        self.ls_start=name
        self.add_coll(name,type)

    def set_ls_stop_col(name="STOPTIME",type="TIMESTAMP not null"):
        self.ls_stop=name
        self.add_coll(name,type) 

    def set_inst_lumi(name="INSTLUMI",type="FLOAT not null"):
        self.inst_lumi=name
        self.add_coll(name,type)

    def set_integrated_lumi(name="INTEGRATED",type="FLOAT default null"):
        self.integrate_lumi=name
        self.add_coll(name,type)

class UxcEnvTable(dbTable):
    def __init__(self, tablename):
        super().__init__(tablename) 
        self.add_call("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")  
        self.set_change_date_col()
        self.set_next_change_date_col()
        self.set_pressure()
        self.set_temperature()
        self.set_relative_humidity()

    def set_change_date_col(self,name="CHANGE_DATE",type="timestamp not null"):
        self.change_date=name
        self.add_coll(name,type)

    def set_next_change_date_col(self,name="NEXT_CHANGE_DATE",type="timestamp not null"):
        self.next_change_date=name
        self.add_coll(name,type)

    def set_pressure(self,name="uxcPressure",type="float default null"):
        self.pressure=name
        self.add_coll(name,type)

    def set_temperature(self,name="uxcTemperature",type="float default null"):
        self.temperature=name
        self.add_coll(name,type)

    def set_relative_humidity(self,name="uxcRH",type="float default null"):
        self.relative_humidity=name
        self.add_coll(name,type) 

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

#CREATE TABLE UXC_ENV ( rec_id bigint auto_increment primary key, LAST_UPDATE timestamp not null, CHANGE_DATE timestamp not null, NEXT_CHANGE_DATE timestamp not null, uxcPressure float default null, uxcTemperature float default null, uxcRH float default null);
