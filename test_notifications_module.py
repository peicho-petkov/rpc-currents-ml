from db_tools import table_notifications, table_predicted_current
from NotificationModule import NotificationManager
from db_tools import rpccurrml
from db_tools import base as dbase


rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
rpccurrml.connect_to_db('RPCCURRML')
rpccurrml.self_cursor_mode()

notmanager = NotificationManager.NotificationManager(rpccurrml,table_predicted_current,100)

notificationstable=table_notifications

#query=notificationstable.get_myqsl_create_query()
#rpccurrml.execute_commit_query_self(query)

query=notificationstable.get_insert_notification_query(316,23,'error','2017-06-06',6.5,1,0,0)
query1=notificationstable.get_update_acknowledged_col_query(1,316,23)
rpccurrml.execute_commit_query_self(query1)

