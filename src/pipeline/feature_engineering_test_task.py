import marbles.core
import marbles.mixins
import luigi
import pandas as pd
from datetime import date
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.utils.general import get_db_conn, select_semantic_features, get_db_credentials
from src.pipeline.feature_engineering_task import FETask

# PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_test_task FETestTask --ingesta consecutiva --year 2021 --month 04 --day 23 --fecha '2021-04-25'

### TEST
class TestFE(marbles.core.TestCase, marbles.mixins.DateTimeMixins):

    def __init__(self, luigi_date):
        super(TestFE, self).__init__()
        self.date = luigi_date

# Validación de fecha
    def test_inspection_date_future(self):
        fecha = self.date
        self.assertDateTimesPast(
            [fecha],
            strict = False,
            msg = "ERROR: Esta fecha no ha ocurrido"
        )
# Registros
    def test_rows_count(self):
        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_semantic_features(credentials, delta_date)

        n_rows = df.shape[0]

        self.assertGreater(n_rows, 1, note = "ERROR: No se tienen registros")

        print('Número de registros cargados: {}'.format(n_rows))



# Variables
    def test_cols_count(self):
        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_semantic_features(credentials, delta_date)

        n_cols = df.shape[1]

        self.assertGreater(n_cols, 1, note = "ERROR: No se tienen registros")

        print('Número de columnas cargadas: {}'.format(n_cols))

######## LUIGI

class FETestTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    fecha = luigi.DateParameter()

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
#        fecha = '{}-{}-{}'.format(self.year, self.month, self.day)
        testing = TestFE(self.fecha)
        testing.test_inspection_date_future()
        testing.test_rows_count()
        testing.test_cols_count()

        r = [("feature engineering", self.fecha , 'Equipo 6')]
        for element in r:
            yield element
