#Authors: Elton Shumka, Peicho Petkov

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Spinner import Spinner
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go

import RPCHVChannelModel
import h2o
from optparse import OptionParser
from EstimatorModule import PredictionsManager, Estimator
from TrainerModule import MLModelManager, MLModelsConfManager, DataManager, MLModelInput, MLModelConf
from db_tools import table_mlmodels, table_mlmodelsconf, table_training, table_autoencoderData, table_predicted_current, rpccurrml, base as dbase
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd
import sys
import logging
import os

from homepage import Homepage
from train import Train
from plotpredictions import Plotpredictions
from manageconfs import ManageConfs
from predict import Predict

mlclasses= ['GLM_V1','GLM_V2','GLM_V3','GLM_V4','GLM_V5','GLM_V6','GLM_V7','AUTOENC_V1','AUTOENC_V2','AUTOENC_V3']

h2o.init()

##############################################################################

sys.stdout = open('out.txt', 'w')
#f.close()

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.UNITED], title="RPC Currents ML Interface"
)
server = app.server

def serve_layout(): 
    q = table_mlmodelsconf.get_select_modelconfnames_query()
    mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]

    return html.Div([
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
                    html.H1(children="ML-based tool for RPC currents monitoring"),
                width=9,
                ),
                dbc.Col(
                    html.Img(src='/assets/lhcbeam.png', style={'height':'30%', 'width':'30%'}),
                width=3,
                ),
            ],
            align="center",
        ),
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
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
           
app.layout = serve_layout


#++++++++++++++ Below are all the callbacks +++++++++++++#

# This callback makes possible the navigation between pages
pathname = None
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/train':
        return Train()
    elif pathname == '/plot_predictions':
        return Plotpredictions()
    elif pathname == '/predict':
        return Predict()
    elif pathname == '/manage_configurations':
        return ManageConfs()
    else:
        return Homepage()
    

# Callback to update the dpids in the dropdown list of the models for the given configuration
old_mlconfname = None
old_options = []
@app.callback(
    Output('dpid_id','options'),
    #Output('dpids_for_training', 'options'),  # Has to be added as a separate callback; DONE, as of november 24
    [Input('modelconfname_id','value')]
)
def change_mlconfname(confname):
    global old_mlconfname
    global old_options

    confname_changed = old_mlconfname != confname
    old_mlconfname = confname

    if confname_changed:
        if confname is not None:
            mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
            mconf = mconf_manager.get_by_name(confname)
            q = table_mlmodels.get_get_dpids_by_modelconf_id_query(mconf.modelconf_id)
            dpids = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]
            print(f"The fetched dpids are: {dpids}")
            options = [{"label" : f"{entry}", "value" : f"{entry}"} for entry in dpids]
            old_options = options[:] 
        else:
            old_options = []
    print(f"The old options are: {old_options}")
    return old_options[:] #, old_options[:]

old_mlconfname = None
old_options = []
@app.callback(
    Output('dpids_for_training', 'options'), 
    [Input('modelconfname_id','value')]
)
def change_mlconfname(confname):
    global old_mlconfname
    global old_options

    confname_changed = old_mlconfname != confname
    old_mlconfname = confname

    if confname_changed:
        if confname is not None:
            mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
            mconf = mconf_manager.get_by_name(confname)
            q = table_mlmodels.get_get_dpids_by_modelconf_id_query(mconf.modelconf_id)
            dpids = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]
            print(f"The fetched dpids are: {dpids}")
            options = [{"label" : f"{entry}", "value" : f"{entry}"} for entry in dpids]
            old_options = options[:] 
        else:
            old_options = []
    print(f"The old options are: {old_options}")
    return old_options[:] 

# This callback is responsible for the creation of a new configuration
n_clicks_last = 0
@app.callback(
    Output("input_conf_name","value"),
    Output("modelconfname_id","options"),
        [Input("create_conf_button","n_clicks")],
        [State("input_conf_name","value")],
        [State("class_name","value")],
        [State('train-period-start-end-date','start_date')],
        [State('train-period-start-end-date','end_date')],
)
def create_new_configuration(n_clicks, conf_name, mlclass, stdate, endate):
    global n_clicks_last
    global mlconfnames

    if n_clicks is None:
        n_clicks = 0

    create_button_pressed = n_clicks > n_clicks_last
    n_clicks_last = n_clicks

    if not create_button_pressed:
        return None

    mconf = MLModelConf()
    mconf_manager = MLModelsConfManager(rpccurrml,table_mlmodelsconf)
    
    mconf.name = conf_name
    mconf.mlclass = mlclass

    mconf.output_cols = table_training.imon

    if mconf.mlclass == 'GLM_V4':
        mconf.input_cols = ",".join([table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    elif mconf.mlclass == 'AUTOENC_V1' or mconf.mlclass == 'AUTOENC_V2' or mconf.mlclass == 'AUTOENC_V3':
        mconf.input_cols = ",".join(table_autoencoderData.dpids)
        mconf.output_cols = ",".join(table_autoencoderData.dpids)
    else:
        mconf.input_cols = ",".join([table_training.vmon,table_training.uxcP,table_training.uxcT,table_training.uxcRH,table_training.instant_lumi,table_training.integrated_lumi,table_training.hours_without_lumi])
    
    mconf.train_from = stdate
    mconf.train_to = endate
    
    mconf.test_from = stdate
    mconf.test_to = endate

    mconf_id = mconf_manager.RegisterMLModelConf(mconf)

    if mconf_id == -1:
        print("modelconf already registered...")
    elif mconf_id == -2:
        print('modelconf registration failed...')
    else:
        print(f"The model configuration registered successfully with modelconf_id {mconf_id}")

    q = table_mlmodelsconf.get_select_modelconfnames_query()
    mlconfnames = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]
    theoptions = [{"label" : entry, "value" : entry} for entry in mlconfnames ]
    print(f"The retrieved confs are: {mlconfnames[:]}")
    return "", theoptions

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# The next set of similar callbacks is responsible for the behavior of buttons preceding dropdown menus or 
# other elements; the callbacks control 'collapse' elements for all pages of the app

@app.callback(
    Output("train_period_collapse", "is_open"),
    [Input("train_period_button", "n_clicks")],
    [State("train_period_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("reg_new_model_class_collapse", "is_open"),
    [Input("class_button", "n_clicks")],
    [State("reg_new_model_class_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("reg_new_conf_name_collapse", "is_open"),
    [Input("reg_button", "n_clicks")],
    [State("reg_new_conf_name_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

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

@app.callback(
    Output("select_train_dpid_collapse", "is_open"),
    [Input("dpid_for_training_button", "n_clicks")],
    [State("select_train_dpid_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("details_collapse", "is_open"),
    [Input("show_train_details", "n_clicks")],
    [State("details_collapse", "is_open")],
)
def toggle_modelconfname_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# The next two callbacks are for the predict page
@app.callback(
    Output("all-models-collapse", "is_open"),
    [Input("select-model-button", "n_clicks")],
    [State("all-models-collapse", "is_open")]
)
def toggle_allmodels_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("active-models-collapse", "is_open"),
    [Input("active-models-button", "n_clicks")],
    [State("active-models-collapse", "is_open")]
)
def toggle_activemodels_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

#The next two callbacks are combined together
n_clicks_last = 0
@app.callback(
    Output("confirm_delete_dialog", "displayed"),
    [Input("delete_conf_button","n_clicks")]
)
def display_confirm_window(n_clicks):
    global n_clicks_last
    if n_clicks is None:
        n_clicks = 0
    print(f"n_clicks has a value of {n_clicks}")

    button_pressed = n_clicks > n_clicks_last
    n_clicks_last = n_clicks

    if button_pressed:
        return True
    return False

submit_n_clicks_last = 0
@app.callback(
    Output("output-provider", "children"),
    #Output("modelconfname_id", "options"),
    [Input("confirm_delete_dialog","submit_n_clicks")],
    [State("modelconfname_id", "value")]
)
def perform_action(submit_n_clicks, config_name):
    #global mlconfs
    global submit_n_clicks_last
    if submit_n_clicks is None:
        submit_n_clicks = 0
    print(f"The value of submit_n_clicks is: {submit_n_clicks}")
    
    confirmation_given = submit_n_clicks > submit_n_clicks_last
    submit_n_clicks_last = submit_n_clicks

    if  confirmation_given:
        #return 'It wasnt easy but hey {}'.format(submit_n_clicks)
        query = table_mlmodelsconf.get_delete_conf_by_name_query(config_name)
        print(query)
        rpccurrml.execute_commit_query_self(query)
        #q = table_mlmodelsconf.get_select_modelconfnames_query()                     #Wasn't able to automaticaly update the modelconf_name list before refreshing the page
        #mlconfs = [res[0] for res in rpccurrml.fetchall_for_query_self(q)]
        #print(f"The retrieved modelconf_names are: {mlconfnames}")
        #theoptions = [{"label" : entry, "value" : entry} for entry in mlconfnames ]
        return f"The configuration {config_name} was deleted"  #, theoptions

##########################################

n_clicks_old = 0
@app.callback(
    Output('hidden-div', 'children'),
    Input('train_button', 'n_clicks'),
    State('modelconfname_id', 'value'),
    State('dpids_for_training', 'value')
)
def perform_training_for_dpid(n_clicks, confname, dpid):
    global n_clicks_old
    if n_clicks is None:
        n_clicks = 0
    train_button_pressed = n_clicks > n_clicks_old
    n_clicks_old = n_clicks

    if train_button_pressed:
        conf_name=confname
        dpid = dpid[0]
        flag = 56
        mojopath="."
        modelpath="."
        print(f"conf_name {conf_name}")
        print(f"dpid {dpid}")
        print(f"flag {flag}")

        RPCHVChannelModel.init(model_conf_name=conf_name,mojofiles_path=mojopath,mlmodels_path=modelpath)

        if "AUTOENC" in RPCHVChannelModel.mconf.mlclass:
            model_ids,dpids = RPCHVChannelModel.train_and_register_autoencoder(True)
            for kv in len(model_ids):
                if model_ids[kv] < 0:
                    print(f"a model configuration with name {conf_name} already registered for DPID {dpids[kv]}...")
                else:
                    print(f"An ML model with model_id {model_ids[kv]} with configuration name {conf_name} for DPID {dpids[kv]} was registered successfully...")
        else:
            h2o.init()
            model_id = RPCHVChannelModel.train_and_register_for_dpid(dpid,flag,True)

            if model_id < 0:
                notification = f"a model configuration with name {conf_name} already registered for DPID {dpid}..."
                print(f"a model configuration with name {conf_name} already registered for DPID {dpid}...")
            else:
                notification = f"An ML model with model_id {model_id} with configuration name {conf_name} for DPID {dpid} was registered successfully..." 
                print(f"An ML model with model_id {model_id} with configuration name {conf_name} for DPID {dpid} was registered successfully...")
        return notification
#

@app.callback(
    Output('hidden-div2', 'children'),
    [Input('interval1', 'n_intervals')])
def update_interval(n):
    #sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    orig_stdout = sys.stdout
    f = open('out.txt', 'a')
    sys.stdout = f
    #print (f'Seconds counted {str(n)}')
    sys.stdout = orig_stdout
    f.close()
    return f'Intervals Passed: {str(n)}'

@app.callback(Output('console-out', 'srcDoc'),
    [Input('interval2', 'n_intervals')])
def update_output(n):
    file = open('out.txt', 'r')
    data=''
    lines = file.readlines()
    if lines.__len__()<=20:
        last_lines=lines
    else:
        last_lines = lines[-20:]
    for line in last_lines:
        data=data+line + '<BR>'
    file.close()
    return data

# ++++++++++++++++++++++++++++++++++++ Prediction page callbacks ++++++++++++++++++++++++++++++++++ #
#TODO: Add a hidden div as generic output; specify what the model list contains (model_ids?, combination of conf_id and dpid?)
@app.callback(
    Output("pred-hidden-div", "children"),
    [Input("perform-the-prediction", "n_clicks")],
    [State("pred-alternative", "value"),
     State("modelconfname_id", "value"),
     State("all-models-dropdown", "value"),
     State("pred-period-start-end-date", "start_date"),
     State("pred-period-start-end-date", "end_date")]
)
def prediction_for_selected_models(n_clicks, predict_alternative, conf_name, modelslist, sdate, edate):
    if predict_alternative == 'selectedmodels':
        for dpid in modelslist:
            #modelslist actually contains dpids atm
            q = table_mlmodelsconf.get_select_modelconfid_by_modelconfname_query(conf_name)
            confid = rpccurrml.fetchall_for_query_self(q)[0][0]
            q = table_mlmodels.get_get_model_id_for_confname_and_dpid_query(confid, dpid)
            model = rpccurrml.fetchall_for_query_self(q)[0][0]
            predict_for_hv_channel_method.predict(model, 56, sdate, edate)
            mesg = f"The model is {model}"
        return mesg
    elif predict_alternative == 'activemodels':
        perform_prediction(sdate, edate)
        mesg = f"Prediction for all active models for period {sdate} to {edate}"
        return mesg

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
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
    
    extractor_pred_curr_table = DataManager.Extractor_MySql(table_predicted_current.tablename, rpccurrml)
    extractor_pred_curr_table.set_column_name_list(["predicted_for", "predicted_value", "measured_value"])
    extractor_pred_curr_table.set_timestamp_col('predicted_for')
    extractor_pred_curr_table.set_time_widow(start_date_last,end_date_last)
    extractor_pred_curr_table.set_model_id_col_name()
    extractor_pred_curr_table.set_dpid_col_name('dpid')
    
    mlinput = None
    if 'AUTOENC' in mconf.mlclass:
        pass
    else:
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
        if type(model) == 'NoneType':
            print("model with conf {mconf.modelconf_id} for dpid {dpid} not found")
            continue
        pf = None
        if 'AUTOENC' in mconf.mlclass:
            extractor_pred_curr_table.set_model_id(model.model_id)
            extractor_pred_curr_table.set_DPID(dpid)
            query = extractor_pred_curr_table.get_data_by_model_id_query()
            print(query)
            pred_data = rpccurrml.fetchall_for_query_self(query)

            if len(pred_data) == 0:
                print("**************************************")
                print("* ERROR: no prediction data found... *")
                print("**************************************")
                continue
            time_format='%Y-%m-%d %H:%M:%S'
            pf = pd.DataFrame( [[ij for ij in i] for i in pred_data] )
            pf.rename(columns={0:table_training.change_date,1:'predicted',2:table_training.imon}, inplace=True)
            pf[table_training.change_date] = pd.to_datetime(pf[table_training.change_date], format=time_format)
            
        else:
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

        if pf is not None:
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

    fig_diff.update_layout(title='<b>Model deviation running average</b>',
                   yaxis_title='<b>IMON-prediciton [&mu;A]</b>')
    
    # fig_diff_histo.update_layout(barmode='stack')

    fig_diff_histo.update_layout(title='<b>Model deviation distribution</b>',
                   xaxis_title='<b>IMON-prediciton [&mu;A]</b>')
    return fig,fig_diff,fig_diff_histo

if __name__ == "__main__":
    app.run_server(debug=False,port=8050,host='192.168.2.192')
