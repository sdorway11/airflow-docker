import logging


class PythonExamples:

    @staticmethod
    def hello_world(greeting: str):
        logger = logging.getLogger(__name__)
        logger.info("Hello World")
        print(greeting)