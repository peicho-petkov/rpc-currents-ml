import h2o
from . import MLModelInput
from . import MLModelManager

class MLTrainer:
    def __init__(self, model_conf, model_files_path, mojo_files_path,extra_col_names=None):
        self.model_conf = model_conf
        self.model_files_path = model_files_path
        self.mojo_files_path = mojo_files_path
        self.extra_col_names = extra_col_names

    def train_model_for_dpid(self,dpid, in_dataset):
        themodel = MLModelManager.MLModel()
        themodel.dpid = dpid
        themodel.modelconf_id = self.model_conf.modelconf_id

        model_name = f'{self.model_conf.modelconf_id}_{dpid}'

        mlinput = MLModelInput.ModelInput(self.model_conf)
        
        incols,outcol,trainig_dataset = mlinput.get_input_for_dataset(dataset=in_dataset,extra_col_names=self.extra_col_names)

        glm = None
        
        if self.model_conf.mlclass == 'GLM_V3' or self.model_conf.mlclass == 'GLM_V4' or self.model_conf.mlclass == 'GLM_V6':
            n = len(incols[:])            
            # Create a beta_constraints frame
            constraints = h2o.H2OFrame({'names':incols[:],
                                        'lower_bounds': [0.]*n,
                                        'upper_bounds': [1e27]*n})
                                        # 'beta_given': [1]*n,
                                        # 'rho': [0.2]*n})
            if self.model_conf.mlclass == 'GLM_V6':
                mask=constraints['names']=='InstLumi'
                constraints[mask,'lower_bounds']=-1e27
            print(constraints)
            glm = h2o.estimators.H2OGeneralizedLinearEstimator(family="gaussian",       
                                                        compute_p_values=False,
                                                        lambda_=0,
                                                        model_id=model_name,
                                                               beta_constraints=constraints)
        else:
            glm = h2o.estimators.H2OGeneralizedLinearEstimator(family="gaussian",       
                                                        compute_p_values=True,
                                                        lambda_=0,
                                                               model_id=model_name)

        glm.train(incols, outcol, training_frame=trainig_dataset)
        
        themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
        themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)
        
        print(glm._model_json['output']['coefficients_table'])
        themodel.mse = glm.mse()
        themodel.r2 = glm.r2()

        
        h2o.remove(glm)                                                             
        h2o.remove(trainig_dataset) 
        
        return themodel

    def train_and_test_model_for_dpid(self,dpid, in_dataset, in_testset):
        themodel = MLModelManager.MLModel()
        themodel.dpid = dpid
        themodel.modelconf_id = self.model_conf.modelconf_id

        model_name = f'{self.model_conf.modelconf_id}_{dpid}'

        mlinput = MLModelInput.ModelInput(self.model_conf)
        
        incols,outcol,trainig_dataset = mlinput.get_input_for_dataset(dataset=in_dataset,extra_col_names=self.extra_col_names)
        test_incols,test_outcol,test_dataset = mlinput.get_input_for_dataset(dataset=in_testset,extra_col_names=self.extra_col_names)
        glm = None
        
        if self.model_conf.mlclass == 'GLM_V3' or self.model_conf.mlclass == 'GLM_V4' or self.model_conf.mlclass == 'GLM_V6':
            n = len(incols[:])            
            # Create a beta_constraints frame
            constraints = h2o.H2OFrame({'names':incols[:],
                                        'lower_bounds': [0.]*n,
                                        'upper_bounds': [1e27]*n})
                                        # 'beta_given': [1]*n,
                                        # 'rho': [0.2]*n})
            if self.model_conf.mlclass == 'GLM_V6':
                mask=constraints['names']=='InstLumi'
                constraints[mask,'lower_bounds']=-1e27
            print(constraints)
            glm = h2o.estimators.H2OGeneralizedLinearEstimator(family="gaussian",       
                                                        compute_p_values=False,
                                                        lambda_=0,
                                                        model_id=model_name,
                                                        beta_constraints=constraints)
        else:
            glm = h2o.estimators.H2OGeneralizedLinearEstimator(family="gaussian",       
                                                        compute_p_values=True,
                                                        lambda_=0,
                                                        model_id=model_name)

        glm.train(incols, outcol, training_frame=trainig_dataset,validation_frame=test_dataset)
        
        themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
        themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)
        
        print(glm._model_json['output']['coefficients_table'])
        themodel.mse = glm.mse()
        themodel.r2 = glm.r2()

        
        h2o.remove(glm)                                                             
        h2o.remove(trainig_dataset) 
        
        return themodel
        
        
