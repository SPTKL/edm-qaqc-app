import json 
import requests
import dash_core_components as dcc
import dash_html_components as html
from .url import base_url

col_order=['borough', 'block', 'lot', 'cd', 'ct2010', 'cb2010',
       'schooldist', 'council', 'zipcode', 'firecomp', 'policeprct',
       'healtharea', 'sanitboro', 'sanitsub', 'address', 'zonedist1',
       'zonedist2', 'zonedist3', 'zonedist4', 'overlay1', 'overlay2',
       'spdist1', 'spdist2', 'spdist3', 'ltdheight', 'splitzone', 'bldgclass',
       'landuse', 'easements', 'ownertype', 'ownername', 'lotarea', 'bldgarea',
       'comarea', 'resarea', 'officearea', 'retailarea', 'garagearea',
       'strgearea', 'factryarea', 'otherarea', 'areasource', 'numbldgs',
       'numfloors', 'unitsres', 'unitstotal', 'lotfront', 'lotdepth',
       'bldgfront', 'bldgdepth', 'ext', 'proxcode', 'irrlotcode', 'lottype',
       'bsmtcode', 'assessland', 'assesstot', 'exempttot', 'yearbuilt',
       'yearalter1', 'yearalter2', 'histdist', 'landmark', 'builtfar',
       'residfar', 'commfar', 'facilfar', 'borocode', 'bbl', 'condono',
       'tract2010', 'xcoord', 'ycoord', 'zonemap', 'zmcode', 'sanborn',
       'taxmap', 'edesignum', 'appbbl', 'appdate', 'plutomapid', 'version',
       'sanitdistrict', 'healthcenterdistrict', 'firm07_flag', 'pfirm15_flag']

def make_null(v1, v2, v3, condo):
    v1 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({"v":v1, "condo":condo})).json()['result'][0]

    v2 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({'v':v2, "condo": condo})).json()['result'][0]
    
    v3 = requests.post(f'{base_url}/pluto-qaqc/null', 
            data=json.dumps({'v':v3, "condo": condo})).json()['result'][0] 

    def generate_graph(v1, v2):
        _v1 = v1['v']
        _v2 = v2['v']
        total1 = v1['total']
        total2 = v2['total']

        y = col_order
        x = []
        for i in y: 
            pct1 = v1[i]/total1
            pct2 = v2[i]/total2
            if pct2 != 0:
                x.append(round((pct1-pct2)/pct2, 4))
            else:
                x.append(None)
        return {'x': y, 
                'y': x, 'type': 
                'line', 'name': f'{_v1} - {_v2}', 
                'text': [f'count_in_{_v1} : {v1[i]}' for i in y]}

    v1v2 = generate_graph(v1, v2)
    v2v3 = generate_graph(v2, v3)

    return dcc.Graph(
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
                    'title': 'Null graph'
                }
            }
        )