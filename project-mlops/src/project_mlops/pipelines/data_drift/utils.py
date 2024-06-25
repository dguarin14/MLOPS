import numpy as np
import scipy.stats
import scipy.spatial


def calculate_psi(expected, actual, buckettype='bins', buckets=10, axis=0):
    '''Calculate the PSI (population stability index) across all variables
    Args:
       expected: numpy matrix of original values
       actual: numpy matrix of new values, same size as expected
       buckettype: type of strategy for creating buckets, bins splits into even splits, quantiles splits into quantile buckets
       buckets: number of quantiles to use in bucketing variables
       axis: axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       psi_values: ndarray of psi values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    '''

    def psi(expected_array, actual_array, buckets):
        '''Calculate the PSI for a single variable
        Args:
           expected_array: numpy array of original values
           actual_array: numpy array of new values, same size as expected
           buckets: number of percentile ranges to bucket the values into
        Returns:
           psi_value: calculated PSI value
        '''

        def scale_range (input, min, max):
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
            '''Calculate the actual PSI value from comparing the values.
               Update the actual value to a very small number if equal to zero
            '''
            if a_perc == 0:
                a_perc = 0.0001
            if e_perc == 0:
                e_perc = 0.0001

            value = (e_perc - a_perc) * np.log(e_perc / a_perc)
            return(value)

        psi_value = np.sum(sub_psi(expected_percents[i], actual_percents[i]) for i in range(0, len(expected_percents)))

        return(psi_value)

    if len(expected.shape) == 1:
        psi_values = np.empty(len(expected.shape))
    else:
        psi_values = np.empty(expected.shape[axis])

    for i in range(0, len(psi_values)):
        if len(psi_values) == 1:
            psi_values = psi(expected, actual, buckets)
        elif axis == 0:
            psi_values[i] = psi(expected[:,i], actual[:,i], buckets)
        elif axis == 1:
            psi_values[i] = psi(expected[i,:], actual[i,:], buckets)

    return(psi_values)



def calculate_psi_categorical(actual, expected):
    actual_perc = actual.value_counts()/len(actual)
    expected_perc = expected.value_counts()/len(expected)
    actual_classes = list(actual_perc.index) 
    expected_classes = list(expected_perc.index)
    PSI = 0
    classes = set(actual_classes + expected_classes)
    for c in classes:
        final_actual_perc = actual_perc[c] if c in actual_classes else 0.00001
        final_expected_perc = expected_perc[c] if c in expected_classes else 0.00001
        PSI += (final_actual_perc - final_expected_perc)*np.log(final_actual_perc/final_expected_perc)
    return PSI



def calculate_js(expected, actual, buckettype='bins', buckets=10, axis=0):
    '''Calculate the JS (population stability index) across all variables
    Args:
       expected: numpy matrix of original values
       actual: numpy matrix of new values, same size as expected
       buckettype: type of strategy for creating buckets, bins splits into even splits, quantiles splits into quantile buckets
       buckets: number of quantiles to use in bucketing variables
       axis: axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       JS_values: ndarray of JS values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    '''


    def scale_range (input, min, max):
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
    actual_percents = np.histogram(actual, breakpoints,density=True)[0] 
    
    # Obtain point-wise mean of the two PDFs Y1 and Y2, denote it as M
    M = (expected_percents + actual_percents) / 2

    # Compute Kullback-Leibler divergence between Y1 and M
    d1 = scipy.stats.entropy(expected_percents, M, base=2)

    # Compute Kullback-Leibler divergence between Y2 and M
    d2 = scipy.stats.entropy(actual_percents, M, base=2)


    # Take the average of d1 and d2 
    # we get the symmetric Jensen-Shanon divergence
    js_dv = (d1 + d2) / 2

    return np.sqrt(js_dv)


def calculate_js_categorical(actual, expected):
    actual_perc = actual.value_counts().reindex(
    actual.unique(), fill_value=0)/len(actual)
    expected_perc = expected.value_counts().reindex(
    expected.unique(), fill_value=0)/len(expected)
   
    # Obtain point-wise mean of the two PDFs Y1 and Y2, denote it as M
    M = (expected_perc + actual_perc) / 2

    # Compute Kullback-Leibler divergence between Y1 and M
    d1 = scipy.stats.entropy(expected_perc, M, base=2)
    
    # Compute Kullback-Leibler divergence between Y2 and M
    d2 = scipy.stats.entropy(actual_perc, M, base=2)

    # Take the average of d1 and d2 
    # we get the symmetric Jensen-Shanon divergence
    js_dv = (d1 + d2) / 2
    
    return np.sqrt(js_dv)