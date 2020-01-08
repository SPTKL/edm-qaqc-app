# -*- coding: utf-8 -*-
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

app.layout = html.Div(children=[
    html.H1(children='PLUTO QAQC'),
    html.H6('version1'),
    dcc.Dropdown(id='v1',
                options=versions_options,
                value='19v1'),
    html.H6('version2'),
    dcc.Dropdown(id='v2',
                options=versions_options,
                value='19v2'),
    html.H6('version3'),
    dcc.Dropdown(id='v3',
                options=versions_options,
                value='19v2_w_corrections'),
    dcc.RadioItems(
                options=[
                    {'label': 'Condo', 'value': 'TRUE'},
                    {'label': 'All', 'value': 'FALSE'}
                ],
                value='TRUE',
                labelStyle={'display': 'inline-block'}, 
                id='condo'
            ), 
    html.Div(id='mismatch-area'),
    html.Div(id='null-area'),
    html.Div(id='aggregate-area')
])

@app.callback(Output('mismatch-area', 'children'),
              [Input('v1', 'value'),
              Input('v2', 'value'),
              Input('v3', 'value'),
              Input('condo', 'value')])
def create_mismatch(v1, v2, v3, condo):
    v1v2 = requests.post(f'{base_url}/pluto-qaqc/mismatch', 
            data=json.dumps({
                "v1":f"{v1}", "v2": f"{v2}", 
                "condo":f"{condo}", "cached":"FALSE"})).json()['result'][0]

    v2v3 = requests.post(f'{base_url}/pluto-qaqc/mismatch', 
            data=json.dumps({
                "v1":f"{v2}", "v2": f"{v3}", 
                "condo":f"{condo}", "cached":"FALSE"})).json()['result'][0]
    
    def generate_graph(r, name):
        r.pop('pair')
        r.pop('condo')
        total = r.pop('total')
        y = list(r.values())
        x = list(r.keys())
        return {'x': x, 'y': y, 'type': 'line', 'name': name}

    _v1v2 = generate_graph(v1v2, v1v2['pair'])
    _v2v3 = generate_graph(v2v3, v2v3['pair'])

    return dcc.Graph(
            figure={
                'data': [
                    _v1v2,
                    _v2v3,
                ],
                'layout': {
                    'title': 'Mismatch graph'
                }
            }
        )

@app.callback(Output('aggregate-area', 'children'),
              [Input('v1', 'value'),
              Input('v2', 'value'),
              Input('v3', 'value'),
              Input('condo', 'value')])
def create_null(v1, v2, v3, condo):
    v1 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({"v":v2, "condo":condo , "cached":"FALSE"})).json()['result'][0]

    v2 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({'v':v2, "condo": condo, "cached":"FALSE"})).json()['result'][0]
    
    v3 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({'v':v3, "condo": condo, "cached":"FALSE"})).json()['result'][0] 

    def generate_graph(r):
        v = r.pop('v')
        r.pop('condo')
        total = r.pop('total')
        y = list(r.values())
        x = list(r.keys())
        return {'x': x, 'y': y, 'type': 'line', 'name': v}

    _v1 = generate_graph(v1)
    _v2 = generate_graph(v2)
    _v3 = generate_graph(v3)

    return dcc.Graph(
            figure={
                'data': [
                    _v1,
                    _v2,
                    _v3,
                ],
                'layout': {
                    'title': 'Null graph'
                }
            }
        )


if __name__ == '__main__':
    app.run_server(debug=True)