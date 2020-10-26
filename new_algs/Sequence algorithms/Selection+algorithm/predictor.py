import numpy as np
import pandas as pd
import time

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


class Predictor():

    def __init__(self, lstats):
        self.__weight = lstats.weight

    @property
    def weight(self):
        return self.__weight

    def run(self, outfolder):
        pass


class ClassificationSet():

    def __init__(self, X, y, c, le):
        self.__X = X
        self.__y = y
        self.__c = c
        self.__le = le

    @staticmethod
    def sanitize_and_init(features, winners, costs):
        # encode class labels to numbers
        le = LabelEncoder().fit(costs.columns.values)
        # merge on index
        merged_set = pd.merge(features, winners, left_index=True, right_index=True)
        merged_set = pd.merge(merged_set, costs, left_index=True, right_index=True)
        # reorder cost columns to be sorted in encoded order
        new_costs_columns = le.inverse_transform(np.sort(le.transform(costs.columns)))
        # turn everything into numpy arrays
        X = merged_set[features.columns].values
        y = le.transform(merged_set[winners.columns].values)
        c = merged_set[new_costs_columns].values
        # reshape y
        y = np.reshape(y, (y.shape[0], 1))

        ## HACK: for stratified sampling, remove events from classes with just 1 member
        unique_elements, counts_elements = np.unique(y, return_counts=True)
        one_member_classes = [unique_elements[i]
                              for i, count in enumerate(counts_elements)
                              if count == 1]
        for outclass in one_member_classes:
            index = np.argwhere(y==outclass)[0][0]
            y = np.delete(y, index)
            X = np.delete(X, index, 0)
            c = np.delete(c, index, 0)
        ###
        return ClassificationSet(X, y, c, le)

    @property
    def X(self):
        return self.__X

    @property
    def y(self):
        return self.__y

    @property
    def c(self):
        return self.__c

    @property
    def le(self):
        return self.__le


class Evaluator():

    @staticmethod
    def accuracy(y_true, y_pred):
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def mre(y_true, y_pred, costs):
        return np.mean([(
                costs[i, y_pred[i]] - costs[i, y_true[i]]
            ) ** 2 for i in range(len(y_true))])

    @staticmethod
    def mre_ovhd(y_true, y_pred, costs, costs_ovhd):
        return np.mean([(
                costs_ovhd[i, y_pred[i]] - costs[i, y_true[i]]
            ) ** 2 for i in range(len(y_true))])


class GenericClassifier():

    def __init__(self, train):
        pass

    @property    
    def algo(self):
        return 0

    @property
    def name(self):
        return "GENERIC"

    def predict(self, test):
        # by default, returns perfect classification
        return test.y

    def evaluate(self, test):
        y_pred = self.predict(test)
        acc = Evaluator.accuracy(test.y, y_pred)
        mre = Evaluator.mre(test.y, y_pred, test.c)
        return acc, mre


class RandomClassifier(GenericClassifier):

    def __init__(self, train):
        super().__init__(train)
        self.__labels = train.le.transform(train.le.classes_)
        # init random state
        np.random.seed(int(time.time()))

    @property
    def name(self):
        return "RANDOM"

    @property
    def labels(self):
        return self.__labels

    def predict(self, test):
        return np.random.choice(self.labels, test.X.shape[0])


class BestAlgoClassifier(GenericClassifier):

    def __init__(self, train):
        super().__init__(train)
        # get best algorithm on average on training set
        u, indices = np.unique(train.y, return_inverse=True)
        self.__algo = u[np.argmax(np.bincount(indices))]

    @property    
    def algo(self):
        return self.__algo

    @property
    def name(self):
        return "BEST"

    def predict(self, test):
        return np.full(test.X.shape[0], self.algo, dtype=int)

