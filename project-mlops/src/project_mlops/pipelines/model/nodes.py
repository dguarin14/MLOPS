"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from sklearn.metrics import f1_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier 
from sklearn.tree import DecisionTreeClassifier

import mlflow

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, explained_variance_score

def Model_Logistic(X_train, y_train):

    model = LogisticRegression(solver='lbfgs', random_state=42)
    model.fit(X_train, y_train)
    return model


def Model_randomForest(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def Model_decisionTree(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def Final_model(X_train, y_train, columns):
    X_train = X_train[columns]
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    return model