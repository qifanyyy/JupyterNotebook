import numpy as np
from MHGP import MHGP
from matplotlib.pylab import *

def myPosterior(z):
    return -np.log(sqrt(2*pi)) -z*z/2.

bounds = [(-3.5,3.5)]
initXs = np.array([[-0.6],[0.5]])
sampler = MHGP(myPosterior, bounds, initXs, 0.01, 0.1, 0.005, 50, 500, 10000, 0.01)
samplesTaken, numOfCallsMHGP, covProposal, max_pt_bo, chain,_ = sampler.RunMHGP()
x = arange(-4,4,.1)
y = myPosterior(x)
#plot(x,y,'ro')
ylabel('Frequency')
xlabel('x')
hist(samplesTaken, bins=80,normed=1)
show()