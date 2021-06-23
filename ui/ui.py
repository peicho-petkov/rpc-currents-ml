import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import date, datetime

mlconfnames = ['conf1','conf2','conf3']
dpids = [315,317,2049]

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.MINTY], title="RPC Currents ML Interface"
)
server = app.server

app.layout = dbc.Container(
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
                            is_open=False,
                        ),
                        html.Br(),
                        dbc.Button(
                            "DPID", id="dpid_button", style={'background-color': 'darkblue'}
                        ),
                        dbc.Collapse(
                            dcc.Dropdown(id='dpid_id', multi = True, searchable = True,
                                    options = [{"label" : entry, "value" : entry} for entry in dpids ]),
                            id="dpid_collapse",
                            is_open=False,
                        ),
                        html.Br(),
                        dbc.Button(
                            "Plotting Period", id="time_period_button", style={'background-color': 'darkblue'}
                        ),
                        dbc.Collapse(
                            dcc.DatePickerRange(
                                id='time-period-start-date',
                                min_date_allowed=date(2016, 1, 1),
                                # max_date_allowed=date(2017, 9, 19),
                                initial_visible_month=date(2018, 11, 30),
                                # end_date=date(2017, 8, 25)
                            ),
                            id="time_period_collapse",
                            is_open=False,
                        ),
                        html.Hr(),
                        dbc.Button(
                            "Plot", id="plot_button", style={'background-color': 'green'}
                        )],
                    width=3,
                ),
                dbc.Col(
                    [dcc.Graph(id="display", style={"height": "90vh"}),],
                    width=9,
                    align="start",
                ),
            ]
        ),
        html.Hr(),
        dcc.Markdown(
            """
        """
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("modelconfname_collapse", "is_open"),
    [Input("mlconfname_button", "n_clicks")],
    [State("modelconfname_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("dpid_collapse", "is_open"),
    [Input("dpid_button", "n_clicks")],
    [State("dpid_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("time_period_collapse", "is_open"),
    [Input("time_period_button", "n_clicks")],
    [State("time_period_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=False,port=8050,host='rpccurdevml.cern.ch')
