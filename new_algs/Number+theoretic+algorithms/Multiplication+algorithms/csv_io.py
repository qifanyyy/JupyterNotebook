# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# A collection of functions for dealing with CSV input and output, generating random input files

import csv
import numpy as np

# CSV value delimiter (may need to be changed depending on input)
delimiter = ','
# Unicode encoding mode
encoding = 'utf-8-sig'

# Write matrix out to file as CSV (Numpy)
def write_csv(data_matrix, filename):
	np.savetxt(filename, data_matrix, delimiter=delimiter, newline='\n', fmt='%d', encoding=encoding)
	
# Read in CSV as file (Numpy)
def read_csv(filename):
	data_matrix = np.loadtxt(filename, delimiter=delimiter, dtype=int, encoding=encoding)
	return data_matrix

# Generate matrix of random values (Numpy)
def generate_random_matrix(num_rows, num_cols):
	#rand_matrix = np.random.rand(num_rows, num_cols)
	rand_matrix = np.random.randint(-1000, 1000, size=(num_rows, num_cols))
	return rand_matrix

# Read from CSV file using csv package only
# Can be used for file read in debug
def read_csv_only(filename):
	data_array = None
	with open(filename, mode='r',  encoding=encoding) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=delimiter)
		file_lines = []
		for row in csv_reader:
			int_row = [int(item) for item in row]
			file_lines.append(int_row)

		data_array = np.array(file_lines)

	print(data_array.shape)
	return data_array
