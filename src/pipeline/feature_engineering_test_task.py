import marbles.core
import marbles.mixins
import luigi
import pandas as pd
from datetime import date, datetime
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.utils.general import get_db_conn, select_semantic_features, get_db_credentials
from src.pipeline.feature_engineering_task import FETask
#from src.utils import unittests

# PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_test_task FETestTask --ingesta consecutiva --year 2021 --month 04 --day 23

### TEST
class TestFE(marbles.core.TestCase, marbles.mixins.DateTimeMixins):

    def __init__(self, luigi_year, luigi_month, luigi_day):
        #super(TestFE, self)._init_()
        self.year = luigi_year
        self.month = luigi_month
        self.day = luigi_day

# Validación de fecha
    def test_inspection_date_future(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today,
            msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: Esta fecha no ha ocurrido!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Registros
    def test_rows_count(self):
        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_semantic_features(credentials, delta_date)

        n_rows = df.shape[0]

        self.assertGreater(n_rows, 1, note = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: No se tienen registros!!!!!!!!!!!!!!!!!!")

        print('Número de registros cargados: {}'.format(n_rows))

# Variables
    def test_cols_count(self):
        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_semantic_features(credentials, delta_date)

        n_cols = df.shape[1]

        self.assertGreater(n_cols, 1, note = "¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: No se tienen registros!!!!!!!!!!!!!!!")

        print('Número de columnas cargadas: {}'.format(n_cols))

######## LUIGI

class FETestTask(CopyToTable):
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

    table = 'tests'

    columns = [("TEST",  "VARCHAR"),
    ("FECHA", "TIMESTAMP WITH TIME ZONE"),
    ("AUTOR", "VARCHAR")
    ]

    def rows(self):
        testing = TestFE(self.year, self.month, self.day)
        testing.test_inspection_date_future()
        testing.test_rows_count()
        testing.test_cols_count()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("feature engineering", pd.to_datetime(date) , 'Equipo 6')]
        for element in r:
            yield element
