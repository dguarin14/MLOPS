"""
This is a boilerplate pipeline 'featureStore'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import feature_hopswork

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func= feature_hopswork,
            inputs='credits',
            outputs= 'data_credits',
            name = 'preprocess_credits_node'
        )


    ])
