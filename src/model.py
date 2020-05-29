import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier,AdaBoostRegressor
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from sklearn.inspection import plot_partial_dependence
from joblib import dump, load
import pickle
import matplotlib.pyplot as plt

def get_feature_importances(model, X_train):
    for i in range(0, len(X_train.columns)):
        print(str(X_train.columns[i]) + ': ' + str(rf_model.feature_importances_[i]))
        
def eval_model(model, X_test, y_test):
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    rec = recall_score(y_test, preds)
    prec = precision_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    print('===ACCURACY===')
    print(acc)
    print('===RECALL===')
    print(rec)
    print('===PRECISION===')
    print(prec)
    print('===F1===')
    print(f1)


if __name__ == '__main__':
    df = pd.read_pickle('../data/pickled_df.pkl')

    y = df['fraud']
    X = df.drop('fraud', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify = y)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=0)
    eval_model(rf_model, X_test, y_test)
    probs = rf_model.predict_proba(X_test)

    get_feature_importances(rf_model, X_train)

    pkl_filename = "../data/rf_taylor_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(rf_model, file)


