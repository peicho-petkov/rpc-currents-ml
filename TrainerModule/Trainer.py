import TrainerModule.MLModelManager as MLModelManager
import TrainerModule.MLModelInput as MLModelInput
import h2o

class Trainer:
    def __init__(self, model_conf, model_files_path, mojo_files_path):
        self.model_conf = model_conf
        self.model_files_path = model_files_path
        self.mojo_files_path = mojo_files_path
        
    def train_model_for_dpid(self,dpid, in_dataset):
        themodel = MLModelManager.MLModel()
        themodel.dpid = dpid
        themodel.modelconf_id = self.model_conf.model_conf_id

        model_name = f'{self.model_conf.modelconf_id}_{dpid}'

        mlinput = MLModelInput.ModelInput(self.model_conf)
        
        incols,outcol,trainig_dataset = mlinput.get_input_for_dataset(in_dataset)
        
        glm = h2o.estimators.H2OGeneralizedLinearEstimator(family="gaussian",       
                                                       lambda_=0,               
                                                       compute_p_values=True,   
                                                       model_id=model_name)

        glm.train(incols, outcol, training_frame=trainig_dataset)
        
        themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
        themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)
        
        h2o.remove(glm)                                                             
        h2o.remove(mlinput) 
        
        
