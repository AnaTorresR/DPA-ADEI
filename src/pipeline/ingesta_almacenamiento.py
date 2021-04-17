import pandas as pd
from sodapy import Socrata
from datetime import date
from datetime import timedelta
import boto3
import pickle
from src.utils.general import *
from src.utils import constants


def get_client(token):
    # Example authenticated client (needed for non-public datasets):
    # extraemos el data set domain de nuestro script src/utils/constants
    dataset_domain = constants.dataset_domain
    client = Socrata(dataset_domain, token)

    return client


def ingesta_inicial(client):
    # Returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.

    # se pasa el data_set identifier para obtener los datos
    # regresa todos los registros que existan hasta el momento
    # para este proyecto el data set cuenta con mas menos 216k de registros

    # extraemos el dataset identifier de nuestro script src/utils/constants
    dataset_id = constants.dataset_id
    ###print(dataset_id)
    results = client.get_all(dataset_id)
    results_df = pd.DataFrame.from_records(results)

    # Serializar objeto obtenido de resultados
    # obj_to_upload = pickle.dumps(results_df)
    ### obj_to_upload = pickle.dumps(results_df)

    # configuración  para la carga en s3 bucket
    # bucket_name = "data-product-architecture-equipo-6"
    # se extrae el nombre del bucket de nuestro script src/utils/constants
    # bucket_name = constants.bucket_name
    # bucket_path = "ingestion/initial/historic-inspections-{}.pkl".format(str(date.today()))

    # se llama a función guardar ingesta
    # guardar_ingesta(bucket_name, bucket_path, obj_to_upload)
    ### bucket_name = constants.bucket_name
    ### bucket_path = "ingestion/initial/historic-inspections-{}.pkl".format(str(date.today()))

    # se llama a función guardar ingesta
    ### guardar_ingesta(bucket_name, bucket_path, obj_to_upload)

    return results_df


def ingesta_consecutiva(client, limit):
    # se utiliza timedelta para restar 7 dias al dia de hoy
    # para traer semanalmente los delta registros
    today = date.today()
    delta_date = today - timedelta(days=7)
    print(delta_date)

    # extraemos el dataset identifier de nuestro script src/utils/constants
    dataset_id = constants.dataset_id

    # se hace un where con la seleccion de 7 dias antes para traer deltas
    results = client.get(dataset_id, where="inspection_date >= '{}'".format(delta_date), limit=limit)
    results_df = pd.DataFrame.from_records(results)

    # Serializar objeto obtenido de resultados
    # obj_to_upload = pickle.dumps(results_df)
    ###obj_to_upload = pickle.dumps(results_df)

    # configuración  para la carga en s3 bucket
    # bucket_name = "data-product-architecture-equipo-6"
    # se extrae el nombre del bucket de nuestro script src/utils/constants
    # bucket_name = constants.bucket_name
    # bucket_path = "ingestion/consecutive/consecutive-inspections-{}.pkl".format(str(today))

    # se llama a función gradar ingesta
    # guardar_ingesta(bucket_name, bucket_path, obj_to_upload)
    ###bucket_name = constants.bucket_name
    ###bucket_path = "ingestion/consecutive/consecutive-inspections-{}.pkl".format(str(today))

    # se llama a función gradar ingesta
    ###guardar_ingesta(bucket_name, bucket_path, obj_to_upload)

    return results_df

def get_s3_resource(aws_creds):
    s3_creds = get_s3_credentials(aws_creds)
    session = boto3.Session(
        aws_access_key_id=s3_creds["aws_access_key_id"],
        aws_secret_access_key=s3_creds["aws_secret_access_key"]
    )

    return session.client('s3')


def guardar_ingesta(bucket_name, bucket_path, obj_to_upload):
    s3_resource = get_s3_resource()

    # accedemos a client desde el resource y se hace upload de documentos
    # s3_resource.meta.client.upload_file(file_to_upload, bucket_name, bucket_path)

    # esto es para guardar objetos
    bucket_name = constants.bucket_name

    s3_resource.put_object(Bucket=bucket_name, Key=bucket_path, Body=obj_to_upload)

    return
