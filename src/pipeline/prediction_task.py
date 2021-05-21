import luigi
import pickle
import luigi.contrib.s3
from datetime import date
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.pipeline.feature_engineering_metadata_task import FEMetadataTask
from src.pipeline.seleccion_modelo_task import SeleccionModeloTask
from src.utils.general import load_s3_object, predictions, get_db_credentials
from src.utils import constants

# PYTHONPATH='.' luigi --module src.pipeline.prediction_task PredictionTask --ingesta consecutiva --year 2021 --month 05 --day 21 --local-scheduler

class PredictionTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
       return {
        'FE_metadata_task' : FEMetadataTask(self.ingesta, self.year, self.month, self.day),
        #'SeleccionModeloTask': SeleccionModeloTask(self.ingesta, self.year, self.month, self.day)
         }

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'results.predictions'

    columns = [("ID_INSPECTION",  "VARCHAR"),
                ("DBA_NAME", "VARCHAR"),
                ("GROUND_TRUTH", "SMALLINT"),
                ("SCORE", "NUMERIC"),
                ("LABEL", "INTEGER"),
                ("PREDICTIONS_DATE", "TIMESTAMP WITH TIME ZONE")]
    def rows(self):

        if self.ingesta == 'historica':
            model_key = '{}-{}-{}-{}-modelo.pkl'.format(constants.initial_path, self.year, self.month, self.day)

        elif self.ingesta == 'consecutiva':
            model_key = '{}-{}-{}-{}-modelo.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)

        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        today = date.today()

        preds = predictions(creds_file, model_key, today)

        r = preds.to_records(index = False)

        for element in r:
            yield element
