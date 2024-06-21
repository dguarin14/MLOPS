"""
This is a boilerplate pipeline 'train_split'
generated using Kedro 0.19.4
"""
import typing as t
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split, cross_val_score # type: ignore

def trainTest_split(df: pd.DataFrame, parameters: t.Dict) -> t.Tuple:
    features = df.columns.to_numpy()[:-1]
    X = df[features]
    y = df['class']
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = parameters['test_size'])
    return X_train, X_test, y_train, y_test