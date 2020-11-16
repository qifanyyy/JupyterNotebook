# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:14:03 2013

@author: hok1
"""

import numpy as np

class MetropolisHastingsAlgorithm:
    def proposedDistribution(self, y):
        return np.random.normal(loc=y)
        
    def distribution(self, x):
        return 1/(np.exp((x-8))+1) if x>=0 else 0
        
    def __init__(self):
        self.chain = [np.random.uniform(0, 10)]
        
    def produceNext(self):
        # implementing Metropolis-Hasting Algorithm
        lastX = self.chain[-1]
        newX = self.proposedDistribution(lastX)
        alpha = min(1, self.distribution(newX) / self.distribution(lastX))
        u = np.random.uniform()
        self.chain.append(newX if alpha > u else lastX)
        
# Sampling sigmoid / Fermi distribution
class SamplingSigmoidDistribution(MetropolisHastingsAlgorithm):
    def distribution(self, x):
        return 1/(np.exp(self.beta*(x-self.fermiEnergy))+1) if x>=0 else 0
        
    def __init__(self):
        MetropolisHastingsAlgorithm.__init__(self)
        self.fermiEnergy = 5
        self.beta = 10.
        
def testrun():
    s = SamplingSigmoidDistribution()
    for i in range(15000):
        s.produceNext()
    return s.chain

if __name__ == '__main__':
    testrun()
