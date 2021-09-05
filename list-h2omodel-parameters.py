#!/usr/bin/env python3

import h2o
import sys

h2o.init()

model_file=sys.argv[1]

print(f"model file: {model_file}")

model = h2o.load_model(model_file)

par_names = model._model_json['output']['coefficients_table']['names']
par_coeff = model._model_json['output']['coefficients_table']['coefficients']
par_std = model._model_json['output']['coefficients_table']['standardized_coefficients']
print(par_names)
print(par_coeff)
zzz = zip(par_names,par_coeff)
zzz_std = zip(par_names,par_std)
print(dict(zzz))
print(dict(zzz_std))
