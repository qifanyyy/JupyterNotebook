import numpy as np
from operator import itemgetter
from utils.information_metrics import *


class MRMR():
    """
    This class implements the mRMR algorithm for feature-selection presented
    by Peng et al. in http://ieeexplore.ieee.org/document/1453511/


    Arguments
    ----------

    n_features : int (default=20), number of feature to select. If None are
        provided, then all the features that are available are ranked/ordered.

    k_max : int (default=None), the maximum number of top-scoring features to
        consider. If None is provided, then all the features that are available
        are consider.

    """

    def __init__(self, n_features=20, k_max=None):
        self.n_features = n_features
        self.k_max = k_max

    @staticmethod
    def _mutual_information_target(X, y):
        """
        Calculate mutual informaton between each column vector of the feature
        matrix X and target vector y.


        Parameters
        ----------
        X : numpy array, feature matrix
        y : numpy array, target vector

        Returns
        -------
        res : list of tuples (idx, val), where idx is the index of the feature
                vector with respect to the feature matrix X, and val is the the
                mutual information value. The list is sorted in ascending order
                with respect to mutual information value.

        """

        mi_vec = []
        for x in X.T:
            mi_vec.append(mutual_information(x, y))

        return sorted(enumerate(mi_vec), key=itemgetter(1), reverse=True)

    def _handle_fit(self, X, y, threshold=0.8):
        """ handler method for fit """

        ndim = X.shape[1]
        if self.k_max:
            k_max = min(ndim, self.k_max)
        else:
            k_max = ndim

        ## TODO: set k_max
        k_max = ndim

        # mutual informaton between feature fectors and target vector
        MI_trg_map = self._mutual_information_target(X, y)

        # subset the data down to k_max
        sorted_MI_idxs = [i[0] for i in MI_trg_map]
        X_subset = X[:, sorted_MI_idxs[0:k_max]]

        # mutual information within feature vectors
        MI_features_map = {}

        # Max-Relevance first feature
        idx0, MaxRel = MI_trg_map[0]

        mrmr_map = [(idx0, MaxRel)]
        idx_mask = [idx0]

        MI_features_map[idx0] = []
        for x in X_subset.T:
            MI_features_map[idx0].append(mutual_information(x, X_subset[:, idx0]))

        for _ in range(min(self.n_features - 1, ndim - 1)):

            # objective func
            phi_vec = []
            for idx, Rel in MI_trg_map[1:k_max]:
                if idx not in idx_mask:
                    Red = sum(MI_features_map[j][idx] for j, _ in mrmr_map) / len(mrmr_map)
                    phi = (Rel - Red)
                    phi_vec.append((idx, phi))

            idx, mrmr_val = max(phi_vec, key=itemgetter(1))

            MI_features_map[idx] = []
            for x in X_subset.T:
                MI_features_map[idx].append(mutual_information(x, X_subset[:, idx]))

            mrmr_map.append((idx, mrmr_val))
            idx_mask.append(idx)

        mrmr_map_sorted = sorted(mrmr_map, key=itemgetter(1), reverse=True)
        return [x[0] for x in mrmr_map_sorted]

    def fit(self, X, y, threshold=0.8):
        """
        fit method.


        Parameters
        ----------
        X : numpy array, discretized data
        y : numpy array or list, class labels
        threshold : float (default=0.8), controls the mutual informaton whithin
            feature vectors.

        Raise
        ----------
        ValueError : if X is not of type numpy.ndarray.
        ValueError : if y is not of type numpy.ndarray or list.
        ValueError : if threshold is not between 0 and 1.

        Returns
        ----------
        matrix : numpy array of size (X.size, n_features),
            containing selected feature vectors

        """

        if type(X) != np.ndarray:
            raise ValueError('X must be of type numpy array.')

        if type(y) != np.ndarray:
            if type(y) == list:
                y = np.array(y)
            else:
                raise ValueError('y must be of type numpy array or list.')

        if not 0.0 < threshold < 1.0:
            raise ValueError('threshold value must be between o and 1.')

        return self._handle_fit(X, y, threshold)
