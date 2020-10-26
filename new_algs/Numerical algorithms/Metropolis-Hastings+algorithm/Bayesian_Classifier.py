import numpy as np
from math import exp, log
import random
import scipy.stats
import matplotlib.pyplot as plt
from copy import deepcopy

#Feature size
N = 2

#Model parameters
Theta = np.array([random.gauss(0,1) for i in range(N)])

def LogPrior(theta_p):
    '''
    Return prior pdf. Multivariate gaussian, Cov = diag(1).
    theta_p = numpy array.
    '''
    global Theta
    return scipy.stats.multivariate_normal(mean=Theta).logpdf(theta_p)

def LogLikelihood(T,X,Y):
    '''
    Return likelihood of data X based on a logistic model.
    T = numpy array, X = numpy array of arrays, Y = numpy array.
    '''
    log_L = 0
    for i in range(len(X)):
        T_x = sum(T*X[i])
        E_t = exp(T_x)
        if Y[i] == 1: log_L += T_x - log(1+E_t)
        else: log_L -= log(1+E_t)
    return log_L

def MCMC(X,Y, b=5000):
    '''
    Return sampling chain.
    Metropolis Hastings Algorithm.
    X = numpy array of arrays, Y = numpy array.
    b = burn in period (int) (default=5000).
    '''
    global Theta, N

    curr = deepcopy(Theta)
    Chain = []

    for i in range(15000):
        Prop = np.array([random.gauss(curr[j],.01) for j in range(N)])
        
        alpha = exp(LogLikelihood(Prop,X,Y) + LogPrior(Prop) -
                    LogLikelihood(curr,X,Y) - LogPrior(curr))

        if random.uniform(0,1) <= alpha:
            curr = deepcopy(Prop)
            if i > b: Chain.append(curr)

    Chain = np.array(Chain) 
    return Chain
        
def test_data_set():
    '''
    Return test data (X, Y) and model parameters.
    '''
    global N
    
    test_theta = np.array([random.gauss(0,1) for i in range(N)])
    X_test, Y_test = [], []

    def model(theta, X):
        E_t = exp(sum(theta*X))
        return E_t/(1+E_t)
        
        
    for i in range(1000):
        X = np.array([random.gauss(0,1) for i in range(N)])
        X_test.append(X)
        p = model(test_theta, X)
        if random.uniform(0,1) <= p: Y_test.append(1)
        else: Y_test.append(0)

    return np.array(X_test), np.array(Y_test), test_theta

def plot(y):
    '''
    Plot series y.
    '''
    t = np.array(range(len(y)))
    plt.plot(t,y)
    plt.show()

if __name__ == '__main__':
    X, Y, T = test_data_set()

    print T
    
    Chain = MCMC(X,Y)
    t_1 = [Chain[j][0] for j in range(len(Chain))]
    t_2 = [Chain[j][1] for j in range(len(Chain))]
    
    plot(t_1)
    plot(t_2)
