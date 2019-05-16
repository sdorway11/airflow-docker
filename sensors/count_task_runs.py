from airflow.models import TaskInstance
from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.db import provide_session
from airflow.utils.decorators import apply_defaults


class CountTaskRuns(BaseSensorOperator):

    @apply_defaults
    def __init__(self, count_dag_id, count_task_id, wait_count, check_time, *args, **kwargs):
        super(CountTaskRuns, self).__init__(*args, **kwargs)
        self.count_dag_id = count_dag_id
        self.count_task_id = count_task_id
        self.wait_count = wait_count
        self.now = check_time
        self.logger.info("Checking from time: {}".format(self.now))

    @provide_session
    def poke(self, context, session=None):

        self.logger.info('Poking for Dag ID: {self.count_dag_id} '
                         'Task ID: {self.count_task_id} ... '.format(**locals()))

        task_instance_model = TaskInstance

        count = session.query(task_instance_model).filter(
            task_instance_model.dag_id == self.count_dag_id,
            task_instance_model.task_id == self.count_task_id,
            task_instance_model.state == "success",
            task_instance_model.start_date >= self.now,
        ).count()

        self.logger.info("Count: {}".format(count))

        if count >= self.wait_count:
            return True
        else:
            return False
