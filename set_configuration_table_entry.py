#!/usr/bin/env python3
from db_tools import table_configuration
from Configuration import Configuration 
from TrainerModule import DataManager
from db_tools import base as dbase
from optparse import OptionParser

if __name__=="__main__":
    oparser = OptionParser()
    oparser.add_option("--parameter-name", action="store", type="string", dest="parameter_name", 
                       help="Enter the name of configuration parameter whose value you want to be changed , string")
    oparser.add_option("--parameter-value", action="store", type="string", dest="parameter_value", 
                       help="Enter the new parameter value, string")

    (options, args) = oparser.parse_args()
    par_name = options.parameter_name
    par_value = options.parameter_value

    rpccurrml = dbase.mysql_dbConnector(host='rpccurdevml',user='ppetkov',password='cmsrpc')
    rpccurrml.connect_to_db('RPCCURRML')
    rpccurrml.self_cursor_mode()

    conf = Configuration(rpccurrml)
    query = conf.SetParameter(par_name,par_value)
    rpccurrml.execute_commit_query_self(query)


