
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
    'complex_dag',
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
    op_kwargs={"greeting": "Really not that complex"},
    dag=dag
)

hola = BashOperator(
    task_id='hola',
    bash_command="echo 'Hola'",
    retries=3,
    dag=dag,
)

bonjour = BashOperator(
    task_id='bonjour',
    bash_command="echo 'Bonjour'",
    retries=3,
    dag=dag,
)

ciao = BashOperator(
    task_id='ciao',
    bash_command="echo 'ciao'",
    retries=3,
    dag=dag,
)

hallo = BashOperator(
    task_id='hallo',
    bash_command="echo 'hallo'",
    retries=3,
    dag=dag,
)

ola = BashOperator(
    task_id='ola',
    bash_command="echo 'ola'",
    retries=3,
    dag=dag,
)

ola.set_upstream(start_dag)
hola.set_upstream(start_dag)
bonjour.set_upstream(start_dag)
hallo.set_upstream(start_dag)
ciao.set_upstream(start_dag)
greeting.set_upstream(start_dag)

start_dag >> hello_world >> greeting
hola.set_upstream(hello_world)
bonjour.set_upstream(hello_world)
hallo.set_upstream(bonjour)
hallo.set_upstream(hola)
ciao.set_upstream(hola)
ola.set_upstream(hallo)

ola.set_downstream(end_dag)
hola.set_downstream(end_dag)
bonjour.set_downstream(end_dag)
hallo.set_downstream(end_dag)
ciao.set_downstream(end_dag)
hello_world.set_downstream(end_dag)
greeting.set_downstream(end_dag)