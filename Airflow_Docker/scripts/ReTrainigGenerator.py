import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
import configparser 
import datetime

from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import Metadata
import pickle
import sdv


config = configparser.ConfigParser()
config.read('/opt/airflow/scripts/config.ini')
conn_string = config.get('DATABASE', 'connection_url')

filepath='/opt/airflow/models/synthesizer.pkl'

table = 'house_prices_fin'

query = f''' select * from {table}'''

def training(query,table):
    db = create_engine(conn_string)
    
    with db.connect() as conn:
        df = pd.read_sql(query, con=conn)
    
    df.drop(columns=['prediction'],inplace=True)
        
  
    metadata = Metadata.detect_from_dataframe(
        data=df,
        table_name='house_prices'
        )
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(df)
    synthesizer.save('/opt/airflow/models/synthesizer.pkl')


if __name__ == "__main__":
    
    training(table)