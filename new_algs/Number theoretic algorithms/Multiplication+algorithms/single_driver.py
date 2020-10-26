# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Driver script to execute SERIAL implementation of ABFT multiplication
# Can be run with or without inputs (generate random files if non supplied)
# run: python single_driver.py [<input_csv_1> <input_csv_2>]

from csv_io import *
from abft import *
from matrix_multiplier import *
from error_insertion import *
import time
import sys


size_i = 1024
size_j = size_i

input_csv_1  = "input_csv_1.csv"
input_csv_2  = "input_csv_2.csv"
output_csv = "output_csv.csv"

start_total = time.time()
if len(sys.argv) > 2:
		input_csv_1 = sys.argv[1]
		input_csv_2 = sys.argv[2]
else:
	# Generate random test matrices and write to file
	
	print("Generating input files of size %d by %d" % (size_i, size_j))
	start = time.time()
	rand_matrix = generate_random_matrix(size_i, size_j)
	write_csv(rand_matrix, input_csv_1)
	rand_matrix = generate_random_matrix(size_j, size_i)
	write_csv(rand_matrix, input_csv_2)
	end = time.time()
	print("\tTime: %s" % str(end-start))

# Read test data from tile (test file IO)
print("Reading input files")
start = time.time()
input_matrix_1 = read_csv(input_csv_1)
input_matrix_2 = read_csv(input_csv_2)
end = time.time()
print("\tTime: %s" % str(end-start))

# Add abft data to input matrices
print("Add ABFT checksums")
start = time.time()
input_matrix_1_abft = add_abft_check_data(input_matrix_1, row_checks = True, col_checks = True)
end = time.time()
print("\tTime 1: %s" % str(end-start))
start = time.time()
input_matrix_2_abft = add_abft_check_data(input_matrix_2, row_checks = True, col_checks = True)
end = time.time()
print("\tTime 2: %s" % str(end-start))

# Corrupt data
#input_matrix_2_abft[4,4] = 7.0
print("Inserting probabilistic Errors (Pre-multiplication)")
start = time.time()
input_matrix_1_abft = insert_prob_error(input_matrix_1_abft)
end = time.time()
print("\tTime 1: %s" % str(end-start))
start = time.time()
input_matrix_2_abft = insert_prob_error(input_matrix_2_abft)
end = time.time()
print("\tTime 2: %s" % str(end-start))

# Apply ABFT correct/detect
print("Verifying ABFT Input Matrices (Pre-multiplication)")
start = time.time()
input_matrix_1_abft = abft_verify(input_matrix_1_abft, row_checks = True, col_checks = True)
end = time.time()
print("\tTime 1: %s" % str(end-start))
start = time.time()
input_matrix_2_abft = abft_verify(input_matrix_2_abft, row_checks = True, col_checks = True)
end = time.time()
print("\tTime 2: %s" % str(end-start))

# Run multiplication procedure
print("Performing multiplication")
start = time.time()
result_matrix_abft = multiply_matrix_abft(input_matrix_1_abft, input_matrix_2_abft)
end = time.time()
print("\tTime: %s" % str(end-start))

print("Inserting probabilistic Errors (Post-multiplication)")
start = time.time()
result_matrix_abft = insert_prob_error(result_matrix_abft)
end = time.time()
print("\tTime: %s" % str(end-start))

# Apply ABFT correct/detect
print("Verifying ABFT Result Matrix (Post-multiplication)")
start = time.time()
result_matrix_abft = abft_verify(result_matrix_abft, row_checks = True, col_checks = True)
end = time.time()
print("\tTime: %s" % str(end-start))

# Standard calculation for comparison
print("Comparing results")
standard_result = np.matrix(input_matrix_1) * np.matrix(input_matrix_2)

# Compare standard and ABFT calculation to ensure correct multiplication results
# Subtract subtract standard result from ABFT result data component, then take norm
value_matrix = strip_abft_check_data(result_matrix_abft, strip_mode = "all")

comp_matrix = standard_result - value_matrix
norm = np.linalg.norm(comp_matrix)
print("Error norm between built-in and ABFT matrix multiplication: %f "% norm)
end = time.time()


print("Writing results to file...")
start = time.time()
write_csv(value_matrix, "output.csv")
write_csv(result_matrix_abft, "output_abft.csv")
end = time.time()
print("\tTime: %s" % str(end-start))


print("Total Elapsed Time: %s" % str(end-start_total))


#print(standard_result)

#print(result_matrix_abft)

