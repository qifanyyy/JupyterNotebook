import numpy as np
import numpy.random as npr
from system_definitions import example_system_twostate
from experiments import multi_experiment_increasing_rollout_count, load_plot_multi_experiment

# Scalar experiment
seed = 1
npr.seed(seed)

# System definition
n,m,A,B,SigmaA,SigmaB = example_system_twostate()

# Number of rollouts
nr = int(1e7)

# Rollout length
ell = int((m**2*n**4)/2 + (m**2*n**2)/2 + m**2 + 1)

# Model estimation points
ns = 100
s_hist = np.unique(np.round(np.logspace(0,np.log10(nr),ns+1,base=10)).astype(int)[1:])
ns_cur = s_hist.size
while s_hist.size < ns:
    ns_cur += 1
    s_hist = np.unique(np.round(np.logspace(0,np.log10(nr),ns_cur+1,base=10)).astype(int)[1:])

# Number of experiments
ne = 50

# Input mean and covariance settings
u_mean_std = 1
u_covr_std = 0.1

timestr = multi_experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,ne,ns,s_hist,nr,ell,u_mean_std,u_covr_std,print_updates=True)
load_plot_multi_experiment(timestr)