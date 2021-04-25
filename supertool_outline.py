import supertool_component_1
import supertool_component_2
from z_training_tools import trainall_for_modelconfname_method
import time

#TODO Organize in time the steps below, which when 'comes online'
# while True:

# Register new model configuration every month, 
# including the past month in the training period
    modelconf_name = supertool_component_1.register_new_model_configuration()

# Use the name of the newly registered model configuration to 
# train all the available dpids on this updated period
    trainall_for_modelconfname_method.trainall(modelconf_name)

# Make predictions and analyse for the past day/days using active models
    supertool_component_2.periodic_evaluation(86400)