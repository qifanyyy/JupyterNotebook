profiling = True
if profiling:
    import cProfile
    import re

import numpy as np
import sys

def update_rule(eta, w, m):
    """
    INPUT:
    eta     -> float (in interval [0,0.5])
    w       -> np.ndarray (1-dimensional, weights)
    m       -> np.ndarray (same dimension as w, costs or gains)
    OUTPUT:
    w       -> np.ndarray (1-dimensional, updated weights)
    p       -> np.ndarray (same dimension as w, new distribution)
    """
    update_rule.counter += 1
    # Update rule for the weights:
    w = (1 - eta * m) * w
    # Calculate sum over all weights:
    phi = w.sum()
    # Calculate corresponding distribution:
    p = w / phi
    return w, p


def random_decision(p):
    """
    INPUT:
    p       -> np.ndarray (1-dimensional, distribution)
    OUTPUT:
    i       -> int (randomly chosen decision)
    """
    # Number of options:
    n = p.size
    # Get random instance over distribution:
    i = np.random.choice(n, 1, p=p)[0]
    return i


def mwup(eta, M, winnow=False, A=np.empty(0)):
    """
    INPUT:
    eta     -> float (in interval [0,0.5])
    M       -> np.ndarray (2-dimensional, costs or gains for all rounds,
               each row one round)
    OUTPUT:
    p       -> np.ndarray (1-dimensional, distribution)
    """
    T, n = M.shape
    w = np.ones(n)
    p = w / n
    for m in M:
        if winnow:
            current = np.matmul(A, p)
            # if (current >= 0).all(): break
        i = random_decision(p)      # for demonstrating purposes
        w, p = update_rule(eta, w, m)
    return p


def random_misclass(A, p):
    """
    INPUT:
    A       -> np.ndarray (2-dimensional, each row on feature vector)
    p       -> np.ndarray (1-dimensional, distribution)
    OUTPUT:
    i       -> int (randomly chosen misclassified example)
               or None (if none exist)
    """
    # Check which examples are misclassified:
    negative_check = np.matmul(A, p) < 0
    # If any misclassified examples exit:
    if negative_check.any():
        # Equal distribution over all misclassified examples:
        choice_prob = negative_check / negative_check.sum()
        return random_decision(choice_prob)
    # If not misclassified examples exist:
    else: return None
        

def winnow(epsilon, A, l):
    """
    INPUT:
    epsilon -> float (margin)
    A       -> np.ndarray (2-dimensional, each row on feature vector)
    l       -> np.ndarray (1-dimensional, labels, all values 1 or -1)
    OUTPUT:
    x       -> np.ndarray (1-dimensional, solution vector, distribution)
    """
    # Initializations:
    n = A.shape[1]
    A = np.matmul(np.diag(l), A)
    rho = abs(A).max()
    eta = epsilon / 2 / rho
    w = np.ones(n)
    x = w / n
    # Randomly choose misclassified example:
    i = random_misclass(A, x)
    # Loop until no misclassified example left:
    while i is not None:
        # Costs:
        m = - A[i] / rho
        # Updated w and x:
        w, x = update_rule(eta, w, m)
        # Randomly choose misclassified example:
        i = random_misclass(A, x)
    return x


def read_data():
    input_data = sys.stdin
    for line in input_data:
        if line[0] == '#':
            values = line.split()[1:4]
            n, k = [np.int(j) for j in values[:2]]
            epsilon = np.float64(values[2])
            A = np.empty([k,n], dtype=np.float64)
            l = np.empty([1,k], dtype=np.int)[0]
            i = 0
        else:
            values = line.split()
            A[i] = [np.float64(j) for j in values[:n]]
            l[i] = np.int(values[n])
            i += 1
    return A, l, epsilon


# example:
epsilon = .5
# A = np.array([[-4,-3], [-3,3], [-3,1], [-2,-4], [-1,5], [-1,-2], [1,3], [1,-4], [3,5], [3,1], [3,-2], [6,4]])
# l = np.array([-1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1])
A = np.array([[-3,-1], [-1,3], [.5,-3], [3,1]])
l = np.array([-1,-1,1,1])
# A, l, epsilon = read_data()
# print(A)
# print(l)
# print(epsilon)
update_rule.counter = 0
x = winnow(epsilon, A, l)
print("SOLUTION:")
print(x)

if profiling:
    cProfile.run('winnow(epsilon, A, l)')