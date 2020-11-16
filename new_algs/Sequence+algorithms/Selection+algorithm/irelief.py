"""
 Iterative RELIEF for Feature Weighting.

This is an implementation of Iterative RELIEF algorithm described in:
Yijun Sun. 'Iterative RELIEF for Feature Weightinig: Algorithms,
Theories and Application'. In IEEE Transactions on Pattern Analysis
and Machine Intelligence, 2006.

This code is written by Davide Albanese, <albanese@fbk.eu>.
(C) 2007 mlpy Developers.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np

# from sklearn.feature_selection.base import SelectorMixin

from .core import compute_irelief

__all__ = ['IRelief']


# class IRelief(SelectorMixin):
class IRelief(object):
    """Iterative RELIEF for feature weighting.

    Long description...

    Parameters
    ----------
    T : int, default=1000
        maximum number of iterations

    sigma : float, default=1.0
        kernel parameter(> 0.0)

    theta : float (> 0.0)
        convergence parameter
    """

    def __init__(self, T=1000, sigma=1.0, theta=0.001):

        if T <= 0:
            raise ValueError("T (max loops) must be > 0")
        if sigma <= 0.0:
            raise ValueError("sigma (kernel width) must be > 0.0")
        if theta <= 0.0:
            raise ValueError("theta (convergence parameter) must be > 0.0")

        self._T = T
        self._sigma = sigma
        self._theta = theta
        self._loops = None
        self._w = None

        self._estimator_type = 'xxx'

    def fit(self, X, y):
        """Compute the feature weights.

        Parameters
        ----------

           X : 2d array_like object
              training data (N, P)
           y : 1d array_like object integer (only two classes)
              target values (N)

        :Raises:
           SigmaError
        """

        xarr = np.asarray(X, dtype=float)
        yarr = np.asarray(y, dtype=int)

        if xarr.ndim != 2:
            raise ValueError("x must be a 2d array_like object")

        if yarr.ndim != 1:
            raise ValueError("y must be an 1d array_like object")

        if xarr.shape[0] != yarr.shape[0]:
            raise ValueError("x, y: shape mismatch")

        if np.unique(y).shape[0] != 2:
            raise ValueError("number of classes must be = 2")

        self._w, self._loops = \
            compute_irelief(xarr, yarr, self._T, self._sigma, self._theta)

    @property
    def feature_importances_(self):
        return self._w

    @property
    def weights(self):
        """Returns the feature weights."""

        if self._w is None:
            raise ValueError("no model computed.")

        return self._w

    @property
    def loops(self):
        """Returns the number of loops."""

        if self._loops is None:
            raise ValueError("no model computed.")

        return self._loops

