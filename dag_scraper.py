from datetime import timedelta, datetime
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator

from scraper import get_df


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 20),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(hours=2),
    'schedule_interval': '@daily'
    }

dag = DAG('dag_scraper',
          default_args=default_args,
          description='Scrap Liverpool Data')

run_etl = PythonOperator(task_id='liverpool_id',
                         python_callable=get_df,
                         dag=dag)

run_etl