#!/usr/bin/env python

'''
This is an implementation of the Metropolis Hastings algorithm.
This is used for Bayesian sampling from a distribution that's typically multidimensional and can't be numerically integrated.
It utilizes Markov chains, which are ordered lists of stochastic (random) variables.
The Markov chain wanders around, only remembering the state of the previous iteration.
When the number of samples approaches infinity, the Markov chain will converge to the posterior distribution.

Usage:
Modify the posterior and proposal distribution functions in mh.py to suit your statistical model.

references:
"Pattern Recognition and Machine Learning" by Christopher Bishop
"Information Theory, Inference, and Learning Algorithms" by David Mackay
"Machine Learning: An Algorithmic Perspective" by Stephen Marsland
'''

import numpy as np
from pylab import *
import random

class MH():
    def __init__(self, p, q, samples, method):
        self.samples = samples # integer number of samples to do, typically > 5,000
        self.method = method # independent or random_walk
        self.chain = np.zeros(samples) # initialize list of samples to 0
        self.p = p # posterior distribution
        self.q = q # proposal distribution
        
    def alpha(self,candidate,current):
        if self.method=="random_walk":
            # Gaussian distribution is symmetric, so equation simplifies to just the Metropolis algorithm
            return min(1, self.p(candidate)/self.p(current))
        else:
            return min(1, self.p(candidate)*self.q(current)/self.p(current)*self.q(candidate))
        
    def generate_candidate(self,mu,sigma):
        # randomly generate a candidate value from the proposal distribution
        if self.method=="independent":
            candidate = random.normalvariate(mu,sigma) # proposed move
        elif self.method=="random_walk":
            candidate = self.chain[i] + random.normalvariate(mu,sigma) # proposed move
        return candidate
        
    def sample(self,mu,sigma,burn_in=250):
        self.chain[0] = random.normalvariate(mu,sigma) # initial value
        u = np.random.uniform(0.0, 1.0, self.samples) # array of uniform random variables (between 0 and 1)
        for i in xrange(1,self.samples-1):
            candidate = self.generate_candidate(mu,sigma)
            # accept/reject scheme
            if u[i]<self.alpha(candidate,self.chain[i]):
                # accept the move
                self.chain[i+1] = candidate
            else:
                # reject the move
                self.chain[i+1] = self.chain[i]
        self.chain = self.chain[burn_in:self.samples] # discard the first burn_in samples to prevent influence of the starting distribution
        
    def plot_results(self):
        # create histogram for distribution
        figure(1)
        hist(self.chain, bins = 30) # histogram
        ylabel('Frequency')
        xlabel('Value')
        title('Histogram of Samples')
        # create trace plot of Markov values over all iterations
        figure(2)
        plot(self.chain)
        ylabel('Values')
        xlabel('Iteration #')
        title('Trace Plot of Markov Values')
        show()
        
    def single_sample(self):
        return self.chain[random.randrange(0,self.samples)]

if __name__ == '__main__':
    def PosteriorDistribution(x):
        # creates a probability density function that serves as the proposal distribution
        # let's use a bimodal distribution to represent a non-symmetric distribution
        # another example could be a mixture of two normal distributions
        mu1 = 3 # mean1
        mu2 = 10 # mean2
        v1 = 10 # variance1
        v2 = 3 # variance2
        return 0.3*exp(-(x-mu1)**2/v1) + 0.7* exp(-(x-mu2)**2/v2)    

    def ProposalDistribution(x):
        # one option is exp(-x**/2)/sqrt(2*pi) # standard normal PDF
        # should be tuned to the posterior distribution
        # specify the hyperparameters (mean and variance)
        return exp(-(x-5)**2/(10**2)) # 5 = mu, 10 = sigma
    
    model = MH(PosteriorDistribution,ProposalDistribution,10000,"independent") # last 2 args are # samples and method
    model.sample(5,10) # mu, sigma, burn-in.  for method="random_walk", set mu=0
    print 'A sample from the PDF is: ' + str(model.single_sample())
    model.plot_results()