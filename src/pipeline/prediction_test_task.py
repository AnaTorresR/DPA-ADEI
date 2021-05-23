import luigi
import pickle
from datetime import date, timedelta
from src.utils import constants
from src.utils import unittests
from src.pipeline.prediction_task import PredictionTask
from src.utils.general import get_db_credentials, get_db_conn, select_predictions
from luigi.contrib.postgres import CopyToTable

class TestPredictionTask(CopyToTable):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
        return PredictionTask(self.ingesta, self.year, self.month, self.day, self.model_type)

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

        df = select_predictions(credentials, delta_date)

        tests = unittests.TestPrediction(df, self.year, self.month, self.day, self.model_type)

        tests.test_label()
        tests.test_score()
        tests.test_ground()
        tests.test_num_columns()
        tests.test_not_empty()
        tests.test_null()
        tests.test_assist()

        date_ = str(self.year + '-' + self.month + '-' + self.day)
        r = [("unit test predicciones", date_ , 'Equipo 6')]
        for element in r:
            yield element

