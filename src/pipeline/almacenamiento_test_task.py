import luigi
import luigi.contrib.s3
import pickle
from src.utils import constants
from src.pipeline.almacenamiento_task import AlmacenamientoTask
from src.utils.general import get_s3_credentials, get_db_credentials, load_s3_object
from src.utils import unittests
from luigi.contrib.postgres import CopyToTable

# PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_test_task TestAlmacenamientoTask --ingesta consecutiva --year 2021 --month 04 --day 15

class TestAlmacenamientoTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return AlmacenamientoTask(self.ingesta, self.year, self.month, self.day)

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
            key = '{}-{}-{}-{}.pkl'.format(constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        df = load_s3_object(creds_file, key)

        tests = unittests.TestAlmacenamiento(df, self.year, self.month, self.day)

        tests.test_categories_risks()
        tests.test_inspection_date_future()
        tests.test_inspection_date_past()
        tests.test_num_columns()
        tests.test_not_empty()
        tests.test_params()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("unit test almacenamiento", date , 'Equipo 6')]
        for element in r:
            yield element
