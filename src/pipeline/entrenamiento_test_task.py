import marbles.core
import marbles.mixins
import luigi
import pandas as pd
from datetime import date, datetime
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.utils.general import get_db_conn, select_semantic_features, get_db_credentials
from src.pipeline.entrenamiento_task import EntrenamientoTask

# PYTHONPATH='.' luigi --module src.pipeline.entrenamiento_test_task EntrenamientoTestTask --ingesta consecutiva --year 2021 --month 04 --day 23

### TEST
class TestEntrenamiento(marbles.core.TestCase, marbles.mixins.DateTimeMixins, marbles.mixins.CategoricalMixins):

    def __init__(self, luigi_year, luigi_month, luigi_day):
        #super(TestFE, self)._init_()
        self.year = luigi_year
        self.month = luigi_month
        self.day = luigi_day
        self.label = [0,1]

# Validación de fecha
    def test_inspection_date_future(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today,
            msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: Esta fecha no ha ocurrido!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Label
    def test_labels(self):

        credentials = 'conf/local/credentials.yaml'
        today = date.today()
        delta_date = today - timedelta(days=7)
        df = select_semantic_features(credentials, delta_date)
        A = set(df['label'])
        B = set(self.label)
        A.issubset(B)
        self.assertTrue(A.issubset(B), msg = "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ERROR: Diferentes etiquetas!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

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

        testing = TestEntrenamiento(self.year, self.month, self.day)
        testing.test_inspection_date_future()
        testing.test_labels()

        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Entrenamiento", date , 'Equipo 6')]
        for element in r:
            yield element
