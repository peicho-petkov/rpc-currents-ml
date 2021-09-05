import dash
from dash_bootstrap_components._components.Spinner import Spinner
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go

################### TODO: put in separate file ###############################
import RPCHVChannelModel
import h2o
from optparse import OptionParser
from EstimatorModule import PredictionsManager, Estimator
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput
from db_tools import table_mlmodels, table_mlmodelsconf, table_training, rpccurrml, base as dbase
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd

q = table_mlmodelsconf.get_select_modelconfnames_query()
mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]

h2o.init()

##############################################################################

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
                        html.Hr(),
                        dbc.Button(
                            "Plot", id="plot_button", style={'background-color': 'green'}
                        )],
                    width=3,
                ),
                dbc.Col([
                    dbc.Spinner(dcc.Graph(id="display", style={"height": "90vh"}),),
                    dbc.Spinner(dcc.Graph(id="display_diff", style={"height": "90vh"}),),
                    dbc.Spinner(dcc.Graph(id="display_diff_histo", style={"height": "90vh"}),),],
                    width=9,
                    align="start",)
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

old_mlconfname = None
old_options = []
@app.callback(
    Output('dpid_id','options'),
    [Input('modelconfname_id','value')]
)
def change_mlconfname(confname):
    global old_mlconfname
    global old_options

    confname_chaged = old_mlconfname != confname
    old_mlconfname = confname

    if confname_chaged:
        if confname is not None:
            mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
            mconf = mconf_manager.get_by_name(confname)
            q = table_mlmodels.get_get_dpids_by_modelconf_id_query(mconf.modelconf_id)
            dpids = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]
            print(dpids)
            options = [{"label" : f"{entry}", "value" : f"{entry}"} for entry in dpids]
            old_options = options[:] 
        else:
            old_options = []
    print(old_options)
    return old_options[:]


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

n_clicks_last = 0
start_date_last = date(1,1,1)
end_date_last = date(1,1,1)
dpids_to_plot_last = []
timeplot_fig_last = None
confname_last = None

@app.callback(
    Output("display","figure"),
    Output("display_diff","figure"),
    Output("display_diff_histo","figure"),
        Input("plot_button","n_clicks"),
        State("modelconfname_id","value"),
        State("dpid_id","value"),
        State('time-period-start-end-date','start_date'),
        State('time-period-start-end-date','end_date'),
    
)
def plot_graph(n_clicks,modelconfname,dpids,start_date,end_date):
    global n_clicks_last
    global start_date_last
    global end_date_last
    global dpids_to_plot_last
    global timeplot_fig_last
    global confname_last

    plot_period_changed = False
    dpids_to_plot = []
    confname_chaged = False

    if n_clicks is None:
        n_clicks = 0

    plot_button_pressed = n_clicks > n_clicks_last
    n_clicks_last = n_clicks

    if timeplot_fig_last is None:
        fig = go.Figure()
        timeplot_fig_last = fig,fig,fig
    else:
        fig = timeplot_fig_last
    
    fig = go.Figure()
    
    if not plot_button_pressed or dpids is None or modelconfname is None or start_date is None or end_date is None:
        return fig,fig,fig

    print(n_clicks,modelconfname,dpids,start_date,end_date)
    

    if start_date_last != start_date or end_date_last != end_date:
        plot_period_changed = True
        start_date_last = datetime.strptime(start_date,'%Y-%m-%d')
        end_date_last =  datetime.strptime(end_date,'%Y-%m-%d')

    if plot_period_changed:
        dpids_to_plot = dpids[:]
        dpids_to_plot_last = dpids_to_plot
    else:
        dpids_to_plot = list(set(dpids).difference(dpids_to_plot_last))
        dpids_to_plot_last = dpids_to_plot_last + dpids_to_plot
    
    
    confname_chaged = modelconfname != confname_last
    confname_last = modelconfname

    print(dpids_to_plot,dpids_to_plot_last)

    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf = mconf_manager.get_by_name(modelconfname)
    
    model_manager = MLModelManager.MLModelsManager(rpccurrml,table_mlmodels)

    extractor_table_training = DataManager.Extractor_MySql(table_training.tablename,rpccurrml)
    extractor_table_training.set_time_widow(start_date_last,end_date_last)
    extractor_table_training.set_column_name_list([table_training.change_date,table_training.imon])
    extractor_table_training.set_FLAG(56)
    mlinput = MLModelInput.ModelInput(mconf)
    if mconf.mlclass == 'GLM_V4':
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.vmon,table_training.change_date])
    else:
        extractor_table_training.set_column_name_list(mconf.input_cols.split(',')+mconf.output_cols.split(',')+[table_training.change_date])
    print("plotting")
    
    data = []
    data_diff = []
    data_diff_histo = []
    
    for dpid in dpids_to_plot_last:
        model = model_manager.get_by_modelconf_id_dpid(mconf.modelconf_id,dpid)
        hv_curr_estimator = Estimator.Estimator(model)
        extractor_table_training.set_DPID(dpid)
        query = extractor_table_training.get_data_by_dpid_flag_query()
        curdata = rpccurrml.fetchall_for_query_self(query)
        if mconf.mlclass == 'GLM_V4':
            incols, outcol, dataset = mlinput.get_input_for_dataset(curdata,[table_training.vmon,table_training.change_date])
        else:
            incols, outcol, dataset = mlinput.get_input_for_dataset(curdata,[table_training.change_date])

        pf = dataset.as_data_frame()
        pf[table_training.change_date] = pd.to_datetime(pf[table_training.change_date].to_list(),unit='ms')
        pf['predicted'], pred_err = hv_curr_estimator.predict_for_dataframe(dataset)

        del hv_curr_estimator

        data=data+[go.Scatter(x=pf[table_training.change_date].values, y=pf[table_training.imon].values,name=f"{dpid} imon",connectgaps = False)]
        data=data+[go.Scatter(x=pf[table_training.change_date].values, y=pf['predicted'].values, name=f"{dpid} predicted",line = dict(dash = 'dash'),connectgaps = False)]
        
        pf['diff_iom_predicted'] = pf[table_training.imon] - pf['predicted']
        
        data_diff_histo = data_diff_histo + [go.Histogram(x=pf['diff_iom_predicted'].values, name=f"{dpid} imon - predicted")]
        
        pf['diff_iom_predicted'] = pf['diff_iom_predicted'].rolling(100).mean()
        data_diff = data_diff + [go.Scatter(x=pf[table_training.change_date].values, y=pf['diff_iom_predicted'].values, name=f"{dpid} imon - predicted",connectgaps = False)]

    fig = go.Figure(data=data)
    print(fig)
    fig_diff = go.Figure(data=data_diff)
    fig_diff_histo = go.Figure(data=data_diff_histo)
    timeplot_fig_last = (fig, fig_diff,fig_diff_histo)
    for f in fig.data:
        print(f.name)
        
    # fig.update_layout(barmode='stack')

    fig.update_layout(title='<b>RPC Current</b>',
                   yaxis_title='<b>Current [&mu;A]</b>')
    
    # fig_diff.update_layout(barmode='stack')
_
    fig_diff.update_layout(title='<b>Model deviation running average</b>',
                   yaxis_title='<b>IMON-prediciton [&mu;A]</b>')
    
    # fig_diff_histo.update_layout(barmode='stack')

    fig_diff_histo.update_layout(title='<b>Model deviation distribution</b>',
                   xaxis_title='<b>IMON-prediciton [&mu;A]</b>')
    return fig,fig_diff,fig_diff_histo

if __name__ == "__main__":
    app.run_server(debug=False,port=8050,host='rpccurdevml.cern.ch')
