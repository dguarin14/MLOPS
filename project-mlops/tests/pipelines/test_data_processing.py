import pytest
import pandas as pd
import numpy as np

from src.project_mlops.pipelines.data_processing.nodes import replace_value, scaleit, map_data, preprocess_credit



def test_map_data():
    names = ['John', 'Jane', 'Alex', 'Emily', 'Michael']
    ages = [28, 22, 35, 29, 42]
    sick = ['Yes', 'No', 'No', 'Yes', 'Yes']

    # Initialize the DataFrame
    df = pd.DataFrame({
        'name': names,
        'age': ages,
        'sick': sick
    })
    value_compare = map_data(df, 'sick', ['Yes','No'])
    print(value_compare.unique())
    assert (len(value_compare.unique())==2)
    assert(np.array_equal(value_compare.unique(), [1.0, 0.0]))

def test_replace_value():
    names = ['John', 'Jane', 'Alex', 'Emily', 'Michael']
    ages = [28, 22, 35, 29, 42]
    sick = ['Yes', 'No', 'No', 'Yes', 'Yes']

    # Initialize the DataFrame
    df = pd.DataFrame({
        'name': names,
        'age': ages,
        'sick': sick
    })

    value_compare = replace_value('sick', ['Yes'], 'No', df)
    assert (len(value_compare.unique())==1)
    assert(np.array_equal(value_compare.unique(), ['No']))

def test_scaleit():
    names = ['John', 'Jane', 'Alex', 'Emily', 'Michael']
    ages = [28, 22, 35, 29, 42]
    sick = ['Yes', 'No', 'No', 'Yes', 'Yes']
    study = [1,2,3,4,5]

    # Initialize the DataFrame
    df = pd.DataFrame({
        'name': names,
        'age': ages,
        'sick': sick,
        'study': study
    })
    value_compare = scaleit(df,['age','study'])
    assert (np.all(value_compare['age'].unique() <= 1))
    assert (np.all(value_compare['study'].unique() <= 1))
    
def test_data_processing():
    names = ['John', 'Jane', 'Alex', 'Emily', 'Michael']
    ages = [28.0, 22.0, 35.0, 29.0, 42.0]
    own_telephone = ['Yes', None, None, 'Yes', 'Yes']
    study = ['yes','yes','no','no','yes']
    classe = ['good','bad','good','bad','good']
    credit = ['all paid', 'yes', 'no credits/all paid', 'no credits/all paid', 'no credits/all paid']
    purpose = ['other', 'restraining', 'domestic appliance', 'repairs', 'yes']

    # Initialize the DataFrame
    df = pd.DataFrame({
        'name': names,
        'own_telephone': own_telephone,
        'age': ages,
        'foreign_worker': study,
        'class': classe,
        'credit_history': credit,
        'purpose': purpose
    })

    value = preprocess_credit(df)
    assert(value.dtypes.apply(lambda x: x == 'float64').all() )
