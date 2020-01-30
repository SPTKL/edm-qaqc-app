# -*- coding: utf-8 -*-
from utils.mismatch import make_mismatch
from utils.null import make_null
from utils.aggregate import make_aggregate
from utils.url import base_url
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

versions = requests.get(f'{base_url}/pluto-qaqc/versions').json()['result']
versions_options = [{'label': i['table_name'], 'value': i['table_name']} for i in versions]
versions_order = [
            '18v2_1', 
            '19v1', '19v2', 
            '20v1', '20v2', '20v3', '20v4',
            '20v5', '20v6', '20v7', '20v8',
            '20v9', '20v10', '20v11', '20v12']

app.layout = html.Div(children=[
    html.H1(children='PLUTO QAQC'),
    html.H6('select version:'),
    dcc.Dropdown(id='version',
                options=versions_options,
                value='20v1'),
    html.Div(id='version_info'),
    dcc.RadioItems(
                options=[
                    {'label': 'Condo', 'value': 'TRUE'},
                    {'label': 'All', 'value': 'FALSE'}
                ],
                value='FALSE',
                labelStyle={'display': 'inline-block'}, 
                id='condo'
            ), 
    html.Div(id='mismatch-area'),
    html.Div(id='null-area'),
    html.Div(id='aggregate-area')
])
@app.callback(Output('version_info', 'children'),
            [Input('version', 'value')])
def display_versions(version): 
    v1 = version
    v2 = versions_order[versions_order.index(version)-1]
    v3 = versions_order[versions_order.index(version)-2]
    return dcc.Markdown(f'''
            + __current__ version: {v1}
            + __previous__ version: {v2}
            + __previous before previous__ version: {v3}
    ''')

@app.callback(Output('mismatch-area', 'children'),
              [Input('version', 'value'),
              Input('condo', 'value')])
def create_mismatch(version, condo):
    v1 = version
    v2 = versions_order[versions_order.index(version)-1]
    v3 = versions_order[versions_order.index(version)-2]
    return make_mismatch(v1, v2, v3, condo)

@app.callback(Output('null-area', 'children'),
              [Input('version', 'value'),
              Input('condo', 'value')])
def create_null(version, condo):
    v1 = version
    v2 = versions_order[versions_order.index(version)-1]
    v3 = versions_order[versions_order.index(version)-2]
    return make_null(v1, v2, v3, condo)

@app.callback(Output('aggregate-area', 'children'),
              [Input('version', 'value'),
              Input('condo', 'value')])
def create_aggregate(version, condo):
    v1 = version
    v2 = versions_order[versions_order.index(version)-1]
    v3 = versions_order[versions_order.index(version)-2]
    return make_aggregate(v1, v2, v3, condo)

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)