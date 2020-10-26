#============================================
# A randomized python algorithm to detect small k-cycles
# in undirected graphs.
# - by Alexander Olson
#
# There is a relatively straightforward algorithm to find triangles in
# a graph, given its adjacency matrix A: by simply calculating A^2, and
# checking for a 1 at index (i, j) in A^2 and at index (j, i) in A, we can
# verify that there is a path of length 2 from i to j and a closing edge 
# from j to i.
#
# The general problem of, "can we find a k-cycle in an undirected graph?"-
# has been proven to be NP-hard. However, by generalizing and randomizing the matrix 
# multiplication algorithm as above, we can find k-cycles of length less than
# lg(n) in a close-to-polynomial O(n^w+lglg(n-1)), where w is the constant
# of matrix multiplication (less than 2.4 with the most efficient implementations):
# the algorithm works with a 98% probability of success.
#
#============================================
#
# You can find a fuller analysis of the algorithm's correctness, accuracy
# and runtime in "kcyclesincreasing.pdf".
#
# If you'd like to use this code for any (non-plagiarizing reason), feel free!
# (But please attribute it).
#============================================

#We'll test our finder here.
import random
import numpy as np
import time

def main():
	#For n increasing from 2^3, 2^4, ..., 2^10, repeat the following process lgn times:
	#We will test the algorithm a graph of size nxn, with a cycle of size lgn. (A)
	#We will also test the algorithm on a graph of a hamiltonian path, and ensure that we return false. (B)
	# (a hamiltonian path should have no cycles!)
	for lgn in range(3, 11):
		#Calculate n.
		n = pow(2, lgn)
		
		for _ in range(0, lgn):
			#Create the adjacency matrix: we construct a random permutation of lgn points from n, and
			#fill that in as a cycle in our matrix.
			A = np.zeros((n, n))
			B = np.zeros((n, n))
			
			#===THE KNUTH SHUFFLE===
			#Create the cycle pi.
			pi = []
			for i in range(0, n):
				pi.append(i)
			
			#Rearrange pi.
			for i in range(0, n-1):
				j = random.randint(i, n-1)
				temp = pi[j]
				pi[j] = pi[i]
				pi[i] = temp
			#=======================
			
			#We can use pi here twice:
			#The first lg(n) points comprise the cycle in the graph represented by A.
			#All n points comprise the hampath in the graph represented by B.
			for i in range(0, lgn-1):
				A[pi[i]][pi[i+1]] = 1
				A[pi[i+1]][pi[i]] = 1
			A[pi[0]][pi[lgn-1]] = 1
			A[pi[lgn-1]][pi[0]] = 1
			
			for i in range(0, n-1):
				B[pi[i]][pi[i+1]] = 1
				
			if cycleSearch(A, lgn) == True:
				print("(A) On a ", lgn ," cycle, in a graph of ", n, " nodes: success!")
			elif cycleSearch(A, lgn) == None:
				print("(A) On a ", lgn ," cycle, in a graph of ", n, " nodes: terminated early?")
			else:
				print("(A) On a ", lgn ," cycle, in a graph of ", n, " nodes: failure...")
				
			if cycleSearch(B, lgn) == True:
				print("(B) On a hampath in a graph of ", n, " nodes: false positive...")
			elif cycleSearch(B, lgn) == None:
				print("(B) On a hampath in a graph of ", n, " nodes: terminated early?")
			else:
				print("(B) On a hampath in a graph of ", n, " nodes: true negative!")	
	return 0
	
#A: the input adjacency matrix for the given graph.
#k: the cycle length we are looking for.
#The algorithm will return *true* if we find a k-cycle, or *false*, if we don't.
#Alternatively, if we find that k > ceil(lg(n)), we will return null and cut it off
#prematurely.
def cycleSearch(A, k):
	#First, let's calculate ceil(lg(n)).
	n = A.shape[0]
	lgn = 0
	while n > 0:
		n = n / 2
		lgn = lgn + 1
	n = A.shape[0]

	#Terminate if k is too large.
	if k > lgn:
		return None
	
	#Calculate (k-1)!.
	km = k-1
	kmf = 1
	while km > 0:
		kmf = kmf * km
		km = km - 1
	
	#------------------
	for _ in range(0, 2 * kmf):
		#First, pick a corresponding permutation of n elements, and rearrange the adjacency matrix.
		
		#===THE KNUTH SHUFFLE===
		#Create the cycle pi.
		pi = []
		for i in range(0, n):
			pi.append(i)
		
		#Rearrange pi.
		for i in range(0, n-1):
			j = random.randint(i, n-1)
			temp = pi[j]
			pi[j] = pi[i]
			pi[i] = temp
		#=======================
		
		#Rearrange the original adjacency matrix based on pi: call this new matrix AR.
		AR = np.zeros((n, n))
		for i in range(0, n):
			for j in range(0, n):
				AR[i][j] = A[pi[i]][pi[j]]	
				
		#------------------				
		#Next, decompose (k-1) into a sum of powers of 2, D.
		# if D[0] = 1 and D[1] = 1, for example, and D has length 2, then (k-1) = 2^0 + 2^1.
		#Create a corresponding list of adjacency matrices, AL.
		# these will be the matrices AR^1, AR^2 and so on.
		#AC represents AR^2^<current base>, starting from 0. Remove entries in AC where not i < j.
		km = k-1
		D = []
		AL = []
		AC = AR.copy()
		for i in range(0, n):
			for j in range(0, n):
				if not i < j: AC[i][j] = 0
		
		while km > 0:
			AL.append(AC.copy())
			
			if km % 2 == 1: D.append(1)
			else: D.append(0)
			
			AC = AC.dot(AC)
			km = km / 2
		#------------------	
		#Build the path matrix for (k-1), AP.
		AP = np.identity(n)
		for i in range(0, len(D)):
			if D[i] == 1: AP = AP.dot(AL[i])
		
		#Iterate over the matrix to find cycles: 
		#points where ij = 1 in AP, and ji = 1 in AR.
		#Return true if we find one.
		
		for i in range(0, n):
			for j in range(0, n):
				if AP[i][j] == 1 and AR[j][i] == 1: return True
	#------------------			
	return False	

if __name__ == "__main__":
	main()
