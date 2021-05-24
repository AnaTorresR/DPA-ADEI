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

    def __init__(self, df, year, month, day, model_type):
        self.df = df
        self.year = year
        self.month = month
        self.day = day
        self.model_type = model_type

    msg_att = "El número de atributos a considerar no coincide con análisis previos."
    msg_col = "El número de métricas no coincide con los análisis anteriores."
    msg_row = "El almacenamiento está vacío, no contiene ninguna observación."
    msg_params = "No se puede analizar sesgo e inequidad de modelos futuros."
    msg_assist = "Nuestro modelo está pensado para utilizarse de manera asistiva."

    def test_attributes(self):
        attributes = self.df.attribute_name
        self.assertTrue(len(set(attributes)) == 3, msg = self.msg_att)

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 5, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_params(self):
        today = datetime.now()
        param = datetime.strptime("{}-{}-{}".format(self.day, self.month, self.year),
        "%d-%m-%Y")
        self.assertTrue(param <= today, msg = self.msg_params)

    def test_assist(self):
        self.assertTrue(self.model_type == 'assistive', msg = self. msg_assist,
        note = "Tu input: {}".format(self.model_type))


class TestPrediction(marbles.core.TestCase, mixins.BetweenMixins):

    def __init__(self, df, year, month, day, model_type):
        self.df = df
        self.year = year
        self.month = month
        self.day = day
        self.model_type = model_type

    msg_label = "La label predicha tiene que ser 0 ó 1."
    msg_score = "El score predicho tiene que estar entre 0 y 1."
    msg_ground = "La ground truth de la predicción tiene que ser 0 ó 1."
    msg_col = "El número de columnas no coincide con datos anteriores."
    msg_row = "La tabla results.predictions está vacía."
    msg_null = "Existen valores nulos en al menos una columna."
    msg_assist = "Nuestro modelo está pensado para utilizarse de manera asistiva."

    def test_label(self):
        good_labels = set([0,1])
        pred_labels = set(self.df.label)
        self.assertTrue(pred_labels.issubset(good_labels), msg = self.msg_label)

    def test_score(self):
        pred_scores = self.df.score.values
        self.assertBetween(pred_scores.all(), strict=False, lower=0, upper=1,
        msg = self.msg_score)

    def test_ground(self):
        good_ground = set([0,1])
        table_ground = set(self.df.ground_truth)
        self.assertTrue(table_ground.issubset(good_ground), msg = self.msg_ground)

    def test_num_columns(self):
        self.assertTrue(len(self.df.columns) == 14, msg = self.msg_col)

    def test_not_empty(self):
        self.assertTrue(len(self.df.index) > 0, msg = self.msg_row)

    def test_null(self):
        self.assertTrue(self.df.id_inspection.isna().sum() == 0, msg = self.msg_null,
        note = "Columna: id_inspection")
        self.assertTrue(self.df.score.isna().sum() == 0, msg = self.msg_null,
        note = "Columna: score")
        self.assertTrue(self.df.label.isna().sum() == 0, msg = self.msg_null,
        note = "Columna: label")
        self.assertTrue(self.df.ground_truth.isna().sum() == 0, msg = self.msg_null,
        note = "Columna: ground_truth")

    def test_assist(self):
        self.assertTrue(self.model_type == 'assistive', msg = self. msg_assist,
        note = "Tu input: {}".format(self.model_type))
