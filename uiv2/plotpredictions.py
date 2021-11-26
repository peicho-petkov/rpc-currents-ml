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

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            """
                        )
                    ],
                    width=True,
                ),
            ],
            align="end",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
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
                            "DPID", id="dpid_button", style={'background-color': 'darkblue'}
                        ),
                        dbc.Collapse(
                            dbc.Spinner(
                            dcc.Dropdown(id='dpid_id', multi = True, searchable = True),),
                            id="dpid_collapse",
                            is_open=True,
                        ),
                        html.Br(),
                        dbc.Button(
                            "Plotting Period", id="time_period_button", style={'background-color': 'darkblue'}
                        ),
                        dbc.Collapse(
                            dcc.DatePickerRange(
                                id='time-period-start-end-date',
                                min_date_allowed=date(2016, 1, 1),
                                # max_date_allowed=date(2017, 9, 19),
                                initial_visible_month=date(2018, 11, 30),
                                # end_date=date(2017, 8, 25)
                            ),
                            id="time_period_collapse",
                            is_open=True,
                        ),
                        html.Br(),
                        dbc.Button(
                            "Plot", id="plot_button", style={'background-color': 'green'}
                        )
                    ]),    
                dbc.Col([
                    dbc.Spinner(dcc.Graph(id="display", style={"height": "90vh"}),),
                    dbc.Spinner(dcc.Graph(id="display_diff", style={"height": "90vh"}),),
                    dbc.Spinner(dcc.Graph(id="display_diff_histo", style={"height": "90vh"}),),],
                    width=9,
                    align="start",),
        ]
        ),
    ],
    fluid=True,
)

def Plotpredictions():
    layout = html.Div([
        nav,
        body
    ])
    return layout


#app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED], title='RPC Currents ML Interface')

#app.layout = Plotpredictions()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=False,port=8050,host='192.168.2.192')

