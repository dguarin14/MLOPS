"""
This is a boilerplate pipeline 'model_grid'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import model_grid

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func= model_grid,
            inputs = ['X_train_data','X_test_data','y_test_data', 'y_train_data'],
            outputs = 'best_name_model',
            name = 'model_grid'
        )


    ])
