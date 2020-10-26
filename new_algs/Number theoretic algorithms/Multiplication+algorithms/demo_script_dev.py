import numpy as np
import numpy.random as npr

from system_definitions import (random_system,
                                example_system_scalar,
                                example_system_twostate,
                                example_system_twostate_diagonal,
                                example_system_erdos_renyi)
from experiments import multi_experiment_increasing_rollout_count, load_plot_multi_experiment


# for development only
import matplotlib.pyplot as plt
plt.close('all')


seed = 1
npr.seed(seed)

# System definition
# n,m,A,B,SigmaA,SigmaB = example_system_scalar()
n,m,A,B,SigmaA,SigmaB = example_system_twostate()
# n,m,A,B,SigmaA,SigmaB = example_system_twostate_diagonal()
# n,m,A,B,SigmaA,SigmaB = random_system(n=3,m=1,seed=seed)
# n,m,A,B,SigmaA,SigmaB = example_system_erdos_renyi(10)

# Number of rollouts
nr = int(1e5)

# Rollout length
# ell = int((m**2*n**4)/2 + (m**2*n**2)/2 + m**2 + 1)
ell = n + m

# Model estimation points
ns = 10

estimation_points = 'log'
if estimation_points == 'linear':
    s_hist = np.round(np.linspace(0,nr,ns+1)).astype(int)[1:]
elif estimation_points == 'log':
    s_hist = np.unique(np.round(np.logspace(0,np.log10(nr),ns+1,base=10)).astype(int)[1:])
    ns_cur = s_hist.size
    while s_hist.size < ns:
        ns_cur += 1
        s_hist = np.unique(np.round(np.logspace(0,np.log10(nr),ns_cur+1,base=10)).astype(int)[1:])

# Number of experiments
ne = 4

# Input mean and covariance settings
u_mean_std = 1
u_covr_std = 0.1

timestr = multi_experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,ne,ns,s_hist,nr,ell,u_mean_std,u_covr_std,print_updates=True)

# experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,nr,ell,u_mean_std,u_covr_std,ns,s_hist,print_updates=True)

load_plot_multi_experiment(timestr)


# timestr = "1569434349p2392745_in_paper"
# load_plot_multi_experiment(timestr)




# # Two-state experiment
# seed = 0
# npr.seed(seed)
# n,m,A,B,SigmaA,SigmaB = example_system_twostate()
# # Number of rollouts
# nr = int(1e6)
# # Rollout length
# ell = int((m**2*n**4)/2 + (m**2*n**2)/2 + m**2 + 1)
# experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,nr,ell)


# Other experiements
# n,m,A,B,SigmaA,SigmaB = random_system(n=4,m=3,seed=seed)

# experiment_fixed_rollout(n,m,A,B,SigmaA,SigmaB,nr,ell)
# experiment_increasing_rollout_length(n,m,A,B,SigmaA,SigmaB,nr,ell)