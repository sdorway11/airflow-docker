import logging


class PythonExamples:

    @staticmethod
    def hello_world(greeting: str):
        logger = logging.getLogger(__name__)
        logger.info("Hello World")
        print(greeting)

    @staticmethod
    def creat_sql():
        sql = "SELECT COUNT(*) " \
              "WHERE task_instance.dag_id = 'simple_dag' " \
              "AND task_instance.task_id = 'end_dag'"

        return sql

    @staticmethod
    def print_sql(**kwargs):
        sql = kwargs['task_instance'].xcom_pull(task_ids=kwargs['pushed_from_task_id'])

        logger = logging.getLogger(__name__)
        logger.info(sql)
