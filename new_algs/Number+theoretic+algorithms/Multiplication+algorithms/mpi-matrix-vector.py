import numpy
# prepare data and save it to files
N = 32
A = numpy.random.rand(N, N)
numpy.save("random-matrix.npy", A)
x = numpy.random.rand(N)
numpy.save("random-vector.npy", x)


from mpi4py import MPI
import numpy
#initialize MPI cluster
comm = MPI.COMM_WORLD
size1 = MPI.COMM_WORLD.Get_size()
rank1 = MPI.COMM_WORLD.Get_rank()
name1 = MPI.Get_processor_name()
p = comm.Get_size()
print("Running %d parallel MPI processes of %d on %s" % (rank1,size1,name1))
#get process id
rank = comm.Get_rank()
#get cluster size
#p = comm.Get_size()
def matvec(comm, A, x):
 m = A.shape[0] // p
 #every process gets a part of the data
 #for t in xrange(iter):
 #   y_part = numpy.inner(m, x)
 y_part = numpy.dot(A[rank * m:(rank+1)*m], x)
 #container for the result
 y = numpy.zeros_like(x)
 #collect results from the pool, write them to container y
 comm.Allgather([y_part, MPI.DOUBLE], [y, MPI.DOUBLE])
 #print("Running %d parallel MPI processes" % comm.size)
 return y
#print("Running %d parallel MPI processes" % comm.size)
A = numpy.load("random-matrix.npy")
x = numpy.load("random-vector.npy")
y_mpi = matvec(comm, A, x)

if rank == 0:
 #test
 y = numpy.dot(A, x)
 print(y_mpi)
 #compare the local and MPI results
 print("sum(y - y_mpi) =", (y - y_mpi).sum())


