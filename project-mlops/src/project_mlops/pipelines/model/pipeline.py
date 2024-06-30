"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import Model_Logistic, Model_randomForest, Model_decisionTree, Final_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
       
         node(
            func= Final_model,
            inputs = ['X_train_data','y_train_data', 'selected_features'],
            outputs = 'model_final',
            name = 'model_final'
        )
    ])
