import h2o
from . import MLModelInput
from . import MLModelManager
import numpy as np
import tensorflow
from tf.autoencoder_rpc import AE_DataManager,RPCAutoencoder
from db_tools import table_autoencoderData

class MLTrainer:
	def __init__(self, model_conf, model_files_path, mojo_files_path, extra_col_names=None):
		self.model_conf = model_conf
		self.model_files_path = model_files_path
		self.mojo_files_path = mojo_files_path
		self.extra_col_names = extra_col_names

	def train_model_for_chid(self, chid, in_dataset):
		themodel = MLModelManager.MLModel()
		themodel.chid = chid
		themodel.modelconf_id = self.model_conf.modelconf_id

		model_name = f'{self.model_conf.modelconf_id}_{chid}'

		mlinput = MLModelInput.ModelInput(self.model_conf)

		incols, outcol, training_dataset = mlinput.get_input_for_dataset(dataset=in_dataset,extra_col_names=self.extra_col_names)

		#glm_tf = None

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
					compute_p_values=False,
					lambda_=0,
					model_id=model_name)

			glm.train(incols, outcol, training_frame=training_dataset)

		# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		# Implement the ML model in tensorflow instead of h2o
		#x_train = training_dataset[:, 0:-1]
		#y_train = training_dataset[:, -1]
		#glm_tf = tensorflow.keras([
		#	tensorflow.keras.layers.Dense(1, activation='linear', input_shape=(8,))
		#	])
		#glm.compile(optimizer='adam', loss='mse')
		#glm_tf.fit(x_train, y_train, epochs=10)
		#glm_tf.summary
		#glm_tf.save(f"tf_glm_{model_name}")

		#themodel.mse = glm_tf.mse()
		#themodel.r2 = glm_tf.r2()
		#return themodel

		# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

		themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
		themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)

		print(glm._model_json['output']['coefficients_table'])
		themodel.mse = glm.mse()
		themodel.r2 = glm.r2()


		h2o.remove(glm)                                                             
		h2o.remove(training_dataset) 

		return themodel

	def train_and_test_model_for_chid(self,chid, in_dataset, in_testset):
		themodel = MLModelManager.MLModel()
		themodel.chid = chid
		themodel.modelconf_id = self.model_conf.modelconf_id

		model_name = f'{self.model_conf.modelconf_id}_{chid}'

		mlinput = MLModelInput.ModelInput(self.model_conf)

		incols,outcol,training_dataset = mlinput.get_input_for_dataset(dataset=in_dataset,extra_col_names=self.extra_col_names)
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
						compute_p_values=False,
						lambda_=0,
						model_id=model_name)

				glm.train(incols, outcol, training_frame=training_dataset,validation_frame=test_dataset)

		themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
		themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)

		print(glm._model_json['output']['coefficients_table'])
		themodel.mse = glm.mse()
		themodel.r2 = glm.r2()


		h2o.remove(glm)                                                             
		h2o.remove(training_dataset) 

		return themodel


	def train_and_refine_model_for_chid(self,chid, in_dataset,scale_sd=5.):
		themodel = MLModelManager.MLModel()
		themodel.chid = chid
		themodel.modelconf_id = self.model_conf.modelconf_id

		model_name = f'{self.model_conf.modelconf_id}_{chid}'

		mlinput = MLModelInput.ModelInput(self.model_conf)

		incols,outcol,training_dataset = mlinput.get_input_for_dataset(dataset=in_dataset,extra_col_names=self.extra_col_names)

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
						compute_p_values=False,
						lambda_=0,
						model_id=model_name)

				glm.train(incols, outcol, training_frame=training_dataset)

		# themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
		# themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)

		print(glm._model_json['output']['coefficients_table'])
		themodel.mse = glm.mse()
		themodel.r2 = glm.r2()

		pred_frame = glm.predict(training_dataset)

		training_dataset['predict'] = pred_frame['predict']

		###### refine training dataframe ######

		training_dataset['diff'] = training_dataset['predict'] - training_dataset[outcol]
		training_dataset['abs_diff'] = training_dataset['diff'].abs()
		training_dataset['sd'] = training_dataset['diff'].sd()[0]

		mask = training_dataset['abs_diff'] < scale_sd*training_dataset['sd']
		print(training_dataset)
		new_training_dataset = training_dataset[mask,:]
		print(new_training_dataset)
		glm.train(incols, outcol, training_frame=new_training_dataset)

		print(glm._model_json['output']['coefficients_table'])
		themodel.mse = glm.mse()
		themodel.r2 = glm.r2()

		themodel.model_path = h2o.save_model(glm, self.model_files_path, force=True)               
		themodel.mojo_path = glm.download_mojo(path=self.mojo_files_path, get_genmodel_jar=True)

		h2o.remove(glm)                                                             
		h2o.remove(training_dataset) 
		h2o.remove(new_training_dataset) 
		return themodel

	def train_autoencoder(self):
		themodel = MLModelManager.MLModel()
		themodel.chid = -1
		themodel.modelconf_id = self.model_conf.modelconf_id

		model_name = f'{self.model_conf.modelconf_id}_{themodel.chid}'
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
			rpc_ae.create_network()
			if self.model_conf.mlclass == 'AUTOENC_V2':
				rpc_ae.set_layers_one_and_five_size(768)
				rpc_ae.set_layers_two_and_four_size(256)
				rpc_ae.set_central_layer_size(64)
				rpc_ae.create_network()
				if self.model_conf.mlclass == 'AUTOENC_V3':
					rpc_ae.set_layers_one_and_five_size(1024)
					rpc_ae.set_layers_two_and_four_size(384)
					rpc_ae.set_central_layer_size(128)
					rpc_ae.create_network()  

	#        rpc_ae.create_network()

		ae_dm = AE_DataManager()

		ae_dm.set_time_window(self.model_conf.train_from,self.model_conf.train_to)

		theData = None       

		for dataset,datedataset in ae_dm.get_dataframe(): 
			if theData is None:
				theData = dataset
				print(f"Shape of theData after initial append: {theData.shape}")
			else:
				theData = np.concatenate((theData, dataset)) 
				print(f"The shape of theData at this point is: {theData.shape}")
				print("Ten more days of data appended!")
				#rpc_ae.train(dataset,dataset)

		print("++++++++++++++++++++++++++++++++++++++")
		print("+       NOW STARTING TO TRAIN         ")
		print("++++++++++++++++++++++++++++++++++++++")
		rpc_ae.train(theData, theData)

		rpc_ae.autoencoder.save(themodel.model_path)

		themodel.mse = 0
		themodel.r2 = 0

		return themodel    

