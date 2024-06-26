"""
This is a boilerplate pipeline 'GreatExpression'
generated using Kedro 0.19.6
"""
import great_expectations as gx # type: ignore
from great_expectations.core import ExpectationSuite, ExpectationConfiguration # type: ignore

def build_expectations(type, columns, suite_c):

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

    
    if type == 'numerical':
        columns = ['duration', 'credit_amount', 'installment_commitment',
       'residence_since', 'age', 'existing_credits', 'num_dependents']
        for i in columns:
            suite_c.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_values_to_be_of_type",
                            kwargs={"column": i, "type_": "float64"},
                        )
                    )
    elif type == 'categorical':
        for i in columns:
            suite_c.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_distinct_values_to_be_in_set",
                            kwargs={"column": i, "value_set": value[i]},
                        )
                    )
    else:
        print(type)
        suite_c.add_expectation(
                        ExpectationConfiguration(
                            expectation_type="expect_column_distinct_values_to_be_in_set",
                            kwargs={"column": 'class', "value_set": ['good', 'bad']},
                        )
                    )
    return suite_c

import pandas as pd # type: ignore
def get_validation_results(checkpoint_result):
    # validation_result is a dictionary containing one key-value pair
    validation_result_key, validation_result_data = next(iter(checkpoint_result["run_results"].items()))

    # Accessing the 'actions_results' from the validation_result_data
    validation_result_ = validation_result_data.get('validation_result', {})

    # Accessing the 'results' from the validation_result_data
    results = validation_result_["results"]
    meta = validation_result_["meta"]
    use_case = meta.get('expectation_suite_name')
    
    
    df_validation = pd.DataFrame({},columns=["Success","Expectation Type","Column","Column Pair","Max Value",\
                                       "Min Value","Element Count","Unexpected Count","Unexpected Percent","Value Set","Unexpected Value","Observed Value"])
    
    
    for result in results:
        # Process each result dictionary as needed
        success = result.get('success', '')
        expectation_type = result.get('expectation_config', {}).get('expectation_type', '')
        column = result.get('expectation_config', {}).get('kwargs', {}).get('column', '')
        column_A = result.get('expectation_config', {}).get('kwargs', {}).get('column_A', '')
        column_B = result.get('expectation_config', {}).get('kwargs', {}).get('column_B', '')
        value_set = result.get('expectation_config', {}).get('kwargs', {}).get('value_set', '')
        max_value = result.get('expectation_config', {}).get('kwargs', {}).get('max_value', '')
        min_value = result.get('expectation_config', {}).get('kwargs', {}).get('min_value', '')

        element_count = result.get('result', {}).get('element_count', '')
        unexpected_count = result.get('result', {}).get('unexpected_count', '')
        unexpected_percent = result.get('result', {}).get('unexpected_percent', '')
        observed_value = result.get('result', {}).get('observed_value', '')
        if type(observed_value) is list:
            #sometimes observed_vaue is not iterable
            unexpected_value = [item for item in observed_value if item not in value_set]
        else:
            unexpected_value=[]
        
        df_validation = pd.concat([df_validation, pd.DataFrame.from_dict( [{"Success" :success,"Expectation Type" :expectation_type,"Column" : column,"Column Pair" : (column_A,column_B),"Max Value" :max_value,\
                                           "Min Value" :min_value,"Element Count" :element_count,"Unexpected Count" :unexpected_count,"Unexpected Percent":unexpected_percent,\
                                                  "Value Set" : value_set,"Unexpected Value" :unexpected_value ,"Observed Value" :observed_value}])], ignore_index=True)
        
    return df_validation

def great_expectations(df):
    context = gx.get_context(context_root_dir = "gx")
    datasource_name = "credit_datasource"
    try:
        datasource = context.sources.add_pandas(name=datasource_name)
    except:
        print("Data Source already exists.")
        datasource = context.datasources[datasource_name]

    suite_credit = context.add_or_update_expectation_suite(expectation_suite_name="credits")

    categorical_features = df.select_dtypes(include=['object']).columns
    numerical_f = df.select_dtypes(include=['float64']).columns
    categorical_f = categorical_features[:-1]
    suite_c = build_expectations( 'numerical', numerical_f, suite_credit)
    suite_c = build_expectations('categorical', categorical_f, suite_c)
    suite_c = build_expectations('target', df['class'], suite_c)

    context.save_expectation_suite(expectation_suite=suite_c)

    data_asset_name = "credits"
    try:
        data_asset = datasource.add_dataframe_asset(name=data_asset_name, dataframe= df)
    except:
        print("The data asset alread exists. The required one will be loaded.")
        data_asset = datasource.get_asset(data_asset_name)
    
    batch_request = data_asset.build_batch_request(dataframe= df)

    checkpoint = gx.checkpoint.SimpleCheckpoint(
        name="checkpoint_correct",
        data_context=context,
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "credits",
            },
        ],
    )
    checkpoint_result = checkpoint.run()

    suite_credit2 = context.add_or_update_expectation_suite(expectation_suite_name="Credit3")

    suite_credit2.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_distinct_values_to_be_in_set",
        kwargs={"column": 'class', "value_set": ['good','bad']},
                        )
                        )
    context.save_expectation_suite(expectation_suite=suite_credit2)
    data_asset = datasource.add_dataframe_asset(name='Credit3', dataframe= df['class'])

    df_validation = get_validation_results(checkpoint_result)

    df_validation

    return df



