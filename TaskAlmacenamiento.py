# PYTHONPATH='.' luigi --module TaskAlmacenamiento Task2  --ingesta consecutiva --year 2021 --month 03 --day 14
# PYTHONPATH='.' luigi --module TaskAlmacenamiento Task2  --ingesta historica --year 2021 --month 02 --day 18


import os
import luigi

#import luigi.contrib.s3
#import boto3
#import joblib

from TaskIngesta import Task1
from src.pipeline.ingesta_almacenamiento import *
from src.utils.general import *


class Task2(luigi.Task):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return Task1(self.ingesta)

    def run(self):

        creds = get_api_token('conf/local/credentials.yaml')

        client = get_client(creds['api_token'])

        if (self.ingesta == 'consecutiva'):
            limit = 1000
            ingesta = ingesta_consecutiva(client, limit)

        if (self.ingesta == 'historica'):
            ingesta = ingesta_inicial(client)

        else:
            print('No such type of ingestion')

        with self.output().open('w') as output_file:
            output_file.write('Lista tu ingesta {}'. format(self.ingesta))

    def output(self):

        if(self.ingesta == 'consecutiva'):
            output_path = '/Users/anatorres/Desktop/ITAM/data-product-architecture-equipo-6/ingestion/consecutive/consecutive-inspections-{}-{}-{}.pkl'.\
            format(self.year, self.month, self.day)

        if (self.ingesta == 'historica'):
            output_path = '/Users/anatorres/Desktop/ITAM/data-product-architecture-equipo-6/ingestion/initial/historic-inspections-{}-{}-{}.pkl'.\
            format(self.year, self.month, self.day)

        return luigi.local_target.LocalTarget(path=output_path)
