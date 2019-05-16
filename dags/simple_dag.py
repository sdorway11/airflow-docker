
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from app.python_examples import PythonExamples

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 1, 30),
    "email": ["sdorway11@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
    'queue': 'default_queue'
}

dag = DAG(
    'simple_dag',
    default_args=default_args,
    description='a simple example of a dag',
    schedule_interval='* * * * *',
    start_date=datetime(2018, 11, 30),
    concurrency=16,
    max_active_runs=1,
    catchup=False)

start_dag = DummyOperator(
    task_id='start_dag',
    dag=dag,
)

end_dag = DummyOperator(
    task_id='end_dag',
    dag=dag,
)

hello_world = BashOperator(
    task_id='hello_world',
    bash_command="echo 'Hello World'",
    retries=3,
    dag=dag,
)

greeting = PythonOperator(
    task_id="greeting",
    python_callable=PythonExamples.hello_world,
    op_kwargs={"greeting": "Nice to meet you"},
    dag=dag
)

start_dag >> hello_world >> greeting >> end_dag
