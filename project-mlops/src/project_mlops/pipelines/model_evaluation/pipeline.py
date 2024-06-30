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
            inputs = ['model_logistic', 'X_test_data','y_test_data'],
            outputs = 'f1_score_logistic',
            name = 'f1_score_logistic'
        ),
         node (
            func= evaluate_f1_score,
            inputs = ['model_randomForest', 'X_test_data','y_test_data'],
            outputs = 'f1_score_randomForest',
            name = 'f1_score_randomForest'
        ),
         node (
            func= evaluate_f1_score,
            inputs = ['model_decisionTree', 'X_test_data','y_test_data'],
            outputs = 'f1_score_decisionTree',
            name = 'f1_score_decisionTree'
        )



    ])