##Authors: Osman Ali, Akshay Krishna

from mpi4py import MPI           ##imports for python library numpy and math
from math import ceil, fabs	 ##Import MPI library for parallel processing 
import numpy
###########################################

comm = MPI.COMM_WORLD		 ##initialize cluster
clu_size = comm.Get_size()	 ##get the cluster size (no. of processing nodes)
rank = MPI.COMM_WORLD.Get_rank() ##get rank of nodes
node_name = MPI.Get_processor_name() ##name of the node 

print("Running %d parallel MPI processes of %d on %s" % (rank,clu_size,node_name))   ##print statement for 

#############defining the function ################

#main function that takes four arguments 
#A = the matrix ,x = vector, size_vec = size of the vector being used,
#iter = no. of iterations*/

def matvecmul(comm,A,x,size_vec,iter):   
 
 for t in xrange(iter):			##the main iterations over the vector
	new_vec = numpy.inner(A,x)	##each node gets a piece of the vector
        y = numpy.zeros_like(x)
	comm.Allgather(
        [new_vec, MPI.DOUBLE], 		##gather the results and return
        [y, MPI.DOUBLE] 
        )
 	
 return new_vec

############## main #############################

#Check results of mpi application using builtin numpy matrix-vec multiplication

size_vec = 32				##size vector, change as needed
iter = 20				##no. of iterations change as needed

comp_vec_size = size_vec // comm.size
size_vec = comm.size * comp_vec_size    ##check that vector size is a multiple of number of nodes

x = numpy.random.rand(size_vec)		## generate random vector of size size_vec
A = numpy.random.rand(comp_vec_size, size_vec) ## generate random matrix of size comp_vec_size, size_vec

y_mpi = matvecmul(comm, A, x,size_vec,iter) ##call the parallel matrix-vector-multiplication program  

############### testing results ################

if rank == 0:				
 #test
 y = numpy.dot(A, x)
 print(y,"y")
 print(y_mpi,"y_mpi")
 #compare the local and MPI results

 print("sum(y - y_mpi) =", (y - y_mpi).sum())
