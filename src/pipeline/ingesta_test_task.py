import luigi
import luigi.contrib.s3
import pickle
from src.utils import constants
from src.pipeline.ingesta_task import IngestaTask
from src.utils.general import get_s3_credentials, get_db_credentials, load_pickle_file
from src.utils import unittests
from luigi.contrib.postgres import CopyToTable

# PYTHONPATH='.' luigi --module src.pipeline.ingesta_test_task TestIngestaTask --ingesta consecutiva --year 2021 --month 04 --day 15

class TestIngestaTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {
        'IngestaTask': IngestaTask(self.ingesta, self.year, self.month, self.day)}

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
            temp_path = 'temp/{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            temp_path = 'temp/{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        tests = unittests.TestIngesta(temp_path, self.year, self.month, self.day)

        tests.test_file_exits()
        tests.test_categories_risks()
        tests.test_inspection_date_future()
        tests.test_inspection_date_past()
        tests.test_num_columns()
        tests.test_not_empty()
        tests.test_params()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("unit test ingesta", date , 'Equipo 6')]
        for element in r:
            yield element
