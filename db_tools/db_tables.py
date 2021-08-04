
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
        colnames=[]
        for colname, coltype in self.colls.items():
            if "not null" in str(coltype).to_lower():
                colnames.append(colname)
        return colnames
    
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

    def get_get_number_of_rows_for_dpid_in_period_query(self, dpid, start_date, end_date):
        query = f"select count(*) from {self.tablename} where {self.dpid}='{dpid}' and {self.change_date} between '{start_date}' and '{end_date}'"
        return query

    def get_get_all_dpids_query(self):
        query = f"select distinct {self.dpid} from {self.tablename}"
        return query

    def get_latest_HoursWithoutLumi_query(self,dpid):
        query = f"SELECT {self.hours_without_lumi} from {self.tablename} where {self.dpid} = {dpid} order by {self.change_date} desc limit 1"
        return query

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
        self.set_active()

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

    def set_active(self,name="ACTIVE",type="tinyint(1) default 0"):
        self.active=name
        self.add_coll(name,type)

    def get_insert_query(self,modelconf_id,dpid,r2,mse,model_path,mojo_path, active_val=0):
        query = f"INSERT INTO {self.tablename} ({self.modelconf_id}, {self.dpid}, {self.r2}, {self.mse}, {self.model_path}, {self.mojo_path}, {self.active}) VALUES ('{modelconf_id}','{dpid}','{r2}','{mse}','{model_path}','{mojo_path}','{active_val}')"
        return query
    
    def get_update_model_query(self, model_id, modelconf_id, dpid, r2, mse, model_path, mojo_path):
        query = f"UPDATE {self.tablename} SET {self.modelconf_id} = '{modelconf_id}', {self.dpid} = '{dpid}', {self.r2} = '{r2}', {self.mse} = '{mse}', {self.model_path} = '{model_path}', {self.mojo_path} = '{mojo_path}' WHERE {self.model_id} = '{model_id}'"
        return query
    
    def get_model_query(self,modelconf_id,dpid):
        query = f"select * from {self.tablename} where {self.modelconf_id} = '{modelconf_id}' and {self.dpid} = '{dpid}'"
        return query

    def get_set_active(self, active):
        query = f"UPDATE {self.tablename} SET {self.active} = '{active}' "
        return query

    def get_set_active_query(self,active_val, modelconf_id,dpid):
        query = f"UPDATE {self.tablename} SET {self.active} = '{active_val}' WHERE {self.modelconf_id} = '{modelconf_id}' and {self.dpid} = '{dpid}'"
        return query
    
    def get_set_active_for_id(self, model_id, active):
        query = f"UPDATE {self.tablename} SET {self.active} = '{active}' WHERE {self.model_id} = '{model_id}'"
        return query

    def get_get_model_ids_by_conf_id_query(self, modelconf_id):
        query = f"select {self.model_id} from {self.tablename} where {self.modelconf_id}='{modelconf_id}'"
        return query

    def get_get_dpid_by_model_id_query(self, model_id):
        query = f"select {self.dpid} from {self.tablename} where {self.model_id} = '{model_id}'"
        return query 

    def get_get_active_model_ids_query(self):
        query = f"select {self.model_id} from {self.tablename} where {self.active}=1"
        return query 

    def get_get_active_model_ids_and_dpids_query(self):
        query = f"select {self.model_id}, {self.dpid} from {self.tablename} where {self.active}=1"
        return query 

    def get_get_confid_dpid_for_mid_query(self, model_id):
        query = f"select {self.modelconf_id}, {self.dpid} from {self.tablename} where {self.model_id} = '{model_id}'"
        return query

    def get_get_active_modelconf_id_query(self):
        query = f"select distinct {self.modelconf_id} from {self.tablename} where {self.active}=1"
        return query

    def get_count_for_conf_id_dpid_query(self, modelconf_id, dpid):
        query = f"select count(*) from {self.tablename} where {self.modelconf_id} = '{modelconf_id}' and {self.dpid} = '{dpid}'"
        return query 

    def get_get_dpids_by_modelconf_id_query(self, modelconf_id):
        query = f"select {self.dpid} from {self.tablename} where {self.modelconf_id} = '{modelconf_id}'"
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

    def get_select_modelconfid_by_modelconfname_query(self, modelconf_name):
        query=f"select {self.modelconf_id} from {self.tablename} where {self.name}='{modelconf_name}'"
        return query

    def get_select_modelconfname_by_modelconfid_query(self, modelconf_id):
        query=f"select {self.name} from {self.tablename} where {self.modelconf_id}='{modelconf_id}'"
        return query

    def get_select_modelconfnames_query(self):
        query=f"select {self.name} from {self.tablename} order by {self.last_update} desc"
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

    def get_get_average_difference_query(self, dpid, model_id):
        query = f"SELECT AVG({self.measured_value} - {self.predicted_value}) from {self.tablename} where {self.dpid}='{dpid}' and {self.model_id}='{model_id}' " 
        return query
    
class ConfigurationTable(dbTable):
    def __init__(self, tablename='Configuration'):
        super().__init__(tablename)
        self.add_coll("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_parameter_name_cols()
        self.set_parameter_value_cols()
        self.set_parameter_value_type_cols()
        self.set_parameter_unit_cols()

    def set_parameter_name_cols(self,name="PARAMETER_NAME",type="VARCHAR(4096) not null"):
        self.parameter_name=name
        self.add_coll(name,type)
        
    def set_parameter_value_cols(self,name="PARAMETER_VALUE",type="VARCHAR(4096) not null"):
        self.parameter_value=name
        self.add_coll(name,type)
    
    def set_parameter_value_type_cols(self,name="PARAMETER_TYPE",type="VARCHAR(4096) not null"):
        self.parameter_value_type=name
        self.add_coll(name,type)

    def set_parameter_unit_cols(self, name="PARAMETER_UNIT", type="VARCHAR(4096) not null"):
        self.parameter_unit=name
        self.add_coll(name, type)
    
    def get_add_parameter_query(self,parameter_name,parameter_value,parameter_type='string'):
        query=f"INSERT INTO {self.tablename} ({self.parameter_name}, {self.parameter_value}, {self.parameter_value_type}) VALUES ('{parameter_name}', '{parameter_value}', '{parameter_type}')"
        return query
    
    def get_set_parameter_value_query(self,parameter_name,parameter_value):
        query=f"UPDATE {self.tablename} SET {self.parameter_value} = '{parameter_value}' WHERE {self.parameter_name}='{parameter_name}'"
        return query

    def get_set_parameter_unit_query(self, parameter_name, parameter_unit):
        query = f"UPDATE {self.tablename} SET {self.parameter_unit} = '{parameter_unit}' WHERE {self.parameter_name} = '{parameter_name}'"
        return query 
    
    def get_get_parameter_value_query(self,parameter_name):
        query=f"SELECT {self.parameter_value},{self.parameter_value_type} from {self.tablename} WHERE {self.parameter_name}='{parameter_name}'"
        return query
    
class NotificationsTable(dbTable):
    ''' Stores warnings and errors. 
        columns: rec_id, last_update, dpid, model_id, notification type (warning/error),
        flag_raised_time, av_discrepancy, sent, acknowleged, masked '''

    def __init__(self, tablename="Notifications"):
        super().__init__(tablename)
        self.add_coll("rec_id","bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE","timestamp not null")
        self.set_dpid_col()
        self.set_model_id_col()
        self.set_notification_type_col()
        self.set_flag_raised_time_col()
        self.set_avg_discrepancy_col()
        self.set_sent_col()
        self.set_acknowledged_col()
        self.set_masked_col()

    def set_dpid_col(self,name="DPID",type="int not null"):
        self.dpid=name
        self.add_coll(name,type)

    def set_model_id_col(self,name="model_id",type="int not null"):
        self.model_id=name
        self.add_coll(name,type)

    def set_notification_type_col(self,name="notification_type", type="VARCHAR(4096) not null"):
        self.notification_type=name
        self.add_coll(name,type)

    def set_flag_raised_time_col(self,name="flag_raised_time",type="datetime not null"):
        self.flag_raised_time=name
        self.add_coll(name,type)

    def set_avg_discrepancy_col(self,name="avg_discrepancy",type="float not null"):
        self.avg_discrepancy=name
        self.add_coll(name,type)

    def set_sent_col(self,name="Sent",type="tinyint(1) not null"):
        self.sent=name
        self.add_coll(name,type)

    def set_acknowledged_col(self,name="Acknowledged",type="tinyint(1) not null"):
        self.acknowledged=name
        self.add_coll(name,type)

    def set_masked_col(self,name="Masked",type="tinyint(1) not null"):
        self.masked=name
        self.add_coll(name,type)

    def get_insert_notification_query(self,dpid,model_id,notification_type,flag_raised_time,avg_discrepancy,sent,acknowledged,masked):
        query=f"INSERT INTO {self.tablename} ({self.dpid},{self.model_id},{self.notification_type},{self.flag_raised_time},{self.avg_discrepancy},{self.sent},{self.acknowledged},{self.masked}) VALUES ('{dpid}','{model_id}','{notification_type}','{flag_raised_time}','{avg_discrepancy}','{sent}','{acknowledged}','{masked}')"
        return query

    def get_update_sent_col_query(self,sent,dpid,model_id):
        query=f"UPDATE {self.tablename} SET {self.sent}='{sent}' WHERE {self.dpid}='{dpid}' AND {self.model_id}='{model_id}'"
        return query

    def get_update_acknowledged_col_query(self,acknowledged,dpid,model_id):
        query=f"UPDATE {self.tablename} SET {self.acknowledged}='{acknowledged}' WHERE {self.dpid}='{dpid}' AND {self.model_id}='{model_id}'"
        return query

    def get_update_masked_col_query(self,masked,dpid,model_id):
        query=f"UPDATE {self.tablename} SET {self.masked}='{masked}' WHERE {self.dpid}='{dpid}' AND {self.model_id}='{model_id}'"
        return query

class dpidStateTable(dbTable):
    '''  A table where in each entry, a dpid (and the corresponding chamber/s) 
         is associated with a modelconf_name and a flag called state (1/0), 
         which shows whether training for this combination is a "go" or not '''

    def __init__(self, tablename = "dpidStatesTable"):
        super().__init__(tablename)
        self.add_coll("rec_id", "bigint auto_increment primary key")
        self.add_coll("LAST_UPDATE", "timestamp not null")
        self.set_dpid_col()
        self.set_chambers_col()
        self.set_modelconf_name_col()
        self.set_state_col()
        
    def set_dpid_col(self, name="DPID", type="int not null"):
        self.dpid = name
        self.add_coll(name, type)

    def set_modelconf_name_col(self, name="modelconf_name", type="VARCHAR(4096) not null"):
        self.modelconf_name = name
        self.add_coll(name, type)

    def set_state_col(self, name="state", type="tinyint(1) not null"):
        self.state = name
        self.add_coll(name, type)

    def set_chambers_col(self, name="chambers", type="VARCHAR(4096)"):
        self.chambers = name
        self.add_coll(name, type)

    def get_insert_entry_query(self, dpid, chambers, conf_name, state):
        query = f"INSERT INTO {self.tablename} ({self.dpid}, {self.chambers},{self.modelconf_name}, {self.state}) VALUES ('{dpid}', '{chambers}','{conf_name}', '{state}')"
        return query

    def get_get_state_for_dpid_and_conf_query(self, dpid, conf_name):
        query = f"SELECT {self.state} FROM {self.tablename} WHERE {self.dpid} = '{dpid}' AND {self.modelconf_name} = '{conf_name}'"
        return query

    def get_set_active_state_query(self, dpid, conf_name, state):
        query = f"UPDATE {self.tablename} SET {self.state} = '{state}' WHERE {self.dpid} = '{dpid}' AND {self.modelconf_name} = '{conf_name}'"
        return query 

    def get_get_all_dpids_query(self):
        query = f"select distinct {self.dpid} from {self.tablename}"
        return query 


class autoencoderData(dbTable):
    ''' A table that contains a timestamp as a first column and all dpids in separate columns,
        the values are the corresponding currents expressed in uA '''

    def __init__(self, dpids, tablename = "autoencoderData"):
        super().__init__(tablename)
        self.add_coll("timestamp", "timestamp not null")
        self.add_all_colls(dpids)

    def add_all_colls(self, dpids):
        for dpid in dpids:    
            self.add_coll(f"dpid{dpid}", "float") 

    

    

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


    conftable = ConfigurationTable()
    print(conftable.get_myqsl_create_query())
    print(conftable.get_add_parameter_query("Pers_time","5","float"))
    print(conftable.get_set_parameter_value_query("Pers_time","10.0"))
    
    print("\n++++ Creating Notifications Table ++++\n")
    notificationtable = NotificationsTable()
    print("The table is called: ",notificationtable.tablename)
    print(notificationtable.get_myqsl_create_query())
    print(notificationtable.get_insert_notification_query(317,23,'warning','2018-03-02',4.5,1,0,0))

    print("\n++++ Creating dpidState Table ++++\n")
    table_dpidstate = dpidStateTable()
    print("The table is called: ", table_dpidstate.tablename)
    print(table_dpidstate.get_myqsl_create_query())
    print(table_dpidstate.get_insert_entry_query(315, "W+2_RB1_1in", "05-2016-07-2017-f56-v2", 1))
    print(table_dpidstate.get_get_state_for_dpid_and_conf_query(315, "05-2016-07-2017-f56-v2"))

    print("\n++++ Creating autoencoderData Table ++++\n")
    dpids = ["315", "316", "354", "380"]
    table_autoencoder = autoencoderData(dpids=dpids)
    print("The table  is called: ", table_autoencoder.tablename)
    print("The create table query is: ")
    print(table_autoencoder.get_myqsl_create_query())
    