import luigi
import luigi.contrib.s3
from src.pipeline.ingesta_task import IngestaTask
from src.pipeline.ingesta_metadata_task import IngestaMetadataTask
from src.utils.general import get_s3_credentials, load_pickle_file
from src.utils import constants
import pickle


# PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_task AlmacenamientoTask --ingesta historica --year 2021 --month 02 --day 18
    # PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_task AlmacenamientoTask --ingesta consecutiva --year 2021 --month 04 --day 15

class AlmacenamientoTask(luigi.Task):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {
        'ingesta_metadata_task' : IngestionMetadataTask(self.ingesta, self.year, self.month, self.day)
         }

    def output(self):

        s3_cred = get_s3_credentials('conf/local/credentials.yaml')

        s3_client = luigi.contrib.s3.S3Client(aws_access_key_id=s3_cred['aws_access_key_id'],
                                              aws_secret_access_key=s3_cred['aws_secret_access_key'])

        if self.ingesta == 'historica':
            output_path = 's3://{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            output_path = 's3://{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        return luigi.contrib.s3.S3Target(path=output_path, client=s3_client, format=luigi.format.Nop)

    def run(self):

        #with self.input()['ingesta_task'].open('rb') as fh:
        #    print("************************** tipo de input open {}".format(type(fh)))
        #    df_load = pickle.load(fh)
        #    print("************************** pickle load {}".format(type(df_load)))
        #    print("************************** pickle head {}".format(df_load.head(2)))

        if self.ingesta == 'historica':
            temp_path = 'temp/{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            temp_path = 'temp/{}/{}-{}-{}-{}.pkl'. \
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        df_load = load_pickle_file(temp_path)

        print(df_load.head(2))

        with self.output().open('w') as output_file:
            pickle.dump(df_load, output_file)
