#Функция для предобработки данных

import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine  

import datetime
import pickle


config = configparser.ConfigParser()
config.read('/opt/airflow/scripts/config.ini')
conn_string = config.get('DATABASE', 'connection_url')

general_table = 'house_prices_fin'
new_data_from_generator = 'house_prices_generator'

n_rows=5
    
def generate(n_rows):

    engine = create_engine(conn_string)
    
    with engine.connect() as conn:
        query = f"SELECT * FROM {general_table}"
        df = pd.read_sql(query, engine)

    new_df = pd.DataFrame()
    for col in df.columns:
        if col == 'id':
            new_df[col] = np.random.randint(1,10000000000)
        else:
            unique_values = df[col].unique()
            new_df[col] = np.random.choice(unique_values,size = n_rows)

    new_df.drop(columns=['prediction'],inplace=True)

    with engine.connect() as conn:
        new_df.to_sql(new_data_from_generator, con=conn, if_exists='append',index=False) 


if __name__ == "__main__":
    
    generate(n_rows)