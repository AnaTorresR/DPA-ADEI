import luigi
import luigi.contrib.s3
from datetime import date
from datetime import timedelta
from src.pipeline.feature_engineering_metadata_task import FEMetadataTask
from src.utils.general import get_s3_credentials, load_pickle_file, select_semantic_features
from src.utils import constants
from src.utils.utils_notebook import train_test
import pickle

# PYTHONPATH='.' luigi --module src.pipeline.entrenamiento_task EntrenamientoTask --ingesta consecutiva --year 2021 --month 04 --day 07 --local-scheduler

class EntrenamientoTask(luigi.Task):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
       return {
        'FE_metadata_task' : FEMetadataTask(self.ingesta, self.year, self.month, self.day)
         }

    def output(self):

        s3_cred = get_s3_credentials('conf/local/credentials.yaml')

        s3_client = luigi.contrib.s3.S3Client(aws_access_key_id=s3_cred['aws_access_key_id'],
                                              aws_secret_access_key=s3_cred['aws_secret_access_key'])

        if self.ingesta == 'historica':
            train_path = 's3://{}/{}/{}-{}-{}-train.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)

            #test_path = 's3://{}/{}/{}-{}-{}-test.pkl'. \
             #  format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)

        elif self.ingesta == 'consecutiva':
            train_path = 's3://{}/{}-{}-{}-{}-train.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)

            #test_path = 's3://{}/{}-{}-{}-{}-test.pkl'. \
            #    format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        return luigi.contrib.s3.S3Target(path=train_path, client=s3_client, format=luigi.format.Nop)

    def run(self):

        credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_semantic_features(credentials, delta_date)

        train_df, test_df = train_test(df)

        with self.output().open('w') as train_file:
            pickle.dump(train_df, train_file)
