"""
This is a boilerplate pipeline 'datadrift'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node  # type: ignore
from .nodes1 import calculate_data_drift

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
       
        
        ]
    )
    return pipeline([])