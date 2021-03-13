#PYTHONPATH='.' luigi --module TaskIngestas Task1 --local-scheduler --ingesta consecutiva

import luigi

class Task1(luigi.Task):

    ingesta = luigi.Parameter()

    def run(self):

        with self.output().open('w') as output_file:
            output_file.write("La ingesta que deseas almacenar es {}".format(self.ingesta))

    def output(self):
        return luigi.local_target.LocalTarget('/Users/anatorres/Desktop/ITAM/DPA-food_inspections/ingesta_{}.csv'.format(self.ingesta))
