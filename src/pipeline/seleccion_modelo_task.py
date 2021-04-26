import luigi
import luigi.contrib.s3
from src.pipeline.entrenamiento_metadata_task import EntrenamientoMetadataTask
from src.utils.general import get_s3_credentials, load_s3_object, modeling
from src.utils import constants
import pickle

class SeleccionModeloTask(luigi.Task):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {
        'entrenamiento_metadata_task' : EntrenamientoMetadataTask(self.ingesta, self.year, self.month, self.day)
         }

    def output(self):

        s3_cred = get_s3_credentials('conf/local/credentials.yaml')

        s3_client = luigi.contrib.s3.S3Client(aws_access_key_id=s3_cred['aws_access_key_id'],
                                              aws_secret_access_key=s3_cred['aws_secret_access_key'])

        if self.ingesta == 'historica':
            output_path = 's3://{}/{}-{}-{}-{}-modelo.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            output_path = 's3://{}/{}-{}-{}-{}-modelo.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        return luigi.contrib.s3.S3Target(path=output_path, client=s3_client, format=luigi.format.Nop)

    def run(self):
        if self.ingesta == 'historica':
            key = '{}-{}-{}-{}-train.pkl'.format(constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            key = '{}-{}-{}-{}-train.pkl'.format(constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        creds_file = 'conf/local/credentials.yaml'

        df = load_s3_object(creds_file, key)

        df_load = modeling(df)

        with self.output().open('w') as output_file:
            pickle.dump(df_load, output_file)
