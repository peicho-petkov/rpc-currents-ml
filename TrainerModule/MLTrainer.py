import h2o
from . import MLModelInput
from . import MLModelManager

from tf.autoencoder_rpc import AE_DataManager,RPCAutoencoder
from db_tools import table_autoencoderData

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
        
        
    def train_and_refine_model_for_dpid(self,dpid, in_dataset,scale_sd=5.):
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
        
        # themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
        # themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)
        
        print(glm._model_json['output']['coefficients_table'])
        themodel.mse = glm.mse()
        themodel.r2 = glm.r2()
        
        pred_frame = glm.predict(trainig_dataset)
        
        trainig_dataset['predict'] = pred_frame['predict']
        
        ###### refine training dataframe ######
        
        trainig_dataset['diff'] = trainig_dataset['predict'] - trainig_dataset[outcol]
        trainig_dataset['abs_diff'] = trainig_dataset['diff'].abs()
        trainig_dataset['sd'] = trainig_dataset['diff'].sd()[0]
        
        mask = trainig_dataset['abs_diff'] < scale_sd*trainig_dataset['sd']
        print(trainig_dataset)
        new_trainig_dataset = trainig_dataset[mask,:]
        print(new_trainig_dataset)
        glm.train(incols, outcol, training_frame=new_trainig_dataset)
        
        print(glm._model_json['output']['coefficients_table'])
        themodel.mse = glm.mse()
        themodel.r2 = glm.r2()

        themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
        themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)
        
        h2o.remove(glm)                                                             
        h2o.remove(trainig_dataset) 
        h2o.remove(new_trainig_dataset) 
        return themodel
    
    def train_autoencoder(self):
        themodel = MLModelManager.MLModel()
        themodel.dpid = -1
        themodel.modelconf_id = self.model_conf.modelconf_id
        
        model_name = f'{self.model_conf.modelconf_id}_{themodel.dpid}'
        themodel.model_path = self.model_files_path+'/'+model_name
        themodel.mojo_path = ''
        
        n_inputs = len(self.model_conf.input_cols.split(','))
        print(self.model_conf.input_cols)
        print(n_inputs)
        rpc_ae = RPCAutoencoder(n_inputs=n_inputs)

        if self.model_conf.mlclass == 'AUTOENC_V1':
            rpc_ae.set_layers_one_and_five_size(512)
            rpc_ae.set_layers_two_and_four_size(128)
            rpc_ae.set_central_layer_size(64)
        if self.model_conf.mlclass == 'AUTOENC_V2':
            rpc_ae.set_layers_one_and_five_size(768)
            rpc_ae.set_layers_two_and_four_size(256)
            rpc_ae.set_central_layer_size(64)

        rpc_ae.create_network()

        ae_dm = AE_DataManager()
        
        ae_dm.set_time_window(self.model_conf.train_from,self.model_conf.train_to)
        
        for dataset,datedataset in ae_dm.get_dataframe():
            rpc_ae.train(dataset,dataset)
        
        rpc_ae.autoencoder.save(themodel.model_path)

        themodel.mse = 0
        themodel.r2 = 0

        return themodel    
        
