from db_tools.db_tables import autoencoderData
from db_tools import rpccurrml, table_training
import pandas as pan

myfile = pan.read_csv("/afs/cern.ch/work/e/eshumka/autoencoder/autoenc-training-2016-new-format.csv")


myfile2 = pan.read_csv("/afs/cern.ch/work/e/eshumka/autoencoder/autoenc-training-2017-modified-format.csv")


myfile3 = pan.read_csv("/afs/cern.ch/work/e/eshumka/autoencoder/autoenc-training-2018-modified-format.csv")

# print(timestamps)

enctable = autoencoderData(tablename = "autoencoderData")
i = 0

timestamps = myfile.timestamp.to_list()

print("++++++ STARTING TO LOAD 2016 DATA INTO THE DATABASE ++++++")
for tstamp in timestamps:
    df = myfile[myfile['timestamp'] == f'{tstamp}']
    vals = df.values.tolist()
    vals = vals[0]
    vals.pop()
    stamp = vals[0]
    vals.pop(0)
    vals = [str(i) for i in vals]
    #print(vals)
    #print(len(vals))
    vals = tuple([stamp] + vals)
    #vals = ",".join(map(str, vals))
    #print(vals)
    query = enctable.get_fill_row_query(values = vals)
    #print(query)
    rpccurrml.execute_commit_query_self(query)
    i = i + 1
    if ( i % 10000 == 0):
        print(stamp)
        print(f"Entry number {i} inserted")
print("++++++ FINISHED LOADING 2016 DATA ++++++")


timestamps = myfile2.timestamp.to_list()

print("++++++ STARTING TO LOAD 2017 DATA INTO THE DATABASE ++++++")
for tstamp in timestamps:
    df = myfile2[myfile2['timestamp'] == f'{tstamp}']
    vals = df.values.tolist()
    vals = vals[0]
    vals.pop()
    vals.pop(0)
    stamp = vals[0]
    vals.pop(0)
    vals = [str(i) for i in vals]
    #print(vals)
    #print(len(vals))
    vals = tuple([stamp] + vals)
    #vals = ",".join(map(str, vals))
    #print(vals)
    query = enctable.get_fill_row_query(values = vals)
    #print(query)
    rpccurrml.execute_commit_query_self(query)
    i = i + 1
    if ( i % 10000 == 0):
        print(stamp)
        print(f"Entry number {i} inserted")
print("++++++ FINISHED LOADING 2017 DATA ++++++")


timestamps = myfile3.timestamp.to_list()

print("++++++ STARTING TO LOAD 2018 DATA INTO THE DATABASE ++++++")
for tstamp in timestamps:
    df = myfile3[myfile3['timestamp'] == f'{tstamp}']
    vals = df.values.tolist()
    vals = vals[0]
    vals.pop()
    vals.pop(0)
    stamp = vals[0]
    vals.pop(0)
    vals = [str(i) for i in vals]
    #print(vals)
    #print(len(vals))
    vals = tuple([stamp] + vals)
    #vals = ",".join(map(str, vals))
    #print(vals)
    query = enctable.get_fill_row_query(values = vals)
    #print(query)
    rpccurrml.execute_commit_query_self(query)
    i = i + 1
    if ( i % 10000 == 0):
        print(stamp)
        print(f"Entry number {i} inserted")
print("++++++ FINISHED LOADING 2018 DATA ++++++")

