import numpy as np
import scipy as scp
import time
import cmath
from lazyarray import larray

"""
A file for storing various mathematical helper functions for each implementation.
"""

###################################################################
#tensor products

def tensor(b,a):

	"""
	Function that takes the tensor product of 2 matrices or vectors.
	Used by Dense implementation (dense.py)
	Behaves identically to np.kron()
	"""
	#Dimension of output
	a0 = a.shape[0]
	a1 = a.shape[1]
	b0 = b.shape[0]
	b1 = b.shape[1]
	outdim = (a0*b0,a1*b1)

	#Initialise output matrix with zeros
	output = np.zeros(outdim,dtype=complex)

	#Calculate output matrix
	for x in range(outdim[0]):
		for y in range(outdim[1]):
			output[x,y] = a[x%a0,y%a1]*b[x//a0,y//a1]

	return output

def tensor_sparse_qubit(A,B):

	'''
	Function that takes the tensor product of 2 Qubits.
	Used by sparse implementation (sparse.py) but does not take 
	advantage of sparse form, since speed difference is minimal
	'''
	#convert to dense matrices
	a = A.toarray()[0]
	b = B.toarray()[0]

	#Dimension of output
	a0 = a.shape[0]
	b0 = b.shape[0]
	outdim = (1,a0*b0)

	#Initialise output matrix with zeros
	output = np.zeros(outdim,dtype=complex)

	#Calculate output matrix
	for x in range(outdim[0]):
		output[0,x] = a[x%a0]*b[x//a0]

	return(output)

def tensor_sparse_gate(a,b):
	'''
	Function that takes the tensor product of 2 Gates.
	Used by sparse implementation (sparse.py)
	Gives the same result as sp.kron
	'''
	#import sparse inside as it breaks lazy if outside
	from scipy import sparse as sp

	#output dimensions
	a0 = a.shape[0]
	a1 = a.shape[1]
	b0 = b.shape[0]
	b1 = b.shape[1]
	outdim = (a0*b0,a1*b1)

	#catch for multiplying empty matrices
	if a.nnz == 0 or b.nnz == 0:
	    return sp.coo_matrix(outdim)

	#convert a from bsr to more standard csc version of sparse
	a = sp.csc_matrix(a)
	#convert b to dense
	b = b.toarray()
	
	#reshape a into data and calculate
	data = a.data.repeat(b.size).reshape(-1,b0,b1)
	data = data * b

	return sp.bsr_matrix((data,a.indices,a.indptr), shape=outdim)

def tensor_lazy(b,a):

	"""
	Function that takes the tensor product of 2 matrices or vectors.
	Used by lazy implementation (lazy.py)
	"""
	
	#Dimension of output
	a0 = a.shape[0]
	a1 = a.shape[1]
	b0 = b.shape[0]
	b1 = b.shape[1]
	outdim = (a0*b0,a1*b1)

	#function to feed creation of lazy output matrix
	#i and j refer to matrix index
	def kron(i,j):
		return a[i%a0,j%a1]*b[i//a0,j//a1]

	#create output
	output = larray(kron,shape=outdim)
	
	return output

#########################################################################
#matrix multiplication

def lazy_mul_gate(b,a):
	"""
	Function for the matrix multiplication of 2 gates.
	Used by lazy implementation (lazy.py)
	"""

	#Dimension of output
	a0 = a.shape[0]
	a1 = a.shape[1]
	b0 = b.shape[0]
	b1 = b.shape[1]
	outdim = (b0,a1)
	
	#function to feed creation of lazy output matrix
	#i and j refer to matrix index
	def mul(i,j):
		elem = sum(map(lambda n: b[i][n]*a[n][j],range(b1)))

		return elem
	
	output = larray(mul,shape=outdim)
		
	return(output)


def lazy_mul(b,a):
	
	"""
	Function for the matrix multiplication of 2 qubits.
	Used by lazy implementation (lazy.py)
	"""

	#Dimension of output
	a0 = a.shape[0]
	a1 = a.shape[1]
	b0 = b.shape[0]
	b1 = b.shape[1]
	outdim = (b0,a1)

	#function which feeds creation of output matrix
	#i and j refer to matrix index
	def mul(i,j):
		elem = sum(map(lambda n: b[i][n]*a[n],range(b1)))

		return elem

	#create output 
	output = larray(mul,shape = outdim)

	return output

#######################################################################
#qubit swapping

def perm_matrix(n,index1,index2):
	'''
	generates a permutation matrix from a list of pairs of numbers 
	to swap
	Used by all implementations 
	'''

	#catch user errors
	assert index1!=index2, "Cant swap qubit with itself"
	assert (index1<n) and (index2<n), "Cant swap qubits beyond size of gate"
	
	#shuffle index
	index1 = n-index1-1
	index2 = n-index2-1
	b = 2**index1 + 2**index2

	#work out which parts correspond to the index being swapped
	swaps = []
	for x in range(2**n):
		for y in range(x):
			if((x^y==b) and (count_bits(x)==count_bits(y))):
				swaps.append((x,y))


	#initialise output matrix with an identity 
	size = 2**n
	i = np.identity(size)
	
	#alter identity into swap matrix
	for pairs in swaps:
		temp = i[pairs[0]].copy()
		i[pairs[0]] = i[pairs[1]]
		i[pairs[1]] = temp
		
	return i

def count_bits(n):
	'''
	helper function for perm_matrix
	counts bits recursively
	'''
	if n==0:
		return 0
	else:
		return (n&1)+count_bits(n>>1)
