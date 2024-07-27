from dash import Dash, html, dcc, callback, Output, Input, dash_table, State, exceptions
import dash_bootstrap_components as dbc
from flask import Flask
#from asgiref.wsgi import WsgiToAsgi
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

dfc = pd.read_csv('media.csv', sep=';')
dfc = dfc.set_index(dfc.iloc[:,0])
dfc = dfc.drop(dfc.columns[0], axis=1)
col = dfc.columns
col = col.sort_values()
dfc = dfc[col]
dfc1 = dfc.iloc[:,:13]
dfc2 = dfc.iloc[:,13:]

fig1 = go.Figure(data=[
    go.Bar(name='Anies', x=dfc1.columns, y=dfc1.values[0],marker_color='rgb(41,128,185)'), #text=str(dfc.values[0]*100)+'%',textposition='auto'),
    go.Bar(name='Prabowo', x=dfc1.columns, y=dfc1.values[1],marker_color='rgb(241,196,15)'), #text=str(dfc.values[1]*100)+'%',textposition='auto'),
    go.Bar(name='Megawati', x=dfc1.columns, y=dfc1.values[2],marker_color='rgb(192,57,43)') #text=str(dfc.values[2]*100)+'%',textposition='auto')
])
fig1.update_layout(barmode='stack')

fig2 = go.Figure(data=[
    go.Bar(name='Anies', x=dfc2.columns, y=dfc2.values[0],marker_color='rgb(41,128,185)'), #text=str(dfc.values[0]*100)+'%',textposition='auto'),
    go.Bar(name='Prabowo', x=dfc2.columns, y=dfc2.values[1],marker_color='rgb(241,196,15)'), #text=str(dfc.values[1]*100)+'%',textposition='auto'),
    go.Bar(name='Megawati', x=dfc2.columns, y=dfc2.values[2],marker_color='rgb(192,57,43)') #text=str(dfc.values[2]*100)+'%',textposition='auto')
])
fig2.update_layout(barmode='stack')

fig3 = go.Figure(data=[
    go.Bar(name='Ridwan Kamil', x=dfc1.columns, y=dfc1.values[3],marker_color='rgb( 22,160,133)'), #text=str(dfc.values[0]*100)+'%',textposition='auto'),
    go.Bar(name='Gibran', x=dfc1.columns, y=dfc1.values[4],marker_color='rgb(211,84,0)'), #text=str(dfc.values[1]*100)+'%',textposition='auto'),
    go.Bar(name='Kaesang', x=dfc1.columns, y=dfc1.values[5],marker_color='rgb(142,68,173)') #text=str(dfc.values[2]*100)+'%',textposition='auto')
])
fig3.update_layout(barmode='stack')

fig4 = go.Figure(data=[
    go.Bar(name='Ridwan Kamil', x=dfc2.columns, y=dfc2.values[3],marker_color='rgb( 22,160,133)'), #text=str(dfc.values[0]*100)+'%',textposition='auto'),
    go.Bar(name='Gibran', x=dfc2.columns, y=dfc2.values[4],marker_color='rgb(211,84,0)'), #text=str(dfc.values[1]*100)+'%',textposition='auto'),
    go.Bar(name='Kaesang', x=dfc2.columns, y=dfc2.values[5],marker_color='rgb(142,68,173)') #text=str(dfc.values[2]*100)+'%',textposition='auto')
])
fig4.update_layout(barmode='stack')

place_holder = None
df_filter = pd.DataFrame(
    {
        "tier": [place_holder],
        "thumbnail1": [place_holder]
    }
)

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = Flask(__name__)

#app = Dash(__name__, external_stylesheets=external_stylesheets)#requests_pathname_prefix='/dash/'
app = Dash(__name__, server=server,requests_pathname_prefix='/', external_stylesheets=[dbc.themes.LITERA], assets_folder='assets')#BOOTSTRAP LUX FLATLY LITERA
app.title = 'Berita'
app._favicon = ("Constellation Logo.ico")

bgcol = 'rgb(255, 255, 255)'
#server = Flask(__name__) # define flask app.server
#server = FastAPI() #uvicorn
#server = app.server #gunicorn

app.layout = html.Div([dbc.Container([
    #html.H2('Teleport News Aggregator',className='text-center'),
    html.Div(html.Center(html.Img(src='https://raw.githubusercontent.com/muhammad5/table/main/assets/title.png',
                     style={'height':'40%', 'width':'40%','display': 'inline-block'}))),
    dbc.Label('News Feed'),
    dbc.Row([dbc.Col(dcc.Dropdown([''], None, id='data-dropdown2', placeholder="Select a tier", disabled=True)),
            dbc.Col(dcc.Dropdown(df['thumbnail1'].unique(), None, id='data-dropdown1', 
                                 placeholder="Select a thumbnail",optionHeight=35))]),
    dash_table.DataTable(data=df.to_dict('records'),columns=[{"name": c, "id": c, 'presentation': 'markdown'} for c in df.columns if c not in ['thumbnail1','logo']], id='table-data',
                         fixed_rows={'headers': True},
                         page_size=75,
                         cell_selectable = False,
                         style_table={'height': '750px', 'overflowY': 'auto','overflowX': 'scroll'},
                         style_cell={'minWidth': 55, 'width': 55, 'maxWidth': 95,
                                     'overflow': 'hidden','textOverflow': 'ellipsis',
                                     'textAlign': 'left','backgroundColor':bgcol},
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
    html.Br(),
    html.H4('Media Coverage Distribution',className='text-center'),
    dbc.Row([dbc.Col(dcc.Graph(figure=fig1)),dbc.Col(dcc.Graph(figure=fig2))]),
    dbc.Row([dbc.Col(dcc.Graph(figure=fig3)),dbc.Col(dcc.Graph(figure=fig4))]),
    #html.Div(id="table-output")
    #dbc.Alert(id='table_out'),
    ],style={'backgroundColor':bgcol})
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

#@app.get("/")
'''
def read_main():
    return {
        "routes": [
            {"method": "GET", "path": "/", "summary": "Landing"},
            {"method": "GET", "path": "/status", "summary": "App status"},
            {"method": "GET", "path": "/dash", "summary": "Sub-mounted Dash application"},
        ]
    }
'''
@app.get("/status")
def get_status():
    return {"status": "ok"}

app.mount('/',WSGIMiddleware(dash_app.server))
#app = WsgiToAsgi(app)

if __name__ == '__main__':
    #uvicorn.run(app, host="0.0.0.0")
    app.run_server(debug=False,host="0.0.0.0")
    #app.run_server(debug=False)
    #serve(app.server,host="0.0.0.0") #waitress
    #http_server = WSGIServer('0.0.0.0', 8080, app)
    #http_server.serve_forever()
#app.run_server(debug=False)

#subprocess.run('waitress-serve --listen=0.0.0.0:8080 app:app.server')
#subprocess.run(['waitress-serve','--listen=0.0.0.0:8080','app:app.server'])
