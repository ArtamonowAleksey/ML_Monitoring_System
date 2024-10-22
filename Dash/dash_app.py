from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import configparser
from pathlib import Path
from sqlalchemy import create_engine  
import datetime

from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error,r2_score

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

dt_list = []
mae_list = []
mape_list =[]
r2_list = []

for i in df['new_dt'].unique():
    train_df = df[df['new_dt']==i]
    mae = round(mean_absolute_error(train_df['SalePrice'],train_df['prediction']),2)
    mape = round(mean_absolute_percentage_error(train_df['SalePrice'],train_df['prediction']),2)
    r2 = round(r2_score(train_df['SalePrice'],train_df['prediction']),2)
    dt_list.append(i)
    mae_list.append(mae)
    mape_list.append(mape)
    r2_list.append(r2)
    
df_cols = pd.DataFrame({'dt': dt_list, 'mae': mae_list,'mape': mape_list,'R2':r2_list})

fig4 = px.line(df_cols, x='dt', y='mae',)
fig5 = px.line(df_cols, x='dt', y='mape')
fig6 = px.line(df_cols, x='dt', y='R2')




app = Dash()

app.layout = html.Div([
    html.H1('Data Manipulation', style={'textAlign':'center'}),
    html.label('Частота запуска Airflow Dag'),
    dcc.Slider(
        id = 'slidar-param1',
        min = 1,
        max = 60,
        step = 1,
        value = data['param1'],
        marks = {i:str(i) for i in range(1,101,10)}

    ),
    html.H1('Data Quality Observation', style={'textAlign':'center'}),
    
    
    html.Div([
    dcc.Graph(id='Sum_Sales',figure = fig1,style={'width':'30%'}),
    dcc.Graph(id='Count_id',figure = fig2,style={'width':'30%'}),
    dcc.Graph(id='Count_distinct_id',figure = fig3,style={'width':'30%'}),
    ],
    style = {'display':'flex','flex-direction':'row','justify-content':'space-around','gap':'40px'}),

    html.H1('Model Quality Observation', style={'textAlign':'center'}),

    html.Div([
    dcc.Graph(id='mae',figure = fig4,style={'width':'30%'}),
    dcc.Graph(id='mape',figure = fig5,style={'width':'30%'}),
    dcc.Graph(id='r2',figure = fig6,style={'width':'30%'}),
    ],
    style = {'display':'flex','flex-direction':'row','justify-content':'space-around','gap':'40px'}),

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
        Output('mae','figure'),
        Output('mape','figure'),
        Output('r2','figure'),
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


    dt_list = []
    mae_list = []
    mape_list =[]
    r2_list = []
    for i in df['new_dt'].unique():
        train_df = df[df['new_dt']==i]
        mae = round(mean_absolute_error(train_df['SalePrice'],train_df['prediction']),2)
        mape = round(mean_absolute_percentage_error(train_df['SalePrice'],train_df['prediction']),2)
        r2 = round(r2_score(train_df['SalePrice'],train_df['prediction']),2)
        dt_list.append(i)
        mae_list.append(mae)
        mape_list.append(mape)
        r2_list.append(r2)
    
    df_cols = pd.DataFrame({'dt': dt_list, 'mae': mae_list,'mape': mape_list,'R2':r2_list})

    fig4 = px.line(df_cols, x='dt', y='mae')
    fig5 = px.line(df_cols, x='dt', y='mape')
    fig6 = px.line(df_cols, x='dt', y='R2')

    return fig1,fig2,fig3,fig4,fig5,fig6

if __name__ == '__main__':
    app.run(debug=True)

