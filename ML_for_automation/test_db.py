from base import oracle_dbConnector, Extractor_Oracle
from datetime import datetime, date

if __name__ == "__main__":

	automation_db = oracle_dbConnector(user='CMS_RPC_PVSS_TEST', password='rpcr22_d3Own') #, dsn_tns="./tnsnames.ora")
	automation_db.connect_to_db(database='int2r_nolb')
	#automation_db.self_cursor_mode()

	query = "SELECT * FROM ( SELECT * FROM CMS_RPC_PVSS_TEST.MLTRAININGDATA) WHERE ROWNUM <= 10"
	#result = automation_db.fetchall_for_query_self(query)

	#print(result)

	extractor = Extractor_Oracle(automation_db)

	#extractor.set_tablename("CMS_RPC_PVSS_TEST.MLTRAININGDATA")
	extractor.set_chamber_id_col_name("CHAMBER_ID")
	extractor.set_flag_col_name("FLAG")
	extractor.set_timestamp_col_name("CHANGE_DATE")
	print(f"startdate = {datetime.strptime('2023-04-05', '%Y-%m-%d')}")
	print(f"enddate = {datetime.strptime('2023-04-08', '%Y-%m-%d')}")
	extractor.set_time_window(datetime.strptime("2023-04-05", '%Y-%m-%d'), datetime.strptime("2023-04-08", '%Y-%m-%d'))

	data = extractor.get_rpccurrents_data("CMS_RPC_PVSS_TEST.MLTRAININGDATA", 447826, 56, ['CHAMBER_ID', 'CHANGE_DATE', 'VMON', 'IMON', 'FLAG', 'INSTLUMI', 'ACC_INT_CHARGE_COLL', 'ACC_INT_CHARGE_NOCOLL'])
	
	print(data)
