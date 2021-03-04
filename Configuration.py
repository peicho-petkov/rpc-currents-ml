from db_tools import table_configuration

class Configuration:
    def __init__(self,db_conn):
        self.db_conn = db_conn 
        
    def AddParameter(self,par_name,par_val,par_val_type):
        query = table_configuration.get_add_parameter_query(par_name,par_val,par_val_type)
        self.db_conn.execute_commit_query_self(query)
    
    def SetParameter(self,par_name,par_val):
        query = table_configuration.get_set_parameter_query(par_name,par_val)
        self.db_conn.execute_commit_query_self(query)
    
    def GetParameter(self,par_name):
        query = table_configuration.get_get_parameter_query(par_name)
        data = self.db_conn.fetchall_query_self(query)
        value = str(data[0][0])
        par_type = str(data[0][1])
        
        if par_type.lower() == 'float':
            value = float(value)
            
        if par_type.lower() == 'int':
            value = int(value)
        
        if 'list' in par_type.lower():
            value_tmp = value.split(',')
            value = []
            if 'int' in par_type.lower():
                for v in value_tmp:
                    value.append(int(v))
            elif 'float' in par_type.lower():
                for v in value_tmp:
                    value.append(float(v))
            else:
                for v in value_tmp:
                    value.append(str(v))
        return value
        
