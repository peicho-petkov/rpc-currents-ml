#!/usr/bin/env python3

import h2o
import sys

h2o.init()

model_file=sys.argv[1]

print(f"model file: {model_file}")

model = h2o.load_model(model_file)

print(model._model_json['output']['coefficients_table'])
