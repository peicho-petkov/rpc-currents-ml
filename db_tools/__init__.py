from .base import *
from .db_tables import *

table_training = db_tables.TrainingDataTable()
table_uxcenv = db_tables.UxcEnvTable()
table_lumi = db_tables.LumiDataTable()
table_mlmodelsconf = db_tables.MLModelsConf()
table_mlmodels = db_tables.MLModels()
table_predicted_current = db_tables.PredictedCurrentsTable()
table_configuration = db_tables.ConfigurationTable()