from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def re_categorize(text):
    """
    Reduces the number of categories in facility type by grouping them by hand-made similarity.

    Args:
        text (string): initial category of facility type

    Returns:
        cat (string): new simplified category
    """
    schools = ['school', 'care', 'kid', 'child', 'college']
    stands = ['stand', 'pop', 'kiosk', 'booth']
    bars = ['liquor', 'liqour', 'tavern', 'bar', 'pub']
    mobile = ['mobile', 'mobil', 'cart', 'truck']
    catering = ['cater', 'banquet', 'event']
    restaurants = ['restaurant']
    packaged = ['pack']
    store = ['store', 'convenien', 'gas', 'grocer', 'dollar']
    shop = ['shop']
    shared = ['shared', 'housing', 'gold']
    market = ['market']
    mart = ['mart']
    storage = ['storage', 'distribution center', 'pantry', 'warehouse']
    health = ['gym', 'herbal', 'herab', 'fitness', 'nutri', 'health', 'weight', 'exercise']
    unlicensed = ['unlicensed']

    slaughter = ['slaught', 'butch']
    culinary_class = ['culinary', 'cooking', 'class', 'pastry']

    if any(word in text for word in schools):
        cat = 'scholar'
    elif any(word in text for word in stands):
        cat = 'stand'
    elif any(word in text for word in mobile):
        cat = 'mobile'
    elif any(word in text for word in catering):
        cat = 'catering'
    elif any(word in text for word in restaurants):
        cat = 'restaurant'
    elif any(word in text for word in packaged):
        cat = 'prepackaged'
    elif any(word in text for word in store):
        cat = 'store'
    elif any(word in text for word in shop):
        cat = 'shop'
    elif any(word in text for word in shared):
        cat = 'shared'
    elif any(word in text for word in market):
        cat = 'market'
    elif any(word in text for word in mart):
        cat = 'mart'
    elif any(word in text for word in storage):
        cat = 'storage'
    elif any(word in text for word in bars):
        cat = 'bar'
    elif any(word in text for word in health):
        cat = 'health'
    elif any(word in text for word in unlicensed):
        cat = 'unlicensed'
    elif any(word in text for word in slaughter):
        cat = 'slaughter'
    elif any(word in text for word in culinary_class):
        cat = 'culinary_class'
    else:
        cat = 'other'

    return cat

def days_last_insp(df):
	df['last_inspection'] = df.sort_values(['license', 'inspection_date']).\
	groupby('license')['inspection_date'].diff()
	df.last_inspection.mask(df.last_inspection.isna(), "0", inplace=True)

	return df

def first_insp(df):
	df['first_inspection'] = df['last_inspection'].isnull().astype(int)
	return df

def create_label(df):
	df['label'] = df['results'].apply(lambda x: '1' if (x == 'pass' or x == 'pass w/ conditions') else '0')
	return df

def one_hot(data):
	ohe = OneHotEncoder(handle_unknown='ignore', categories= 'auto')
	categorical_cols = ['risk']

	array_hot_encoded = ohe.fit_transform(data[categorical_cols]).toarray()
	column_name = ohe.get_feature_names(categorical_cols)
	data_hot_encoded = pd.DataFrame(array_hot_encoded, index=data.index, columns= column_name)
	data_other_cols = data.drop(columns=categorical_cols)
	data_out = pd.concat([data_hot_encoded, data_other_cols], axis=1)
	return data_out

def feature_selection(df):
	df = df.drop(['license', 'address','city', 'state', 'results', 'latitude', 'longitude', 'inspection_id', 'dba_name', 'aka_name'], axis = 1)
	return df

def feature_engineering(df):
	df['facility_type'] = df.facility_type.apply (lambda row: re_categorize(row))
	df = days_last_insp(df)
	df = first_insp(df)
#	df = one_hot(df)
	df = create_label(df)
#	df['violations'] = df.violations.str.extract('(\d+)')
	df = feature_selection(df)

	return df
