from db_tools import db_tables
from db_tools import rpccurrml

class MLModelConf:
    def __init__(self):
        self.modelconf_id = -1
        self.name = ''
        self.mlclass = ''
        self.input_cols = ''
        self.output_cols = ''
        self.train_from = ''
        self.train_to = ''
        self.test_from = ''
        self.test_to = ''
    def print(self):
        print("modelconf_id =",self.modelconf_id)
        print("name =",self.name)
        print("mlclass =",self.mlclass)
        
class MLModelsConfManager:
    def __init__(self,connector,mlmodelsconftab):
        self._connector = connector
        self._mlmodelsconftab = mlmodelsconftab
        self._connector.self_cursor_mode()
    
    def RegisterMLModelConf(self, ml_model_descr):
        #check it a model with the same name exists
        query = self._mlmodelsconftab.get_select_query_by_model_name(ml_model_descr.name)
        res = self._connector.fetchall_for_query_self(query)
        print(query)
        if len(res) > 0:
            return -1
        
        query = self._mlmodelsconftab.get_insert_query(ml_model_descr.name, ml_model_descr.mlclass,ml_model_descr.input_cols,ml_model_descr.output_cols,ml_model_descr.train_from,ml_model_descr.train_to,ml_model_descr.test_from,ml_model_descr.test_to)
        print(query)
        self._connector.execute_commit_query_self(query)

        query = self._mlmodelsconftab.get_select_query_by_model_name(ml_model_descr.name)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) != 1:
            return -2
        
        col_names = self._mlmodelsconftab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        return res_dict[self._mlmodelsconftab.modelconf_id]
    
    def UpdateRegisteredMLModelConf(self, ml_model_descr):
        query = self._mlmodelsconftab.get_select_query_by_model_name(ml_model_descr.name)
        print(query)
        res = self._connector.fetchall_for_query_self(query)
        print(res)
        if len(res) != 1:
            return -2
        
        query = self._mlmodelsconftab.update_by_modelconf_id_query(ml_model_descr.modelconf_id,ml_model_descr.name, ml_model_descr.mlclass,ml_model_descr.input_cols,ml_model_descr.output_cols,ml_model_descr.train_from,ml_model_descr.train_to,ml_model_descr.test_from,ml_model_descr.test_to)
        self._connector.execute_commit_query_self(query)
        return 0
        
    def get_by_modelconf_id(self,modelconf_id):
        query = self._mlmodelsconftab.get_select_query_by_modelconf_id(modelconf_id)
        res = self._connector.fetchall_for_query_self(query)
        print(query)
        if len(res) != 1:
            return None
        
        col_names = self._mlmodelsconftab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        
        ml_model = MLModelConf()
        ml_model.name = res_dict[self._mlmodelsconftab.name]
        ml_model.modelconf_id = res_dict[self._mlmodelsconftab.modelconf_id]
        ml_model.mlclass = res_dict[self._mlmodelsconftab.mlclass]
        ml_model.input_cols = res_dict[self._mlmodelsconftab.input_cols]
        ml_model.output_cols = res_dict[self._mlmodelsconftab.output_cols]
        ml_model.train_from = res_dict[self._mlmodelsconftab.train_from]
        ml_model.train_to = res_dict[self._mlmodelsconftab.train_to]
        ml_model.test_from = res_dict[self._mlmodelsconftab.test_from]
        ml_model.test_to = res_dict[self._mlmodelsconftab.test_to]
        
        return ml_model

    def get_by_name(self,name):
        query = self._mlmodelsconftab.get_select_query_by_model_name(name)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) != 1:
            return None
        
        col_names = self._mlmodelsconftab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        
        ml_model = MLModelConf()
        ml_model.name = res_dict[self._mlmodelsconftab.name]
        ml_model.modelconf_id = res_dict[self._mlmodelsconftab.modelconf_id]
        ml_model.mlclass = res_dict[self._mlmodelsconftab.mlclass]
        ml_model.input_cols = res_dict[self._mlmodelsconftab.input_cols]
        ml_model.output_cols = res_dict[self._mlmodelsconftab.output_cols]
        ml_model.train_from = res_dict[self._mlmodelsconftab.train_from]
        ml_model.train_to = res_dict[self._mlmodelsconftab.train_to]
        ml_model.test_from = res_dict[self._mlmodelsconftab.test_from]
        ml_model.test_to = res_dict[self._mlmodelsconftab.test_to]
        
        return ml_model


class MLModel:
    def __init__(self):
        self.model_id = -1
        self.modelconf_id= -1
        self.dpid = -1
        self.r2 = -1
        self.mse = -1
        self.model_path = ''
        self.mojo_path = ''

class MLModelsManager:
    def __init__(self,connector,mlmodelstab):
        self._connector = connector
        self._mlmodelstab = mlmodelstab
        self._connector.self_cursor_mode()
    
    def RegisterMLModel(self, ml_model):
        #check it a model with the same name exists
        query = self._mlmodelstab.get_model_query(ml_model.modelconf_id,ml_model.dpid)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) > 0:
            return -1
        
        query = self._mlmodelstab.get_insert_query(ml_model.modelconf_id,ml_model.dpid,ml_model.r2,ml_model.mse,ml_model.model_path,ml_model.mojo_path)
        self._connector.execute_commit_query_self(query)

        query = self._mlmodelstab.get_model_query(ml_model.modelconf_id,ml_model.dpid)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) != 1:
            return -2
        
        col_names = self._mlmodelstab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        return res_dict[self._mlmodelstab.model_id]
    
    def UpdateRegistedMLModel(self, ml_model):
        #check it a model with the same name exists
        query = self._mlmodelstab.get_model_query(ml_model.modelconf_id,ml_model.dpid)
        res = self._connector.fetchall_for_query_self(query)
        if len(res) != 1:
            return -2

        col_names = self._mlmodelstab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        
        if ml_model.model_id < 0:
            ml_model.model_id = res_dict[self._mlmodelstab.model_id]
        
        query = self._mlmodelstab.get_update_model_query(ml_model.model_id, ml_model.modelconf_id, ml_model.dpid, ml_model.r2, ml_model.mse, ml_model.model_path, ml_model.mojo_path)
        print(query)
        self._connector.execute_commit_query_self(query)
        return 0
        
    def get_by_modelconf_id_dpid(self,modelconf_id,dpid):
        query = self._mlmodelstab.get_model_query(modelconf_id,dpid)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) != 1:
            return None
        
        col_names = self._mlmodelstab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        
        ml_model = MLModel()
        ml_model.model_id = res_dict[self._mlmodelstab.model_id]
        ml_model.modelconf_id= res_dict[self._mlmodelstab.modelconf_id]
        ml_model.dpid = res_dict[self._mlmodelstab.dpid]
        ml_model.r2 = res_dict[self._mlmodelstab.r2]
        ml_model.mse = res_dict[self._mlmodelstab.mse]
        ml_model.model_path = res_dict[self._mlmodelstab.model_path]
        ml_model.mojo_path = res_dict[self._mlmodelstab.mojo_path]
        
        return ml_model
    
    def get_by_modelconf_name_and_dpid(self,mlmodelsconftab,modelconf_name,dpid):
        
        mlconf_manager = MLModelsConfManager(self._connector,mlmodelsconftab)
        mlconf = mlconf_manager.get_by_name(modelconf_name)
        modelconf_id=mlconf.modelconf_id
        
        query = self._mlmodelstab.get_model_query(modelconf_id,dpid)
        res = self._connector.fetchall_for_query_self(query)
        
        if len(res) != 1:
            return None
        
        col_names = self._mlmodelstab.get_col_names()
        col_values = res[0]
        
        res_dict = dict(zip(col_names,col_values))
        
        ml_model = MLModel()
        ml_model.model_id = res_dict[self._mlmodelstab.model_id]
        ml_model.modelconf_id= res_dict[self._mlmodelstab.modelconf_id]
        ml_model.dpid = res_dict[self._mlmodelstab.dpid]
        ml_model.r2 = res_dict[self._mlmodelstab.r2]
        ml_model.mse = res_dict[self._mlmodelstab.mse]
        ml_model.model_path = res_dict[self._mlmodelstab.model_path]
        ml_model.mojo_path = res_dict[self._mlmodelstab.mojo_path]
        
        return ml_model
        
    def set_mlmodels_active_state(self, mlmodelsconftab, modelconf_name, enable=1):
        # confmanager = MLModelsConfManager(self._connector, mlmodelsconftab)
        # modelconf = confmanager.get_by_name(modelconf_name)
        # modelconf_id = modelconf.modelconf_id
        # The three commented lines above are redundant to the next two lines
        
        query = mlmodelsconftab.get_select_modelconfid_by_modelconfname_query(modelconf_name)
        modelconf_id = self._connector.fetchall_for_query_self(query)[0]

        thequery = self._mlmodelstab.get_get_model_ids_by_conf_id_query(modelconf_id)
        model_ids = list()
        model_ids = self._connector.fetchall_for_query_self(thequery)
        if len(model_ids) < 1:
            print("[-][-] No models found for that model configuration name!! [-][-]")
            exit(0)

        for model_id in model_ids:
            myquery = self._mlmodelstab.get_set_active_for_id(model_id, enable)
            self._connector.execute_commit_query_self(myquery)
        
        # return modelconf, model_ids 
    

