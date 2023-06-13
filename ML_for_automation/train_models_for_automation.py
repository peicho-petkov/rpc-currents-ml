#!/usr/bin/env python3

# Train the models for the ML part of the RPC automation
# Connect to the automation database, read data from MLTrainingData
# and store models in the path specified in the MLConfiguration table

import RPCChamberModel
from Configuration import Configuration
from TrainerModule import MLModelManager, MLTrainer, DataManager
from TrainerModule.MLModelManager import MLModelsConfManager, MLModelsManager
from optparse import OptionParser
from db_tools import table_mlmodelsconf, table_training, automation_db, table_configuration
import h2o

def train_for_chamber(model_conf_name, chid, flag, mojopath, modelpath):
	conf_name = model_conf_name
	RPCChamberModel.init(model_conf_name=conf_name, mojofiles_path=mojopath, mlmodels_path=modelpath)

	if 'AUTOENC' in RPCChamberModel.mconf.mlclass:
		model_ids, chids = RPCChamberModel.train_and_register_autoencoder(True)
		for kv in range(len(model_ids)):
			model_id = model_ids[kv]
			chid = chids[kv]
			if model_id == -1:
				print(f"A model configuration with name {conf_name} already registered for CHID {chid}...")
			elif model_id == -2:
				print(f"No data for CHID {chid} and model configuration {conf_name}")
			elif model_id >= 0:
				print(f"An ML model with model_id {model_id} with configuration name {conf_name} for CHID {chid} was registered successfully...")      

	if 'GLM' in RPCChamberModel.mconf.mlclass:
		model_id = RPCChamberModel.train_and_register_for_chid(chid,flag,True)

		if model_id == -1:
			print(f"A model configuration with name {conf_name} already registered for CHID {chid}...")
		elif model_id == -2:
			print(f"No data for CHID {chid} and model configuration {conf_name}")
		elif model_id >= 0:
			print(f"An ML model with model_id {model_id} with configuration name {conf_name} for CHID {chid} was registered successfully...")


if __name__ == "__main__":
	oparser = OptionParser()
	oparser.add_option("--modelconf-name", action="store", type="string", dest="modelconf_name",
			help="The modelconfname of the models you want to train")

	(options, args) = oparser.parse_args()
	modelconf_name = options.modelconf_name

	modelconfmanager = MLModelManager.MLModelsConfManager(automation_db, table_mlmodelsconf)
	model_conf = modelconfmanager.get_by_name(modelconf_name)
	print(model_conf.train_from)
	print(model_conf.flags)

	train_start_date = model_conf.train_from            # options.change_date_start
	train_end_date = model_conf.train_to                # options.change_date_end

	conf = Configuration(automation_db)
	mojopath = conf.GetParameter("mojo_path") 
	print(f"mojopath: {mojopath}")
	modelpath = conf.GetParameter("model_path") 
	print(f"modelpath: {modelpath}")
	#flag = int(conf.GetParameter("flag"))
	flag = model_conf.flags
	print(f"+++++++++ flag = {flag}")

	if "AUTOENC" in model_conf.mlclass:
		train_for_chamber(modelconf_name, -1, flag, mojopath, modelpath)
	else:
		query = table_training.get_get_all_chids_query()
		print(query)
		chids = automation_db.fetchall_for_query_self(query)
		chids = [i[0] for i in chids] 
		h2o.init()

		for chid in chids:
			train_for_chamber(modelconf_name, chid, flag, mojopath, modelpath)

