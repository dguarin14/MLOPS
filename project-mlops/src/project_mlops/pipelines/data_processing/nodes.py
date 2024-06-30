"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.19.4
"""
import pandas as pd
import numpy as np
import scipy.stats

def calculate_psi(expected, actual, buckettype='bins', buckets=10, axis=0):
    def psi(expected_array, actual_array, buckets):
        def scale_range(input, min, max):
            input += -(np.min(input))
            input /= np.max(input) / (max - min)
            input += min
            return input

        breakpoints = np.arange(0, buckets + 1) / (buckets) * 100
        if buckettype == 'bins':
            breakpoints = scale_range(breakpoints, np.min(expected_array), np.max(expected_array))
        elif buckettype == 'quantiles':
            breakpoints = np.stack([np.percentile(expected_array, b) for b in breakpoints])

        expected_percents = np.histogram(expected_array, breakpoints)[0] / len(expected_array)
        actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)

        def sub_psi(e_perc, a_perc):
            if a_perc == 0:
                a_perc = 0.0001
            if e_perc == 0:
                e_perc = 0.0001
            value = (e_perc - a_perc) * np.log(e_perc / a_perc)
            return value

        psi_value = np.sum(sub_psi(expected_percents[i], actual_percents[i]) for i in range(len(expected_percents)))
        return psi_value

    # Ajuste aquí para definir correctamente la longitud de psi_values
    if axis == 0:
        psi_values = np.empty(expected.shape[1])
    elif axis == 1:
        psi_values = np.empty(expected.shape[0])

    for i in range(len(psi_values)):
        if axis == 0:
            psi_values[i] = psi(expected[:, i], actual[:, i], buckets)
        elif axis == 1:
            psi_values[i] = psi(expected[i, :], actual[i, :], buckets)

    return psi_values

def calculate_js(expected, actual, buckettype='bins', buckets=10, axis=0):
    def scale_range(input, min, max):
        input += -(np.min(input))
        input /= np.max(input) / (max - min)
        input += min
        return input

    breakpoints = np.arange(0, buckets + 1) / (buckets) * 100
    if buckettype == 'bins':
        breakpoints = scale_range(breakpoints, np.min(expected), np.max(expected))
    elif buckettype == 'quantiles':
        breakpoints = np.stack([np.percentile(expected, b) for b in breakpoints])

    expected_percents = np.histogram(expected, breakpoints, density=True)[0]
    actual_percents = np.histogram(actual, breakpoints, density=True)[0]
    M = (expected_percents + actual_percents) / 2
    d1 = scipy.stats.entropy(expected_percents, M, base=2)
    d2 = scipy.stats.entropy(actual_percents, M, base=2)
    js_dv = (d1 + d2) / 2

    return np.sqrt(js_dv)

def calculate_data_drift_psi(X_train, X_test, buckettype='bins', buckets=10, axis=0):
    print(f"X_train type: {type(X_train)}, shape: {X_train.shape}")
    print(f"X_test type: {type(X_test)}, shape: {X_test.shape}")

    expected_numerical = X_train.select_dtypes(include=['float64', 'int64'])
    actual_numerical = X_test.select_dtypes(include=['float64', 'int64'])

    print(f"expected_numerical shape: {expected_numerical.shape}")
    print(f"actual_numerical shape: {actual_numerical.shape}")

    psi_values = calculate_psi(expected_numerical.values, actual_numerical.values, buckettype, buckets, axis)

    return psi_values

def calculate_data_drift_js(X_train, X_test, buckettype='bins', buckets=10, axis=0):
    expected_numerical = X_train.select_dtypes(include=['float64', 'int64'])
    actual_numerical = X_test.select_dtypes(include=['float64', 'int64'])

    js_values = calculate_js(expected_numerical.values, actual_numerical.values, buckettype, buckets, axis)

    return js_values
