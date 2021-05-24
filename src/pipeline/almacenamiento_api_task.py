import luigi
import pickle
import luigi.contrib.s3
from datetime import date
from datetime import timedelta
from luigi.contrib.postgres import CopyToTable
from src.pipeline.prediction_metadata_task import PredictionMetadataTask
from src.utils.general import load_s3_object, predictions, get_db_credentials, select_predictions
from src.utils import constants

# PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_api_task AlmacenamientoApiTask --ingesta consecutiva --year 2021 --month 05 --day 23 --local-scheduler

class AlmacenamientoApiTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
       return {
        'PredictionMetadataTask': PredictionMetadataTask(self.ingesta, self.year, self.month, self.day, self.model_type)
         }

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'api.scores'

    columns = [("ID_INSPECTION",  "INTEGER"),
                ("DBA_NAME", "VARCHAR"),
                ("LICENSE", "INTEGER"),
                ("FACILITY_TYPE", "VARCHAR"),
                ("RISK", "VARCHAR"),
                ("ADDRESS", "VARCHAR"),
                ("ZIP", "INTEGER"),
                ("INSPECTION_DATE", "TIMESTAMP WITH TIME ZONE"),
                ("INSPECTION_TYPE", "VARCHAR"),
                ("VIOLATIONS", "VARCHAR"),
                ("GROUND_TRUTH", "SMALLINT"),
                ("SCORE", "NUMERIC"),
                ("LABEL", "INTEGER"),
                ("PREDICTIONS_DATE", "TIMESTAMP WITH TIME ZONE"),
                ("MODEL", "VARCHAR")]

    def rows(self):

        creds_file = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        preds = select_predictions(creds_file, delta_date)

        r = preds.to_records(index = False)

        for element in r:
            yield element
