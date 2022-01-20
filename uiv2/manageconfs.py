#Authors: Elton Shumka, Peicho Petkov

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from navbar import Navbar
from dash.dependencies import Input, Output, State
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go

import h2o
import pandas as pd
import matplotlib.pyplot as plt
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training, table_predicted_current, rpccurrml, base as dbase
from EstimatorModule import PredictionsManager, Estimator

q = table_mlmodelsconf.get_select_modelconfnames_query()
mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]

mlclasses= ['GLM_V1','GLM_V2','GLM_V3','GLM_V4','GLM_V5','GLM_V6','GLM_V7','AUTOENC_V1','AUTOENC_V2','AUTOENC_V3']

nav = Navbar()

body = dbc.Container([
       html.Hr(),
        dcc.Markdown(
            "CREATE YOUR OWN MODEL CONFIGURATION"
        ),
       dbc.Button(
            "ML Models Configuration name", id="mlconfname_button", style={'background-color': 'darkblue'}
        ),
        dbc.Collapse(
            dcc.Dropdown(id = 'modelconfname_id',
                    options = [{"label" : entry, "value" : entry} for entry in mlconfnames ]),
            id="modelconfname_collapse",
            is_open=True,
        ),
        dcc.ConfirmDialog(
            id='confirm_delete_dialog',
            message='Are you sure you want to delete this Configuration?'
        ),
        html.Button(
                "Delete Selected Configuration",
                id="delete_conf_button", style={'background-color': 'red'}),
        html.Div(id='output-provider'),
        html.Br(),
        dbc.Button(
            "Enter Name for New Configuration (mm-yyyy-mm-yyyy-f56-mlclass-vx)", id="reg_button", style={'background-color': 'CadetBlue'}
        ),
        dbc.Collapse(
            dcc.Input(
                id='input_conf_name', value='', type='text'
            ),
            id="reg_new_conf_name_collapse",
            is_open=True,
        ),
        html.Br(),
        dbc.Button(
            "Choose model class", id="class_button", style={'background-color': 'CadetBlue'}
        ),
        dbc.Collapse(
            dcc.Dropdown( id='class_name',
                options = [{"label": entry, "value": entry} for entry in mlclasses]),
            id="reg_new_model_class_collapse",
            is_open=True,
        ),
        html.Br(),
        dbc.Button(
            "Training and Testing Period", id="train_period_button", style={'background-color': 'CadetBlue'}
        ),
        dbc.Collapse(
            dcc.DatePickerRange(
                id='train-period-start-end-date',
                min_date_allowed=date(2016, 1, 1),
                # max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2018, 11, 30),
                # end_date=date(2017, 8, 25)
            ),
            id="train_period_collapse",
            is_open=True,
        ),
        html.Br(),
        dbc.Button(
            "Create Configuration", id="create_conf_button", style={'background-color': 'Green'}
        ),
        ],
fluid=True,
)

def ManageConfs():
    layout = html.Div([
        nav,
        body
    ])
    return layout


#app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED], title='RPC Currents ML Interface')

#app.layout = Train()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=False,port=8050,host='192.168.2.192')

