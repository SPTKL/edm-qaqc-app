import dash_core_components as dcc
import dash_html_components as html
import requests
import json
from .url import base_url

versions = requests.get(f'{base_url}/pluto-qaqc/versions').json()['result']
versions_options = [{'label': i['table_name'], 'value': i['table_name']} for i in versions]
versions_order = [
            '18v2_1', 
            '19v1', '19v2', 
            '20v1', '20v2', '20v3', '20v4',
            '20v5', '20v6', '20v7', '20v8',
            '20v9', '20v10', '20v11', '20v12']

header = html.Div([
    html.Div(className='three columns'),
    html.Div([
        html.Div([
            html.Img(
                src='https://github.com/NYCPlanning/dcp-logo/raw/master/dcp_logo_772.png',
                style={'width':'60%'})
        ])
    ],id='logo', className='two columns'), 
    html.Div([
        html.H1(children='PLUTO QAQC'),
    ], id='title', className='four columns'),
    html.Div(id='github')
], className='twelve columns', style={'display':'inline-block'})

body = html.Div([
    html.Div(className='three columns'),
    html.Div([
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
                    id='condo'), 
    ],id='control', className='two columns'), 
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Mismatch Analysis', 
                    children=[html.Div(id='mismatch-area')]),
            dcc.Tab(label='Null Analysis', 
                    children=[html.Div(id='null-area')]),
            dcc.Tab(label='Aggregate Analysis', 
                    children=[html.Div(id='aggregate-area')]),
        ])
    ], id='graphs', className='seven columns')
], className='twelve columns', style={'display':'inline-block'})

layout = html.Div(children=[
    header,
    body
])