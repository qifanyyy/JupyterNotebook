from sklearn import ensemble
import numpy as np

class BaseAlgSel(object):

    def __init__(self, modeltype='ET', n_estimators=100, n_jobs=-1):
        self.modeltype = modeltype
        self.n_estimators = n_estimators
        self.learner = None
        self.n_jobs = n_jobs
        if self.modeltype=='ET':
            self.treesmodel = ensemble.ExtraTreesRegressor
        elif self.modeltype=='RF':
            self.treesmodel = ensemble.RandomForestRegressor

    def predict_algID(self, X):
        preds = self.predict_runtime(X)
        BestAlgIDs = preds.argmin(axis=1)
        return BestAlgIDs

class AlgSel_SingleOutputModel(BaseAlgSel):
    def __init__(self, modeltype='ET', n_estimators=100, n_jobs=-1):
        super(AlgSel_SingleOutputModel,self).__init__(
            modeltype = modeltype,
            n_estimators = n_estimators,
            n_jobs = n_jobs)
        self.name = 'Single-output ' + modeltype

    def __str__(self):
        s = 'Single-output ' + self.modeltype
        s += "; ntrees=%d" % (self.n_estimators)
        return s

    def fit(self, X, y):
        print 'training single-output', self.modeltype
        etrgrs = []
        for i in range(y.shape[1]):
            print '\tsingle-output', self.modeltype, i
            etrgr = self.treesmodel(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
            etrgr.fit(X, y[:,i])
            etrgrs += [etrgr]
        self.learner = etrgrs

    def predict_runtime(self, X):
        preds = []
        for etrgr in self.learner:
            pred = etrgr.predict(X)
            preds += [pred]
        preds = np.array(preds)
        preds = preds.T

        return preds


class AlgSel_StackModel(BaseAlgSel):
    def __init__(self, modeltype='ET', n_estimators=100, n_jobs=-1):
        super(AlgSel_StackModel,self).__init__(
            modeltype = modeltype,
            n_estimators = n_estimators,
            n_jobs = n_jobs)

    def __str__(self):
        s = 'Stack Single-output ' + self.modeltype
        s += "; ntrees=%d" % (self.n_estimators)
        return s

    def fit(self, X, y):
        print 'training stack-model', self.modeltype
        # 1st model
        print '  1st stage'
        etrgrs1 = []
        pred1 = []
        for i in range(y.shape[1]):
            print '\tsingle-output', self.modeltype, i
            etrgr = self.treesmodel(n_estimators=self.n_estimators, n_jobs=-1)
            etrgr.fit(X, y[:,i])
            pred = etrgr.predict(X)
            pred1 += [pred]
            etrgrs1 += [etrgr]
        pred1 = np.array(pred1).T

        # 2nd model
        print '  2nd stage'
        X_stack = np.concatenate((X, pred1), axis=1)
        print 'X_stack:', X_stack.shape
        etrgrs2 = []
        for i in range(y.shape[1]):
            print '\tsingle-output', self.modeltype, i
            etrgr = self.treesmodel(n_estimators=self.n_estimators, n_jobs=-1)
            etrgr.fit(X_stack, y[:,i])
            etrgrs2 += [etrgr]

        self.learner = [etrgrs1, etrgrs2]

    def predict_runtime(self, X):
        etrgrs1 = self.learner[0]
        etrgrs2 = self.learner[1]
        # 1st model
        pred_test1 = []
        for etrgr in etrgrs1:
            pred = etrgr.predict(X)
            pred_test1 += [pred]
        pred_test1 = np.array(pred_test1).T

        # 2nd model
        X_test_stack = np.concatenate((X, pred_test1), axis=1)

        pred_test2 = []
        for etrgr in etrgrs2:
            pred = etrgr.predict(X_test_stack)
            pred_test2 += [pred]
        pred_test2 = np.array(pred_test2).T

        return pred_test2


class AlgSel_MultiOutputModel(BaseAlgSel):
    def __init__(self, modeltype='ET', n_estimators=100, n_jobs=-1):
        super(AlgSel_MultiOutputModel,self).__init__(
            modeltype = modeltype,
            n_estimators = n_estimators,
            n_jobs = n_jobs)

    def __str__(self):
        s = 'Multi-output ' + self.modeltype
        s += "; ntrees=%d" % (self.n_estimators)
        return s

    def fit(self, X, y):
        print 'training multi-output', self.modeltype
        self.learner = self.treesmodel(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
        self.learner.fit(X, y)

    def predict_runtime(self, X):
        preds = self.learner.predict(X)
        return preds


class AlgSel_CombinedModel(BaseAlgSel):
    def __init__(self, modeltype='ET', n_estimators=100, alpha=0.5, n_jobs=-1):
        super(AlgSel_CombinedModel,self).__init__(
            modeltype = modeltype,
            n_estimators = n_estimators,
            n_jobs = n_jobs)
        self.alpha = alpha

    def __str__(self):
        s = 'Combined Single- and Multi-output ' + self.modeltype
        s += "; ntrees=%d" % (self.n_estimators)
        s += "; alpha=%d" % (self.alpha)
        return s

    def fit(self, X, y):
        print '\tcombined single- and multi-output', self.modeltype
        print '\tmulti-output', self.modeltype
        rgrmul = self.treesmodel(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
        rgrmul.fit(X, y)
        etrgrs = []
        for i in range(y.shape[1]):
            print '\tsingle-output', self.modeltype, i
            etrgr = self.treesmodel(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
            etrgr.fit(X, y[:,i])
            etrgrs += [etrgr]
        self.learner = [rgrmul, etrgrs]

    def predict_runtime(self, X):
        rgrmul = self.learner[0]
        preds_mul = rgrmul.predict(X)
        preds = []
        for etrgr in self.learner[1]:
            pred = etrgr.predict(X)
            preds += [pred]
        preds = np.array(preds)
        preds = preds.T
        preds_combined = self.alpha*preds_mul + (1-self.alpha)*preds
        return preds_combined

