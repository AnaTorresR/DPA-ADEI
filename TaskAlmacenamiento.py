# PYTHONPATH='.'  luigi --module TaskAlmacenamiento Task2 --ingesta consecutiva --year 2021 --month 03 --day 14
# PYTHONPATH='.' luigi --module TaskAlmacenamiento Task2 --ingesta historica --year 2021 --month 02 --day 18


import luigi
import luigi.contrib.s3
import boto3

from TaskIngesta import Task1
from src.pipeline.ingesta_almacenamiento import *
from src.utils.general import *


class Task2(luigi.Task):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()


    def requires(self):
        return Task1(self.ingesta, self.year,
        self.month,  self.day)

    def run(self):

        #path = '/Users/anatorres/Desktop/ITAM/data-product-architecture-equipo-6/ingestion/consecutive/consecutive-inspections-{}-{}-{}.pkl'.format(self.year, self.month, self.day)

        #with open(path, 'rb') as input_file:
        #    ingesta = pickle.load(input_file)

        #with self.output().open('wb') as output_file:
         #  pickle.dump(ingesta, output_file)

         with self.output().open('w') as output_file:
            output_file.write("prueba")

    def output(self):

        s3_creds = get_s3_credentials('conf/local/credentials.yaml')

        contribs = luigi.contrib.s3.S3Client(aws_access_key_id=s3_creds['aws_access_key_id'],
                     aws_secret_access_key=s3_creds['aws_secret_access_key'])

        if(self.ingesta == 'consecutiva'):
            output_path = 's3://data-product-architecture-equipo-6/ingestion/consecutive/consecutive-inspections-{}-{}-{}.pkl'.format(self.year, self.month, self.day)
            #output_path = '/Users/anatorres/Desktop/ITAM/DPA-food_inspections/luigi/consecutive-inspections-{}-{}-{}.pkl'.format(self.year, self.month, self.day)

        if (self.ingesta == 'historica'):
            output_path = 's3://data-product-architecture-equipo-6/ingestion/initial/historic-inspections-{}-{}-{}.pkl'.format(self.year, self.month, self.day)
            #output_path = '/Users/anatorres/Desktop/ITAM//DPA-food_inspections/luigi/historic-inspections-{}-{}-{}.pkl'.format(self.year, self.month, self.day)

        #return luigi.local_target.LocalTarget(path=output_path, format=luigi.format.Nop)
        return luigi.contrib.s3.S3Target(path= output_path,
         client = contribs)
