import numpy as np


def entropy(x):
    """
    Also known as Shanon Entropy, returns the empirical entropy in the input
    vector x.
    Reference: https://en.wikipedia.org/wiki/Entropy_(information_theory)
    """
    _, count = np.unique(x, return_counts=True, axis=0)
    prob = count/len(x)
    return np.sum((-1) * prob * np.log2(prob))


def joint_rntropy(y, x):
    """
    H(y; x)
    Reference: https://en.wikipedia.org/wiki/Joint_entropy
    """
    yx = np.c_[y, x]
    return entropy(yx)


def conditional_entropy(y, x):
    """
    conditional entropy = Joint Entropy - Entropy of x
    H(y|x) = H(y; x) - H(x)
    Reference: https://en.wikipedia.org/wiki/Conditional_entropy
    """
    return joint_rntropy(y, x) - entropy(x)


def mutual_information(x, y):
    """
    Information Gain, I(y; x) = H(y) - H(y|x)
    Reference: https://en.wikipedia.org/wiki/Information_gain_in_decision_trees#Formal_definition

    Returns the information gain/mutual information [H(x) - H(x|y)]
    """
    return (entropy(x) - conditional_entropy(x, y))
