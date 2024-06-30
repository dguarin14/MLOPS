"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.4
"""

from sklearn.metrics import f1_score # type: ignore
import logging

logger = logging.getLogger(__name__)

def evaluate_f1_score(model_ev, X_test, y_test, columns):
    X_test = X_test[columns]
    y_pred = model_ev.predict(X_test)
    train_score = f1_score(y_test, y_pred)
    message = 'Model has a f1 score of: '+ str(train_score)
    logger.info(message)
    return train_score
