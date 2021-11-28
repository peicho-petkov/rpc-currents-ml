#Authors: Elton Shumka, Peicho Petkov

import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from navbar import Navbar
from db_tools import table_notifications, rpccurrml
import pandas as pd

nav = Navbar()

q = table_notifications.get_retrieve_data_for_homepage_table_query()
res = rpccurrml.fetchall_for_query_self(q)

df = pd.DataFrame(res)
dropcol = df.columns[1]
df = df.drop([dropcol], axis=1)
#dfasdict = df.to_dict()
df = df.rename(columns={0:'dpid',2:'# of warnings', 3:'# of errors', 4:'flag_raised_time'})
body = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H2("Overview"),
                    html.P(
                        """\
    The goal of this web user interface is to provide a platform for the study of RPC currents. 
    The tool implemented in this interface maintains communication with a database where data about the RPC muon chambers are stored. This data
    contains information about the measured currents on RPC chambers during Run2 (2016-2018); incoming new data will be available as we enter in Run3 
    during 2022. 
    Additionally, data about LHC parameters, environmental parameters and HV working points are stored in the database. All this data was organized in
    the database in order to utilize it in the training of Machine Learning models that model the behavior of RPC currents in time, as a function of 
    the parameters mentioned above.
    Two categories of models are implemented: Generalized Linear Models; using the h2o platform, and Autoencoder Neural Networks; using TensorFlow.
    Both categories have shown good predictive capabilities. The predictive capabilities of the trained models are used to develop a live monitoring tool:
    the predictions are compared to the incoming data and if the differences exceed some predetermined values, this is interpreted as an indication of 
    chamber misbehavior. To the right, the latest Warning and Errors are shown.
                                """
                                , style={'text-align':'justify'}),
                ],
                md=4,
                #style={'background-color':'red'},
            ),
            dbc.Col(
                [
                    html.H2("Summary of Warnings and Errors"),
                    dash_table.DataTable(
                       id="warning_table",
                       #columns=[{'name':'dpid','id':'dpid'},{'name':'# of warnings','id':'warnings'},{'name':'# of errors','id':'errors'},{'name':'Flag raised time','id':'timestamp'}],
                       data=df.to_dict('records'),
                       columns=[{'name':i, 'id':i} for i in df.columns]
                    )
                ]   
            )
            ],
            justify='start',
        )    
        
    ],     
    className='mt-4',  
)

def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])

app.layout = Homepage()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=False,port=8050,host='192.168.2.192')

