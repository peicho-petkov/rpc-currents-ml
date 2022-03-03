#Authors: Elton Shumka, Peicho Petkov

import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from navbar import Navbar
from db_tools import table_configuration, rpccurrml
import pandas as pd

nav = Navbar()

q = table_configuration.get_get_tabledata_query()
res = rpccurrml.fetchall_for_query_self(q)

df = pd.DataFrame(res)
df = df.rename(columns={0:'rec_id',1:'LAST_UPDATE', 2:'PARAMETER_NAME', 3:'PARAMETER_VALUE', 4:'PARAMETER_TYPE', 5:'PARAMETER_UNIT'})

body = dbc.Container(
    [
        html.H2("Configuration parameters table from DB"),
        dash_table.DataTable(
           id="parameters_table",
           #columns=[{'name':'dpid','id':'dpid'},{'name':'# of warnings','id':'warnings'},{'name':'# of errors','id':'errors'},{'name':'Flag raised time','id':'timestamp'}],
           data=df.to_dict('records'),
           columns=[{'name':i, 'id':i} for i in df.columns],
           editable=True
        ),
        html.Br(),
        dcc.ConfirmDialog(
            id='confirm-changes-dialog',
            message='Are you sure you want to store the changes in the database?'
        ),
        html.Button(
                "SAVE CHANGES", id="save_changes_button", style = {'background-color':'darkblue'}    
        ),
        html.Div(id='output-provider-for-table')
    ]
)

def Configurationtab():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])

app.layout = Configurationtab()

if __name__ == "__main__":
    #app.run_server()
    app.run_server(debug=True,port=8050,host='192.168.2.192')

