# -*- coding: utf-8 -*-
from utils.mismatch import make_mismatch
from utils.null import make_null
from utils.aggregate import make_aggregate
from utils.url import base_url
from utils.style import style
from utils.layout import layout
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import dash
import json
import flask

external_stylesheets = [
    'https://nyc-planning-style-guide.netlify.com/assets/css/nyc-planning.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, 
                server=server,
                meta_tags=[
                    {'charset':'utf-8'},
                    {'http-equiv': 'X-UA-Compatible','content': 'IE=edge'},
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
                ],
                external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

versions_order = [
            '18v2_1', 
            '19v1', '19v2', 
            '20v1', '20v2', '20v3', '20v4',
            '20v5', '20v6', '20v7', '20v8',
            '20v9', '20v10', '20v11', '20v12']
app.title = 'EDM QAQC APP'
app.head = [
    html.Link(
        href='https://use.fontawesome.com/releases/v5.8.2/css/all.css',
        rel='stylesheet'
    ),(style)
]

app.layout = layout

@app.callback(
        Output('version', 'options'),
        [Input('none', 'children')]
    )
def refresh_options(none):
    versions = requests.get(f'{base_url}/pluto-qaqc/versions').json()['result']
    versions_options = [{'label': i['table_name'], 'value': i['table_name']} for i in versions]
    return versions_options

@app.callback(Output('version_info', 'children'),
            [Input('version', 'value')])
def display_versions(version): 
    v1 = version
    v2 = versions_order[versions_order.index(version)-1]
    v3 = versions_order[versions_order.index(version)-2]
    return dcc.Markdown(f'''
            + __current__: {v1}
            + __previous__: {v2}
            + __previous previous__: {v3}
    ''', className='no-bullet')

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
    app.run_server(debug=True, port=8050)