# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Communication protocols, data partitioning, and final matrix assembly

from abft import *
import pickle

# Converts data from array to bytes form and inserts error
def data_to_message(data):
	message = pickle.dumps(data, protocol=0)
	return message

# Converts messaged into array data
def message_to_data(message):
	data = pickle.loads(message)
	return data

# Partitions matrix into chunks needed by each worker process
def partition_data(input_mat_1, input_mat_2, arr_x, arr_y):
	part_data = []

	chunk_size_x = int(input_mat_1.shape[0] / arr_x)
	chunk_size_y = int(input_mat_2.shape[1] / arr_y)

	print("Chunk sizes")
	print(chunk_size_x)
	print(chunk_size_y)

	# Iterate over chunk indexes 
	for x in range(arr_x):
		for y in range(arr_y):
			# Get data from first matrix (slicing along X axis)
			start_ind = x * chunk_size_x
			stop_ind = (x + 1) * chunk_size_x
			mat_1_slice = input_mat_1[start_ind:stop_ind, :]

			# Get data from second matrix (slicing along Y axis)
			start_ind = y * chunk_size_y
			stop_ind = (y + 1) * chunk_size_y
			mat_2_slice = input_mat_2[:, start_ind:stop_ind]

			proc_id = (x * arr_y) + y
			#print("Data for proc %d at %d %d" % (proc_id, x, y))

			# Save data chunk to list
			part_data.append((mat_1_slice, mat_2_slice))

	return part_data

def abft_data_partition(data_tup):

	abft_x_part = add_abft_check_data(data_tup[0], row_checks = True, col_checks = True)
	abft_y_part = add_abft_check_data(data_tup[1], row_checks = True, col_checks = True)

	abft_data_tup = (abft_x_part, abft_y_part)

	return abft_data_tup

def reconstruct_results(result_dict, arr_x, arr_y):

	assert len(result_dict.items()) == arr_x * arr_y, "Invalid number of results for reconstruction"

	# pre alloc final matrix
	x_size = result_dict[0].shape[0] - 1
	final_x = x_size * arr_x
	y_size = result_dict[0].shape[1] - 1
	final_y = y_size * arr_y

	final_matrix = np.zeros((final_x, final_y))

	# Copy results into final matrix
	for x in range(arr_x):
		for y in range(arr_y):
			sub_mat_index = (x * arr_y) + y
			
			start_x = x_size * x
			end_x = x_size * (x + 1)
			start_y = y_size * y
			end_y = y_size * (y + 1) 

			sub_matrix_abft = result_dict[sub_mat_index]
			sub_matrix = strip_abft_check_data(sub_matrix_abft, strip_mode = "all")

			final_matrix[start_x:end_x, start_y:end_y] = sub_matrix

			#for i in range(start_x, end_x):
			#	for j in range(start_y, end_y):
			#		final_matrix


	return final_matrix
