"""
This is a boilerplate pipeline 'feature_importance'
generated using Kedro 0.19.6
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.feature_selection import RFE
import logging
from typing import Dict, Any
import shap
import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


def feature_importance(X_train: pd.DataFrame, y_train: pd.DataFrame):
    model = LogisticRegression(solver='lbfgs', random_state=42)
    
    log.info("----------------------------")
    log.info(f"We start with: {len(X_train.columns)} columns")
    y_train = np.ravel(y_train)
    rfe = RFE(model)
    rfe = rfe.fit(X_train, y_train)
    f = rfe.get_support(1) # the most important one
    X_cols = X_train.columns[f].tolist()

    log.info(f"Number of best columns is: {len(X_cols)}")
    
    return X_cols

def create_shap_summary_plot( X_train, y_train):
    model = LogisticRegression(solver='lbfgs', random_state=42)
    model.fit(X_train, y_train)
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_train)

    shap.summary_plot(shap_values, X_train)
    plt.show()

