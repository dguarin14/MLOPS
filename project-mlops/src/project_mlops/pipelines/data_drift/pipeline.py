"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node  # type: ignore
from .nodes import calculate_data_drift

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                calculate_data_drift,
                inputs=["X_train_data", "X_test_data"],
                outputs=["psi_values", "js_values"],
                name="calculate_data_drift_node",
            ),
        
        ]
    )
    return pipeline([])
