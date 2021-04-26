import marbles.core
import marbles.mixins
import luigi
import pandas as pd
from datetime import date, datetime
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.utils.general import load_s3_object, get_db_credentials
from src.pipeline.entrenamiento_task import EntrenamientoTask
from src.utils import constants


# PYTHONPATH='.' luigi --module src.pipeline.entrenamiento_test_task EntrenamientoTestTask --ingesta consecutiva --year 2021 --month 04 --day 23

### TEST
class TestEntrenamiento(marbles.core.TestCase, marbles.mixins.DateTimeMixins, marbles.mixins.CategoricalMixins):

    def __init__(self, luigi_df, luigi_year, luigi_month, luigi_day):
        #super(TestFE, self)._init_()
        self.year = luigi_year
        self.month = luigi_month
        self.day = luigi_day
        self.df = luigi_df
        self.label = ['0','1']

# Validación de fecha
    def test_inspection_date_future(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today,
            msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: Esta fecha no ha ocurrido!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Registros
    def test_rows_count(self):

        n_rows = self.df.shape[0]

        self.assertGreater(n_rows, 1, note = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: No se tienen registros!!!!!!!!!!!!!!!!!!")

        print('Número de registros cargados: {}'.format(n_rows))

# Variables
    def test_cols_count(self):

        n_cols = self.df.shape[1]

        self.assertGreater(n_cols, 1, note = "¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: No se tienen registros!!!!!!!!!!!!!!!")

        print('Número de columnas cargadas: {}'.format(n_cols))

######## LUIGI

class EntrenamientoTestTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return EntrenamientoTask(self.ingesta, self.year, self.month, self.day)

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
        if self.ingesta == 'historica':
            key = '{}-{}-{}-{}-train.pkl'.format(constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}-train.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        df = load_s3_object(creds_file, key)

        testing = TestEntrenamiento(df, self.year, self.month, self.day)
        testing.test_inspection_date_future()
        testing.test_rows_count()
        testing.test_cols_count()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Entrenamiento", date , 'Equipo 6')]
        for element in r:
            yield element
