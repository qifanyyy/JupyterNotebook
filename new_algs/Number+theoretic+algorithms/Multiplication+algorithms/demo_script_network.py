import numpy as np
import numpy.linalg as la
import numpy.random as npr
from os import path

from system_definitions import (example_system_twostate, example_system_erdos_renyi)
from experiments import experiment_fixed_rollout, experiment_fixed_rollout_var_only, load_plot_multi_experiment


# for development only
import matplotlib.pyplot as plt
plt.close('all')

seed = None
npr.seed(seed)

# System definition
# n, m, A, B, SigmaA, SigmaB = example_system_twostate()
n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj = example_system_erdos_renyi(8, seed=seed, detailed_outputs=True)

# Rollout length
ell = int((m**2*n**4)/2 + (m**2*n**2)/2 + m**2 + 1)
# ell = n*n + n*m


# Number of rollouts
# nr = int(1e2)
nr = int(1e6 / ell)


if nr*ell > 1e7:
    raise Exception("You have requested a large dataset, please reduce the length or number of rollouts.")

# Input mean and covariance settings
u_mean_std = 1*1.0
u_covr_std = 1*0.1

# Plotting model estimate split option
split = False

# timestr = experiment_fixed_rollout(n, m, A, B, SigmaA, SigmaB, nr, ell)
timestr, Ahat, Bhat, SigmaAhat, SigmaBhat, varAi_hat, varBj_hat, figs, axs = experiment_fixed_rollout_var_only(n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj, nr, ell, split=split)


for M, Mhat, label in zip([A, B, SigmaA, SigmaB], [Ahat, Bhat, SigmaAhat, SigmaBhat], ['A', 'B', 'SigmaA', 'SigmaB']):
    print(label)
    diff = M-Mhat
    print('Frobenius norm of errors: %f' % la.norm(diff, ord='fro'))
    print('  Maximum absolute error: %f' % np.max(np.abs(diff)))
    print('')

print('Normalized variance error, mean and max for paper:')
print(np.mean(np.abs(varAi-varAi_hat)/varAi))
print(np.max(np.abs(varAi-varAi_hat)/varAi))
print(np.mean(np.abs(varBj-varBj_hat)/varBj))
print(np.max(np.abs(varBj-varBj_hat)/varBj))


if split:
    fnames = ['network_estimates_AB', 'network_estimates_SigmaAB']
    for fname, fig in zip(fnames, figs[1]):
        path_out = path.join('.', 'network_images', fname+'.png')
        fig.savefig(path_out, dpi=600)
else:
    fname = 'network_estimates'
    fig = figs[1]
    path_out = path.join('.', 'network_images', fname+'.png')
    fig.savefig(path_out, dpi=600)



# from plotting import plot_model_estimates
# plot_model_estimates(A, B, SigmaA, SigmaB, Ahat, Bhat, SigmaAhat, SigmaBhat)
