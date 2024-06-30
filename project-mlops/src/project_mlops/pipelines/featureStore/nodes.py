"""
This is a boilerplate pipeline 'featureStore'
generated using Kedro 0.19.6
"""
import logging
from typing import Any, Dict, Tuple

import numpy as np # type: ignore
import pandas as pd # type: ignore

from great_expectations.core import ExpectationSuite, ExpectationConfiguration # type: ignore

from pathlib import Path

from kedro.config import OmegaConfigLoader # type: ignore
from kedro.framework.project import settings # type: ignore
import hopsworks # type: ignore

def build_expectations(name, type, columns):

    value = {'checking_status' : ['<0', '0<=X<200', 'no checking', '>=200'],
     'credit_history': ['critical/other existing credit', 'existing paid', 'delayed previously',
 'no credits/all paid', 'all paid'],
     'purpose':['radio/tv', 'education', 'furniture/equipment', 'new car', 'used car',
 'business', 'domestic appliance', 'repairs', 'other', 'retraining'],
     'savings_status':['no known savings', '<100', '500<=X<1000', '>=1000', '100<=X<500'],
     'employment':['>=7', '1<=X<4', '4<=X<7', 'unemployed', '<1'],
     'personal_status':['male single', 'female div/dep/mar', 'male div/sep', 'male mar/wid'],
     'other_parties':['none', 'guarantor', 'co applicant'],
    'property_magnitude':['real estate', 'life insurance', 'no known property', 'car'],
    'other_payment_plans':['none', 'bank', 'stores'],
    'housing':['own', 'for free', 'rent'],
    'job':['skilled', 'unskilled resident', 'high qualif/self emp/mgmt',
 'unemp/unskilled non res'],
    'own_telephone':['yes', 'none'],
    'foreign_worker':['yes', 'no']   
    }

    expectation_suite_bank = ExpectationSuite(
        expectation_suite_name= name
    )
    
    if type == 'numerical':
        columns = ['duration', 'credit_amount', 'installment_commitment',
       'residence_since', 'age', 'existing_credits', 'num_dependents']
        for i in columns:
            expectation_suite_bank.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_values_to_be_of_type",
                            kwargs={"column": i, "type_": "float64"},
                        )
                    )
    elif type == 'categorical':
        for i in columns:
            expectation_suite_bank.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_distinct_values_to_be_in_set",
                            kwargs={"column": i, "value_set": value[i]},
                        )
                    )
    else:
        print(type)
        expectation_suite_bank.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_distinct_values_to_be_in_set",
                            kwargs={"column": 'class', "value_set": ['good' 'bad']},
                        )
                    )
    return expectation_suite_bank

def save_feature_store(df, group_name, expectations,feature_group_version,description, ):
    print(df.index)
    project = hopsworks.login(
        api_key_value="SdmqGu8BDdngCQsZ.b1fUsORi1IuRzIKsu7sEKPfcVk3wNxiZk7wL7tKUlbS5BHJzwrsf82e8idCdUcNU", project="mlopsDALI"
    )
    feature_store = project.get_feature_store()

    object_feature_group = feature_store.get_or_create_feature_group(
        name=group_name,
        version=feature_group_version,
        description= description,
        primary_key=["index"],
        online_enabled=False,
        expectation_suite=expectations,
    )
    object_feature_group.insert(
        features=df,
        overwrite=False,
        write_options={
            "wait_for_job": True,
        },
    )
    object_feature_group.statistics_config = {
        "enabled": True,
        "histograms": True,
        "correlations": True,
    }
    object_feature_group.update_statistics_config()
    object_feature_group.compute_statistics()

    return object_feature_group


def feature_hopswork(df):
    
    categorical_features = df.select_dtypes(include=['object']).columns
    numerical_f = df.select_dtypes(include=['float64']).columns
    categorical_f = categorical_features[:-1]

    validation_expectation_numerical = build_expectations("numerical_expectation","numerical", numerical_f)
    validation_expectation_categorical = build_expectations("categorical_expectations","categorical",categorical_f)
    validation_expectation_target = build_expectations("target_expectations","target",'')

    numerical_feature_descriptions =[]
    categorical_feature_descriptions =[]
    target_feature_descriptions =[]
    df_numeric = df[numerical_f]
    df_categorical = df[categorical_features]
    df_target = df['class']

    df_numeric.loc[:, "index"] = df_numeric.index
    df_categorical.loc[:, "index"] = df_categorical.index
    df_target.loc["index"] = df_target.index

    object_fs_categorical_features= save_feature_store(df_categorical,'categorical_features',validation_expectation_categorical,1,'categorical_feature_descriptions')
    object_fs_num_features= save_feature_store(df_numeric,'numerical_features',validation_expectation_numerical,1,'numerical_feature_descriptions')

    df_target = pd.DataFrame()
    df_target['class'] = df['class']
    df_target.loc[:, "index"] = df_target.index 

    object_fs_target_features= save_feature_store(df_target,'target_features',validation_expectation_target,1,'target_feature_descriptions')
    return df