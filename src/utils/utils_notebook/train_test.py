import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def one_hot(data):
    ohe = OneHotEncoder(handle_unknown='ignore', categories= 'auto')
    categorical_cols = ['risk','facility_type', 'inspection_type']

    array_hot_encoded = ohe.fit_transform(data[categorical_cols]).toarray()
    column_name = ohe.get_feature_names(categorical_cols)
    data_hot_encoded = pd.DataFrame(array_hot_encoded, index=data.index, columns= column_name)
    data_other_cols = data.drop(columns=categorical_cols)
    data_out = pd.concat([data_hot_encoded, data_other_cols], axis=1)
    return data_out

def split(data):
    """70% train 30% test"""
    train_size = round(datos.shape[0]*0.70)
    test_size = round(datos.shape[0]*0.30)

    train = pd.DataFrame(data.head(train_size)).reset_index(drop=True)
    test = pd.DataFrame(data.tail(test_size)).reset_index(drop=True)

    #X_train = train.loc[:, train.columns != 'label']

    #y_train = train.label

    #X_test = test.loc[:, test.columns != 'label']

    #y_test = test.label

    return train, test

def train_test(data):
    df = one_hot(data)
    df = split(df)
    return df

