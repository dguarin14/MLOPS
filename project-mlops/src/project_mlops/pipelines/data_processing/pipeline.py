"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import preprocess_credit



def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preprocess_credit,
            inputs='credits',
            outputs= 'preprocess_credits',
            name = 'preprocess_credits_node'
        )
    ])

