#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from scipy.io.arff import loadarff
from sklearn.feature_extraction import DictVectorizer


class Arff2Skl():

    def __init__(self, fname):
        assert(os.path.exists(fname))
        self._data, self._meta = loadarff(fname)
        self._t = {'X': DictVectorizer(sparse=False),
                   'y': DictVectorizer(sparse=False)}

    def to_dict(self):
        D = self.__arrf2dict()
        return D

    def transform(self, lab=[]):
        D = self.__arrf2dict()
        if not lab:
            lab = self._meta.names()[-1]
        D, l = self.__split_label(D, lab)
        X = self._t['X'].fit_transform(D)
        y = self._t['y'].fit_transform(l)
    
        return X, y

    def inverse_transform(self, X, y):
        D = self._t['X'].inverse_transform(X)
        l = self._t['y'].inverse_transform(y)
        return D, l

    def __arrf2dict(self):
        D = []
        for sample in self._data:
            d = {}
            for val, cat in zip(sample, self._data.dtype.names):
                d[cat] = str(val)
            D.append(d)
        return D

    def __split_label(self, D, lab):
        l = []
        for d in D:
            l.append({lab: d.pop(lab)})
        return D, l

    @property
    def data(self):
        return self._data

    @property
    def meta(self):
        return self._meta


if __name__ == '__main__':
    cvt = Arff2Skl('phishing.arff')
    X, y = cvt.transform()
    D, l = cvt.inverse_transform(X, y)
    print(D, l)
