import pandas as pd
import luigi
from src.pipeline.almacenamiento_metadata_task import AlmacenamientoMetadataTask
from luigi.contrib.postgres import CopyToTable
from src.utils.general import load_s3_object, get_db_credentials
from src.utils import constants
from src.utils.utils_notebook.cleaning import cleaning

# PYTHONPATH='.' luigi --module src.pipeline.cleaning_task CleaningTask --ingesta consecutiva --year 2021 --month 04 --day 30

class CleaningTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return AlmacenamientoMetadataTask(self.ingesta, self.year, self.month, self.day)

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'clean.features'

    columns = [("inspection_id", "VARCHAR"),
                ("dba_name", "VARCHAR"),
                ("aka_name", "VARCHAR"),
                ("license", "VARCHAR"),
                ("facility_type", "VARCHAR"),
                ("risk", "VARCHAR"),
                ("address", "VARCHAR"),
                ("city", "VARCHAR"),
                ("state", "VARCHAR"),
                ("zip", "INTEGER"),
                ("inspection_date", "TIMESTAMP WITHOUT TIME ZONE"),
                ("inspection_type", "VARCHAR"),
                ("results", "VARCHAR"),
                ("violations", "VARCHAR"),
                ("latitude", "NUMERIC(12, 4)"),
                ("longitude", "NUMERIC(12,4)")]

    def rows(self):

        if self.ingesta == 'historica':
            key = '{}-{}-{}-{}.pkl'.format(constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        df = load_s3_object(creds_file, key)

        df = cleaning(df)

        r = df.to_records(index = False)

        for element in r:
            yield element
