"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import evaluate_f1_score


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([

        node (
            func= evaluate_f1_score,
            inputs = ['model_final', 'X_test_data','y_test_data', 'selected_features'],
            outputs = 'f1_score_final',
            name = 'f1_score_final'
        )
    ])