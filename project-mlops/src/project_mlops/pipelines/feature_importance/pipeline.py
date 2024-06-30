"""
This is a boilerplate pipeline 'feature_importance'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import feature_importance, create_shap_summary_plot

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(        [
            node(
                func=feature_importance,
                inputs=["X_train_data", "y_train_data"],
                outputs="selected_features",
                name="feature_selection_node",
            ),
            node(
                func=create_shap_summary_plot,
                inputs=[ "X_train_data", "y_train_data"],
                outputs=None,  # We will see just the visual that's why we said None
                name="create_shap_summary_plot_node",
            )
        ]
        )
