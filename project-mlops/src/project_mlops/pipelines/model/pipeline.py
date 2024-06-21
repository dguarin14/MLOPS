"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import Model_Logistic


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func= Model_Logistic,
            inputs = ['X_train_data','y_train_data'],
            outputs = 'model_logistic',
            name = 'model_logistic'
        )
    ])
