import pandas as pd
import numpy as np

import configparser
from sqlalchemy import create_engine  

import datetime
import pickle
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

config_path = Path(__file__).resolve().parent / 'config.ini'
models_path = Path(__file__).resolve().parent.parent  /'models'

config = configparser.ConfigParser()
config.read(config_path)
conn_string = config.get('DATABASE', 'connection_url')



#Таблица куда записываем предобработанный house_prices

#Основная таблица

general_table = 'house_prices_fin'

#Таблица с новыми данными которые генерируются

new_data_from_generator = 'house_prices_generator'

#Таблица куда сохраняются предобработанные данные

table_upload = 'house_prices_preprocess'

#Загрузка самой модели

with open(models_path / 'XGBRegressor.pkl', 'rb') as f:
    XGB_model = pickle.load(f)


def model_apply(table_upload,new_data_from_generator,general_table):
    
    engine = create_engine(conn_string)
        
    with engine.connect() as conn:
        
        query = f"SELECT * FROM {table_upload}"
        
        df = pd.read_sql(query, engine)

    df['prediction'] = XGB_model.predict(df)

    
    with engine.connect() as conn:
        
        query = f"SELECT * FROM {new_data_from_generator}"
        
        gen_df = pd.read_sql(query, engine)

    fin = gen_df.join(df['prediction'])

    
    with engine.connect() as conn:
        
        fin.to_sql(general_table, con=conn, if_exists='append',index=False)

if __name__ == "__main__":
    model_apply(table_upload,new_data_from_generator,general_table)