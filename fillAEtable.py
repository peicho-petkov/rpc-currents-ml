from db_tools.db_tables import autoencoderData
from db_tools import rpccurrml, table_training
import pandas as pan

myfile = pan.read_csv("~/autoencoder/autoenc-training-2016-new-format.csv")

timestamps = myfile.timestamp.to_list()
# print(timestamps)

enctable = autoencoderData()
i = 0
for tstamp in timestamps:
    df = myfile[myfile['timestamp'] == f'{tstamp}']
    vals = df.values.tolist()
    vals = vals[0]
    vals.pop()
    stamp = vals[0]
    print(stamp)
    vals.pop(0)
    vals = [str(i) for i in vals]
    #print(vals)
    vals = tuple([stamp] + vals)
    #vals = ",".join(map(str, vals))
    #print(len(vals))
    query = enctable.get_fill_row_query(values = vals)
    #print(query)
    rpccurrml.execute_commit_query_self(query)
    i = i + 1
    print(f"Entry number {i} inserted")
