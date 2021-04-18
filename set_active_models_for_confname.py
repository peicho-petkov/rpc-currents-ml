#!/usr/bin/env python3

from TrainerModule import MLModelManager
from db_tools import table_mlmodels, table_mlmodelsconf
from optparse import OptionParser
from db_tools import base as dbase

if __name__ == "__main__":
    oparser = OptionParser()
    oparser.add_option("--modelconf-name", action="store", type="string", dest="modelconf_name",
                        help="The modelconfname of the models you want to train")
    oparser.add_option("--enable", action="store", type="string", dest="enable",
                        help="
    query = table_mlmodels.get_set_active(0)
    rpccurrml.execute_commit_query_self(query)

    modelmanager = MLModelManager.MLModelsManager(rpccurrml, table_mlmodels)
    modelmanager.set_mlmodels_active_state(table_mlmodelsconf, modelconf_name,)
