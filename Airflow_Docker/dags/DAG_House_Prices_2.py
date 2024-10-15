
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator


default_args = {
        'owner':'airflow',
        'depends_on_past': False,
        'catchup': False    
        }


with DAG(
        dag_id = 'House_Prices_Model', #Имя которое отображается в Airflow
        default_args = default_args,
        schedule_interval = '*/10 * * * *', #Каждые 10 минут
        start_date = days_ago(1)
    ) as dag:
        
        data_generator = BashOperator(
        task_id='data_generator',
        bash_command='python /opt/airflow/scripts/house_prices_generator.py',  # Укажите путь к вашему скрипту
    )
        data_transform = BashOperator(
        task_id='data_transform',
        bash_command='python /opt/airflow/scripts/data_transform.py',  # Укажите путь к вашему скрипту
        #bash_command='source /path/to/myenv/bin/activate && python /path/to/your_script.py'
    )
        model_apply = BashOperator(
        task_id='XGBRegressor',
        bash_command='python /opt/airflow/scripts/XGB_model.py',  # Укажите путь к вашему скрипту
    )
        
data_generator >> data_transform  >> model_apply
#data_transform
#model_apply