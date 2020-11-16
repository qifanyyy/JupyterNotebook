# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Driver script to execute SERIAL implementation of ABFT multiplication 
# Can be run with or without inputs (generate random files if non supplied)
# run: python multi_driver.py <input_csv_1> <input_csv_2>
# Expects servers to be started with IPs listed in processor_addresses
# Use run_distributed.py to start network simulation and invoke in context

from csv_io import *
from abft import *
from abft_communication import *
from abft_client import *
from matrix_multiplier import *
from error_insertion import *
import time
import sys

# Processor array size
arr_x = 4
arr_y = 4

# Use only one processor
run_serial = False

# Processor array server addresses
processor_addresses = [	
					#("127.0.0.1", 9999),
					("10.0.0.2", 9999),
					("10.0.0.3", 9999),
					("10.0.0.4", 9999),
					("10.0.0.5", 9999),
					("10.0.0.6", 9999),
					("10.0.0.7", 9999),
					("10.0.0.8", 9999),
					("10.0.0.9", 9999),
					("10.0.0.10", 9999),
					("10.0.0.11", 9999),
					("10.0.0.12", 9999),
					("10.0.0.13", 9999),
					("10.0.0.14", 9999),
					("10.0.0.15", 9999),
					("10.0.0.16", 9999),
					("10.0.0.17", 9999),
					]

# Matrix size
size_i = 1024
size_j = size_i

#input_csv_1  = "input_csv_1.csv"
#input_csv_2  = "input_csv_2.csv"
#output_csv = "output_csv.csv"

def distributed_abft(input_1 = None, input_2 = None):
	
	input_csv_1  = "input_csv_1.csv"
	input_csv_2  = "input_csv_2.csv"
	output_csv = "output_csv.csv"

	start_total = time.time()
	
	if input_1 == None and input_2 == None:
		# Generate random test matrices and write to file
		print("Generating input files of size %d by %d" % (size_i, size_j))
		start = time.time()
		rand_matrix = generate_random_matrix(size_i, size_j)
		write_csv(rand_matrix, input_csv_1)
		rand_matrix = generate_random_matrix(size_j, size_i)
		write_csv(rand_matrix, input_csv_2)
		end = time.time()
		print("\tTime: %s" % str(end-start))
	else:
		input_csv_1 = input_1
		input_csv_2 = input_2

	# Read test data from tile (test file IO)
	print("Reading input files")
	start = time.time()
	input_matrix_1 = read_csv(input_csv_1)
	input_matrix_2 = read_csv(input_csv_2)
	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Partition Data
	print("Partitioning data")
	start = time.time()
	partitioned_data = partition_data(input_matrix_1, input_matrix_2, arr_x, arr_x)
	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Add ABFT checks to each data chunk
	print("Adding ABFT checksums to data partitions")
	start = time.time()
	transmission_data = []
	for data_part_chunk in partitioned_data:
		abft_part_chunk = abft_data_partition(data_part_chunk)
		transmission_data.append(abft_part_chunk)
	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Insert errors before transmission
	print("Inserting errors (Client)")
	start = time.time()
	for proc_id in range(arr_x * arr_x):
		print("Errors for %s" % (proc_id))
		good_data = transmission_data[proc_id]
		bad_1 = insert_prob_error(good_data[0])
		bad_2 = insert_prob_error(good_data[1])
		bad_data = (bad_1, bad_2)
		transmission_data[proc_id] = bad_data
	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Transmit data to processing servers
	# 	Potentially insert errors
	print("Transmitting Data")
	workers = {}
	results = {}
	start = time.time()
	for proc_id in range(0, arr_x * arr_x):
	#for proc_id in range(0, 1):
		proc_add = processor_addresses[proc_id]
		
		if run_serial:
			proc_add = processor_addresses[0]
		
		host = proc_add[0]
		port = proc_add[1]

		worker_sock = open_socket(host, port)

		workers[proc_id] = worker_sock

		data = transmission_data[proc_id]

		transmit_to_server(proc_id, worker_sock, data)

		print("Transmitted data to processor %s" % proc_id)
		
		if run_serial:
			result, rec_proc = receive_from_server(proc_id, worker_sock)
			assert rec_proc == proc_id, "Received wrong data?"
			results[proc_id] = result
			print("Result received from %s" % proc_id)

	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Wait on results
	if run_serial == False:

		print("Waiting for workers to send results")
		start = time.time()
		for proc_id in range(0, arr_x * arr_x):
			#print("Receiving data from processor %s" % proc_id)
			worker_sock = workers[proc_id]

			result, rec_proc = receive_from_server(proc_id, worker_sock)
			assert rec_proc == proc_id, "Received wrong data?"
			results[proc_id] = result
			print("Result received from %s" % proc_id)

		end = time.time()
		print("\tTime: %s" % str(end-start))

	# Correct data if necessary
	print("Checking for necessary corrections")
	start = time.time()
	for proc_id in range(arr_x * arr_y):
		print("Correcting results from %s" % (proc_id))
		to_check = results[proc_id]
		corrected = abft_verify(to_check, row_checks = True, col_checks = True)
		results[proc_id] = corrected

	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Reconstruct full matrix
	print("Reconstructing result matrix")
	start = time.time()
	final_matrix = reconstruct_results(results, arr_x, arr_y)
	end = time.time()
	print("\tTime: %s" % str(end-start))

	# Standard calculation for comparison
	print("Comparing results")
	standard_result = np.matrix(input_matrix_1) * np.matrix(input_matrix_2)

	print("Final matrix shape: %s" % str(final_matrix.shape))
	print("Non-parallel check matrix shape: %s" % str(standard_result.shape))
	#print(final_matrix)
	#print(standard_result)
	assert standard_result.shape == final_matrix.shape, "Result is wrong size!"

	# Compare standard and ABFT calculation to ensure correct multiplication results
	comp_matrix = standard_result - final_matrix
	norm = np.linalg.norm(comp_matrix)
	print("Error norm between built-in and ABFT matrix multiplication: %f "% norm)
	end = time.time()
	print("\tTime: %s" % str(end-start))

	print("Adding ABFT checks to final result")
	start = time.time()
	final_matrix_abft = add_abft_check_data(final_matrix, row_checks = True, col_checks = True)
	end = time.time()
	print("\tTime: %s" % str(end-start))


	print("Writing results to file...")
	start = time.time()
	write_csv(final_matrix, "output.csv")
	write_csv(final_matrix_abft, "output_abft.csv")
	end = time.time()
	print("\tTime: %s" % str(end-start))

	
	print("Total Elapsed Time: %s" % str(end-start_total))

if __name__ == "__main__":
	input_1 = None
	input_2 = None
	if len(sys.argv) > 2:
		input_1 = sys.argv[1]
		input_2 = sys.argv[2]
	distributed_abft(input_1, input_2)


