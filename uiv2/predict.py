#Authors: Elton Shumka, Peicho Petkov

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
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
from z_prediction_tools.predict_for_period_and_active_method import perform_prediction
from z_prediction_tools import predict_for_hv_channel_method

q = table_mlmodelsconf.get_select_modelconfnames_query()
mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]

q = table_mlmodels.get_get_active_model_ids_and_dpids_query()
midsdpids = rpccurrml.fetchall_for_query_self(q)

q = table_mlmodels.get_get_active_modelconf_id_query()
activeconf = rpccurrml.fetchall_for_query_self(q)[0][0]

q = table_mlmodelsconf.get_select_modelconfname_by_modelconfid_query(activeconf)
actconfname = rpccurrml.fetchall_for_query_self(q)[0][0]

#TODO: Decide what prediction options will be available

nav = Navbar()

body = dbc.Container([
        html.Hr(),
        dcc.Markdown(
            "MAKE A PREDICTION" 
        ),
        dbc.Button(
            "Prediction Period", id="prediction-period", style={'background-color': 'darkblue'}    
        ),
        dbc.Collapse(
            dcc.DatePickerRange(
                id="pred-period-start-end-date",
                min_date_allowed=date(2016, 1, 1),
                initial_visible_month=date(2018, 5, 31),
            ),
            id="pred-period-collapse",
            is_open=True
        ),
        html.Br(),
        dbc.Button(
            "ML Models Configuration name", id="mlconfname_button", style={'background-color': 'darkblue'}
        ),
        dbc.Collapse(
            dcc.Dropdown(id = 'modelconfname_id',
                    options = [{"label" : entry, "value" : entry} for entry in mlconfnames ]),
            id="modelconfname_collapse",
            is_open=True,
        ),
        html.Br(),
        dbc.Button(
            "SELECT A DPID", id="select-model-button", style={'background-color': 'magenta'}    
        ),
        dbc.Collapse(
            dcc.Dropdown(id="all-models-dropdown", 
                options = [{'label': entry[1], 'value': entry[1]} for entry in midsdpids],
                multi=True, searchable=True),
            id="all-models-collapse",
            is_open=True
        ),
        html.Br(),
        dcc.Markdown(
            f"THE ACTIVE CONFIGURATION IS: {actconfname}"  
        ),
        dbc.Button(
            "ACTIVE MODELS", id="active-models-button", style={'background-color': 'magenta'}    
        ),
        dbc.Collapse(
            dcc.Dropdown(id="active-models-dropdown", 
                options = [{'label':entry[0], 'value':entry[0]} for entry in midsdpids],
                multi=True, searchable=True),
            id="active-models-collapse",
            is_open=True
        ),
        html.Hr(),
        dcc.RadioItems(
            options=[
                {'label':'Predict only for selected models', 'value':'selectedmodels'},
                {'label':'Predict for all active models', 'value':'activemodels'}
            ],
            labelStyle={'display':'block'},
            id="pred-alternative"
        ),
        html.Br(),
        dbc.Button(
            "Perform prediction", id="perform-the-prediction", style={'background-color': 'green'}    
        ),
        html.Div(id="pred-hidden-div"),
        ],
fluid=True,
)

def Predict():
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

