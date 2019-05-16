from datetime import datetime, timedelta

from airflow import DAG
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
    'xcom_dag',
    default_args=default_args,
    description='dag showing sensors',
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

create_sql = PythonOperator(
    task_id="create_sql",
    python_callable=PythonExamples.creat_sql,
    dag=dag
)

run_sql = PythonOperator(
    task_id="run_sql",
    python_callable=PythonExamples.print_sql,
    op_kwargs={"pushed_from_task_id": "create_sql"},
    provide_context=True,
    dag=dag
)

start_dag >> create_sql

create_sql >> run_sql

end_dag << run_sql
