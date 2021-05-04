import luigi
import pickle
from datetime import date
from datetime import timedelta
from src.utils import constants
from src.utils import unittests
from src.pipeline.aequitas_task import AequitasTask
from src.utils.general import *
from luigi.contrib.postgres import CopyToTable

## PYTHONPATH='.' luigi --module src.pipeline.aequitas_test_task TestAequitasTask --ingesta consecutiva --year 2021 --month 05 --day 03

class TestAequitasTask(CopyToTable):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
        return AequitasTask(self.ingesta, self.year, self.month, self.day, self.model_type)

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'tests'

    columns = [("TEST",  "VARCHAR"),
                ("FECHA", "TIMESTAMP WITH TIME ZONE"),
                ("AUTOR", "VARCHAR")]

    def rows(self):

        if self.ingesta == 'historica':
            #key = 's3://{}/{}-{}-{}-{}-aequitas.pkl'. \
            key = '{}-{}-{}-{}-aequitas.pkl'. \
                format(constants.initial_path, self.year, self.month, self.day)

        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}-aequitas.pkl'. \
                format(constants.concecutive_path, self.year, self.month, self.day)

        else:
            print('No such type of ingestion')

        credentials = 'conf/local/credentials.yaml'

        df = load_s3_object(credentials, key)

        tests = unittests.TestAequitas(df, self.year, self.month, self.day, self.model_type)

        tests.test_attributes()
        tests.test_num_columns()
        tests.test_not_empty()
        tests.test_params()
        tests.test_assist()

        date_ = str(self.year + '-' + self.month + '-' + self.day)
        r = [("unit test aequitas", date_ , 'Equipo 6')]
        for element in r:
            yield element
