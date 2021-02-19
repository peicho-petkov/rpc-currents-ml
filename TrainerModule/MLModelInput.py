import TrainerModule.MLModelManager as MLModelManager
import h2o
import db_tools.db_tables as db_tables

class ModelInput:
    def __init__(self,model_conf = None):
        self.supported_modelclasses = ['GLM_V1','GLM_V2']
        if model_conf is not None:
            self.set_model_conf(model_conf)
            
    def set_model_conf(self,model_conf):
        if not model_conf.mlclass in self.supported_modelclasses:
            raise Exception(f"Sorry, Not Suppored MODEL CLASS ({model_conf.mlclass})")
        self.model_conf = model_conf
        
    def get_input_for_dataset(self,dataset):
        if self.model_conf.mlclass == 'GLM_V1':
            return self.glm_v1(dataset)        
        elif self.model_conf.mlclass == 'GLM_V2':
            return self.glm_v2(dataset)
            
    def glm_v1(self,dataset):
        incols = []
        outcols = []
        input_ds = dataset
        
        return incols,outcols,input_ds
        
    def glm_v2(self,dataset):

        incols = self.model_conf.input_cols.split(',')
        outcols = self.model_conf.output_cols.split(',')[0]
        
        trng_tbl = db_tables.TrainingDataTable()
        
        input_ds = h2o.H2OFrame.from_python(dataset,column_names=incols)
        
        input_ds['WHV'] = input_ds[trng_tbl.vmon]/input_ds[trng_tbl.uxcP]                                    
        input_ds['LexpWHV'] = input_ds[trng_tbl.instant_lumi]*input_ds['WHV'].exp()                              
        input_ds[trng_tbl.uxcRH] = input_ds[trng_tbl.uxcRH]*1000
        input_ds[trng_tbl.uxcT] = input_ds[trng_tbl.uxcT]*1000    
        
        incols.append('LexpWHV')                                                         
        
        return incols,outcols,input_ds