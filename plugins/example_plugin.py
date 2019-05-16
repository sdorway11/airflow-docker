import logging

from airflow.plugins_manager import AirflowPlugin

from sensors.count_task_runs import CountTaskRuns

log = logging.getLogger(__name__)


class MainPlugin(AirflowPlugin):
    name = "custom_sensors"
    sensors = [CountTaskRuns]
