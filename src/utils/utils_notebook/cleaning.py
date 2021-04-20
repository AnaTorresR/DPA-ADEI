import pandas as pd
import unicodedata
import numpy 


def cla(col):
    return col.lower().replace('/', '_').replace(' ', '_').replace('ñ', 'n')


def clean_column(data):
    data.rename(columns={col: cla(col) for col in data.columns.values}, inplace=True)
    return data

def changeType(data, list_Col, d_type):
    for name in list_Col:
        data[name] = data[name].astype(d_type)
    return data

def changeType_date(df):
    df['inspection_date'] = pd.to_datetime(df['inspection_date'])
    return df

def convert_lower(data, vars_lower):
    """
     Converting observatios for selected columns into lowercase.
        args:
            data (dataframe): data that is being analyzed.
            vars_lower (list): list of the columns' names in the dataframe that will be changed to lowercase.
        returns:
            data(dataframe): dataframe that is being analyzed with the observations (of the selected columns) in lowercase.
    """
    for i in vars_lower:
        data[i] = data[i].str.lower()
    return data

def fix_dates(df):
	"""Fixes date format"""
	listFecha = ["inspection_date"]
	date_format = "mm/dd/aaaa"
	type_format = '%m/%d/%Y'

	changeType_date(df,listFecha, type_format)

	return df

def lowercase(df):
	df['address'] = df.address.str.lower()
	df['facility_type'] = df.facility_type.str.lower()
	df['risk'] = df.risk.str.lower()
	df['city'] = df.city.str.lower()
	df['state'] = df.state.str.lower()
	df['inspection_type'] = df.inspection_type.str.lower()
	df['results'] = df.results.str.lower()
	df['violations'] = df.violations.str.lower()
	df['dba_name'] = df.dba_name.str.lower()
	df['aka_name'] = df.aka_name.str.lower()

	return df

def fix_typos(typo):
    """
    Evaluates if a typo was made while writing the word "chicago" or if the word
    is entirely different by comparing the set of characters of each word.
    Args:
        typo (string): string to evaluate
    Returns:
        string (string): "chicago" if its a typo, the original string otherwise
    """

    string = "chicago"

    if len(set(string) & set(typo)) >=  5:
        pass
    else:
        string = typo

    return string

def imputations(df):
	"""Imputations of missing data"""
	df.facility_type.mask(df.facility_type.isna(), "other", inplace=True)
	df.city.mask(df.city.isna(), "chicago", inplace=True)
	df.state.mask(df.city.isna(), "il", inplace=True)
	df.aka_name.mask(df.aka_name.isna(), df.dba_name, inplace=True)
	df.violations.mask(df.violations.isna(), '0', inplace=True)
	df.zip.mask(df.zip.isna(), '0', inplace=True)
	return df

def cleaning(pkl):
	df = clean_column(pkl)
	df = changeType_date(df)
	df = lowercase(df)
	df = imputations(df)
	df['city'] = df.city.apply (lambda row: fix_typos(row))
	df = df.drop('location', axis = 1)
	return df
