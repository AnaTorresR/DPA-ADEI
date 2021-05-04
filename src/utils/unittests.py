import marbles.core
import pandas as pd
import pickle
from datetime import date, datetime
from marbles.mixins import mixins
from src.utils.general import load_pickle_file


class TestIngesta(marbles.core.TestCase,  mixins.CategoricalMixins, mixins.FileMixins, marbles.mixins.DateTimeMixins):

    def __init__(self, path, year, month, day):
        self.path = path
        self.year = year
        self.month = month
        self.day = day
        self.RISKS = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'All']
        self.df = load_pickle_file(path)

    msg_file = "El archivo pkl de ingesta no existe."
    msg_risks = "Los niveles de Risks de la nueva ingesta no coinciden con los datos anteriores."
    msg_date = "La ingesta contiene datos del futuro o del pasado."
    msg_col = "El número de columnas no coincide con los datos anteriores."
    msg_row = "La ingesta está vacía, no contiene ninguna observación."
    msg_params = "No se pueden ingestar datos del futuro."

    def test_file_exits(self):
        self.assertFileExists(self.path, msg = self.msg_file)

    def test_categories_risks(self):
        A = set(self.df['risk'])
        A = {x for x in A if pd.notna(x)}
        B = set(self.RISKS)
        self.assertTrue(A.issubset(B), msg= self.msg_risks)

    def test_inspection_date_future(self):
        today = date.today()
        dates = pd.to_datetime(self.df['inspection_date'])
        self.assertDateTimesBefore(dates, today, msg = self.msg_date)

    def test_inspection_date_past(self):
        first_insp = datetime.strptime( '04-01-2021', "%d-%m-%Y")
        dates = pd.to_datetime(self.df['inspection_date'])
        self.assertDateTimesAfter(dates, first_insp, msg = self.msg_date)

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 17, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_params(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today, msg = self.msg_params)

class TestAlmacenamiento(marbles.core.TestCase, marbles.mixins.DateTimeMixins):

    def __init__(self, df, year, month, day):
        self.df = df
        self.year = year
        self.month = month
        self.day = day

    RISKS = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'All']

    msg_risks = "Los niveles de Risks de la nueva ingesta no coinciden con los datos anteriores."
    msg_date = "El almacenamiento contiene datos del futuro o del pasado. Revisar la ingesta."
    msg_col = "El número de columnas no coincide con los datos anteriores."
    msg_row = "El almacenamiento está vacío, no contiene ninguna observación. Revisar ingesta."
    msg_params = "No se pueden ingestar datos del futuro."

    def test_categories_risks(self):
        A = set(self.df['risk'])
        A = {x for x in A if pd.notna(x)}
        B = set(self.RISKS)
        self.assertTrue(A.issubset(B), msg= self.msg_risks)

    def test_inspection_date_future(self):
        today = date.today()
        dates = pd.to_datetime(self.df['inspection_date'])
        self.assertDateTimesBefore(dates, today, msg = self.msg_date,
        note="Fechas de inspección mayores a las de hoy.")

    def test_inspection_date_past(self):
        first_insp = datetime.strptime( '04-01-2021', "%d-%m-%Y")
        dates = pd.to_datetime(self.df['inspection_date'])
        self.assertDateTimesAfter(dates, first_insp, msg = self.msg_date,
        note = "Fechas de inspección previas al inicio de las inspecciones.")

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 17, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_params(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today, msg = self.msg_params)

class TestCleaning(marbles.core.TestCase):

    def __init__(self, df, year, month, day):
        self.df = df
        self.year = year
        self.month = month
        self.day = day

    msg_low = """Existen datos en el data frame con texto que utiliza mayúsuclas.
    Es necasario que todo esté en minúsculas"""
    msg_nas = "El data frame tiene valores faltantes. Revisar que la imputación se hizo correctamente."
    msg_col = "El número de columnas no coincide con los datos anteriores."
    msg_row = "El almacenamiento está vacío, no contiene ninguna observación"
    msg_params = "No se pueden ingestar datos del futuro."

    def test_lower(self):
        risks = self.df.risk
        results = self.df.results
        facilities = self.df.facility_type
        cities = self.df.city
        self.assertTrue(set(risks) == set(risks.str.lower()), msg = self.msg_low, note = "Columna: risk")
        self.assertTrue(set(results) == set(results.str.lower()), msg = self.msg_low, note = "Columna: results")
        self.assertTrue(set(facilities) == set(facilities.str.lower()), msg = self.msg_low, note ="Columna: facility_type")
        self.assertTrue(set(cities) == set(cities.str.lower()), msg = self.msg_low, note = "Columna: city")

    def test_not_nas(self):
        facilities = self.df.facility_type
        cities = self.df.city
        self.assertFalse(facilities.isna().values.any(), msg = self.msg_nas, note = "Columna: facility_type")
        self.assertFalse(cities.isna().values.any(), msg = self.msg_nas, note = "Columna: city")

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 16, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_params(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today, msg = self.msg_params)

class TestAequitas(marbles.core.TestCase):

    def __init__(self, df, year, month, day):
        self.df = df
        self.year = year
        self.month = month
        self.day = day

    msg_att = "El número de atributos a considerar no coincide con análisis previos."
    msg_col = "El número de métricas no coincide con los análisis anteriores."
    msg_row = "El almacenamiento está vacío, no contiene ninguna observación."
    msg_params = "No se puede analizar sesgo e inequidad de modelos futuros."

    def test_attributes(self):
        attributes = self.df.attribute_name
        self.assertTrue(len(set(attributes)) == 3, msg = self.msg_att)

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 6, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_params(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today, msg = self.msg_params)
