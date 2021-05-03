import luigi
import luigi.contrib.s3
from datetime import date
from datetime import timedelta
from src.pipeline.seleccion_modelo_metadata_task import SeleccionModeloMetadataTask
from src.utils.general import *
from src.utils import constants
import pickle

## PYTHONPATH='.' luigi --module src.pipeline.aequitas_task AequitasTask --ingesta consecutiva --year 2021 --month 05 --day 03 --local-scheduler

class AequitasTask(luigi.Task):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()
    model_type = luigi.Parameter(default= 'assistive')

    def requires(self):
        return SeleccionModeloMetadataTask(self.ingesta, self.year, self.month, self.day)

    def output(self):

        s3_cred = get_s3_credentials('conf/local/credentials.yaml')

        s3_client = luigi.contrib.s3.S3Client(aws_access_key_id=s3_cred['aws_access_key_id'],
                                              aws_secret_access_key=s3_cred['aws_secret_access_key'])

        if self.ingesta == 'historica':
            output_path = 's3://{}/{}-{}-{}-{}-aequitas.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)

        elif self.ingesta == 'consecutiva':
            output_path = 's3://{}/{}-{}-{}-{}-aequitas.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)

        else:
            print('No such type of ingestion')

        return luigi.contrib.s3.S3Target(path=output_path, client=s3_client, format=luigi.format.Nop)

    def run(self):

        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        if self.ingesta == 'historica':
            model_key = '{}-{}-{}-{}-modelo.pkl'.format(constants.initial_path, self.year, self.month, self.day)

            train_key =  '{}-{}-{}-{}-train.pkl'.format(constants.initial_path, self.year, self.month, self.day)

        elif self.ingesta == 'consecutiva':
            model_key = '{}-{}-{}-{}-modelo.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)

            train_key = '{}-{}-{}-{}-train.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        aequitas_pre = aequitas_preprocessing(credentials, delta_date, train_key, model_key)

        aequitas_table = aequitas(aequitas_pre)

        with self.output().open('w') as output_file:
            pickle.dump(aequitas_table, output_file)
