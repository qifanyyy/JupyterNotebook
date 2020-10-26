import numpy as np
import numpy.random as npr
import numpy.linalg as la
import matplotlib.pyplot as plt
from time import time
import os
import sys
sys.path.append("..")

from matrixmath import specrad, vec
from ltimult import dare_mult
from system_identification import generate_sample_data, collect_rollouts, estimate_model, estimate_model_var_only, ctrb
from pickle_io import pickle_import, pickle_export



# Load same system used in pol-grad experiments
folderstr = os.path.join('..', 'example_systems')
timestr = '1587086073p9661696_example_network_all_steps_sysid'
dirname_in = os.path.join(folderstr, timestr)
filename_in = os.path.join(dirname_in, 'system_init.pickle')
SS = pickle_import(filename_in)

# Get the true minimum cost
true_min_cost = SS.ccare

# Reprocess system parameters to match format used in sys-id code
n = np.copy(SS.n)
m = np.copy(SS.m)
A = np.copy(SS.A)
B = np.copy(SS.B)
varAi = np.copy(SS.a)
varBj = np.copy(SS.b)
Aa = SS.Aa
Bb = SS.Bb



Ai = np.moveaxis(SS.Aa, 2, 0)
Bj = np.moveaxis(SS.Bb, 2, 0)
SigmaA = np.sum([varAi[i]*np.outer(vec(Ai[i]), vec(Ai[i])) for i in range(SS.p)], axis=0)
SigmaB = np.sum([varBj[j]*np.outer(vec(Bj[j]), vec(Bj[j])) for j in range(SS.q)], axis=0)
Q = np.copy(SS.Q)
R = np.copy(SS.R)

# Rollout length (same as pol-grad)
ell = 20

# Number of rollouts
# Max number of rollouts = nr*num_iters from pol-grad experiment
nr = 1000
num_iters = 200
ns = 10

# Number of experiments/trials
ne = 20


# s_hist = np.arange(0, nr*num_iters, nr*num_iters/ns)[1:].astype(int)
# ns -= 1
s_hist = np.unique(np.round(np.logspace(0,np.log10(nr*num_iters),ns+1,base=10)).astype(int)[1:])


c_hist = np.zeros([ne, ns])
for j in range(ne):
    for i, nr_s in enumerate(s_hist):
        print('trial %d/%d, nr %i' % (j+1, ne, nr_s))

        # Generate sample data
        u_mean_hist, u_covr_hist, u_hist, Anoise_hist, Bnoise_hist = generate_sample_data(n, m, SigmaA, SigmaB, nr_s, ell)

        # Collect rollout data
        x_hist = collect_rollouts(n, m, A, B, nr_s, ell, Anoise_hist, Bnoise_hist, u_hist)
        t_hist = np.arange(ell+1)

        # Estimate the model
        Ahat, Bhat, SigmaAhat, SigmaBhat, varAi_hat, varBj_hat = estimate_model_var_only(n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj,
                                                                                     nr_s, ell, x_hist, u_mean_hist, u_covr_hist,
                                                                                     detailed_outputs=True)

        # Synthesize certainty-equivalent optimal control
        P, K = dare_mult(Ahat, Bhat, varAi_hat, SS.Aa, varBj_hat, SS.Bb, Q, R)



        # Ahat, Bhat, SigmaAhat, SigmaBhat = estimate_model(n, m, A, B, SigmaA, SigmaB, nr, ell, x_hist, u_mean_hist, u_covr_hist)
        #
        #
        # SigmaAhat_eigvals, SigmaAhat_eigvecs = la.eig(SigmaAhat)
        # varAi_hat = np.maximum(np.real(SigmaAhat_eigvals), 0)
        # Aa_hat = np.real(np.moveaxis(np.array([SigmaAhat_eigvecs[i].reshape([n, n], order='F') for i in range(varAi_hat.size)]), 0, 2))
        #
        # SigmaBhat_eigvals, SigmaBhat_eigvecs = la.eig(SigmaBhat)
        # varBj_hat = np.maximum(np.real(SigmaBhat_eigvals), 0)
        # Bb_hat = np.real(np.moveaxis(np.array([SigmaBhat_eigvecs[j].reshape([m, m], order='F') for j in range(varBj_hat.size)]), 0, 2))

        # # Synthesize certainty-equivalent optimal control
        # P, K = dare_mult(Ahat, Bhat, varAi_hat, Aa_hat, varBj_hat, Bb_hat, Q, R)

        if P is not None:
            SS.setK(K)
            c_hist[j, i] = SS.c
        else:
            c_hist[j, i] = np.inf


figsize = (6, 3)
fig = plt.figure(figsize=figsize)
costnorm = (c_hist/true_min_cost)-1
y_lwr = np.percentile(costnorm, 10, axis=0)
y_upr = np.percentile(costnorm, 90, axis=0)
plt.fill_between(s_hist, y_lwr, y_upr, alpha=0.3)
plt.plot(s_hist, np.mean(costnorm, axis=0), linewidth=3)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of rollouts')
plt.ylabel('Normalized cost diff.')
plt.title('System identification')
plt.show()
img_dirname_out = os.path.join(dirname_in, 'analysis_plots')
filename_out = 'plot_'+'costnorm'+'_vs_rollouts_sysid'
path_out = os.path.join(img_dirname_out,filename_out)
plt.savefig(path_out, dpi=300, bbox_inches='tight')