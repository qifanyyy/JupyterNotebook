"""
Nodebechukwu Okoye and Jakob Lopez
Submit: sbatch OkoyeLopezProjectNaiveParallelScript
"""
import multiprocessing as mp
import numpy as np
import time

def multiply(id):
	"""
	Each process multiplies their share of matrix 1 by matrix 2
	
	Parameters:
		id - id of the process executing this function. Used to index matrix 1.
	
	Returns:
		2-D matrix multiplication product
	"""
	return np.matmul(split_m1[id], m2)	

# Matrix size
n = 1024

num_workers = 4

# Initialize array nxn with random numbers 1 - 5
m1 = np.random.randint(1, 5, size =(n, n)) 
m2 = np.random.randint(1, 5, size =(n, n))

# Evenly split array for workers by rows
split_m1 = np.vsplit(m1, num_workers)

# Create pool for workers
pool = mp.Pool(num_workers)


start_time = time.time()

# Have each worker multiply their share of matrix 1
for i in range(num_workers):
	pool.apply_async(multiply, args = (i, ))
pool.close()
pool.join()

end_time = time.time()

print("Naive parallel finished in {0} seconds \n".format(end_time - start_time))
