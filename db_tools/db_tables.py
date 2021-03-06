
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
                collnames.append(collnames)
        return collnames
    
    def get_col_names(self):
        return list(self.colls)

class TrainingDataTable(dbTable):
    def __init__(self,tablename='TrainingData'):
        super().__init__(tablename)
        self.add_coll("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_change_date_col()
        self.set_imon_col()
        self.set_vmon_col()
        self.set_pdid_col()
        self.set_flag_col()
        self.set_inst_lumi_col()
        self.set_uxc_p()
        self.set_uxc_t()
        self.set_uxc_rh()
        self.set_uxc_dp()
        self.set_integrated_lumi()
        self.set_hours_without_lumi()
        
    def get_insert_data_query(self,chdate,imon,vmon,dpid,flag,inst_lumi,p,t,rh,int_lumi,hrs_wo_lumi):
        query="INSERT INTO {table} ({dpid_col}, {ichange_col}, {imon_col}, {vmon_col}, {flag_col}, {p_col}, {t_col}, {rh_col}, {inst_col}, {integrated_col}, {h_wo_lumi}) VALUES ('{dpid}','{ichange}','{imon}','{vmon}','{flag}','{p}','{t}','{rh}','{instl}','{intl}','{hwol}')".format(table=self.tablename,
            dpid_col=self.dpid, ichange_col=self.change_date, imon_col=self.imon, vmon_col=self.vmon,flag_col=self.flag, p_col=self.uxcP, t_col=self.uxcT, rh_col=self.uxcRH, inst_col=self.instant_lumi, integrated_col=self.integrated_lumi, h_wo_lumi=self.hours_without_lumi,
            dpid=dpid, ichange=chdate, imon=imon, vmon=vmon, flag=flag, p=p, t=t, rh=rh, instl=inst_lumi, intl=int_lumi,hwol=hrs_wo_lumi)
        return query
        
    def set_imon_col(self,name='IMON',type="float not null"):
        self.imon=name
        self.add_coll(name,type)

    def set_vmon_col(self,name='VMON',type="float not null"):
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
        self.integrated_lumi=name
        self.add_coll(name,type)

    def set_hours_without_lumi(self,name="HoursWithoutLumi",type="float default null"):
        self.hours_without_lumi=name
        self.add_coll(name,type)

class LumiDataTable(dbTable):
    def __init__(self, tablename='LUMI_DATA'):
        super().__init__(tablename)
        self.add_coll("modelconf_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_ls_start_col()
        self.set_ls_stop_col()
        self.set_inst_lumi()
        self.set_integrated_lumi()

    def set_ls_start_col(self,name="STARTTIME",type="TIMESTAMP not null"):
        self.ls_start=name
        self.add_coll(name,type)

    def set_ls_stop_col(self,name="STOPTIME",type="TIMESTAMP not null"):
        self.ls_stop=name
        self.add_coll(name,type) 

    def set_inst_lumi(self,name="INSTLUMI",type="FLOAT not null"):
        self.inst_lumi=name
        self.add_coll(name,type)

    def set_integrated_lumi(self,name="INTEGRATED",type="FLOAT default null"):
        self.integrated_lumi=name
        self.add_coll(name,type)
        
    def get_inst_int_lumi_query(self,timestamp):
        query = "select {inst_col}, {integrated_col} from {table} where '{timest}' between {st_col} and {end_col}".format(table=self.tablename,inst_col=self.inst_lumi,integrated_col=self.integrated_lumi,timest=timestamp.strftime("%Y-%m-%d %H:%M:%S"),st_col=self.ls_start,end_col=self.ls_stop)
        return query
class UxcEnvTable(dbTable):
    def __init__(self, tablename='UXC_ENV'):
        super().__init__(tablename) 
        self.add_coll("rec_id","bigint auto_increment primary key")
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
        
    def get_data_query(self,timestamp):
        query = "select {p_col}, {t_col}, {rh_col} from {table} where '{timest}' between {lastch_col} and {nextch_col}".format(table=self.tablename,p_col=self.pressure,t_col=self.temperature,rh_col=self.relative_humidity,timest=timestamp.strftime("%Y-%m-%d %H:%M:%S"),lastch_col=self.change_date,nextch_col=self.next_change_date)
        return query

class MLModels(dbTable):
    def __init__(self, tablename='MLModels'):
        super().__init__(tablename)
        self.add_coll("model_id","bigint auto_increment primary key")
        self.model_id = 'model_id'
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_modelconf_id()
        self.set_dpid()
        self.set_r2()
        self.set_mse()
        self.set_model_path()
        self.set_mojo_path()

    def set_modelconf_id(self,name="MODELCONF_ID",type="int not null"):
        self.modelconf_id=name
        self.add_coll(name,type)
        
    def set_dpid(self,name="DPID",type="int not null"):
        self.dpid=name
        self.add_coll(name,type)
        
    def set_r2(self,name="R2",type="float default null"):
        self.r2=name
        self.add_coll(name,type)

    def set_mse(self,name="MSE",type="float default null"):
        self.mse=name
        self.add_coll(name,type)
        
    def set_model_path(self,name="MODEL_PATH",type="VARCHAR(4096) not null"):
        self.model_path=name
        self.add_coll(name,type)

    def set_mojo_path(self,name="MOJO_PATH",type="VARCHAR(4096) not null"):
        self.mojo_path=name
        self.add_coll(name,type)

    def get_insert_query(self,modelconf_id,dpid,r2,mse,model_path,mojo_path):
        query=f"INSERT INTO {self.tablename} ({self.modelconf_id}, {self.dpid}, {self.r2}, {self.mse}, {self.model_path}, {self.mojo_path}) VALUES ('{modelconf_id}','{dpid}','{r2}','{mse}','{model_path}','{mojo_path}')"
        return query
    
    def get_update_model_query(self, model_id, modelconf_id, dpid, r2, mse, model_path, mojo_path):
        query = f"UPDATE {self.tablename} SET {self.modelconf_id} = '{modelconf_id}', {self.dpid} = '{dpid}', {self.r2} = '{r2}', {self.mse} = '{mse}', {self.model_path} = '{model_path}', {self.mojo_path} = '{mojo_path}' WHERE {self.model_id} = '{model_id}'"
        return query
    
    def get_model_query(self,modelconf_id,dpid):
        query=f"select * from {self.tablename} where {self.modelconf_id} = '{modelconf_id}' and {self.dpid} = '{dpid}'"
        return query

class MLModelsConf(dbTable):
    def __init__(self, tablename='MLModelsConf'):
        super().__init__(tablename)
        self.add_coll("modelconf_id","bigint auto_increment primary key")
        self.modelconf_id = 'modelconf_id'
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.last_update = "LAST_UPDATE"
        self.set_name()
        self.set_mlclass()
        self.set_input_cols()
        self.set_output_cols()
        self.set_train_from()
        self.set_train_to()
        self.set_test_from()
        self.set_test_to()
    
    def set_name(self,name="NAME",type="VARCHAR(4096) not null"):
        self.name=name
        self.add_coll(name,type)
        
    def set_mlclass(self,name="mlclass",type="VARCHAR(4096) not null"):
        self.mlclass=name
        self.add_coll(name,type)
        
    def set_input_cols(self,name="INPUT_COLS",type="VARCHAR(4096) not null"):
        self.input_cols=name
        self.add_coll(name,type)
    
    def set_output_cols(self,name="OUTPUT_COLS",type="VARCHAR(4096) not null"):
        self.output_cols=name
        self.add_coll(name,type)
    
    def set_train_from(self,name="train_from",type="timestamp not null"):
        self.train_from=name
        self.add_coll(name,type)

    def set_train_to(self,name="train_to",type="timestamp not null"):
        self.train_to=name
        self.add_coll(name,type)
    
    def set_test_from(self,name="test_from",type="timestamp not null"):
        self.test_from=name
        self.add_coll(name,type)

    def set_test_to(self,name="test_to",type="timestamp not null"):
        self.test_to=name
        self.add_coll(name,type)

    def get_insert_query(self,name, mlclass,input_cols,output_cols,train_from,train_to,test_from,test_to):
        query = f"INSERT INTO {self.tablename} ({self.name}, {self.mlclass}, {self.input_cols}, {self.output_cols}, {self.train_from}, {self.train_to}, {self.test_from}, {self.test_to}) VALUES ('{name}', '{mlclass}', '{input_cols}', '{output_cols}', '{train_from}', '{train_to}', '{test_from}', '{test_to}')"
        return query
    
    def update_by_name_query(self,name, mlclass,input_cols,output_cols,train_from,train_to,test_from,test_to):
        query = f"UPDATE {self.tablename} SET {self.mlclass} = '{mlclass}', {self.input_cols} = '{input_cols}', {self.output_cols} = '{output_cols}', {self.train_from} = '{train_from}', {self.train_to} = '{train_to}', {self.test_from} = '{test_from}', {self.test_to} = '{test_to}' WHERE {self.name} = '{name}'"
        return query
    
    def update_by_modelconf_id_query(self,modelconf_id,name, mlclass,input_cols,output_cols,train_from,train_to,test_from,test_to):
        query = f"UPDATE {self.tablename} SET {self.name} = '{name}', {self.mlclass} = '{mlclass}', {self.input_cols} = '{input_cols}', {self.output_cols} = '{output_cols}', {self.train_from} = '{train_from}', {self.train_to} = '{train_to}', {self.test_from} = '{test_from}', {self.test_to} = '{test_to}' WHERE {self.modelconf_id} = '{modelconf_id}'"
        return query
    
    def get_select_query_by_model_name(self,name):
        query=f"select * from {self.tablename} where {self.name} = '{name}'"
        return query

    def get_select_query_by_modelconf_id(self,modelconf_id):
        query=f"select * from {self.tablename} where {self.modelconf_id} = '{modelconf_id}'"
        return query

class PredictedCurrentsTable(dbTable):
    def __init__(self, tablename='PredictedCurrent'):
        super().__init__(tablename)
        self.add_coll("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_dpid()
        self.set_model_id()
        self.set_predicted_for()
        self.set_predicted_value()
        self.set_predicted_value_error()
        self.set_measured_value()
    
    def set_dpid(self,name="dpid",type="int not null"):
        self.dpid=name
        self.add_coll(name,type)
    
    def set_predicted_for(self,name="predicted_for",type="timestamp not null"):
        self.predicted_for=name
        self.add_coll(name,type)
    
    def set_model_id(self,name="model_id",type="int not null"):
        self.model_id=name
        self.add_coll(name,type)
    
    def set_predicted_value(self,name="predicted_value",type="float not null"):
        self.predicted_value=name
        self.add_coll(name,type)
        
    def set_predicted_value_error(self,name="predicted_value_error",type="float not null"):
        self.predicted_value_error=name
        self.add_coll(name,type)
        
    def set_measured_value(self,name="measured_value",type="float"):
        self.measured_value=name
        self.add_coll(name,type)
    
    def get_insert_query(self, model_id, dpid, predicted_for, predicted_value, predicted_value_error, measured_value):
        query = f"INSERT INTO {self.tablename} ({self.model_id}, {self.dpid}, {self.predicted_for}, {self.predicted_value}, {self.predicted_value_error}, {self.measured_value}) VALUES ('{model_id}', '{dpid}', '{predicted_for}', '{predicted_value}', '{predicted_value_error}', '{measured_value}')"
        return query
    
    def get_select_by_dpid_model_id_dpid_timewindow_query(self, dpid, model_id, begw, endw):
        query = f"select * from {self.tablename} where {self.model_id} = '{model_id}' and {self.dpid} = '{dpid}' and {self.predicted_for} between '{begw}' and '{endw}' order by {self.predicted_for} asc"
        return query
    

if __name__ == "__main__":
    print("creating...")
    model_table_conf = MLModelsConf()
    print(model_table_conf.get_col_names(),'\n',
    model_table_conf.get_select_query_by_modelconf_id(5),'\n',
    model_table_conf.get_select_query_by_model_name("ha taka"))
    
    #CREATE TABLE UXC_ENV ( rec_id bigint auto_increment primary key, LAST_UPDATE timestamp not null, CHANGE_DATE timestamp not null, NEXT_CHANGE_DATE timestamp not null, uxcPressure float default null, uxcTemperature float default null, uxcRH float default null);
    pred_vals_table = PredictedCurrentsTable()
    q = pred_vals_table.get_myqsl_create_query()
    print(q)
