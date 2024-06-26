"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import Model_Logistic, Model_randomForest, Model_decisionTree


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func= Model_Logistic,
            inputs = ['X_train_data','y_train_data'],
            outputs = 'model_logistic',
            name = 'model_logistic'
        ), 
        node(
            func= Model_randomForest,
            inputs = ['X_train_data','y_train_data'],
            outputs = 'model_randomForest',
            name = 'model_randomForest'
        ),
        node(
            func= Model_decisionTree,
            inputs = ['X_train_data','y_train_data'],
            outputs = 'model_decisionTree',
            name = 'model_decisionTree'
        )
    ])
