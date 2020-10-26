import os.path

import pandas as pd
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, precision_score, f1_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

import config as cfg


class GenericClassifier():
    train_data = None
    model = None
    name = 'Default'
    model_path = 'Default'

    def __init__(self, X, y, name):

        df = pd.DataFrame(X)
        df['class'] = y

        self.train_data = df

        # Initialize model
        self.name = name
        self.model_path = '{}{}.pkl'.format(cfg.MODELS_PATH, self.name)
        self.__set_trained_model()

    def __save_model(self):
        try:
            joblib.dump(self.model, self.model_path)
        except Exception as e:
            raise e

    def __load_model(self):
        try:
            return joblib.load(self.model_path)
        except Exception as e:
            raise e

    def __set_trained_model(self):

        # If model exists return trained model
        if os.path.isfile(self.model_path):
            classifier = self.__load_model()

            # Set object model
            self.model = classifier


        else:
            classifier = RandomForestClassifier(n_estimators=1000)
            # svm.SVC()
            # rdf.RandomForestClassifier(n_estimators=250)
            # MultinomialNB()
            # MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2),random_state=1)
            classifier.fit(self.train_data[:], self.train_data['class'].values)

            # Set object model
            self.model = classifier

            # Save model to file
            self.__save_model()

    def __evaluate_classifiers(self, df_results):
        cols = df_results.shape[1]
        classes = df_results['class'].unique()
        output = pd.DataFrame()
        for i in range(31, cols):
            df_temp = df_results[df_results.columns[[30, i]]]
            for classe in classes:
                df_temp_class = df_temp[df_temp['class'] == classe]
                df_temp_inv = df_temp[df_temp.ix[:, 1] == classe]
                acc = accuracy_score(y_pred=df_temp_class.ix[:, 1], y_true=df_temp_class.ix[:, 0])
                acc_inv = accuracy_score(y_pred=df_temp_inv.ix[:, 1], y_true=df_temp_inv.ix[:, 0])
                ap = precision_score(y_pred=df_temp_class.ix[:, 1], y_true=df_temp_class.ix[:, 0], average='weighted')
                f1 = f1_score(y_pred=df_temp_inv.ix[:, 1], y_true=df_temp_inv.ix[:, 0], average='micro')
                out_temp = pd.DataFrame([df_temp_class.columns[1], classe, acc, ap, acc_inv, f1]).T
                output = output.append(out_temp)
        output.columns = ['classifier', 'class', 'accuracy', 'binary precision', 'precision', 'f1']
        return output

    def __get_classifiers(self):
        classifiers = {'RandomForrest': RandomForestClassifier(n_estimators=250)
            , 'ExtraTrees': ExtraTreesClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2,
                                                 random_state=0)
            , 'SupportVectorMachines': svm.SVC()
            , 'Multinomial Naive Bayes': MultinomialNB()
            , 'Gaussian Naive Bayes': GaussianNB()
            , 'Neural Networks': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
            , 'AdaBoost': AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1.0
                                             , random_state=None)
            , 'Gradient Boosting': GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=5
                                                              , subsample=0.3, min_samples_split=2, min_samples_leaf=1,
                                                              max_depth=3, init=None, random_state=None,
                                                              max_features=None, verbose=2)
            , 'Decision Trees': DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
            , '3KNN-BTREE': KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree')
            , '3KNN': KNeighborsClassifier(n_neighbors=3)
                       }
        return classifiers

    def __get_trained_classifiers(self):
        classifiers = {'RandomForrest': RandomForestClassifier(n_estimators=250)
            , 'ExtraTrees': ExtraTreesClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2,
                                                 random_state=0)
            , 'SupportVectorMachines': svm.SVC()
            , 'Multinomial Naive Bayes': MultinomialNB()
            , 'Gaussian Naive Bayes': GaussianNB()
            , 'Neural Networks': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
            , 'AdaBoost': AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1.0
                                             , random_state=None)
            , 'Gradient Boosting': GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=5
                                                              , subsample=0.3, min_samples_split=2, min_samples_leaf=1,
                                                              max_depth=3, init=None, random_state=None,
                                                              max_features=None, verbose=2)
            , 'Decision Trees': DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
            , '3KNN-BTREE': KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree')
            , '3KNN': KNeighborsClassifier(n_neighbors=3)
                       }

        train_counts = self.train_data.ix[:, 0:self.train_data.shape[1] - 1]

        for classifier in classifiers:
            model = classifiers[classifier]
            model.fit(train_counts, self.train_data['class'].values)
            classifiers[classifier] = model

        return classifiers

    def get_prediction(self, examples, model=None):
        examples = self.__pre_process_line(examples)
        example_counts = self.count_vect.transform([examples])
        if model is None:
            predictions = self.model.predict(example_counts)
        else:

            predictions = model.predict(example_counts.toarray())
        return predictions  # [1, 0]

    def get_evaluation(self, model=None):
        if model is None:
            model = self.model
        scores = cross_val_score(model, self.train_data.ix[:, 0:self.train_data.shape[1] - 1]
                                 , self.train_data['class'], cv=10)
        return scores.mean(), scores.std()

    def get_metalearning_evaluation(self):

        cv_folds = 10
        classifiers = self.__get_classifiers()

        results = []
        init_data = self.train_data

        for classifier in classifiers:
            t_data = self.train_data.ix[:, 0:self.train_data.shape[1] - 1]
            print("Started model: {0}".format(classifier))
            model = classifiers[classifier].fit(t_data, self.train_data['class'].values)

            # Predict with cross validation
            init_data['eval_' + classifier] = cross_val_predict(model, t_data, self.train_data['class'], cv=cv_folds)

            # Evaluate with cross validation
            scores = cross_val_score(model, t_data, self.train_data['class'], cv=cv_folds)
            results.append([classifier, scores.mean(), scores.std()])

        # Get meta model predictions
        # init_data['eval_metamodel'] = self.get_trusted_predictions()

        output = pd.DataFrame(results)
        output.columns = ['classifier', 'mean accuracy', 'std accuracy']
        class_eval_result = self.__evaluate_classifiers(init_data)
        return output, class_eval_result

    def get_class_balance(self):
        return self.train_data.groupby('class').count()

    def get_model_class_trust_matrix(self):
        matrix = pd.read_csv('./static/trust_matrix_iris.csv', sep=',')
        return matrix

    def get_trusted_predictions(self):
        classifiers = self.__get_trained_classifiers()
        trust_matrix = self.get_model_class_trust_matrix()
        predict_bag = []
        for classifier in classifiers:
            idx = 0
            print("Started model: {0}".format(classifier))
            model = classifiers[classifier]
            prediction = cross_val_predict(model, self.train_data.ix[:, 0:self.train_data.shape[1] - 1], self.train_data['class'].values, cv=10)
            # Get trust ratio
            for pred in prediction:
                ratio = trust_matrix[(trust_matrix['model'] == classifier) & (trust_matrix['class'] == pred)]['trust_ratio']
                predict_bag.append([idx, classifier, pred, float(ratio)])
                idx += 1
        # out_predictions= [c[0][1] for c in pd.DataFrame(predict_bag).groupby([0,2]).sum().groupby(0).idxmax().values]

        # O TIO
        out_predictions = list(pd.DataFrame(predict_bag).ix[pd.DataFrame(predict_bag).groupby([0])[3].idxmax()][2])
        return pd.Series(out_predictions)
