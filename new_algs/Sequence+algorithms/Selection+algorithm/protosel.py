import numpy as np
from sklearn import neighbors


def enn(data, target):
    """Edited Nearest Neighbor.

    Args:
        data: Data values array.
        target: Target values array

    Returns: Boolean mask of selected instances.
    """
    clf = neighbors.KNeighborsClassifier(3)
    clf.fit(data, target)
    sel = clf.predict(data) == target
    return sel


def renn(data, target):
    """Repeated ENN.

    Args:
        data: Data values array.
        target: Target values array.

    Returns: Boolean mask of selected instances.
    """
    # Select all the instances
    sel = np.ones(len(data), bool)
    clf = neighbors.KNeighborsClassifier(3)

    stop = False
    while not stop:
        clf.fit(data[sel], target[sel])
        # Indices of misclassified instances
        misclassified = (clf.predict(data[sel]) != target[sel]).nonzero()[0]
        # Unselect misclassified instances
        sel[misclassified] = False
        # If there is no misclassified instances, then stops
        if len(misclassified) == 0:
            stop = True

    return sel


def allknn(data, target):
    """All KNN.

    Args:
        data: Data values array.
        target: Target values array.

    Returns: Boolean mask of selected instances.
    """
    sel = []  # Boolean masks of selected instances

    # k takes values [1, .., K] where K = 3
    for k in xrange(1, 4):
        clf = neighbors.KNeighborsClassifier(k)
        clf.fit(data, target)
        sel.append(clf.predict(data) == target)

    # Substitue True and False values with ones and zeros
    sel = [np.where(mask, 1, 0) for mask in sel]

    # Sum masks. Those instances selected less than K times were removed for a
    # given k value -> Thus they are marked for removal (True)
    total = np.array(sel)
    total = np.sum(sel, axis=0)

    sel = total == 3
    return sel


def rnn(data, target):
    """Reduced Nearest Neighbor.

    Args:
        data: Data values array.
        target: Target values array.

    Returns: Boolean mask of selected instances.
    """
    sel = np.ones(len(data), bool)
    clf = neighbors.KNeighborsClassifier(1)

    for p in xrange(len(data)):
        sel[p] = False
        clf.fit(data[sel], target[sel])
        if (clf.predict(data) != target).any():
            sel[p] = True

    return sel
