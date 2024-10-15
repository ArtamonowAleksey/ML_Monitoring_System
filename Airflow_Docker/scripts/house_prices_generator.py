#Функция для генерации новых данных

import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine  
import datetime
import pickle


config = configparser.ConfigParser()
config.read('/opt/airflow/scripts/config.ini')
conn_string = config.get('DATABASE', 'connection_url')


#Таблица с новыми данными которые генерируются

new_data_from_generator = 'house_prices_generator'


with open('/opt/airflow/models/my_synthesizer.pkl', 'rb') as f:
    synthesizer = pickle.load(f)  

def upload_generator_data(new_data_from_generator):

    #Генерация случайных данных

    synthetic_data = synthesizer.sample(num_rows=10)
    
    #Баг с обучением

    synthetic_data['3SsnPorch'] = 0

    #Убираем баг и подставляем дату

    synthetic_data['dt'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    engine = create_engine(conn_string) 
    
    with engine.connect() as conn:
        synthetic_data.to_sql(new_data_from_generator, con=conn, if_exists='replace',index=False) 

if __name__ == "__main__":
    upload_generator_data(new_data_from_generator)

    
