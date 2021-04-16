import luigi
from src.pipeline.ingesta_almacenamiento import get_client, ingesta_inicial, ingesta_consecutiva
from src.utils.general import get_api_token
from src.utils import constants
import pickle


# PYTHONPATH='.' luigi --module src.pipeline.ingesta_task IngestaTask --ingesta consecutiva --year 2021 --month 03 --day 24

class IngestaTask(luigi.Task):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def output(self):

        if self.ingesta == 'historica':
            output_path = 'temp/{}/{}-{}-{}-{}.pkl'.\
                format(constants.bucket_name, constants.initial_path, self.year, self.month, self.day)
        elif self.ingesta == 'consecutiva':
            output_path = 'temp/{}/{}-{}-{}-{}.pkl'.\
                format(constants.bucket_name, constants.concecutive_path, self.year, self.month, self.day)
        else:
            print('No such type of ingestion')

        return luigi.local_target.LocalTarget(path=output_path, format=luigi.format.Nop)

    def run(self):

        creds = get_api_token('conf/local/credentials.yaml')
        client = get_client(creds['api_token'])

        if self.ingesta == 'historica':
            print("dentro de historica")
            df_ing = ingesta_inicial(client)
        elif self.ingesta == 'consecutiva':
            print("dentro de consecutiva")
            limit = 1000
            df_ing = ingesta_consecutiva(client, limit)
        else:
            print('No such type of ingestion')

        with self.output().open('wb') as output_file:
            pickle.dump(df_ing, output_file)
