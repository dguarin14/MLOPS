"""
This is a boilerplate pipeline 'model_grid'
generated using Kedro 0.19.6
"""
import mlflow # type: ignore

from sklearn.model_selection import train_test_split # type: ignore
from sklearn.datasets import load_wine # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.metrics import mean_squared_error, explained_variance_score # type: ignore
import logging
logger = logging.getLogger(__name__)
import warnings

from sklearn.metrics import f1_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier  # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore

import mlflow # type: ignore

from sklearn.model_selection import train_test_split # type: ignore
from sklearn.datasets import load_wine # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.metrics import mean_squared_error, explained_variance_score # type: ignore
from sklearn.model_selection import GridSearchCV # type: ignore
from mlflow import MlflowClient # type: ignore
from sklearn.metrics import f1_score # type: ignore

def model_grid(X_train, X_test, y_test, y_train, columns):
    X_train = X_train[columns]
    X_test = X_test[columns]

    print("------------------------")
    mlflow.end_run()
    mlflow.set_experiment("mlflow_project_credits_1")
   
    models_dict = {
            'RandomForestClassifier': RandomForestClassifier(),
            'DecisionTreeClassifier': DecisionTreeClassifier(),
            'LogisticRegression':  LogisticRegression()
        }
    solvers = ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']

    params = {
                'RandomForestClassifier': {'n_estimators': [100,50,20],
                                        'max_depth': [None, 10, 5, 20]},
                'DecisionTreeClassifier': {'criterion' : ["gini", "entropy", 'log_loss'],
                                        'max_depth': [None, 10, 5, 20]},
                'LogisticRegression': solvers
    }

    results = {}

    for model_name, model in models_dict.items():
        
        if model_name == 'RandomForestClassifier':

            for p_1 in params["RandomForestClassifier"]["n_estimators"]:
                for p_2 in params["RandomForestClassifier"]["max_depth"]:
                    run_name = model_name + "_"+ str(p_1)+"_"+str(p_2)
                    with mlflow.start_run(run_name=run_name) as run:
                        model = RandomForestClassifier(n_estimators = p_1, max_depth = p_2, random_state = 42)
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        train_score = f1_score(y_test, y_pred)
                        results[run_name] = train_score
                        mlflow.log_param("n_estimators", str(p_1))
                        mlflow.log_param("max_depth", str(p_2))
                        mlflow.log_metric("f1_score", train_score)
                        print(run_name, train_score)
        elif model_name == 'DecisionTreeClassifier':
            for p_1 in params["DecisionTreeClassifier"]["criterion"]:
                for p_2 in params["DecisionTreeClassifier"]["max_depth"]:
                    run_name = model_name +"_"+ str(p_1)+"_"+str(p_2)
                    with mlflow.start_run(run_name=run_name) as run:
                        model = DecisionTreeClassifier(criterion = p_1, max_depth = p_2, random_state = 42)
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        train_score = f1_score(y_test, y_pred)
                        results[run_name] = train_score
                        mlflow.log_param("criterion", str(p_1))
                        mlflow.log_param("max_depth", str(p_2))
                        mlflow.log_metric("f1_score", train_score)
                        print(run_name, train_score)
        else:
            for i in params['LogisticRegression']:
                run_name = model_name +"_"+ str(i)
                with mlflow.start_run(run_name=run_name) as run:
                    model = LogisticRegression(solver= i,random_state=42)
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    train_score = f1_score(y_test, y_pred)
                    results[run_name] = train_score
                    mlflow.log_param("solvers", i)
                    mlflow.log_metric("f1_score", train_score)
                    print(run_name, train_score)
    best_model_name = max(results, key=results.get)
    print( best_model_name, results[best_model_name])
    message = "best mode: " + best_model_name + str(results[best_model_name])
    logger.info(message)
    mlflow.end_run()
    return best_model_name