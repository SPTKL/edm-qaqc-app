import dash_core_components as dcc
import dash_html_components as html
import requests
import json
from .url import base_url

versions = requests.get(f'{base_url}/pluto-qaqc/versions').json()['result']
versions_options = [{'label': i['table_name'], 'value': i['table_name']} for i in versions]

header = html.Header([
    html.Div([
        html.Div([
                html.Div([
                    html.Img(src='https://raw.githubusercontent.com/NYCPlanning/dcp-logo/master/dcp_logo_772.png',
                            alt="NYC Planning",
                            style={'max-height': '4.5rem'},
                            className='header-logo medium-margin-right medium-margin-bottom')
                ], className='cell medium-shrink'),
                html.Div([
                    html.Div([
                        html.H1(children='PLUTO QAQC', className='no-margin'),
                        html.P(children='EDM - Data Engineering', className='medium-margin-bottom')
                    ], id='title', className='no-margin')
                ], className='cell medium-auto'), 
                html.P([
                    html.A([
                        html.Img(src='/assets/GitHub-Mark-32px.png',
                            className='large-margin-top')
                    ], href='https://github.com/NYCPlanning/db-pluto')
                ],className='cell medium-shrink no-margin show-for-medium')
            ], className='grid-x text-center medium-text-left align-middle')
    ], className='grid-container')
], className='xlarge-padding-top large-padding-bottom bg-white-smoke')

body = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H6('select version:'),
                dcc.Dropdown(id='version',
                            options=versions_options,
                            value='20v1'),
                dcc.RadioItems(
                            options=[
                                {'label': 'Condo', 'value': 'TRUE'},
                                {'label': 'All', 'value': 'FALSE'}
                            ],
                            value='FALSE',
                            labelStyle={'display': 'inline-block'}, 
                            id='condo'), 
                html.Div(id='version_info'),
            ],id='control', className='sticky large-padding-top large-padding-bottom is-anchored is-at-top')
        ], className='medium-4 large-3 cell medium-order-1 sticky-container'), 
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Mismatch Analysis',
                        children=[html.Div(id='mismatch-area')]),
                dcc.Tab(label='Null Analysis', 
                        children=[html.Div(id='null-area')]),
                dcc.Tab(label='Aggregate Analysis', 
                        children=[html.Div(id='aggregate-area')]),
            ])
        ], id='graphs', className='medium-8 large-9 cell medium-order-2 large-padding-top large-padding-bottom')
    ], className='grid-x grid-margin-x')
    ], className='grid-container', id='main-content')

layout = html.Div(children=[
    header,
    body
])