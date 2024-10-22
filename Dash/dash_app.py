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
    
df['new_dt'] = pd.to_datetime(df['dt']).dt.strftime('%d-%m-%Y')
grouped = df[['new_dt','Id','SalePrice']].groupby(['new_dt']).agg({'Id':['count','nunique'],'SalePrice':'sum'}).reset_index()
grouped.columns = ['_'.join(col) for col in grouped.columns] 

fig1 = px.line(grouped, x='new_dt_', y='SalePrice_sum')
fig2 = px.line(grouped, x='new_dt_', y='Id_count')
fig3 = px.line(grouped, x='new_dt_', y='Id_nunique')


app = Dash()

app.layout = html.Div([
    html.H1('Data Quality Observation', style={'textAlign':'center'}),
    
    
    html.Div([
    dcc.Graph(id='Sum_Sales',figure = fig1,style={'width':'30%'}),
    dcc.Graph(id='Count_id',figure = fig2,style={'width':'30%'}),
    dcc.Graph(id='Count_distinct_id',figure = fig3,style={'width':'30%'}),
    ],
    style = {'display':'flex','flex-direction':'row','justify-content':'space-around','gap':'40px'}),

    html.H1('Model Quality Observation', style={'textAlign':'center'}),

    dcc.Interval(
        id = 'Interval',
        interval=10000,
        n_intervals = 0
                 )

    
    ])

@app.callback(
        Output('Sum_Sales','figure'),
        Output('Count_id','figure'),
        Output('Count_distinct_id','figure'),
        Input('Interval','n_intervals')
)
   
  
def update_graph(_):

    engine = create_engine(conn_string)

    with engine.connect() as conn:
        
        query = f"SELECT * FROM {general_table}"
        
        df = pd.read_sql(query, engine)
    
    df['new_dt'] = pd.to_datetime(df['dt']).dt.strftime('%d-%m-%Y')
    grouped = df[['new_dt','Id','SalePrice']].groupby(['new_dt']).agg({'Id':['count','nunique'],'SalePrice':'sum'}).reset_index()
    grouped.columns = ['_'.join(col) for col in grouped.columns] 

    fig1 = px.line(grouped, x='new_dt_', y='SalePrice_sum')
    fig2 = px.line(grouped, x='new_dt_', y='Id_count')
    fig3 = px.line(grouped, x='new_dt_', y='Id_nunique')

    return fig1,fig2,fig3

if __name__ == '__main__':
    app.run(debug=True)

