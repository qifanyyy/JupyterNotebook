# n = 251
# Using no. of alphabets = 20 and w = 4
# For w = 4, k = 2 and 20 alphabet, min index (aa) = 194
# and maximum index (tt) = 232. Therefore we create a matrix 
# where aa maps to (0,0); i.e. hash function subtracts 194 
# from sum of chars to get hashing index
# Max possible buckets (with 20 alpahbets) = 400
# Max no.of rotaion invariant (Lshift) words with w=4 := 16
import csv
import sys
import math
import numpy as np
import saxpy.discord as discord
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize
from itertools import permutations

# m is the number of shapes in dataset
n = int(input('Enter length of time-series:'))
m = int(input('Enter no. of shapes:'))
max_possible_buckets = m*m
sax_words = []
visited = set() 	# Set to store what all buckets have been used; saves time;
sax_words_ri = []	# Read from sax_words_ri_all_Lshifts into sax_words_ri

with open('sax_words_ri_all_Lshifts.txt', 'r') as sax_words_file:
	sax_words_ri = ([line.split() for line in sax_words_file])

# Assumes a 2 letter string only; Hard-coded;
# Also updates the visited array every time it's called
def get_hash(word): #input param 2 letter string
	n=ord(word[0])+ord(word[1])
	h = n-194
	visited.add(h)
	return h

CM = np.zeros((m,m), dtype=int)
#instead of while true, run for 30 times
temp_counter = 30
while temp_counter > 0:
	bucket_list = []
	for i in range(max_possible_buckets):
		bucket_list.append([0] * 1)
	lsh_indices = np.random.random_integers(0,3,2)
	line_num = -1
	for line in sax_words_ri:
		line_num+=1 # line_num indicates which time series we are currently processing
		for word in line:
			bucket_list[get_hash(word[lsh_indices[0]]+word[lsh_indices[1]])].append(line_num)

# All words have been put into buckets
	for ind in visited:
		for i in bucket_list[ind]:
			for j in bucket_list[ind]:
				if i != j:
					CM[i][j]+=1;
	temp_counter-=1

max_collisions = []
line_num = 0
for i in CM:
	max = -9999
	for j in i:
		if j > max:
			max = j
	max_collisions.append((max,line_num))
	line_num+=1

Outer_tuples = sorted(max_collisions) 				# outer heuristic
Inner_tuples = sorted(max_collisions, reverse=True) # inner heuristic

with open('heuristics'+sys.argv[1]+'.txt', 'w+') as h:
	# Use loops to convert from list of tuples to list of values
	# for i in Outer_tuples:
	# 	Outer.append(i[0])
	# for i in Inner_tuples:
	# 	Inner.append(i[0])
	for i in Outer_tuples:
		h.write(str(i[1]))
		h.write(' ')
	h.write('\n')
	for i in Inner_tuples:
		h.write(str(i[1]))
		h.write(' ')
