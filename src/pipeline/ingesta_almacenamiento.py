import pandas as pd
from sodapy import Socrata


def get_client(dataset_domain, token):
    # domain_food = "data.cityofchicago.org"
    # dataset_id = "4ijn-s7e5"
    # limit_res = 2000

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    # client = Socrata(domain_food, None)

    # Example authenticated client (needed for non-public datasets):
    client = Socrata(dataset_domain, token)

    return client


def ingesta_inicial(client, dataset_id):
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    # results = client.get(dataset_id, limit=limit_res)
    results = client.get_all(dataset_id)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df


def get_s3_resource():
    pass


def guardar_ingesta():
    pass
