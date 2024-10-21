from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import configparser
from pathlib import Path
from sqlalchemy import create_engine  
import datetime

config_path = Path(__file__).resolve().parent.parent  /'Tests' / 'config.ini'

config = configparser.ConfigParser()
config.read(config_path)
conn_string = config.get('DATABASE', 'connection_url')

#Основная таблица

general_table = 'house_prices_fin'

engine = create_engine(conn_string)

with engine.connect() as conn:
        
    query = f"SELECT * FROM {general_table}"
        
    df = pd.read_sql(query, engine)

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    '''
    dcc.Dropdown(df['Id'].unique(), 'Canada', id='dropdown-selection'),
    dcc.Dropdown(df['Id'].unique(), 'Canada', id='dropdown-selection'),
    '''
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df['Id']==value]
    df['new_dt'] = datetime.datetime.df['dt'].date()
    
    return px.histogram(df, x='new_dt', y='prediction')

if __name__ == '__main__':
    app.run(debug=True)
