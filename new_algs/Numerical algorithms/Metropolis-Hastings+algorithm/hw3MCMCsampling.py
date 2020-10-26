import scipy as sc
import scipy.stats as st
import scipy.io as scio
import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy import shape
import hw3MCMCsampling_functions as fn
import scipy.linalg as lin
import os
import math

# CONSTANTS:
a = -25
b = 20
a_vec = [4.0,2.0]
b_vec = [-7.0,5.0]
a_vec = np.array(a_vec)
b_vec = np.array(b_vec)
num_bins = 100
num_bins_2Dim = [150,150]

# User Input Arguments, specifying details of experiment run:
print("D \t\t= dimensionality of target distribution (1 or 2 D for this hw)")
print("proposal dist. \t= the type of proposal distribution to use")
print("sigma \t\t= the standard deviation for our proposal distribution")
print("n \t\t= number of samples to generate")
print("burn_in \t= number of initial samples to discard")
print("keep_every \t= keep every keep_every'th sample...discard the rest to reduce auto-correlation")
print("calcErr \t= calculate and print the error every calcErr'th sample")
print("print_accept_rt \t= calculate and print the current accept_rt every print_accept_rt'th sample")
print("\n")

hw3_exp_id = raw_input("experiment ID: \t\t")
proposal_dist = raw_input("proposal_dist: \t\t")
D = int(raw_input("D: \t\t\t"))
if D == 1:
    sigma = float(raw_input("sigma: \t\t\t"))
else:
    cov_string = raw_input("cov: \t\t\t")
    cov = cov_string.split()
    cov = np.array(cov)
    sigma = np.reshape(cov, (D,D))
n = int(raw_input("n: \t\t\t"))
burn_in = int(raw_input("burn_in: \t\t"))
keep_every = int(raw_input("keep_every: \t\t"))
err_interval = int(raw_input("calcErr every: \t\t"))
print_accept_rt_interval = int(raw_input("print_accept_rt every: \t"))

add_header = raw_input("add header? (y/n) \t")
print("\n\n")

num_samples_fnl = 0 
try:
    # create file in subdirectory for output of metadata for each experiment:
    fname = "hw3_exp" + str(hw3_exp_id) + ".csv"
    cur_dir = os.getcwd()
    path_name = "exp" + str(hw3_exp_id)
    path = os.path.join(cur_dir, path_name)
    if os.access(path, os.F_OK):
        os.chdir(path)
        out = open(fname, 'w')
    else:
        os.mkdir(path)
        os.chdir(path)
        out = open(fname, 'w')
    
    # write experiment parameters out to file:
    out_header = ("expID,"
        "D,"
        "proposal_dist,"
        "sigma,"
        "n,"
        "burn_in,"
        "keep_every\n")
    out.write(out_header)
    if D == 1:    
        out_header_data = str(hw3_exp_id) +","\
            + str(D) +","\
            + str(proposal_dist) +","\
            + str(sigma) +","\
            + str(n) +","\
            + str(burn_in) +","\
            + str(keep_every)
    elif D == 2:
        out_header_data = str(hw3_exp_id) +","\
            + str(D) +","\
            + str(proposal_dist) +","\
            + str(sigma[0,:]) + str(sigma[1,:]) +","\
            + str(n) +","\
            + str(burn_in) +","\
            + str(keep_every)
    out.write(out_header_data)
    out_sub_header = ("\n\nit_num,"
        "samples,"
        "accept_rt,"
        "sample_set\n")
    out.write(out_sub_header)
    
    err = -1
    # determine starting value for mu_initial:   
    if D == 1:
        samples = np.empty(n + burn_in)
        mu_initial = (float(b-a))*np.random.rand() + a
        ########################################################
        # RUN ALGORITHM:
        samples, errs, accept_rt_fnl, accept_rt_list = fn.runMetropolisHastings_1Dim(n + burn_in, mu_initial, sigma, err_interval, num_bins, print_accept_rt_interval)
        ########################################################
        # discard burn-in samples:
        samples = samples[burn_in:]
        # discard most samples - only keep every keep_every'th sample...to reduce auto-correlation:
        samples_final = list()
        for i in xrange(0, len(samples)):
            if i % keep_every == 0:
                samples_final.append(samples[i])
        # calculate the final error:
        err_fnl = fn.calcError_1Dim(samples_final, num_bins)
        errs.append(err_fnl)
        print("FINAL err_fnl: = " + str(err_fnl))
        print("FINAL accept_rt: = " + str(accept_rt_fnl))
        out.write("accept_rt_fnl," + str(accept_rt_fnl) + "\n")
        num_samples_fnl = len(samples_final)
        # write samples_final out to file:
        for i in xrange(0, num_samples_fnl):
            out.write(str(i) + "," + str(samples_final[i]) + ", ," + "samples_final\n")
        # write full sample set out to file:
        out.write(out_sub_header)
        for i in xrange(0, len(samples)-1):
            out.write(str(i) + "," + str(samples[i]) + "," + str(accept_rt_list[i]) + ",samples_full\n")
        # write out errs:
        out.write("\nit_num,err\n")
        for i in xrange(0, len(errs)):
            out.write(str(err_interval*i) +"," + str(errs[i]) + "\n")
        # show and save histogram comparing generated samples to target pdf:
        fn.showAndSaveHistogram_1Dim(samples_final, num_bins, hw3_exp_id, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl)
        fn.showAndSaveWalk_1Dim(samples, "full", num_bins, hw3_exp_id, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl)
        fn.showAndSaveWalk_1Dim(samples_final, "kept", num_bins, hw3_exp_id, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl)
   
    elif D == 2:
        samples = np.empty((2, n + burn_in))
        mu_initial = (b_vec - a_vec)*np.random.rand(D) + a_vec
        print("mu_initial = " + str(mu_initial))
        ########################################################
        # RUN ALGORITHM:
        samples, errs, accept_rt_fnl, accept_rt_list = fn.runMetropolisHastings_nDim(n + burn_in, D, mu_initial, sigma, err_interval, num_bins_2Dim, num_bins, print_accept_rt_interval)
        ########################################################
        # discard burn-in samples:
        samples = samples[:,burn_in:]
        # discard most samples - only keep every keep_every'th sample...to reduce auto-correlation:
        samples_final = np.empty((2,int(n/keep_every)))
        for j in xrange(0, len(samples[0,:]) - 1):
            if j % keep_every == 0:
                samples_final[:,j/keep_every] = samples[:,j] 
        # calculate the final error:
        err_fnl = fn.calcError_2Dim(samples_final, num_bins_2Dim, num_bins)
        errs.append(err_fnl)
        print("FINAL err_fnl: = " + str(err_fnl))
        print("FINAL accept_rt: = " + str(accept_rt_fnl))
        out.write("accept_rt_fnl," + str(accept_rt_fnl) + "\n")
        num_samples_fnl = len(samples_final[0,:])
        # write samples_final out to file:
        for j in xrange(0, num_samples_fnl):
            out.write(str(j) + "," + str(samples_final[:,j]) + ", ,samples_final\n")
        # write full sample set out to file:
        out.write(out_sub_header)
        for j in xrange(0, len(samples[0,:])):
            out.write(str(j) + "," + str(samples[:,j]) + "," + str(accept_rt_list[j]) + ",samples_full\n")
        # write out errs:
        out.write("\nit_num,err\n")
        for i in xrange(0, len(errs)):
            out.write(str(err_interval*i) +"," + str(errs[i]) + "\n")
        fn.showAndSaveHistogram_2Dim(samples_final, num_bins_2Dim, hw3_exp_id, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl) 
  
finally:
    out.close()

try:
    # create file to track final results of all experiments:
    os.chdir(os.path.pardir)
    f_results = open("hw3_results.csv", 'a')
    if add_header == 'y':
        results_header = ("expID,"
        "D,"
        "proposal_dist,"
        "sigma,"
        "n,"
        "burn_in,"
        "keep_every,"
        "num_samples_fnl,"
        "err_fnl,"
        "accept_rt_fnl\n")
        f_results.write(results_header)
        
    # output summary of results to master results file:
    if D == 1:
        results = str(hw3_exp_id) +","\
            + str(D) +","\
            + str(proposal_dist) +","\
            + str(sigma) +","\
            + str(n) +","\
            + str(burn_in) +","\
            + str(keep_every) +","\
            + str(num_samples_fnl) +","\
            + str(err_fnl) +","\
            + str(accept_rt_fnl) + "\n"
    elif D == 2:
        results = str(hw3_exp_id) +","\
            + str(D) +","\
            + str(proposal_dist) +","\
            + str(sigma[0,:]) + str(sigma[1,:]) +","\
            + str(n) +","\
            + str(burn_in) +","\
            + str(keep_every) +","\
            + str(num_samples_fnl) +","\
            + str(err_fnl) +","\
            + str(accept_rt_fnl) + "\n"
    f_results.write(results)

finally:
    f_results.close()    
