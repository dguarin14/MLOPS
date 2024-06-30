"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node  # type: ignore
from .nodes import calculate_data_drift_psi, calculate_data_drift_js

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=calculate_data_drift_psi,
                inputs=["X_train_data", "X_val_data"],
                outputs="psi_values",
                name="calculate_psi",
            ) ,
            node(
                func=calculate_data_drift_js,
                inputs=["X_train_data", "X_val_data"],
                outputs="js_values",
                name="calculate_js",
            )
        ]
    )
