"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.19.4
"""

from utils import calculate_psi, calculate_psi_categorical, calculate_js, calculate_js_categorical
import matplotlib.pyplot as plt  

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import nannyml as nml

def calculate_data_drift(X_train, X_test, buckettype='bins', buckets=10, axis=0):
    """
    Calculate the data drift between the expected and actual datasets.
    This function calculates the PSI and JS  between the expected and actual datasets
    
    Args:
        expected: The expected dataset.
        actual: The actual dataset.
        buckettype: The type of bucketing to use for the data drift calculation.
        buckets: The number of buckets to use for the data drift calculation.
        axis: The axis to calculate the data drift on.
        
    Returns:
        psi_values: The PSI values for the data drift calculation.
        js_values: The JS divergence values for the data drift calculation.        
    """
    #Only calculate PSI and JS for numerical columns and categorical columns will be calculated separately

    #Filter out numerical columns
    expected_numerical = X_train.select_dtypes(include=['float64', 'int64'])
    actual_numerical = X_test.select_dtypes(include=['float64', 'int64'])

    #Calculate PSI and JS for numerical columns
    psi_values = calculate_psi(expected_numerical, actual_numerical, buckettype, buckets, axis)
    js_values = calculate_js(expected_numerical, actual_numerical, buckettype, buckets, axis)

    #Filter out categorical columns
    expected_categorical = X_train.select_dtypes(include=['object'])
    actual_categorical = X_test.select_dtypes(include=['object'])

    #Calculate PSI and JS for categorical columns
    psi_values_categorical = calculate_psi_categorical(expected_categorical, actual_categorical)
    js_values_categorical = calculate_js_categorical(expected_categorical, actual_categorical)

    return psi_values, js_values

