# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Function for inserting probabilistic errors into matrices

from abft import *
import numpy as numpy

single_error_prob = 0.20
double_error_prob = 0.005

# Probabilistically inserts errors into ABFT matrix representations
def insert_prob_error(input_matrix):
	new_matrix = input_matrix
	mat_shape = input_matrix.shape 
	num_rows = mat_shape[0]
	num_cols = mat_shape[1]


	# Determine number of errors to insert
	num_error = 0 

	flip = np.random.uniform(0,1)
	if flip <= single_error_prob:
		num_error += 1
		if flip <= double_error_prob:
			num_error += 1
		

	# For each error
	for x in range(num_error):

		# Calculate location
		row_loc = np.random.randint(num_rows)
		col_loc = np.random.randint(num_cols)


		# Calculate value
		error_value = np.random.randint(-1000, 1000)


		# Insert
		new_matrix[row_loc, col_loc] = error_value

		print("Inserted error at %d : %d (%s)" % (row_loc, col_loc, str(error_value)))

	return new_matrix