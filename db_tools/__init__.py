from .base import *
from .db_tables import *

table_training = db_tables.TrainingDataTable()
table_uxcenv = db_tables.UxcEnvTable()
table_lumi = db_tables.LumiDataTable()
table_mlmodelsconf = db_tables.MLModelsConf()
table_mlmodels = db_tables.MLModels()
table_predicted_current = db_tables.PredictedCurrentsTable()
table_configuration = db_tables.ConfigurationTable()
table_notifications = db_tables.NotificationsTable()
table_dpidstates = db_tables.dpidStateTable()
#table_autoencoder = db_tables.autoencoderData()

rpccurrml = mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
rpccurrml.connect_to_db('RPCCURRML')
rpccurrml.self_cursor_mode()

omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
omds.connect_to_db('cman_int2r')
