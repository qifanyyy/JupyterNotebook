#!/usr/bin.env python
#functions.py

#import required packages
import numpy as np
import matplotlib.pyplot as plt
import time
import struct
import math
import random
import params
import datetime
import os


#gen_est: generates an inital random estimate as a starting point
def gen_est(h_S, w_S, vol, h_C, w_C):
	#randomly selects the data points and 'fills' space with random value
	est = np.zeros([h_S, w_S])
	supp_pos = random.sample(range(0, (h_S*w_S)-1), vol)
	for i in supp_pos:
		x, y = divmod(i, w_S)
		est[x, y] = np.random.rand(1)

	#pad the random estimate	
	pad = np.zeros([h_C, w_C])
	pad[(h_S//2):h_C-(h_S//2), (w_S//2):w_C-(w_S//2)] = est
	est = pad
	return (est)



#gen_soln: generates a solution to be reconstructed and it's support
def gen_soln(h_S, w_S, vol, h_C, w_C):
	#randomly selects the data points and 'fills' space with random value - solution
	supp_pos = random.sample(range(0, (h_S*w_S)-1), vol)
	soln = np.zeros([h_S, w_S])
	for i in supp_pos:
		x, y = divmod(i, w_S)
		soln[x, y] = np.random.rand(1)
	pad = np.zeros([h_C, w_C])
	pad[(h_S//2):h_C-(h_S//2), (w_S//2):w_C-(w_S//2)] = soln
	soln = pad

	#uses same positions of generated solution to create support of solution 
	soln_supp = np.zeros([h_S, w_S])
	for j in supp_pos:
		x, y = divmod(j, w_S)
		soln_supp[x, y] = 1
	pad2 = np.zeros([h_C, w_C])
	pad2[(h_S//2):h_C-(h_S//2), (w_S//2):w_C-(w_S//2)] = soln_supp
	soln_supp = pad2
	return (soln, soln_supp)



#gen_supps: generate 'n_S' number of random supports
def gen_supps(h_S, w_S, vol, n_S, h_C, w_C):
	supps = []

	for i in range(n_S):
		#randomly selects the data points and 'fills' space with random value
		supp_frame = np.zeros([h_S, w_S])
		supp_pos = random.sample(range(0, (h_S*w_S)-1), vol)
		for i in supp_pos:
			x, y = divmod(i, w_S)
			supp_frame[x, y] = 1

		pad = np.zeros([h_C, w_C])
		pad[(h_S//2):h_C-(h_S//2), (w_S//2):w_C-(w_S//2)] = supp_frame
		supp_frame = pad

		supps.append(supp_frame)
	return (supps)



#init: generates all needed arrays using other functions
def init(h_S, w_S, vol, n_S, h_C, w_C):
	supps = []

	init_est = gen_est(h_S, w_S, vol, h_C, w_C)
	supps = gen_supps(h_S, w_S, vol, n_S, h_C, w_C)
	soln, soln_supp = gen_soln(h_S, w_S, vol, h_C, w_C)
	supps.insert(0, soln_supp)
	return (init_est, soln, supps, soln_supp)




#append_arrays: combines all arrays into one list
def append_arrays(init_est, soln, supps, x_sol, four_err, real_err, support_select):
	supps.insert(0, soln)
	supps.insert(0, init_est)
	supps.extend([x_sol, four_err, real_err, support_select])
	return (supps)




#display_errorplots: generates combines error plot of four/real/select/ratio
def display_errorplots(four_err, real_err, support_select):
	#create required x-axis arrays
	iter_array = range(0, params.iterations)
	support_iter_array = range(0, params.iterations)
	supp_ratio_array = np.arange(params.supp_ratio_divisor, params.iterations+params.supp_ratio_divisor, params.supp_ratio_divisor)
	support_select = support_select[1::2]

	
	#combine all error plots into one graph
	fig, ax1 = plt.subplots()

	ax1.set_xlabel('Iterations')
	ax1.set_ylabel('Error')
	ax1.plot(iter_array, four_err, color='tab:blue')
	ax1.plot(iter_array, real_err, color='tab:red')
	plt.yscale('log')
	plt.gca().legend(('four', 'real'))	

	ax2 = ax1.twinx() 

	ax2.set_ylabel('Support')  
	#ax2.plot(supp_ratio_array, real_ratio, '-', color='tab:green')
	ax2.plot(support_iter_array, support_select, '-', color='tab:purple')
	plt.gca().legend(('supportselect'))	

	fig.tight_layout() 
	plt.show()

	ratio_supports = support_select
	ratio_supports[ ratio_supports > 0] = 1
	ratio_supports = np.logical_not(ratio_supports).astype(int)
	#calculate and save support_ratio in arrays
	real_ratio = []
	for i in range(params.iterations//params.supp_ratio_divisor):
		real_ratio.append(np.mean(ratio_supports[i*params.supp_ratio_divisor:(i*params.supp_ratio_divisor)+params.supp_ratio_divisor]))



	plt.plot(supp_ratio_array, real_ratio , lw = 0.8)
	plt.show()





#RMS_error: calculate RMS error
def RMS_error(arg1, arg2):
	a = np.sum(np.square(arg2 - arg1))
	b = np.sum(np.square(arg1))
	return (np.sqrt(a/b))



#error_metrics: contains all required error metrics to be calculated each run
def error_metrics(fourier_amps, x_sol, soln):
	four_error = RMS_error(fourier_amps, np.abs(diff_pattern(x_sol)))
	phase_error = RMS_error(np.angle(diff_pattern(soln)), np.angle(diff_pattern(x_sol)))
	real_error = RMS_error(soln, x_sol)

	return (four_error, phase_error, real_error)
	



#diff_pattern: 2d fourier transform
def diff_pattern(array):
	fourier_amps = np.fft.fft2(array)
	return (fourier_amps)




#mag_proj: perfroms fourier projection
def mag_proj(gk, diff_patt_amps):
	GK = np.fft.fft2(gk)
	updated_est = diff_patt_amps*np.exp(1j*np.angle(GK))
	return (np.real(np.fft.ifft2(updated_est)))



#supp_proj: performs support projection
def supp_proj(gk, support):
	projgk = gk * support
	return (projgk[:,:])



#thresholding: ensures that the image is positive
def thresholding(x_new, low_threshold):
	x_new[x_new <= low_threshold] = low_threshold
	return(x_new)



#mask_supp_proj
def mask_supp_proj(gk, supps):
	err = []
	for i in supps:
		test = gk * i
		error = np.sum(np.square(test - gk))
		err.append(error)
		

	min_err = err.index(min(err))
	params.support_select.append(min_err)
	
	return (gk * supps[min_err])


#r_mag_proj: performs the relaxed fourier projection
def r_mag_proj(gk, fourier_amps, beta):
	gamma_M = -1/beta
	return (1+gamma_M)*mag_proj(gk, fourier_amps) - gamma_M*gk



#r_supp_proj: performs the relaxed support projection
def r_supp_proj(gk, supps, beta):
	gamma_S = 1/beta
	return (1+gamma_S)*mask_supp_proj(gk, supps) - gamma_S*gk



#DM_alg: performs the difference map algorithm
def DM_alg(gk, fourier_amps, supps, beta):
	#x_1 = PaFbXn
	x_1 = mag_proj(r_supp_proj(gk, supps, beta), fourier_amps)
	#x_2 = PbFaXn
	x_2 = mask_supp_proj(r_mag_proj(gk, fourier_amps, beta), supps)

	#equation to solve for next iterate in the difference map algorithm
	x_new = gk + beta * (x_1 - x_2)
	gk = x_new

	#returns both the new iterate and a solution in real space to calculate errors
	return (gk, x_2)


def RRR_alg(gk, fourier_amps, supps, beta):

	p1 = mask_supp_proj(gk, supps)
	r1 = p1 + (p1 - gk)

	p2 = mag_proj(r1, fourier_amps)

	x_new = gk + beta * (p2 - p1)
	gk = x_new

	return (gk, p2)


#gen_folder: generates a unique folder for each run that stores all needed arrays
def gen_folder(now):
	return("id_"+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second))




#tic: used for time keeping
def tic():
	return(time.clock())



#toc: used for time keeping
def toc(start_time):
	end_time = time.clock()
	return(end_time - start_time)



#save_arrays: saves all required into a date/time folder 
def save_arrays(arrays, elapsed_t):
	now = datetime.datetime.now()
	time_str = "id_"+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)

	#creates a folder if needed based on number of supports
	if not os.path.exists("results/supp_"+str(params.n_S)):
		os.mkdir("results/supp_"+str(params.n_S))

	#created unique folder for run
	folder = "results/supp_"+str(params.n_S)+"/"+time_str
	os.mkdir(folder)

	#cycle through list of arrays and save each individual one
	array_num = 0
	for i in arrays:
		fn = folder+"/"+str(array_num)+".csv"
		np.savetxt(fn, i, delimiter = ',')
		array_num += 1

	#generate text file for each run with some information
	names = np.array(['Iterations:', 'Beta:', 'Time', 'Supports'])
	data = np.array([params.iterations, params.beta, elapsed_t, params.n_S])
	ab = np.zeros(names.size, dtype=[('var1', 'U6'), ('var2', float)])
	ab['var1'] = names
	ab['var2'] = data

	np.savetxt(folder+"/"+'info.txt', ab, fmt="%s %10.3f")
	return()

 	

###################################################################################################

def RAAR_init(h_S, w_S, vol, h_C, w_C):
	init_est = gen_est(h_S, w_S, vol, h_C, w_C)
	soln, soln_supp = gen_soln(h_S, w_S, vol, h_C, w_C)
	return(init_est, soln, soln_supp)


def array_plot(array_list):
	count = 1
	for i in array_list:
		plt.subplot(1, len(array_list), count ), \
		plt.imshow(i, cmap = 'gray')
		count += 1					
	plt.show()

def iter_array_plot(array_list):
	x_axis = range(params.iterations)
	colours = "bg"
	colour_index = 0

	for i in array_list:
		plt.plot(x_axis, i, lw = 0.8, c = colours[colour_index])
		colour_index += 1

	plt.gca().legend(('four', 'real'))				
	plt.title('Four/Real')
	plt.yscale('log')
	plt.show()


def RAAR_alg(gk, soln_supp, fourier_amps, beta_n, low_thresh, upp_thresh):
	x_1 = mag_proj(supp_proj(gk, soln_supp), fourier_amps)
	x_2 = mag_proj(gk, fourier_amps)
	x_3 = supp_proj(gk, soln_supp)

	x_new = beta_n * ((2 * x_1) - x_2 - gk) + (1 - 2 * beta_n) * x_3 
	x_new = thresholding(x_new, low_thresh, upp_thresh)
	gk = x_new
	return (gk)

def display_iter(ii):
	print('Iteration:', ii) 

def sparseness(data):
	tot = 0.
	for i in range(data.shape[0]-1):
	    tot += ((((data[i+1:]-data[i])**2).sum(1))**.5).sum()
	avg = tot/((data.shape[0]-1)*(data.shape[0])/2.)
	return(avg)