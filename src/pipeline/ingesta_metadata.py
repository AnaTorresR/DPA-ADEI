import pandas as pd
import luigi
import psycopg2

from src.pipeline.ingesta_task import IngestaTask
from luigi.contrib.postgres import CopyToTable
from src.utils.general import get_db_credentials

#from src.utils import constants

# PYTHONPATH='.' luigi --module src.pipeline.ingesta_metadata Metadata --ingesta consecutiva --year 2021 --month 04 --day 15 --local-scheduler

class IngestionMetadata(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return IngestaTask(self.ingesta, self.year, self.month, self.day)

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'ingestion_metadata'

    columns = [("Task", "VARCHAR"),
               ("Fecha", "TIMESTAMP WITH TIME ZONE"),
               ("Autor", "VARCHAR")]

    def rows(self):
        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Ingesta {}".format(self.ingesta), date , 'Equipo 6')]
        for element in r:
            yield element
