
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils import timezone

from sensors.count_task_runs import CountTaskRuns

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
    'sensor_dag',
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

count_tasks_sensor = CountTaskRuns(
    task_id="count_tasks_sensor",
    count_dag_id="simple_dag",
    count_task_id="end_dag",
    check_time=timezone.utcnow(),
    wait_count=5,
    poke_interval=30,
    dag=dag
)

count_tasks_sensor.set_upstream(start_dag)
count_tasks_sensor.set_downstream(end_dag)
