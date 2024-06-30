"""
This is a boilerplate pipeline 'GreatExpression'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import great_expectations

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
         node(
            func= great_expectations,
            inputs='data_credits',
            outputs= 'gx_credits',
            name = 'credits_gx'
        )

    ])
