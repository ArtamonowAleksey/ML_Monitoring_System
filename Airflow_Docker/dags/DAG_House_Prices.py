
from airflow.decorators import dag,task
from airflow.utils.dates import days_ago
import subprocess
from pathlib import Path

scripts_path = Path(__file__).resolve().parent.parent  /'scripts'


@dag(
        schedule_interval = '*/20 * * * *', #Каждые 20 минут
        start_date = days_ago(1),
        catchup = False 
    ) 
def House_Prices_Model():
    
    @task
    def data_generator():
       result = subprocess.run(['python',scripts_path / 'house_prices_generator.py'],capture_output=True,text=True)

    @task
    def MySyntheticGenerator():
        result = subprocess.run(['python',scripts_path /'MySyntheticGenerator.py'],capture_output=True,text=True)

    @task
    def data_transform():
        result = subprocess.run(['python',scripts_path / 'data_transform.py'],capture_output=True,text=True)
    
    @task
    def XGBRegressor():
        result = subprocess.run(['python',scripts_path /'XGB_model.py'],capture_output=True,text=True)

    @task
    def ReTrainingGen():
        result = subprocess.run(['python',scripts_path /'ReTrainigGenerator.py'],capture_output=True,text=True)
    
    @task
    def ReTrainXGBoost():
        result = subprocess.run(['python',scripts_path /'ReTrainXGBoost.py'],capture_output=True,text=True)
    

    data_generator = data_generator()
    MySyntheticGenerator = MySyntheticGenerator()
    data_transform = data_transform()
    XGBRegressor = XGBRegressor()
    ReTrainingGen = ReTrainingGen()
    ReTrainXGBoost = ReTrainXGBoost()
    
    data_generator >> MySyntheticGenerator >> data_transform >> XGBRegressor >> [ReTrainingGen,ReTrainXGBoost]
 
House_Prices_Model_instance = House_Prices_Model()