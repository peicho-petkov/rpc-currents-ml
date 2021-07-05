#!/usr/bin/env python3

import h2o
from db_tools import rpccurrml,table_mlmodels,table_mlmodelsconf


h2o.init()
rpccurrml.self_cursor_mode()

q = f"select {table_mlmodelsconf.name},{table_mlmodelsconf.modelconf_id} from {table_mlmodelsconf.tablename}"
conf_confid = rpccurrml.fetchall_for_query_self(q)

for confname_id in conf_confid:
    conf_id = confname_id[1]
    q = f"select {table_mlmodels.model_path} from {table_mlmodels.tablename} where {table_mlmodels.modelconf_id} = {conf_id}"
    paths = rpccurrml.fetchall_for_query_self(q)
    
    for model_file in paths:
        model_file = model_file[0]
        print(f"model file: {model_file}")

        model = h2o.load_model(model_file)

        print(model._model_json['output']['coefficients_table'])

        par_names = model._model_json['output']['coefficients_table']['names']                                                       
        par_coeff = model._model_json['output']['coefficients_table']['coefficients']                                                
        par_std = model._model_json['output']['coefficients_table']['standardized_coefficients']                                     
        print(par_names)                                                                                                             
        print(par_coeff)                                                                                                             
        zzz = zip(par_names,par_coeff)                                                                                               
        zzz_std = zip(par_names,par_std)                                                                                             
        print(dict(zzz))                                                                                                             
        print(dict(zzz_std))