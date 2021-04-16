import pandas as pd
import luigi
import psycopg2
import yaml
import pickle

from luigi.contrib.postgres import CopyToTable
from src.utils import constants


class Task1(CopyToTable):

    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {'ingesta_task': IngestaTask(self.ingesta,
                                            self.year,
                                            self.month,
                                            self.day)}


    if self.ingesta == 'historica':
        data = pickle.load(open('temp/{}/{}-{}-{}-{}.pkl'.\
                format(constants.bucket_name,
                       constants.initial_path,
                       self.year,
                       self.month,
                        self.day),
                         'rb'))
    elif self.ingesta == 'consecutiva':
        data = pickle.load(open('temp/{}/{}-{}-{}-{}.pkl'.\
                format(constants.bucket_name,
                       constants.concecutive_path,
                       self.year,
                       self.month,
                        self.day),
                        'rb'))
    else:
        print('No such type of ingestion')

    n_cols = data.shape[1]
    n_rows = data.shape[0]

    get_db_conn('conf/local/credentials.yaml')

    #user = credentials['user']
    #password = credentials['pass']
    #database = credentials['db']
    #host = credentials['host']
    #port = credentials['port']

    table = 'metadata'

    columns = [("Task", "VARCHAR"),
               ("Date", "TIMESTAMP WITH TIMEZONE"),
               ("Author", "VARCHAR"),
               ("N_COLS", "INTEGER"),
               ("N_ROWS", "INTEGER")
               ]

    def rows(self):
        date = str(self.day + '-' + self.month + '-' + self.year)
        r = [("Ingesta", date , 'Equipo 2', n_cols, n_rows)]
        for element in r:
            yield element
