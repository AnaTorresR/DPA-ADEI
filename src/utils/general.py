import yaml
import pickle
import numpy as np
import psycopg2
import boto3
import pandas as pd

from sklearn.model_selection import GridSearchCV
#from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier

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
    select *
    from
        semantic.features
    where
        inspection_date >= '{}'
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
