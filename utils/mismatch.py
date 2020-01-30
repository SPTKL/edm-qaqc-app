import json 
import requests
import dash_core_components as dcc
import dash_html_components as html
from .url import base_url

finance_columns = ['assessland', 'assesstot', 'exempttot', 
                   'residfar', 'commfar', 'facilfar', 
                   'taxmap', 'appbbl', 'appdate']

area_columns = ['lotarea', 'bldgarea', 'builtfar', 'comarea', 'resarea', 
                 'officearea', 'retailarea', 'garagearea', 'strgearea', 
                 'factryarea', 'otherarea', 'areasource']

zoning_columns = ['zonedist1', 'zonedist2', 'zonedist3', 'zonedist4', 
                  'overlay1', 'overlay2', 'spdist1', 'spdist2', 'spdist3', 
                  'ltdheight', 'splitzone', 'zonemap', 'zmcode', 'edesignum']

geo_columns = ['cd', 'ct2010', 'cb2010', 'schooldist',
               'council', 'zipcode', 'firecomp', 'policeprct', 
               'healtharea', 'sanitboro', 'sanitsub', 'address',
               'borocode', 'bbl', 'tract2010', 'xcoord', 'ycoord', 
               'sanborn', 'edesignum', 'sanitdistrict', 
               'healthcenterdistrict', 'histdist', 'firm07_flag', 'pfirm15_flag']

bldg_columns = ['bldgclass', 'landuse', 'easements', 'ownertype', 
                'ownername', 'numbldgs', 'numfloors', 'unitsres', 
                'unitstotal', 'lotfront', 'lotdepth', 'bldgfront', 
                'bldgdepth', 'ext', 'proxcode', 'irrlotcode', 
                'lottype', 'bsmtcode', 'yearbuilt', 'yearalter1',
                'yearalter2', 'landmark', 'condono']

other_columns = ['plutomapid', 'dcasdate', 'zoningdate', 'landmkdate',
                 'basempdate', 'masdate', 'polidate', 'edesigdate']

def make_mismatch(v1, v2, v3, condo):
    v1v2 = requests.post(f'{base_url}/pluto-qaqc/mismatch', 
            data=json.dumps({
                "v1":f"{v1}", "v2": f"{v2}", 
                "condo":f"{condo}"})).json()['result'][0]

    v2v3 = requests.post(f'{base_url}/pluto-qaqc/mismatch', 
            data=json.dumps({
                "v1":f"{v2}", "v2": f"{v3}", 
                "condo":f"{condo}"})).json()['result'][0]
    v1v2_total = v1v2['total']
    v2v3_total = v2v3['total']
    a = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, finance_columns)
    b = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, area_columns)
    c = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, zoning_columns)
    d = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, geo_columns)
    e = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, bldg_columns)
    f = generate_graph(v1v2, v2v3, v1v2_total, v2v3_total, other_columns)

    config={
        'displaylogo':False,
        'displayModeBar':False
        }

    return html.Div([
       dcc.Graph(
            config=config,
                figure={
                    'data': a,
                    'layout': {'title': f'Mismatch graph -- finance'}
                    }
                ), 
        dcc.Graph(
            config=config,
                figure={
                    'data': b,
                    'layout': {'title': f'Mismatch graph -- area'}
                    }
                ), 
        dcc.Graph(
            config=config,
                figure={
                    'data': c,
                    'layout': {'title': f'Mismatch graph -- zoning'}
                    }
                ), 
        dcc.Graph(
            config=config,
                figure={
                    'data': d,
                    'layout': {'title': f'Mismatch graph -- geo'}
                    }
                ),
        dcc.Graph(
            config=config,
                figure={
                    'data': e,
                    'layout': {'title': f'Mismatch graph -- building'}
                    }
                ), 
        dcc.Graph(
            config=config,
                figure={
                    'data': f,
                    'layout': {'title': f'Mismatch graph -- other'}
                    }
                )
    ])


def generate_graph(r1, r2, v1v2_total, v2v3_total, group):
    g1 = generate_graph_data(r1, v1v2_total, r1['pair'], group)
    g2 = generate_graph_data(r2, v2v3_total, r2['pair'], group)
    return [g1, g2]

def generate_graph_data(r, total, name, group):
    r = {key:value for (key,value) in r.items() if key in group}
    y = [r[i] for i in group]
    x = group
    text = [f'pct: {round(r[i]/total*100, 2)}' for i in group]
    return {'x': x, 'y': y, 'type': 'line', 'name': name, 'text': text}
