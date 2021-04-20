import luigi
import luigi.contrib.s3
from luigi.contrib.postgres import CopyToTable
from src.pipeline.feature_engineering_task import FETask
from src.utils.general import get_db_credentials
from src.utils import constants
import pickle

# PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_metadata_task FEMetadataTask --ingesta consecutiva --year 2021 --month 04 --day 30 --local-scheduler

class FEMetadataTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return FETask(self.ingesta, self.year, self.month, self.day)

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'metadata'

    columns = [("Task", "VARCHAR"),
               ("INGESTION", "VARCHAR"),
               ("FECHA", "TIMESTAMP WITHOUT TIME ZONE"),
               ("AUTOR", "VARCHAR")]

    def rows(self):
        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("feature engineering","Ingesta {}".format(self.ingesta), date , 'Equipo 6')]
        for element in r:
            yield element
