import json 
import requests
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from .url import base_url

col_order=[ 'unitsres','lotarea','bldgarea','comarea',
            'resarea','officearea','retailarea','garagearea',
            'strgearea','factryarea','otherarea','assessland',
            'assesstot','exempttot','firm07_flag','pfirm15_flag']

def make_aggregate(v1, v2, v3, condo):
    v1 = requests.post(f'{base_url}/pluto-qaqc/aggregate', 
            data=json.dumps({"v":v1, "condo":condo})).json()['result'][0]

    v2 = requests.post(f'{base_url}/pluto-qaqc/aggregate', 
            data=json.dumps({'v':v2, "condo": condo})).json()['result'][0]
    
    v3 = requests.post(f'{base_url}/pluto-qaqc/aggregate', 
            data=json.dumps({'v':v3, "condo": condo})).json()['result'][0] 

    def generate_graph(v1, v2):
        _v1 = v1['v']
        _v2 = v2['v']

        y = col_order
        x = [v1[i]/v2[i]-1 for i in y]
        text = [f'pct: {round(i*100,2)}' for i in x]
        return {'x': y, 
                'y': x,
                'type': 'line', 
                'name': f'{_v1} - {_v2}',
                'text': text}
    v1v2 = generate_graph(v1, v2)
    v2v3 = generate_graph(v2, v3)

    return html.Div([
        dcc.Graph(
            config={
                'displaylogo':False,
                'showAxisRangeEntryBoxes': True
            },
            figure={
                'data': [
                    v1v2,
                    v2v3
                ],
                'layout': {
                    'title': 'Aggregate graph'
                }
            }
        ), 
        dash_table.DataTable(
            id='aggregate_table',
            columns=[{"name": i, "id": i} for i in col_order],
            data=[v1, v2, v3],
        )
    ])