#Authors: Elton Shumka, Peicho Petkov

import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from navbar import Navbar
from db_tools import table_notifications, rpccurrml
import pandas as pd

nav = Navbar()

body = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H2("Info"),
                    html.P(
                        """\
    The goal of this web user interface is to provide a platform for the study of RPC currents. 
    The tool implemented in this interface maintains communication with a database where data about the RPC muon chambers are stored. This data
    contains information about the measured currents on RPC chambers during Run2 (2016-2018); incoming new data will be available as we enter in Run3 
    during 2022. 
    Additionally, data about LHC parameters, environmental parameters and HV working points are stored in the database. All this data was organized in
    the database in order to utilize it in the training of Machine Learning models that model the behavior of RPC currents in time, as a function of 
    the parameters mentioned above.
    Two categories of models are implemented: Generalized Linear Models; using the h2o platform (www.h2o.ai), and Autoencoder Neural Networks; using TensorFlow (www.tensorflow.org).
    Both categories have shown good predictive capabilities. The predictive capabilities of the trained models are used to develop a live monitoring tool:
    the predictions are compared to the incoming data and if the differences exceed some predetermined values, this is interpreted as an indication of 
    chamber misbehavior. 
                                """
                                , style={'text-align':'justify'}),
                    html.H2("Code repository"),
                    html.P(
                        """\
    The code for this user interface as well as the underlying modules and tools performing the database management, training of ML models, prediction and validation,
    as well as plotting of results can be found at the following link: https://github.com/peicho-petkov/rpc-currents-ml/
                                """
                                , style={'text-align':'justify'}),
                ],
                md=8,
                #style={'background-color':'red'},
            ),
            ],
            justify='start',
        )    
        
    ],     
    className='mt-4',  
)

def Aboutinfo():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])

app.layout = Aboutinfo()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=False,port=8050,host='192.168.2.192')

