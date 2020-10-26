#!/usr/bin.env python
#mask_algorithm.py

#import required packages
import numpy as np
import matplotlib.pyplot as plt
import time
import struct
import math
import funcs
import params
import datetime
import os
import random

#reset support_select
params.support_select = []

#beign timing
start_t = funcs.tic()

#initialise all required components
init_est, soln, supps, soln_supp = funcs.init(params.h_S, params.w_S, params.vol, params.n_S, params.h_C, params.w_C)
fourier_amps = np.abs(funcs.diff_pattern(soln))
gk = init_est


#initlialise error arrays
four_err = np.zeros(params.iterations)
real_err = np.zeros(params.iterations)
phase_err = np.zeros(params.iterations)



#main loop
for ii in range(params.iterations):
	
	gk, x_sol = funcs.DM_alg(gk, fourier_amps, supps, params.beta)
	
	four_err[ii], phase_err[ii], real_err[ii] = \
					funcs.error_metrics(fourier_amps, x_sol, soln)

#finish timing
elapsed_t = funcs.toc(start_t)

#append all arrays and then save to the run's uniqe folder
arrays = funcs.append_arrays(init_est, soln, supps, x_sol, four_err, real_err, params.support_select)
funcs.save_arrays(arrays, elapsed_t)	


