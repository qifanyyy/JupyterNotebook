"""
Noise PGA
=====

# A simple genetic algorithm for feature selection with DEAP library

.. note::
    "Zhu, M., & Chipman, H. (2006). Darwinian Evolution in Parallel Universes: A Parallel Genetic Algorithm
    for Variable Selection. Technometrics, 48(4), 491-502"
    .. _a link: http://www.jstor.org/stable/25471241

.. note::
    "Chun-Xia Zhang et al.(2016) Randomizing outputs to increase variable selection accuracy.
    Neurocomputing, Volume 218, 19 December 2016, Pages 91-102, ISSN 0925-2312"
    .. _a link: http://www.sciencedirect.com/science/article/pii/S0925231216309638

.. module:: noisePGA
   :platform: Unix, Windows
   :synopsis: A simpe genetic algorithm for feature selection

"""

import numpy as np
import pandas as pd
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from sklearn.model_selection import cross_val_score
from sklearn.base import BaseEstimator
from sklearn.base import clone as clone_estimator


class NoiseGAEnsemble(BaseEstimator):

    def __init__(self, estimator, ens_size=10, ngen=15, pop_size='data', prior=0.3333, mut_rate='data',
                 cross_prob=0.5, s=1.2, cv=5, random_state=0, n_jobs=1, verbose=1,):
        """
        PGA ensemble class

        Parameters
        ----------
        estimator : object
        an scikit-learn style estimator
        ens_size : int
            size of ensemble. Default is 10.
        ngen: int
            number of generation in each evolution path. Default is 15.
        pop_size: int or 'data'
            size of initial population in each evolution path.
            If 'data', the size set as  p + p % 2, where p is number of variable.
        border: str
            method of handling borders in space scaling.
        prior: float
            prior probability of the feature emerging for each position in DNA string.
            Using for generate initial population.
        mut_rate:float or 'data'
            mutation rate. The probability of mutating an individual.
            If 'data', mutation rate set as 1 / (size of populaiton)
        cross_prob: float
            the probability of mating two individuals. Defaul is 0.5.
        s: float
            parameter of distortion to control the amount of added noise.
            If 0, means no noise added
        cv: int, cross-validation generator or an iterable
            integer, to specify the number of folds in a KFold
            an object to be used as a cross-validation generator
            an iterable yielding train, test splits
        random_state:int
            random_state parameter for KFold function.
        verobse: int
            verbose paramter for deap.algorithms. Whether or not to log the statistics


        Example
        ---------
        X, y, coef = make_regression(n_samples=150, n_features=100, n_informative=15, n_targets=1,
                                     noise=0.0, coef=True)
        lr = LinearRegression()
        nga = NoiseGAEnsemble(lr, ngen=15, ens_size=50, cv=5, s=1.2)
        nga.fit(X, y)
        print('TRUE: ', np.where(coef > 0)[0])
        print('PRED: ', np.where(nga.get_rmean() > 0.4)[0])
        """

        self.model = estimator
        self.esize = ens_size
        self.NGEN = ngen
        self.cv = cv
        self.n_jobs = n_jobs

        if pop_size == 'data':
            self.pop_size = None
        else:
            self.pop_size = pop_size + pop_size % 2
        if mut_rate == 'data':
            self.MUTPB = None
        else:
            self.MUTPB = mut_rate

        self.prior = prior
        self.CXPB = cross_prob
        self.distortion = s
        self.r_matrix = None
        self.ens_sga = np.empty(ens_size, dtype='object')
        self.verbose = verbose
        self.rs = random_state

    def fit(self, X, y):
        self.X = X
        self.y = y
        n, p = X.shape
        B = self.esize
        ystd = y.std()
        r_matrix = np.zeros((B, p))
        s = self.distortion
        if self.pop_size is None:
            self.pop_size = p + p % 2
        if self.MUTPB is None:
            self.MUTPB = 1. / self.pop_size
        for j in range(B):
            if self.verbose > 0:
                print('##############################')
                print('##############################')
                print('##############################')
                print('PATH # ', j, '  of ', B)
            s = self.distortion
            z = np.random.random()
            yj = y + s * z * ystd
            param = self.get_ga_param()
            self.ens_sga[j] = SGASelection(**param)
            self.ens_sga[j].fit(self.X, yj)
            lastest = self.ens_sga[j].lastest
            r_matrix[j, :] = self._rjb(lastest)
        self.r_matrix = r_matrix
        return self

    def transform(self, X, threshold=0):
        r_mean = self.r_matrix.mean(axis=0)
        th = np.zeros(X.shape[1]) + threshold
        ic = r_mean > th
        if isinstance(X, np.ndarray):
            return X[:, ic]
        elif isinstance(X, pd.DataFrame):
            return X.iloc[:, ic]

    def _rjb(self, pop):
        a = np.array(pop)
        return a.mean(axis=0)

    def get_rmean(self, columns=None):
        r_mean = self.r_matrix.mean(axis=0)
        if columns:
            df = pd.DataFrame(r_mean.reshape(1, -1), columns=columns)
            return df
        else:
            return r_mean

    def get_ga_param(self):
        param = {}
        param['estimator'] = clone_estimator(self.model)
        param['ngen'] = self.NGEN
        param['pop_size'] = self.pop_size
        param['prior'] = self.prior
        param['mut_rate'] = self.MUTPB
        param['cross_prob'] = self.CXPB
        param['cv'] = self.cv
        param['n_jobs'] = self.n_jobs
        param['verbose'] = self.verbose
        param['random_state'] = self.rs
        return param


class SGASelection(BaseEstimator):

    def __init__(self, estimator, ngen=100, pop_size='data', prior=0.3333, mut_rate='data', cross_prob=0.5,
                 cv=5, n_jobs=1, verbose=1, random_state=None):
        self.model = estimator
        self.NGEN = ngen
        if isinstance(pop_size, int):
            self.pop_size = pop_size + pop_size % 2
        else:
            self.pop_size = pop_size
        self.MUTPB = mut_rate
        self.prior = prior
        self.CXPB = cross_prob
        self.bs = None
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.rs = random_state

    def fit(self, X, y):
        self.X = X
        self.y = y
        n, p = X.shape
        self.bs = BinaryString(p, self.prior)
        if self.pop_size is None or self.pop_size == 'data':
            self.pop_size = p + p % 2
        if self.MUTPB is None or self.MUTPB == 'data':
            self.MUTPB = 1. / self.pop_size
        self._init_deap(p)
        pop = self.toolbox.population(n=self.pop_size)
        self._run_deap(pop)
        self.lastest = pop
        return self

    def transform(self, X):
        last = self.lastest[0]
        w = np.array(last)
        z = np.zeros(w.shape[0])
        if isinstance(X, np.ndarray):
            return X[:, w > z]
        elif isinstance(X, pd.DataFrame):
            return X.iloc[:, w > z]

    def _get_attr(self):
        p = self.prior
        return np.random.choice((0, 1), 16, p=[1 - p, p])[0]

    def _neg_AIC(self, individual):
        cv = self.cv
        w = np.array(individual)
        z = np.zeros(w.shape[0])
        ic = w > z
        if not ic.any():
            ic[np.random.randint(ic.shape[0])] = True
        X = self.X[:, ic]
        y = self.y
        n = X.shape[0]
        RSS = cross_val_score(self.model, X, y, scoring='neg_mean_squared_error',
                              cv=cv, n_jobs=1)
        RSS = np.fabs(np.array(RSS))

        F = 2 * np.array(individual).sum() + n * np.log(RSS.mean())

        return -F,

    def _init_deap(self, ind_size):
        self.creator = creator
        self.creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        self.creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_bool", self.bs)
        self.toolbox.register("individual", tools.initRepeat, self.creator.Individual,
                              self.toolbox.attr_bool, ind_size)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self._neg_AIC)
        self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=self.MUTPB)
        self.toolbox.register("select", tools.selBest)

    def _run_deap(self, pop):
        MU = self.pop_size // 2
        LAMBDA = self.pop_size // 2
        algorithms.eaMuPlusLambda(pop, self.toolbox, MU, LAMBDA, self.CXPB, self.MUTPB, self.NGEN,
                                  verbose=self.verbose)
        return pop


class BinaryString():
    # Class for control on individuals generation
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.count = 0
        self.bstring = None

    def __call__(self):
        count = self.count
        self.count = count + 1
        if count == 0:
            self.bstring = self.generate()
        elif count == self.size - 1:
            self.count = 0
            if not self.bstring.any():
                return 1  # preventing the generation of a zero string
        return self.bstring[count]

    def generate(self):
        s = self.size
        p = self.prob
        return np.random.choice((0, 1), s, p=[1 - p, p])
