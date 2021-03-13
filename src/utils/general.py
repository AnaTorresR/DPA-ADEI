import yaml
import pickle

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


def load_pickle_file(path):
    data_pkl = pickle.load(open(path, "rb"))
    return data_pkl


def save_pickle_file(df, path):
    # '/full/path/to/file'
    with open(path, 'wb') as f:
        pickle.dump(df, f)
        f.close()
    return
