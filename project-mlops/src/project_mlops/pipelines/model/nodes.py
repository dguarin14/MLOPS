"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from sklearn.metrics import f1_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier 
from sklearn.tree import DecisionTreeClassifier


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