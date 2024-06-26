"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from sklearn.metrics import f1_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore

import mlflow

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, explained_variance_score

def Model_Logistic(X_train, y_train):

    mlflow.set_tracking_uri("http://127.0.0.1:5000/")

    with mlflow.start_run(run_name="tracking experiment_1", description='checking model') as run:
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
        
        rf.fit(X_train, y_train)
        print("1")
    mlflow.end_run()
    
    mlflow.set_experiment("mlflow_first_example")
    model = LogisticRegression(solver='lbfgs', random_state=42)
    model.fit(X_train, y_train)
    return model
