"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.19.4
"""

from sklearn.metrics import f1_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore


def Model_Logistic(X_train, y_train):
    model = LogisticRegression(solver='lbfgs', random_state=42)
    model.fit(X_train, y_train)
    return model
