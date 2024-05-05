from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def my_task():
    print("Running my task")

dag = DAG('my_dag',
          schedule_interval='@daily',
          start_date=datetime(2021, 1, 1))

task = PythonOperator(task_id='my_task',
                      python_callable=my_task,
                      dag=dag)
