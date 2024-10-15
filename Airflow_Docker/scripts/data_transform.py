#Функция для предобработки данных

import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine  

import datetime
import pickle
from sklearn.preprocessing import LabelEncoder

config = configparser.ConfigParser()
config.read('/opt/airflow/scripts/config.ini')
'''config.read('/home/aleksey/Notebooks_Projects/House-Prices-Airflow-Superset/Airflow_Docker/scripts/config.ini')'''
conn_string = config.get('DATABASE', 'connection_url')

#Таблица куда записываем предобработанный house_prices

#Основная таблица

general_table = 'house_prices_fin'

#Таблица с новыми данными которые генерируются

new_data_from_generator = 'house_prices_generator'

#Таблица куда сохраняются предобработанные данные

table_upload = 'house_prices_preprocess'

# Загрузка сохраненного pipeline для числовых данных

with open('/opt/airflow/models/num_pipe.pkl', 'rb') as f:
    num_pipe = pickle.load(f)  


#Загрузка сохраненного категориального импутера

with open('/opt/airflow/models/cat_imputer.pkl', 'rb') as f:
    cat_imputer = pickle.load(f) 

#Загрузка сохраненного OrdinalEncoder

with open('/opt/airflow/models/ordinal_encoder.pkl', 'rb') as f:
    ordinal_encoder = pickle.load(f)

for_drop =['PoolQC', 'MiscFeature', 'Alley', 'Fence','Id','dt','SalePrice']

def preprocess(new_data_from_generator,table_upload):

    #Загрузка df из БД

    engine = create_engine(conn_string)
        
    with engine.connect() as conn:
        
        query = f"SELECT * FROM {new_data_from_generator}"
        
        df = pd.read_sql(query, engine)

    for_drop =['PoolQC', 'MiscFeature', 'Alley', 'Fence','Id','dt','SalePrice']
    
    df.drop(columns=for_drop,inplace=True)
    
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.to_list()
    cat_cols = df.select_dtypes(include=['object']).columns.to_list()
    
    df[num_cols] = pd.DataFrame(num_pipe.transform(df[num_cols]),columns = num_cols)

    df[cat_cols] = pd.DataFrame(cat_imputer.transform(df[cat_cols]),columns = cat_cols)

    df[cat_cols] = pd.DataFrame(ordinal_encoder.transform(df[cat_cols]),columns = cat_cols,index=df.index )

    #Запись таблицы в БД

    engine = create_engine(conn_string) 
    
    with engine.connect() as conn:
        
        df.to_sql(table_upload, con=conn, if_exists='replace',index=False) 

if __name__ == "__main__":
    preprocess(new_data_from_generator,table_upload)