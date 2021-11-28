from db_tools import table_autoencoderData, dpid_colnames
from db_tools import rpccurrml


for dpidcol in dpid_colnames:
    #print(dpidcol)
    #query = f"update {table_autoencoderData.tablename} set {dpidcol}='-1' where {dpidcol}='-42'"
    #rpccurrml.execute_commit_query_self(query)
    query = f" SELECT timestamp FROM {table_autoencoderData.tablename} WHERE {dpidcol} = -42.0 "
    timestamps = rpccurrml.fetchall_for_query_self(query)
    for tstamp in timestamps:
        #print(tstamp[0])
        query = f" UPDATE {table_autoencoderData.tablename} SET {dpidcol}=-0.5, timestamp=timestamp WHERE timestamp = '{tstamp[0]}' "
        #print(query)
        rpccurrml.execute_commit_query_self(query)
    print(f"Done replacing for column {dpidcol}")
