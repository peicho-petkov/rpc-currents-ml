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

q = table_mlmodelsconf.get_select_modelconfnames_query()
mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]

nav = Navbar()

body = dbc.Container([
        dbc.Button(
            "ML Models Configuration name", id="mlconfname_button", style={'background-color': 'darkblue'}
        ),
        dbc.Collapse(
            dcc.Dropdown(id = 'modelconfname_id',
                    options = [{"label" : entry, "value" : entry} for entry in mlconfnames ]),
            id="modelconfname_collapse",
            is_open=True,
        ),
        html.Hr(),
        dcc.Markdown(
            "TRAIN YOUR MODELS"
        ),
        dbc.Button("Select DPID for Training",
                    id="dpid_for_training_button", style={'background-color': 'Orchid'}
                    ),
        dbc.Collapse(
            dcc.Dropdown(
                id="dpids_for_training", multi=True, searchable=True,
            ),
            id="select_train_dpid_collapse",
            is_open=True,
        ),
        dbc.Button(
                "TRAIN", id="train_button", style={'background-color': 'Green'}
                ),
        html.Div(id='hidden-div'),    # A placeholder for callback output
        #The following elements create the window where terminal output will be redirected
        dcc.Interval(
                id='interval1', interval = 1 * 1000,
                n_intervals=0),
        dcc.Interval(
                id='interval2', interval = 1 * 1000,
                n_intervals=0),
        dbc.Collapse(
            html.Iframe(id='console-out', srcDoc='', style={'width':'100%', 'height':420, 'scrolling':'yes', 'overflow':'scroll'}),
                id='details_collapse', is_open=False),
        dbc.Button("Details", id='show_train_details', style={'background-color': 'Orchid'}),
        html.Div(id='hidden-div2', style={'display':'none'})
        ],
fluid=True,
)

def Train():
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

