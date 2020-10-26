import sys
import csv
import numpy as np
from saxpy.znorm import znorm

def dist(a, b):
	return np.sqrt(np.sum((a-b)**2))

S = []
if sys.argv[2] != '':
	m = sys.argv[2]
else:
	m = input('Enter no. of shapes in time series.')
n = int(input('Enter length of time series.'))
m = int(m)

with open('DATA/'+sys.argv[1], newline='') as test_file:
	lines = csv.reader(test_file)
	for line in lines: 					# every line is a list of strings
		# del line[0] 					# remove 1st element as it is the class (TODO - pop this into a separate array)
		data = np.array(line) 			# every line/row in the file as a np string array
		data = np.asfarray(data,float) 	# converted to np float array
		data_znorm = znorm(data)
		S.append(data_znorm)
S = np.asfarray(S, float)
dist_matrix = np.zeros((m,m) , dtype=float)
dist_array = np.zeros(n,float)
for i in range(0,m):
	for j in range(i+1,m):
		for k in range(0,n):
			dist_array[k] = dist(S[i],np.roll(S[j],k))
		dist_matrix[i][j] = min(dist_array)
		dist_matrix[j][i] = dist_matrix[i][j]


with open ('dist', 'w') as f:
	dist_matrix.tofile(f, ' ')
