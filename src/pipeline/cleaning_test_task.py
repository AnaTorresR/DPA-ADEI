import luigi
import pickle
from datetime import date
from datetime import timedelta
from src.utils import constants
from src.utils import unittests
from src.pipeline.cleaning_task import CleaningTask
from src.utils.general import get_db_credentials, get_db_conn, select_clean_features
from luigi.contrib.postgres import CopyToTable

# PYTHONPATH='.' luigi --module src.pipeline.cleaning_test_task TestCleaningTask --ingesta consecutiva --year 2021 --month 04 --day 15

class TestCleaningTask(CopyToTable):
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

    table = 'tests'

    columns = [("TEST",  "VARCHAR"),
                ("FECHA", "TIMESTAMP WITH TIME ZONE"),
                ("AUTOR", "VARCHAR")]

    def rows(self):

        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_clean_features(credentials, delta_date)

        tests = unittests.TestCleaning(df, self.year, self.month, self.day)

        tests.test_lower()
        tests.test_not_nas()
        tests.test_num_columns()
        tests.test_not_empty()
        tests.test_params()

        date_ = str(self.year + '-' + self.month + '-' + self.day)
        r = [("unit test cleaning", date_ , 'Equipo 6')]
        for element in r:
            yield element
