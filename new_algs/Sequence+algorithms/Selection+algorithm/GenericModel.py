import json
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from _helpers.Database import Database
from _helpers.LoggerHelper import Logger
from config import DIR, TEST_DATA, DB_PATH


class GenericModel:
    CLASSES = [10, 100, 1000, 10000, 100000, 1000000]
    DB = Database(DB_PATH)

    @staticmethod
    def reformat_array():
        """
        input: string like '[123 324 567]'
            * transform to a list
            * cast elements to integer
        :return:
        """
        return lambda x: [int(elem) for elem in x[1:-1].split()]

    @staticmethod
    def extract_features(path_target_data, path_train_data, chunksize, table_name, FORCE=False):

        # If table already exists and is not to force, we only save that info to a csv file
        if GenericModel.DB.table_exists(table_name) and not FORCE:
            GenericModel.DB.db_table_to_csv(table_name, DIR + 'csv_files/{}.csv'.format(table_name))
            return 0

        iterations = 0
        feature_arr = []

        if path_target_data is not None:
            df_target = pd.read_csv(path_target_data, encoding='latin1', error_bad_lines=False, index_col='Id')
            target = df_target['Predicted']
        else:
            target = None

        for df_train in pd.read_csv(path_train_data, iterator=True, encoding='latin1', error_bad_lines=False, names=["id", "length", "array"],
                                    chunksize=chunksize):
            df_train['array'] = df_train['array'].apply(GenericModel.reformat_array())
            features = [GenericModel.np_extract_array_features(row, target) for _, row in df_train.iterrows()]
            GenericModel.DB.append_df_to_table(features, table_name, df_train['id'])
            feature_arr = feature_arr + features
            iterations = iterations + 1

        # Generate CSV
        GenericModel.DB.db_table_to_csv(table_name, '../csv_files/{}.csv'.format(table_name))

        return iterations

    @staticmethod
    def np_extract_array_features(row, target):
        array = np.array(row['array'])
        dist_between_elems = [array[i + 1] - array[i] for i in range(len(array) - 1)]

        return {
            'id': row['id'],
            'length': len(array),
            'max': max(array),
            'min': min(array),
            'dist_min_max': max(array) - min(array),
            # Compute the weighted average along the specified axis.
            'average': np.average(array, axis=0),
            # Compute the arithmetic mean along the specified axis
            'mean': np.mean(array, axis=0),  # reduce(lambda x, y: x + y, array) / len(array),
            'q1': np.percentile(array, 25),
            'q2': np.percentile(array, 50),  # median
            'q3': np.percentile(array, 75),
            'std_deviation': np.std(array, axis=0),
            'variance': np.var(array, axis=0),
            'avg_diff': sum(dist_between_elems) / len(dist_between_elems),
            'sorted_percentage': len([index for index, value in enumerate(array) if index != 0 and array[index] > array[index - 1]]) / len(
                array) * 100,
            'target': int(target[row['id']]) if target is not None else '',
        }

    @staticmethod
    def apply_model(algorithm, parameters, feature_cols, model_file, test_size=0.15):
        try:
            algorithm = GenericModel.get_algorithm(algorithm, parameters)
            classifier = algorithm['function']
            classifier_name = algorithm['name']
            classifier_parameters = algorithm['parameters']
        except ModuleNotFoundError as e:
            return str(e)

        dataset = GenericModel.DB.load_csv(DIR + 'csv_files/train_features_data.csv')

        feature_arr = [dataset.columns.get_loc(feature_name) for feature_name in feature_cols]
        X = dataset.iloc[:, feature_arr].values

        y = dataset.iloc[:, dataset.columns.get_loc("target")].values

        # Get Train and Test Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)  # , random_state=None)

        # df_pymrmr = dataset[-1:] + dataset[:-1]
        # a = pymrmr.mRMR(df_pymrmr, 'MIQ', 5)

        # Fit to model
        classifier.fit(X_train, y_train)

        # Predict Output
        y_pred = classifier.predict(X_test)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        # Get Accuracy
        accuracy = accuracy_score(y_test, y_pred) * 100

        Logger.send('--------------------------------------------')
        Logger.send(classifier_name)
        Logger.send('Parameters: ' + classifier_parameters)
        Logger.send("Features used: " + json.dumps(feature_cols))
        Logger.send("Accuracy is: {} %".format(accuracy))
        Logger.send('Confusion Matrix: {}'.format(str(cm)))
        Logger.send('--------------------------------------------')

        # PUT EVERYTHING TO TRAIN
        classifier.fit(X, y)

        # save the model to disk
        filename = DIR + 'bin_models/' + model_file
        pickle.dump(classifier, open(filename, 'wb'))

        return filename, accuracy

    @staticmethod
    def apply_model_by_class(algorithm_obj, class_length, test_size=0.3):
        try:
            algorithm = GenericModel.get_algorithm(algorithm_obj['name'], algorithm_obj['parameters'])
            classifier = algorithm['function']
            classifier_name = algorithm['name']
            classifier_parameters = algorithm_obj['parameters']
        except ModuleNotFoundError as e:
            return str(e)

        dataset = GenericModel.DB.load_csv(DIR + 'csv_files/train_features_data.csv')

        feature_arr = [dataset.columns.get_loc(feature_name) for feature_name in algorithm_obj['feature_cols']]
        X = dataset.iloc[:, feature_arr][dataset.length == class_length].values

        y = dataset.iloc[:, dataset.columns.get_loc("target")][dataset.length == class_length].values

        # Get Train and Test Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)  # , random_state=None)

        # Fit to model
        classifier.fit(X_train, y_train)

        # Predict Output
        y_pred = classifier.predict(X_test)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        # Get Accuracy
        accuracy = accuracy_score(y_test, y_pred) * 100

        Logger.send('--------------------------------------------')
        Logger.send(classifier_name)
        Logger.send('Length: {}'.format(str(class_length)))
        Logger.send('Parameters: ' + str(classifier_parameters).replace('\'', '\"'))
        Logger.send("Features used: " + json.dumps(algorithm_obj['feature_cols']))
        Logger.send("Accuracy is: {} %".format(accuracy))
        Logger.send('Confusion Matrix: {}'.format(str(cm)))
        Logger.send('--------------------------------------------')

        # PUT EVERYTHING TO TRAIN
        classifier.fit(X, y)

        # save the model to disk
        model_name = 'by_class_' + str(class_length) + '_' + str(datetime.now()) + '.sav'
        filename = DIR + 'bin_models/' + model_name
        pickle.dump(classifier, open(filename, 'wb'))

        return filename, accuracy

    @staticmethod
    def predict(bin_model, feature_cols, output_file_name):
        # Extract Features
        chunksize = 10
        GenericModel.extract_features(None, DIR + TEST_DATA, chunksize, 'test_features_data')
        df_features = GenericModel.DB.get_df_from_table('test_features_data')

        # load saved model from disk
        feature_arr = [df_features.columns.get_loc(feature_name) for feature_name in feature_cols]
        X_test_data = df_features.iloc[:, feature_arr].values

        loaded_model = pickle.load(open(bin_model, 'rb'))
        result = loaded_model.predict(X_test_data)

        df_output = pd.DataFrame()
        df_output['Id'] = df_features["id"]
        df_output['Predicted'] = result

        # save to CSV
        df_output.to_csv(output_file_name, index=False, columns=['Id', 'Predicted'], header=True)

    @staticmethod
    def predict_with_voting_system(algorithm_objs, output_file_name):
        """
        algorithm_objs = [
            {
                bin_model: <string>,
                feature_cols: [<string>, <string>, ...]
            }
        ]
        :param algorithm_objs:
        :param output_file_name:
        :return:
        """
        # Extract Features
        chunksize = 10
        GenericModel.extract_features(None, DIR + TEST_DATA, chunksize, 'test_features_data')
        df_features = GenericModel.DB.get_df_from_table('test_features_data')

        predictions = []

        for algorithm_obj in algorithm_objs:
            # load saved model from disk
            feature_arr = [df_features.columns.get_loc(feature_name) for feature_name in algorithm_obj['feature_cols']]
            X_test_data = df_features.iloc[:, feature_arr].values

            loaded_model = pickle.load(open(algorithm_obj['bin_model'], 'rb'))
            result = loaded_model.predict(X_test_data)
            predictions.append(result)
        #  voting_system_predictions =
        results = []
        for i in range(len(predictions[0])):
            how_1 = 0
            how_2 = 0
            for p in predictions:
                if p[i] == 1:
                    how_1 += 1
                if p[i] == 2:
                    how_2 += 1
            if how_1 > how_2:
                results.append(1)
            if how_1 < how_2:
                results.append(2)

        print(results)

        df_output = pd.DataFrame()
        df_output['Id'] = df_features["id"]
        df_output['Predicted'] = results

        # save to CSV
        df_output.to_csv(output_file_name, index=False, columns=['Id', 'Predicted'], header=True)

    @staticmethod
    def predict_with_voting_system_by_class(classes, output_file_name):
        # Extract Features
        chunksize = 10
        GenericModel.extract_features(None, DIR + TEST_DATA, chunksize, 'test_features_data')
        df_features = GenericModel.DB.get_df_from_table('test_features_data')

        df_output = pd.DataFrame()

        # for each class
        for _class in classes:
            predictions = []
            df_out_by_class = pd.DataFrame()
            df_out_by_class['Id'] = df_features[df_features.length == _class['len']]["id"]

            # for each model to apply voting system
            for bin_model in _class['models']:
                # load saved model from disk
                feature_arr = [df_features.columns.get_loc(feature_name) for feature_name in bin_model['feature_cols']]
                X_test_data = df_features.iloc[:, feature_arr][df_features.length == _class['len']].values

                loaded_model = pickle.load(open(bin_model['model_file'], 'rb'))
                result = loaded_model.predict(X_test_data)
                predictions.append(result)

            #  voting_system_predictions =
            results = []
            for i in range(len(predictions[0])):
                how_1 = 0
                how_2 = 0
                for p in predictions:
                    if p[i] == 1:
                        how_1 += 1
                    if p[i] == 2:
                        how_2 += 1
                if how_1 > how_2:
                    results.append(1)
                if how_1 < how_2:
                    results.append(2)

            df_out_by_class['Predicted'] = results

            df_output = df_output.append(df_out_by_class)

        # df_output['Id'] = df_features["id"]
        # df_output['Predicted'] = results

        # save to CSV
        df_output.to_csv(output_file_name, index=False, columns=['Id', 'Predicted'], header=True)

    @staticmethod
    def get_algorithm(algorithm_code, parameters):
        if algorithm_code == 'decision_tree':
            algorithm = {
                'name': 'Decision Tree Classifier',
                'function': DecisionTreeClassifier(**parameters),
                'grid_search': {
                    'max_depth': np.arange(1, 20),
                    'criterion': ['gini', 'entropy'],
                    'min_samples_split': np.arange(10, 500, 20)
                }
            }

        elif algorithm_code == 'knn':
            algorithm = {
                'name': 'K Neighbors Classifier',
                'function': KNeighborsClassifier(**parameters),
                'grid_search': {
                    'n_neighbors': np.arange(3, 9, 2),
                    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                }
            }

        elif algorithm_code == 'gaussian_naive_bayes':
            algorithm = {
                'name': 'Gaussian Naive Bayes Classifier',
                'function': GaussianNB(**parameters)
            }

        elif algorithm_code == 'multinomial_naive_bayes':
            algorithm = {
                'name': 'Multinomial Naive Bayes Classifier',
                'function': MultinomialNB(**parameters),
                'grid_search': {
                    'alpha': (1, 0.1, 0.01, 0.001, 0.0001, 0.00001)
                }
            }

        elif algorithm_code == 'svm':
            algorithm = {
                'name': 'Support Vector Machine (SVM)',
                'function': svm.SVC(**parameters),
                'grid_search': {
                    'kernel': ['rbf'],
                    'gamma': [1e-3, 1e-4],
                    'C': [1, 10, 100, 1000]
                }
            }

        elif algorithm_code == 'random_forest':
            algorithm = {
                'name': 'Random Forest',
                'function': RandomForestClassifier(**parameters),
                'grid_search': {
                    'n_estimators': np.arange(100, 1000, 100),
                    'max_features': ['auto', 'sqrt', 'log2'],
                    'max_depth': [3, 4, 5, 6, 7, 8, 9, 10],
                    'criterion': ['gini', 'entropy']
                }
            }

        elif algorithm_code == 'neural_networks':
            algorithm = {
                'name': 'Neural Networks',
                'function': MLPClassifier(**parameters),
                'grid_search': {
                    'solver': ['lbfgs', 'sgd', 'adam'],
                    'max_iter': np.arange(250, 2000, 250),
                    'alpha': 10.0 ** -np.arange(1, 7),
                    'hidden_layer_sizes': np.arange(5, 12),
                    'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    # 'hidden_layer_sizes': [(5, 2), (7, 7), (128,), (128, 7)],
                }
            }

        elif algorithm_code == 'extra_trees':
            algorithm = {
                'name': 'Extra Trees Classifier',
                'function': ExtraTreesClassifier(**parameters),
                'grid_search': {
                    'n_estimators': np.arange(50, 1000, 50),
                    'min_sample_split': np.arange(1, 6),
                    'max_depth': np.arange(3, 10),
                    'criterion': ['gini', 'entropy']
                }
            }

        elif algorithm_code == 'ada_boost':
            algorithm = {
                'name': 'Ada Boost Classifier',
                'function': AdaBoostClassifier(**parameters),
                'grid_search': {
                    'n_estimators': np.arange(50, 500, 50),
                    'learning_rate': np.arange(0.1, 2, 0.05),
                    "base_estimator__criterion": ["gini", "entropy"]
                }
            }

        elif algorithm_code == 'gradient_boost':
            algorithm = {
                'name': 'Gradient Boosting Classifier',
                'function': GradientBoostingClassifier(**parameters),
                'grid_search': {
                    'n_estimators': np.arange(10, 500, 10),
                    'max_depth': np.arange(1, 10, 1),
                    'learning_rate': np.arange(0.05, 2, 0.05),
                    'min_samples_leaf': np.arange(20, 200, 20)
                }
            }

        else:
            raise ModuleNotFoundError('Algorithm not available.')

        # String with parameters used
        algorithm['parameters'] = '; '.join([parameter + ': ' + str(value) for parameter, value in parameters.items()])

        return algorithm

    @staticmethod
    def grid_search(algorithm_code, feature_cols, test_size, class_len=None, pca=False):
        try:
            algorithm = GenericModel.get_algorithm(algorithm_code, {})
            classifier = algorithm['function']
            classifier_name = algorithm['name']
            classifier_parameters = algorithm['parameters']
            classifier_grid_search = algorithm['grid_search']
        except ModuleNotFoundError as e:
            return str(e)

        dataset = GenericModel.DB.load_csv(DIR + 'csv_files/train_features_data.csv')

        feature_arr = [dataset.columns.get_loc(feature_name) for feature_name in feature_cols]
        if class_len is None:
            X = dataset.iloc[:, feature_arr].values
            y = dataset.iloc[:, dataset.columns.get_loc("target")].values
        else:
            X = dataset.iloc[:, feature_arr][dataset.length == class_len].values
            y = dataset.iloc[:, dataset.columns.get_loc("target")][dataset.length == class_len].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)  # , random_state=None)

        """
        For PCA ANalysis
        """
        kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        if pca:
            pipe = Pipeline([
                ('pca', PCA()),
                ('clf', classifier),
            ])
            parameters = {'pca__n_components': [2, 3, 4, 5, 6, 7]}
            for k, v in classifier_grid_search.items():
                parameters['clf__' + k] = v

            CV_rfc = GridSearchCV(pipe, parameters, cv=kf, n_jobs=-1, verbose=1)
        else:
            CV_rfc = GridSearchCV(estimator=classifier, param_grid=classifier_grid_search, cv=kf)
        CV_rfc.fit(X_train, y_train)

        Logger.send('------------------GRID--------------------------')
        Logger.send(classifier_name)
        Logger.send("Features used: " + json.dumps(feature_cols))
        Logger.send("Best Params: " + str(CV_rfc.best_params_))
        Logger.send("Accuracy: " + str(CV_rfc.best_score_))
        Logger.send('------------------------------------------------')

        # if class_len is None:
        #     _, acc = GenericModel.apply_model(algorithm_code, CV_rfc.best_params_, feature_cols, 'x.csv', 0.3)
        # else:
        #     algorithm_obj = {
        #         'name': algorithm_code,
        #         'parameters': CV_rfc.best_params_,
        #         'feature_cols': feature_cols
        #     }
        #     _, acc = GenericModel.apply_model_by_class(algorithm_obj, class_len)

        return CV_rfc.best_params_, str(CV_rfc.best_score_)

    @staticmethod
    def recursive_feature_elimination(feature_cols, algorithm, parameters):
        # Recursive Feature Elimination
        from sklearn.feature_selection import RFE
        # create a base classifier used to evaluate a subset of attributes
        try:
            algorithm = GenericModel.get_algorithm(algorithm, parameters)
            classifier = algorithm['function']
            classifier_name = algorithm['name']
            classifier_parameters = algorithm['parameters']
        except ModuleNotFoundError as e:
            return str(e)

        dataset = GenericModel.DB.load_csv('../csv_files/train_features_data.csv')
        feature_arr = [dataset.columns.get_loc(feature_name) for feature_name in feature_cols]
        X = dataset.iloc[:, feature_arr].values
        y = dataset.iloc[:, dataset.columns.get_loc("target")].values

        # create the RFE model and select 3 attributes
        rfe = RFE(classifier, 3)
        rfe = rfe.fit(X, y)
        # summarize the selection of the attributes
        print(rfe.support_)
        print(rfe.ranking_)
