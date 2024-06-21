"""
This is a boilerplate pipeline 'train_split'
generated using Kedro 0.19.4
"""

from kedro.pipeline import Pipeline, pipeline, node # type: ignore
from .nodes import trainTest_split

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
             func= trainTest_split,
             inputs=["preprocess_credits", "params:split_options"],
             outputs= ["X_train_data","X_test_data","y_train_data","y_test_data"],
             name= 'split'
             )

    ])
