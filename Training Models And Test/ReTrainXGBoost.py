import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
import configparser 
import datetime

from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import Metadata
import pickle
import sdv
import warnings

warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/config.ini')
conn_string = config.get('DATABASE', 'connection_url')

table = 'house_prices_fin'

# Загрузка сохраненного pipeline для числовых данных

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/num_pipe.pkl', 'rb') as f:
    num_pipe = pickle.load(f)  


#Загрузка сохраненного категориального импутера

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/cat_imputer.pkl', 'rb') as f:
    cat_imputer = pickle.load(f) 

#Загрузка сохраненного OrdinalEncoder

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/ordinal_encoder.pkl', 'rb') as f:
    ordinal_encoder = pickle.load(f)


query = f''' 

select * from {table}

'''

filepath = '/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/XGBRegressor.pkl'

def training(query,table):
    db = create_engine(conn_string)
    
    with db.connect() as conn:
        df = pd.read_sql(query, con=conn)
    
    for_drop = ['PoolQC', 'MiscFeature', 'Alley', 'Fence','Id','dt']
    
    df.drop(columns=for_drop,inplace=True)

    target = df[['SalePrice']]

    df.drop(columns=['SalePrice'],inplace=True)

    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.to_list()

    cat_cols = df.select_dtypes(include=['object']).columns.to_list()

    

    XGBRegressor.save(filepath)

if __name__ == "__main__":
    
    training(query,table)
