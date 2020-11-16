# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Multiplication protocol for calculating matrix product

import numpy as np
from abft import *

# Changes iteration order (could increase speed)
row_then_col = False

# Calculates dot product of row and col of two matrices
def dot_product(row, col):
	assert len(row) == len(col), "Invalid size for dot product"

	prod_sum = 0

	for i in range(len(row)):
		prod_sum += row[i] * col[i]

	return prod_sum

# Conducts matrix multiplication on an ABFT encoded matrices
def multiply_matrix_abft(matrix_1_in, matrix_2_in):

	# Strip down coding for multiplication
	matrix_1 = strip_abft_check_data(matrix_1_in, strip_mode = "row")
	matrix_2 = strip_abft_check_data(matrix_2_in, strip_mode = "col")

	shape_1 = matrix_1.shape
	shape_2 = matrix_2.shape
	
	# Verify valid shape
	assert shape_1[1] == shape_2[0], "Matrix Shapes not multipliable!"

	new_shape = (shape_1[0], shape_2[1])

	result_matrix = np.zeros(new_shape)

	# Begin multiplication
	# Iterate over rows
	if row_then_col:

		for i in range(new_shape[0]):
			# Iterate over cols (elements of rows)
			for j in range(new_shape[1]):
				old_row = matrix_1[i,:]
				old_col = matrix_2[:,j]

				# Calculate dot product of row and col in corresponding matrices
				prod_sum = dot_product(old_row, old_col)

				result_matrix[i,j] = prod_sum

	else:
		for j in range(new_shape[1]):
			# Iterate over cols (elements of rows)
			for i in range(new_shape[0]):
				old_row = matrix_1[i,:]
				old_col = matrix_2[:,j]

				# Calculate dot product of row and col in corresponding matrices
				prod_sum = dot_product(old_row, old_col)

				result_matrix[i,j] = prod_sum

	return result_matrix
