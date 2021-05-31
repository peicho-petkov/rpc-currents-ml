from . import MLModelManager
import h2o
from db_tools import table_training

class ModelInput:
    def __init__(self,model_conf = None):
        self.supported_modelclasses = ['GLM_V1','GLM_V2','GLM_V3','GLM_V4','GLM_V5']
        # GLM_V3 - fixed sign paramaters
        # GLM_V4 - fixed sign paramaters; HV term excluded
        # GLM_V5 - GLM_V2 + exp(hv/p)
        
        if model_conf is not None:
            self.set_model_conf(model_conf)
            
    def set_model_conf(self,model_conf):
        if not model_conf.mlclass in self.supported_modelclasses:
            raise Exception(f"Sorry, Not Suppored MODEL CLASS ({model_conf.mlclass})")
        self.model_conf = model_conf
        
    def get_input_for_dataset(self,dataset,extra_col_names=None):
        if self.model_conf.mlclass == 'GLM_V1':
            return self.glm_v1(dataset,extra_col_names)        
        elif self.model_conf.mlclass == 'GLM_V2':
            return self.glm_v2(dataset,extra_col_names)
        elif self.model_conf.mlclass == 'GLM_V3':
            return self.glm_v3(dataset,extra_col_names)
        elif self.model_conf.mlclass == 'GLM_V4':
            return self.glm_v4(dataset,extra_col_names)
        elif self.model_conf.mlclass == 'GLM_V5':
            return self.glm_v5(dataset,extra_col_names)
            
    def glm_v1(self,dataset,extra_col_names):
        incols = []
        outcols = []
        input_ds = dataset
        
        return incols,outcols,input_ds
        
    def glm_v2(self,dataset,extra_col_names):
        incols = self.model_conf.input_cols.split(',')
        outcols = self.model_conf.output_cols.split(',')
        colnames = incols+outcols
        if extra_col_names is not None:
            colnames = incols+outcols+extra_col_names
        outcols = outcols[0]
        print("intcols ",incols)
        print("outcols ",outcols)
        
        input_ds = h2o.H2OFrame.from_python(dataset,column_names=colnames)
        
        print(input_ds)
        
        input_ds['WHV'] = input_ds[table_training.vmon]/input_ds[table_training.uxcP]                                    
        input_ds['LexpWHV'] = input_ds[table_training.instant_lumi]*input_ds['WHV'].exp()                              
        input_ds[table_training.uxcRH] = input_ds[table_training.uxcRH]*1000
        input_ds[table_training.uxcT] = input_ds[table_training.uxcT]*1000    
        
        incols.append('LexpWHV')                                                         
        
        return incols,outcols,input_ds

    def glm_v3(self,dataset,extra_col_names):
        incols = self.model_conf.input_cols.split(',')
        outcols = self.model_conf.output_cols.split(',')
        colnames = incols+outcols
        if extra_col_names is not None:
            colnames = incols+outcols+extra_col_names
        outcols = outcols[0]
        print("intcols ",incols)
        print("outcols ",outcols)
        
        input_ds = h2o.H2OFrame.from_python(dataset,column_names=colnames)
        
        print(input_ds)
        
        input_ds['WHV'] = input_ds[table_training.vmon]/input_ds[table_training.uxcP]                                    
        input_ds['expWHV'] = input_ds['WHV'].exp()

        incols.append('expWHV')

        input_ds['LexpWHV'] = input_ds[table_training.instant_lumi]*input_ds['WHV'].exp()                              
        input_ds[table_training.uxcRH] = input_ds[table_training.uxcRH]*1000
        input_ds[table_training.uxcT] = input_ds[table_training.uxcT]*1000
    
        input_ds[table_training.hours_without_lumi] = input_ds[table_training.hours_without_lumi]*(-1.0)
        
        input_ds[table_training.integrated_lumi] = input_ds[table_training.integrated_lumi]
        
        input_ds[table_training.uxcP] = input_ds[table_training.uxcP]

        incols.append('LexpWHV')                                                         

        input_ds['1overP'] = 1.0/input_ds[table_training.uxcP]

        incols.append('1overP')                                                         

        input_ds['1overT'] = 1.0/input_ds[table_training.uxcT]

        incols.append('1overT') 

        input_ds['1overRH'] = 1.0/input_ds[table_training.uxcRH]

        incols.append('1overRH') 

        
        return incols,outcols,input_ds

    def glm_v4(self,dataset,extra_col_names):
        incols = self.model_conf.input_cols.split(',')
        outcols = self.model_conf.output_cols.split(',')
        colnames = incols+outcols

        if extra_col_names is not None:
            colnames = incols+outcols+extra_col_names
            print(colnames)

        outcols = outcols[0]
        print("intcols ",incols)
        print("outcols ",outcols)
        
        input_ds = h2o.H2OFrame.from_python(dataset,column_names=colnames)
        
        print(input_ds)
        
        input_ds['WHV'] = input_ds[table_training.vmon]/input_ds[table_training.uxcP]                                    
        input_ds['LexpWHV'] = input_ds[table_training.instant_lumi]*input_ds['WHV'].exp()                              
        input_ds[table_training.uxcRH] = input_ds[table_training.uxcRH]*1000
        input_ds[table_training.uxcT] = input_ds[table_training.uxcT]*1000    
        input_ds[table_training.hours_without_lumi] = input_ds[table_training.hours_without_lumi]*(-1.0)
        input_ds[table_training.integrated_lumi] = input_ds[table_training.integrated_lumi]
        input_ds[table_training.uxcP] = input_ds[table_training.uxcP]*(-1.0)

        incols.append('LexpWHV')                                                         
        
        return incols,outcols,input_ds

    def glm_v5(self,dataset,extra_col_names):
        incols = self.model_conf.input_cols.split(',')
        outcols = self.model_conf.output_cols.split(',')
        colnames = incols+outcols
        if extra_col_names is not None:
            colnames = incols+outcols+extra_col_names
        outcols = outcols[0]
        print("intcols ",incols)
        print("outcols ",outcols)
        
        input_ds = h2o.H2OFrame.from_python(dataset,column_names=colnames)
        
        print(input_ds)
        
        input_ds['WHV'] = input_ds[table_training.vmon]/input_ds[table_training.uxcP]                                    
        input_ds['expWHV'] = input_ds['WHV'].exp()

        incols.append('expWHV')

        input_ds['LexpWHV'] = input_ds[table_training.instant_lumi]*input_ds['expWHV']                              
        input_ds[table_training.uxcRH] = input_ds[table_training.uxcRH]*1000
        input_ds[table_training.uxcT] = input_ds[table_training.uxcT]*1000    
        
        incols.append('LexpWHV')                                                         
        
        return incols,outcols,input_ds
