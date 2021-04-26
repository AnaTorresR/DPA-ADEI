import marbles.core
import marbles.mixins
import luigi
import sys
import pandas as pd
from datetime import date, datetime
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.utils.general import load_s3_object, get_db_credentials
from src.utils import constants
from src.pipeline.seleccion_modelo_task import SeleccionModeloTask

class TestSeleccionModelo(marbles.core.TestCase, marbles.mixins.DateTimeMixins, marbles.mixins.CategoricalMixins):

    def __init__(self, luigi_df, luigi_year, luigi_month, luigi_day):
        #super(TestFE, self)._init_()
        self.year = luigi_year
        self.month = luigi_month
        self.day = luigi_day
        self.df = luigi_df

# Validación de fecha
    def test_inspection_date_future(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today,
            msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: Esta fecha no ha ocurrido!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Registros
    def test_file_size(self):
        size = sys.getsizeof(self.df)
        self.assertTrue(size>0, msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ ERROR: NO SE GUARDÓ NADA!!!!!!!!!!!!!!!!!!!!!!!!!!")

######## LUIGI

class SeleccionModeloTestTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return SeleccionModeloTask(self.ingesta, self.year, self.month, self.day)

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
            key = '{}-{}-{}-{}-modelo.pkl'.format(constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}-modelo.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        df = load_s3_object(creds_file, key)

        testing = TestSeleccionModelo(df, self.year, self.month, self.day)
        testing.test_inspection_date_future()
        testing.test_file_size()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Selección modelo", date , 'Equipo 6')]
        for element in r:
            yield element
