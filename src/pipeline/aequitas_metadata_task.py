import luigi
import luigi.contrib.s3
from luigi.contrib.postgres import CopyToTable
from src.pipeline.aequitas_test_task import TestAequitasTask
from src.utils.general import get_db_credentials
from src.utils import constants
import pickle

# PYTHONPATH='.' luigi --module src.pipeline.aequitas_metadata_task AequitasMetadataTask --ingesta consecutiva --year 2021 --month 04 --day 07 --local-scheduler

class AequitasMetadataTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
        return TestAequitasTask(self.ingesta, self.year, self.month, self.day, self.model_type)

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'metadata'

    columns = [("Task", "VARCHAR"),
               ("INGESTION", "VARCHAR"),
               ("FECHA", "TIMESTAMP WITH TIME ZONE"),
               ("AUTOR", "VARCHAR")]

    def rows(self):
        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Aequitas","Ingesta {}".format(self.ingesta), date , 'Equipo 6')]
        for element in r:
            yield element
