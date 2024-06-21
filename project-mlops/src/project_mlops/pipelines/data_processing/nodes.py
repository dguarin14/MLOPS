"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.4
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


def map_data(df, column, values):
    df[column] = df[column].map({values[0]: 1.0, values[1]: 0.0})
    return df[column]

def replace_value(name_column, replace_v, new_value, df):
    for i in replace_v:
        df[name_column] = df[name_column].replace(i, new_value)
    return df[name_column]

def hot_dummies(categorical, df,num):
    df_dummies = pd.get_dummies(df[categorical]).astype(float)
    for i in num:
        df_dummies[i]= df[i]
    return df_dummies

def scaleit(df,columns):
    min_max = MinMaxScaler().fit(df[columns])
    min_max_X = min_max.transform(df[columns])
    pandas_min_max = pd.DataFrame(min_max_X, columns=columns)
    for i in columns:
        df[i] = pandas_min_max[i]
    return df

def preprocess_credit(credit_data):

    categorical_features = credit_data.select_dtypes(include=['object']).columns
    numerical_features = credit_data.select_dtypes(include=['float64']).columns
    credit_data['own_telephone'] = map_data(credit_data, 'own_telephone', ['yes','none'])
    credit_data['foreign_worker'] = map_data(credit_data, 'foreign_worker', ['yes','no'])  
    credit_data['class'] = map_data(credit_data, 'class', ['good','bad']) 
    to_add = ['own_telephone','foreign_worker', 'class']
    categorical_features = credit_data.select_dtypes(include=['object']).columns
    credit_data['credit_history'] = replace_value('credit_history',['no credits/all paid'],'all paid', credit_data)
    credit_data['purpose'] = replace_value('purpose',['retraining','domestic appliance','repairs'],'other', credit_data)
    cf = categorical_features.to_numpy()
    cf2 = cf[:-1]
    df = hot_dummies(cf2, credit_data, numerical_features)
    df_scale = scaleit(df, numerical_features)
    for i in to_add:
        df_scale[i]= credit_data[i]

    return df_scale
