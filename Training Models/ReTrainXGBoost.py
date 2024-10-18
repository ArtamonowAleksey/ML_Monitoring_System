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
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/config.ini')
conn_string = config.get('DATABASE', 'connection_url')


# Загрузка сохраненного pipeline для числовых данных

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/num_pipe.pkl', 'rb') as f:
    num_pipe = pickle.load(f)  


#Загрузка сохраненного категориального импутера

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/cat_imputer.pkl', 'rb') as f:
    cat_imputer = pickle.load(f) 

#Загрузка сохраненного OrdinalEncoder

with open('/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/ordinal_encoder.pkl', 'rb') as f:
    ordinal_encoder = pickle.load(f)

table = 'house_prices_fin'

query = f''' 

select * from {table}

'''

filepath = '/home/aleksey/House-Prices-Airflow-Superset/Training Models And Test/XGBRegressor.pkl'

def training(query,table):
    db = create_engine(conn_string)
    
    with db.connect() as conn:
        df = pd.read_sql(query, con=conn)
    
    target = df[['SalePrice']]
    for_drop = ['PoolQC', 'MiscFeature', 'Alley', 'Fence','Id','dt','prediction','SalePrice']
    
    df.drop(columns=for_drop,inplace=True)

    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.to_list()

    cat_cols = df.select_dtypes(include=['object']).columns.to_list()

    df[num_cols] = pd.DataFrame(num_pipe.transform(df[num_cols]),columns = num_cols)

    df[cat_cols] = pd.DataFrame(cat_imputer.transform(df[cat_cols]),columns = cat_cols)

    df[cat_cols] = pd.DataFrame(ordinal_encoder.transform(df[cat_cols]),columns = cat_cols,index=df.index )

    X_train = df
    Y_train = target

    xgb_params ={"learning_rate": 0.1,
                        "max_depth": 4,
                        "min_child_weight":1,
                        "gamma":0.1,
                        "colsample_bytree":0.3
            }
    
    xgb_model = XGBRegressor(**xgb_params).fit(X_train, Y_train)

    with open(filepath, "wb") as f:
        pickle.dump(xgb_model, f)
    

if __name__ == "__main__":
    
    training(query,table)
