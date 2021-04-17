import luigi
import luigi.contrib.s3
from luigi.contrib.postgres import CopyToTable
from src.pipeline.cleaning_task import CleaningTask
from src.utils.general import get_db_credentials
import pickle

# PYTHONPATH='.' luigi --module src.pipeline.cleaning_metadata_task CleaningMetadataTask --ingesta consecutiva --year 2021 --month 04 --day 15 --local-scheduler
# Port forwarding ssh -i ~/.ssh/id_rsa -NL localhost:9999:localhost:8082 atorres@ec2-3-134-110-173.us-east-2.compute.amazonaws.com

class CleaningMetadataTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return CleaningTask(self.ingesta, self.year, self.month, self.day)

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
        r = [("cleaning/preprocessing","Ingesta {}".format(self.ingesta), date , 'Equipo 6')]
        for element in r:
            yield element

