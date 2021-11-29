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

q = table_notifications.get_get_tabledata_query()
res = rpccurrml.fetchall_for_query_self(q)

df = pd.DataFrame(res)
df = df.rename(columns={0:'rec_id',1:'LAST_UPDATE', 2:'DPID', 3:'model_id', 4:'notification_type', 5:'flag_raised_time', 6:'avg_discrepancy', 7:'Sent', 8:'Acknowledged', 9:'Masked'})

body = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H2("Notifications table from DB"),
                    dash_table.DataTable(
                       id="notifications_table",
                       #columns=[{'name':'dpid','id':'dpid'},{'name':'# of warnings','id':'warnings'},{'name':'# of errors','id':'errors'},{'name':'Flag raised time','id':'timestamp'}],
                       data=df.to_dict('records'),
                       columns=[{'name':i, 'id':i} for i in df.columns]
                    )
                ],
                md=4,
                #style={'background-color':'red'},
            ),
            ],
            justify='start',
        )    
        
    ],     
    className='mt-4',  
)

def Warningtab():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])

app.layout = Warningtab()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=False,port=8050,host='192.168.2.192')

