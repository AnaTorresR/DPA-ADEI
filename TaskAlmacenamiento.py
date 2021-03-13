# PYTHONPATH='.' luigi --module TaskAlmacenamiento Task2  --ingesta consecutiva --year 2021 --month MARZO

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

        return luigi.local_target.\
        LocalTarget('/Users/anatorres/Desktop/ITAM/DPA-food_inspections/luigi/YEAR={}/MONTH={}/ingesta_{}.csv'.\
        format(self.year, str(self.month), self.ingesta))
