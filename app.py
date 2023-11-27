from dash import Dash, html, dcc, callback, Output, Input, dash_table, State, exceptions
import dash_bootstrap_components as dbc
from flask import Flask
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn
#from waitress import serve
#from gevent.pywsgi import WSGIServer
#import subprocess
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('berita.csv', sep=';', nrows=50000)
df['to'] = df['to'].apply(lambda x: "<a href={} target='_blank'>link</a>".format(x))
df['thumbnail1'] = df['thumbnail']
#df['thumbnail'] = df['logo'].apply(lambda x: "<img src={} width='100' height='50' />".format(x))
#df['thumbnail'] = df['thumbnail'].apply(lambda x: "<img src='assets/{}.PNG' width='100' height='30' />".format(x))
df['thumbnail'] = df['thumbnail'].apply(lambda x: "<img src='https://raw.githubusercontent.com/muhammad5/table/main/assets/{}.png' width='100' height='30' />".format(x))

place_holder = None
df_filter = pd.DataFrame(
    {
        "tier": [place_holder],
        "thumbnail1": [place_holder]
    }
)

external_stylesheets = [dbc.themes.BOOTSTRAP]


#app = Dash(__name__, external_stylesheets=external_stylesheets)
app = Dash(__name__, requests_pathname_prefix='/dash/', external_stylesheets=[dbc.themes.LITERA], assets_folder='assets')#BOOTSTRAP LUX FLATLY LITERA
app.title = 'Berita'
app._favicon = ("Constellation Logo.ico")

server = Flask(__name__) # define flask app.server
#server = FastAPI() #uvicorn
#server = app.server #gunicorn

app.layout =dbc.Container([
    dbc.Label('News Feed'),
    dbc.Row([dbc.Col(dcc.Dropdown([''], None, id='data-dropdown2', placeholder="Select a tier", disabled=True)),
            dbc.Col(dcc.Dropdown(df['thumbnail1'].unique(), None, id='data-dropdown1', 
                                 placeholder="Select a thumbnail",optionHeight=35))]),
    dash_table.DataTable(data=df.to_dict('records'),columns=[{"name": c, "id": c, 'presentation': 'markdown'} for c in df.columns if c not in ['thumbnail1','logo']], id='table-data',
                         fixed_rows={'headers': True},
                         page_size=75,
                         style_table={'height': '750px', 'overflowY': 'auto','overflowX': 'scroll'},
                         style_cell={'minWidth': 55, 'width': 55, 'maxWidth': 95,
                                     'overflow': 'hidden','textOverflow': 'ellipsis',
                                     'textAlign': 'left'},
                         style_data={'whiteSpace': 'normal',
                                     'height': 'auto',
                                     'lineHeight': '20px'},
                         style_cell_conditional=[
                             {'if': {'column_id': 'title'},
                              'width': '50%'},
                              {'if': {'column_id': 'to'},
                               'width': '5%'},
                               {'if': {'column_id': 'thumbnail'},
                               'width': '10%'},
                                {'if': {'column_id': 'tier'},
                               'width': '10%'}
                        ],
                        #css=[{"selector": "tr:first-child", "rule": "display: none",},],
                        
                        
                              
                        #tooltip_data=[{column: {'value': str(value), 'type': 'markdown'} 
                        #               for column, value in row.items()} 
                        #               for row in df.to_dict('records')],
                        #tooltip_duration=None,
                        filter_action="native",
                        markdown_options={"html": True},
                        ),
    html.Div(id="table-output")
    #dbc.Alert(id='table_out'),
])

#@callback(Output('table_out', 'children'), Input('table-data', 'active_cell'))
#def update_graph(active_cell):
#    return str(active_cell) if active_cell else "Click the table"

# Callback for updating table based on dropdown selection
@app.callback(
    Output("data-dropdown2", "options"),
    Output("table-data", "data"),
    Output('data-dropdown2',"disabled"),
    Output("data-dropdown2", "value"),
    [Input("data-dropdown1", "value"),
     Input("data-dropdown2", "value")],
     prevent_initial_call=True)
    #[State("data-dropdown", "value"), State("table-data", "data")],)
def update_table(value1,value2):
    data = df.copy()
    tiers = ['']
    tier = None
    status = True
    thumbs = data.thumbnail1.unique()
    
    if value1 is not None:
        data = data[data.astype(str)['thumbnail1'] == value1]
        tiers = data.tier.unique()
        status = False
    if value2 is not None and value1 is not None:
        data = data[data.astype(str)['tier'] == value2]
        tier = value2

    return tiers, data.to_dict("records"), status, tier

dash_app = app
app = FastAPI()
app.mount('/dash',WSGIMiddleware(dash_app.server))

if __name__ == '__main__':
    uvicorn.run(app, port=1000)
    #app.run_server(debug=False,host="0.0.0.0")
    #app.run_server(debug=False)
    #serve(app.server,host="0.0.0.0") #waitress
    #http_server = WSGIServer('0.0.0.0', 8080, app)
    #http_server.serve_forever()
#app.run_server(debug=False)

#subprocess.run('waitress-serve --listen=0.0.0.0:8080 app:app.server')
#subprocess.run(['waitress-serve','--listen=0.0.0.0:8080','app:app.server'])
