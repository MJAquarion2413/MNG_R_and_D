# Filename: hello_airflow.py
# Place this script in ~/airflow/dags

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Define the Python function to be run by the Airflow task
def greet():
    print("Hello Airflow!")


# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'hello_airflow',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the task using a PythonOperator to call the function
greet_task = PythonOperator(
    task_id='print_hello',
    python_callable=greet,
    dag=dag,
)

# No dependencies to set for this single-task DAG
