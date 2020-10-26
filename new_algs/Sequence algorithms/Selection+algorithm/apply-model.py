from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

from _helpers.Database import Database
from config import DB_TRAIN_FEATURE_TABLE
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


def knn_model(k, train_data, test_data, feature_cols, predict_col):
    # Create the knn model.
    # Look at the five closest neighbors.

    knn = KNeighborsRegressor(n_neighbors=k, )
    # Fit the model on the training data.
    knn.fit(train_data[feature_cols], train_data[predict_col])
    # Make point predictions on the test set using the fit model.
    predictions = knn.predict(test_data[feature_cols])
    # probs = knn.predict_proba(test[feature_cols])

    return predictions


def decision_tree(X_train, X_test, y_train, y_test):
    from sklearn.metrics import classification_report, confusion_matrix

    model = DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
    model.fit(X_train, y_train)
    cv_decision_tree = cross_val_score(model, X_train, y_train, cv=10)

    y_predicted = model.predict(X_test)
    y_real = np.array(y_test.transpose())[0]
    accuracy = accuracy_score(y_real, y_predicted)*100

    return accuracy


def apply_model(model, df):
    x = ['length']  # , 'max', 'min', 'dist_min_max', 'average', 'mean', 'q1', 'q2', 'q3', 'std_deviation', 'variance', 'target']
    y = ['target']

    # Randomly shuffle the index of nba.
    # random_indices = permutation(df.index)
    # Set a cutoff for how many items we want in the test set (in this case 1/3 of the items)
    # test_cutoff = np.math.floor(len(df) / 3)
    # Generate the test set by taking the first 1/3 of the randomly shuffled indices.
    # test_data = df.loc[random_indices[1:test_cutoff]]
    # Generate the train set with the rest of the data.
    # train_data = df.loc[random_indices[test_cutoff:]]
    df = df[['length', 'target']]

    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # X.iloc[X_train]

    if model == 'knn':
        k = 2
        # predictions = knn_model(k, train_data, test_data, x, y)

    elif model == 'decision_tree':
        predictions = decision_tree(X_train, X_test, y_train, y_test)

    else:
        raise Exception('No available model was selected.')

    # Get the actual values for the test set.
    # actual = test_data[x]

    # Compute the mean squared error of our predictions.
    # error = (((predictions - actual) ** 2).sum()) / len(predictions)

    return error['target']


def main():
    start_time = datetime.now()

    db = Database()
    df = db.get_df_from_table(DB_TRAIN_FEATURE_TABLE)
    error = apply_model('decision_tree', df)

    delta_time = (datetime.now() - start_time)
    print('Ended in {} seconds. Error: {}'.format(delta_time, error))


main()
