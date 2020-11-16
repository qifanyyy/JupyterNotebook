import sys
sys.path.insert(0,'kineticsCode/')
import numpy as np
from kinmodel_ssfun import ssfun
from MHGPBO_with_localgp_adaCov import MHGPBO


def uniform(z, low, high):
   if z<low or z>high:
       return 1.0e-45
   return 1.0/(high - low)

def logmyPosterior(z):
   p = ssfun(z)
   N = 40
   sig = 0.1
   loglikelihood = -N*0.5*np.log(2*np.pi) -N*0.5*np.log(sig) - 0.5*(1/(sig))*p
   retval = np.log(uniform(z[0],0.0,2.0)) + np.log(uniform(z[1],0.0,0.10)) + np.log(uniform(z[2],0.0,2.0)) +\
            np.log(uniform(z[3],0.0,0.10)) + np.log(uniform(z[4],0.0,2.0)) + np.log(uniform(z[5],0.0,2.0)) + loglikelihood   
   return retval


l = 0.0
bounds = [(l,2.0),(l,0.10),(l,2.0),(l,0.10),(l,2.0),(l,2.0)]
sampler = MHGPBO(f = logmyPosterior, dim = 6, lowerbounds = [l,l,l,l,l,l], upperbounds = [2.0, 0.10, 2.0, 0.10, 2.0, 2.0], xInit = None, 
                 GPVariance = 0.1, GPLengthScale = [0.1,0.1,0.1,0.1,0.1,0.1], GPNoiseVariance = 1e-10, 
                 BO_max_iteration = 50, GPTrainIteration = 20000, totalIteration = 20000, burninPeriod = 20000, 
                 threshold = 0.1, maxEntryofCov = 0.001, isVerbose = 1, logData = True)
samplesTaken = sampler.RunMHGP()
print('MHGP completed running. Saving the samples in file...')
samplesTaken.dump('sampleMHGP_localgp_withAdacov_thresh0.1_maxcov0.001_Oct6_2019')
print('Done!')

