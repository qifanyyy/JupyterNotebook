"""
Binary Coordinate Ascent algorithm for feature subset selection

Authors: Amin Zarshenas <mzarshen@hawk.iit.edu>
         Vijay Srinivas Tida
         Kenji Suzuki
"""

import numpy as np
from sklearn.utils import check_X_y
from sklearn.model_selection import cross_val_score
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted


class BCA(BaseEstimator):

    """Feature Selection with Binary Coordinate Ascent Algorithm

    Given an external estimator, the goal of binary coordinate ascent
    (BCA) algorithm is to select features which maximize an objective
    function of an estimator. It returns a binary vector with its size
    equal to the number of features, where zero or one indicates a
    feature at that position is not selected, or selected, respectively.
    First the best feature subset is initialized (specified as a binary
    vector). The default initialization is the vector of all zeros,
    corresponding to no input features selected. The corresponding
    objective function of an specified estimator is then calculated for
    the initial subset. BCA algorithm then iteratively select or remove
    features, one at a time, by flipping the binary elements of the
    binary vector of features, and examine if the selection/removal can
    increase the objective function. The process will be repeated over
    this vector for several times untill a convergance criteria is
    reached (can be set to number of iterations or a delta for objective
    value). The algorithm will return a binary vector corresponding to
    the "best" subset of features.

    Read more in the reference link specified below:

    http://www.sciencedirect.com/science/article/pii/S0950705116302416

    Parameters
    ----------
    
    estimator : object
        A supervised learning estimator with a `` fit `` method that will
        be used along with an objective function, in order to calculate
        the importance of a feature subset.

    scoring : string
        The metric to be used as objective to be maximized, e.g., roc_auc,
        accuracy, etc.
        Note: at the moment sklearn cross_val_score inside the BCA class
        supports binary classification only for roc_auc.

    cv : int, cross-validation generator or an iterable, optional
        The cv parameter used inside the sklearn cross_val_score.

    delta : float

        The delta used to determine the convergance of the objective function.

    Examples
    --------

    The following example shows how to select the optimial subset of features
    in the breast cancer dataset.

    >>> from bca import BCA
    >>> from sklearn.datasets import load_breast_cancer
    >>> from sklearn.naive_bayes import GaussianNB
    >>> X, y = load_breast_cancer().data, load_breast_cancer().target
    >>> estimator = GaussianNB()
    >>> selector = BCA(estimator, scoring='accuracy', cv=5)
    >>> selector = selector.fit(X, y)
    >>> selector.features
    [ 1  4  6  7 16 20 21 22 23 27 28]
    >>> selector.score
    0.971989226626
    >>> selector.predict(X[20:25])
    [1 1 0 0 0]
    
    """
    
    def __init__(self, estimator, scoring='accuracy', cv=5, delta=10**-5):
        self.estimator = estimator
        self.scoring = scoring
        self.cv = cv
        self.delta = delta

    def _estimator_type(self):
        return self.estimator._estimator_type

    def fit(self, X, y, initial_subset=None, fit_estimator=True, verbose=True):
        """Fit the BCA model to find the best subset of features, and
        potentially fit the estimator on the best subset.

        Parameters
        ----------

        X : {array-like, sparse matrix},  shape=[n_samples,n_features]
            The training input samples.

        y : array-like, shape = [n_samples]
            The target values.

        initial_subset : binary vector, shape=[n_features]
            The initial subset. Default to all zeros ("None").

        fit_estimator : boolean,
            Indicates to fit the estimator on the final features or not.

        verbose : boolean
            Indicates the verbosity of the algorithm.

        Returns
        -------

        self : class object 
            The BCA object with trained classifier

        """
        return self._fit(X, y, initial_subset, fit_estimator, verbose)

    def _fit(self, X, y, initial_subset, fit_estimator, verbose):

        X, y = check_X_y(X, y, "csc")

        # scoring function
        def scorer(features):
            return self._scorer(X, y, features, verbose=verbose)

        # initialization
        iteration = 0
        n_features = X.shape[1]
        if initial_subset is not None:
            features = initial_subset
        else:
            features = np.zeros(n_features)

        score = scorer(features)

        if verbose:
            print ("Iteration {0} starts...".format(iteration))

        if verbose:
            self._print_features(features, score)

        # main BCA loop of feature selection
        stop = False

        if verbose:
            print("\nBCA algorithm starts...")

        while not stop:
            iteration += 1
            if verbose:
                print("\nIteration {0} starts...".format(iteration))
            score_best = score

            # one iteration over all features
            for i in range(n_features):
                # flip one of the feature to create a new subset
                features_trial = features.copy()
                features_trial[i] = not features_trial[i]
                score_trial = scorer(features_trial)

                # modify the features if the new subset is better
                if score_trial > score:
                    features = features_trial.copy()
                    score = score_trial

                if verbose:
                    self._print_features(features, score)

            # after each iteration check if the maximization converged
            if abs(score_best-score) < self.delta:
                stop = True

        if verbose:
            print ("\nBCA algorithm finished...")

        # fit a final estimator on the entire dataset
        if fit_estimator:
            if verbose:
                print ("\nFitting the final estimator...")
            self.estimator.fit(X[:, features == 1], y)

        # set final attributes
        self.features = np.arange(len(features))[features == 1]
        self.score = score

        return self

    def predict(self, X):
        """Reduce X to the selected features and then predict using the
        underlying estimator.
        
        Parameters
        ----------
        
        X : array of shape [n_samples, n_features]
            The input samples.
        
        Returns
        -------
        
        y : array of shape [n_samples]
            The predicted target values.

        """
        check_is_fitted(self, 'estimator')
        return self.estimator.predict(X[:, self.features])

    def _scorer(self, X, y, features, verbose):

        if np.sum(features) > 0:
            return np.mean(cross_val_score(self.estimator, X[:, features == 1],
                           y, scoring=self.scoring, cv=self.cv,
                           verbose=verbose))
        else:
            return -np.inf

    def _print_features(self, features, score):
        features = np.arange(len(features))[features == 1]
        print("best feature set so far is {0} with score = {1}".
              format(features, score))
