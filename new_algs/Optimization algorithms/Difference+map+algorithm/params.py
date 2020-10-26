#!/usr/bin.env python
#parameters.py

#import required packages
import numpy as np
import math

########
#general
########
beta = 0.5
iterations = 100000

runs = 50		#number of runs performed by script
low_supps = 11	#range of number of support to run over
upp_supps = 12


threshold = 1/1000000 	#convergence threshold
location = "results/beta_0.2/supp_14/" #analysis folder
run = "id_2019918223346"

##################
#mask_algorithm.py
##################
h_S = 16				#height of support area
w_S = 16				#width of support area

h_C = 32				#height of computational area
w_C = 32				#width of computational area

vol = int(h_S*w_S*0.5)  #volume: number of non-zero pixels
n_S = 2					#number of additional supports 

support_select = []		#list of support selections
supp_ratio_divisor = 100
		

#############
#RAAR_test.py
#############
beta_1 = 0.7
 		