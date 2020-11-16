import sys
sys.path.append("..")

import numpy as np
from base import NeighborsBase
from sklearn.base import ClassifierMixin
from sklearn.neighbors import NearestNeighbors

class MLkNN(ClassifierMixin, NeighborsBase):
    def __init__(self, n_neighbors=5, s = 1, metric = 'minkowski', p=2,
                 algorithm='auto', leaf_size=30, metric_params=None,n_jobs = None):
        
        
        super().__init__(
            n_neighbors=n_neighbors,
            algorithm=algorithm,
            leaf_size=leaf_size, metric=metric, p=p,
            metric_params=metric_params,
            n_jobs=n_jobs)
        
        self._k = n_neighbors
        self.s = s
        self.nn_obj = self.__set_nn_obj()
        self.prior = None
        self.posterior = None
        
    def __set_params(self, X, y):
        n_labels = y.shape[1]
        self.__dict__.update({'n_labels': n_labels})
        self.__fit_nn_obj(X)
    
    def __set_nn_obj(self):
        if self.metric is not None:
            return NearestNeighbors(n_neighbors = self._k + 1, metric = self.metric,
                algorithm = self.algorithm, leaf_size = self.leaf_size, p = self.p,
                metric_params = self.metric_params, n_jobs = self.n_jobs)
        else:
            raise Exception("Metric cannot be none")
        
    def __fit_nn_obj(self, X):
        _ = self.nn_obj.fit(X)
    
    def __get_nn_matrix(self, X, train=False):
        if train:
            return self.nn_obj.kneighbors(X, n_neighbors=self._k+1, return_distance=False)[:,1:]
        else:
            return self.nn_obj.kneighbors(X, n_neighbors=self._k, return_distance=False)
    
#     def __get_membership_counting_vectors(nn_mat):
#         C_x = np.empty(self.y_train.shape)
#         for i, row in enumerate(nn_mat):
#             C_x[i] = self.y_train[row[1:]].sum(axis=0)
#         return C_x
    
    def __set_prior(self, y_train):
        prior = np.zeros((self.n_labels, 2))
        prior[:,1] = (self.s + y_train.sum(axis=0)) / (self.s * 2 + y_train.shape[0])
        prior[:,0] = 1 - prior[:,1]
        setattr(self, 'prior', prior)
    
    def __set_posterior(self, C_x, y):
        posterior = np.zeros((self.n_labels, self._k+1, 2))
        for label in range(self.n_labels):
            c = np.zeros(self._k + 1)
            c_p = np.zeros(self._k + 1)
            for row in range(C_x.shape[0]):
                d = C_x[row,label]
                if y[row,label] == 1:
                    c[d] += 1
                else:
                    c_p[d] += 1
            for neighbor in range(self._k+1):
                posterior[label,neighbor,1]=(self.s+c[neighbor])/(self.s*(self._k+1)+c.sum())
                posterior[label,neighbor,0]=(self.s+c_p[neighbor])/(self.s*(self._k+1)+c_p.sum())

        setattr(self, 'posterior', posterior)
    
    def __get_membership_counting_vectors(self, nn_mat, y_train):
        return np.array([y_train[row].sum(axis=0) for row in nn_mat], dtype=int)
    
    def fit(self, X, y):
        if y.shape[1] < 2:
            raise ValueError("Target must be one-hot encoded label vectors")
        
        self.__dict__.update({'__x_train': X, '__y_train': y})
        
        self.__set_params(X, y)
        self.__set_prior(y)
        nn_mat = self.__get_nn_matrix(X)#, train=True)
        
        C_x = self.__get_membership_counting_vectors(nn_mat, y)
        self.__set_posterior(C_x, y)
    
    def predict(self, X):
        y_pred = np.zeros((X.shape[0], self.n_labels))
        nn_mat = self.__get_nn_matrix(X)
        C_x = self.__get_membership_counting_vectors(nn_mat, getattr(self, '__y_train'))
        for label in range(self.n_labels):
            for row in range(C_x.shape[0]):
                y_t_1 = self.prior[label, 1] * self.posterior[label, C_x[row, label], 1]
                y_t_0 = self.prior[label, 0] * self.posterior[label, C_x[row, label], 0]
                y_pred[row, label] = int(y_t_0 <= y_t_1)
        
        return y_pred.astype(int)
    
    def predict_proba(self, X):
        r_pred = np.zeros((X.shape[0], self.n_labels))
        nn_mat = self.__get_nn_matrix(X)
        C_x = self.__get_membership_counting_vectors(nn_mat, getattr(self, '__y_train'))
        for label in range(self.n_labels):
            for row in range(C_x.shape[0]):
                y_t_1 = self.prior[label, 1] * self.posterior[label, C_x[row, label], 1]
                y_t_0 = self.prior[label, 0] * self.posterior[label, C_x[row, label], 0]
                r_pred[row, label] = y_t_1 / (y_t_0 + y_t_1)
        
        return r_pred
    
    def __get_valid_metric(self, show_all=False):
        if show_all:
            return neighbors.VALID_METRICS
        
        if self.algorithm == 'auto':
            if (callable(self.metric) or
                  self.metric in neighbors.VALID_METRICS['ball_tree']):
                alg_check = 'ball_tree'
            else:
                alg_check = 'brute'
        else:
            alg_check = self.algorithm
        return neighbors.VALID_METRICS[alg_check]
    
    def VALID_METRIC(self, show_all=False):
        return self.__get_valid_metric(show_all)
        
