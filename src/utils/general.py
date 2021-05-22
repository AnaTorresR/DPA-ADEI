import yaml
import pickle
import pandas as pd
import psycopg2
import boto3
import numpy as np
from datetime import date
from datetime import timedelta
from sklearn.model_selection import GridSearchCV
#from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier
from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness
from aequitas.plotting import Plot
from aequitas.preprocessing import preprocess_input_df
from src.utils.utils_notebook.train_test import train_test, train_test_original

def read_yaml_file(yaml_file):
    """ load yaml cofigurations """

    config = None
    try:
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Couldnt load the file')

    return config


def get_api_token(credentials_file):
    credentials = read_yaml_file(credentials_file)
    api_creds = credentials['food_inspections']
    return api_creds


def get_s3_credentials(credentials_file):
    credentials = read_yaml_file(credentials_file)
    s3_creds = credentials['s3']
    return s3_creds

def get_db_credentials(creds_file):
    credentials = read_yaml_file(creds_file)
    db_creds = credentials['db']
    return db_creds

def get_db_conn(creds_file):
    creds = read_yaml_file(creds_file)['db']

    connection = psycopg2.connect(
        user=creds['user'],
        password=creds['pass'],
        host=creds['host'],
        port=creds['port'],
        database=creds['db']
    )
    return connection

def load_s3_object(creds_file, key):

    s3_creds = get_s3_credentials(creds_file)

    session = boto3.Session(
    aws_access_key_id=s3_creds['aws_access_key_id'],
    aws_secret_access_key=s3_creds['aws_secret_access_key']
    )

    s3 = session.client('s3')

    response = s3.get_object(Bucket='data-product-architecture-equipo-6',
    Key =key)
    body = response['Body'].read()
    df = pickle.loads(body)
    return df

def load_pickle_file(path):
    data_pkl = pickle.load(open(path, "rb"))
    return data_pkl

def save_pickle_file(df, path):
    # '/full/path/to/file'
    with open(path, 'wb') as f:
        pickle.dump(df, f)
        f.close()
    return

def select_clean_features(creds, date):

    con = get_db_conn(creds)
    q = """
    select *
    from
        clean.features
    where
        inspection_date >= '{}'
    """.format(date)

    df = pd.read_sql(q, con)
    return df

def select_semantic_features(creds,date):
    con = get_db_conn(creds)
    q = """
    select
       facility_type,
       risk,
       zip,
       inspection_date,
       inspection_type,
       case when (violations = 'nan') then '0' else violations end as violations,
       last_inspection,
       first_inspection,
       label
    from
        semantic.features
    where
        inspection_date >= '{}'
    """.format(date)

    df = pd.read_sql(q, con)
    return df

def select_predictions(creds, date):

    con = get_db_conn(creds)
    q = """
    select *
    from
        results.predictions
    where
        predictions_date >= '{}'
    """.format(date)

    df = pd.read_sql(q, con)
    return df

def modeling(df):

    X = df.loc[:, df.columns != 'label']

    y = df.label

    np.random.seed(19960311)

    classifier = RandomForestClassifier(oob_score=True, random_state=1234)

    hyper_param_grid = {'n_estimators': [100, 200],
                    'max_depth': [5, 10, 15],
                    'min_samples_split': [10, 20]}

    gs = GridSearchCV(classifier,
                 hyper_param_grid,
                 scoring = 'precision',
                 cv = 5,
                 n_jobs = -1)

    modelos = gs.fit(X, y)
    modelo_bueno = modelos.best_estimator_

    return modelo_bueno

def aequitas_preprocessing(creds, date, train_key, model_key):

    datos = select_semantic_features(creds, date)
    train = load_s3_object(creds, train_key)
    modelo = load_s3_object(creds, model_key)

    X_train = train.loc[:, train.columns != 'label']
    y_train = train.label

    modelo_predicciones = modelo.predict(X_train)
    modelo_predicted_scores = modelo.predict_proba(X_train)

    preds = pd.DataFrame(modelo_predicted_scores[:, 1], columns=['score'])
    data = pd.concat([datos, preds], axis = 1)
	# Precisión 97
    data['score'] = data['score'].apply(lambda x: '0' if x < 0.665264 else '1')

    data= data.drop(['zip', 'inspection_date', 'last_inspection', 'first_inspection'], axis = 1)
    data = data.rename(columns = {'label': 'label_value'})
    data['label_value'] = data['label_value'].astype('str')
#    data = data.dropna()
    data = data.drop('violations', axis =1)

    return data


def aequitas(df):

    df_top, _ = preprocess_input_df(df)

    df_top['label_value']=df_top['label_value'].astype(float)
    df_top['score']=df_top['score'].astype(int)

    g = Group()
    xtab, attrbs = g.get_crosstabs(df_top)

    bias = Bias()

    bdf = bias.get_disparity_predefined_groups(xtab, original_df=df_top,
          ref_groups_dict={'facility_type':'restaurant', 'risk':'risk 1 (high)', 'inspection_type':'canvass'},
          alpha=0.05)

    sesgo = bdf[['attribute_name', 'attribute_value'] + bias.list_disparities(bdf)].round(2)
    sesgo = sesgo[['attribute_name', 'attribute_value', 'for_disparity', 'fnr_disparity', 'tpr_disparity']]

    return sesgo


def predictions(creds, model_key, date):

    # Test
    delta_date = date - timedelta(days=7)
    df = select_semantic_features(creds, delta_date)
    train_df, test_df = train_test(df)

    # Loading model
    modelo = load_s3_object(creds, model_key)

    # Predictions
    X_test = test_df.loc[:, test_df.columns != 'label']
    y_test = test_df.label
    modelo_predicciones = modelo.predict(X_test)
    modelo_predicted_scores = modelo.predict_proba(X_test)
    preds = pd.DataFrame(modelo_predicted_scores[:, 1], columns=['score'])
    preds['label'] = preds['score'].apply(lambda x: '0' if x < 0.665264 else '1')

    #Joining preds with original data
    dfc = select_clean_features(creds, delta_date)
    train_orig, test_orig = train_test_original(dfc)
    data = pd.concat([test_orig, preds], axis = 1)
    data = data[['inspection_id', 'dba_name', 'score', 'label']]
    data['ground_truth'] = y_test
    data['predictions_date'] = str(delta_date + timedelta(days=7))
    data = data[['inspection_id', 'dba_name', 'ground_truth', 'score', 'label', 'predictions_date']]

    return data
