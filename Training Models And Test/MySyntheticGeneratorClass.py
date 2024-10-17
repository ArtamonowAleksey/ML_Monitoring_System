
import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine  

import datetime
import pickle

config = configparser.ConfigParser()
config.read('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/config.ini')
conn_string = config.get('DATABASE', 'connection_url')

general_table = 'house_prices_fin'

#Загрузка df из БД

engine = create_engine(conn_string)
        
with engine.connect() as conn:
    query = f"SELECT * FROM {general_table}"
    df = pd.read_sql(query, engine)


class MySyntheticGenerator:
    def __init__(self,df,n_rows=5):
        self.df = df
        self.n_rows = n_rows
    
    def generate(self):
        n_rows=5
        new_df = pd.DataFrame()
        
        for col in self.df.columns:
            if col == 'id':
                new_df[col] = np.random.randint(1,10000000000)
            else:
                unique_values = self.df[col].unique()
                new_df[col] = np.random.choice(unique_values,size=self.n_rows)
        return new_df


generator = MySyntheticGenerator(df,n_rows=10)
df = generator.generate()

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/MySyntheticGenerator.pkl','wb') as f:
    pickle.dump(generator,f)

