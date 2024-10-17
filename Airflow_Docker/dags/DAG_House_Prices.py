
from airflow.decorators import dag,task
from airflow.utils.dates import days_ago
import subprocess

@dag(
        schedule_interval = '*/10 * * * *', #Каждые 10 минут
        start_date = days_ago(1),
        catchup = False 
    ) 
def House_Prices_Model():
    
    @task
    def data_generator():
       result = subprocess.run(['python','/opt/airflow/scripts/house_prices_generator.py'],capture_output=True,text=True)

    @task
    def data_transform():
        result = subprocess.run(['python','/opt/airflow/scripts/data_transform.py'],capture_output=True,text=True)
    
    @task
    def XGBRegressor():
        result = subprocess.run(['python','/opt/airflow/scripts/XGB_model.py'],capture_output=True,text=True)

    @task
    def ReTrainingGen():
        result = subprocess.run(['python','/opt/airflow/scripts/ReTrainigGenerator.py'],capture_output=True,text=True)

    data_generator = data_generator()
    data_transform = data_transform()
    XGBRegressor = XGBRegressor()
    ReTrainingGen = ReTrainingGen()
    
    
    
    data_generator >> data_transform >> XGBRegressor >> ReTrainingGen
 
House_Prices_Model_instance = House_Prices_Model()