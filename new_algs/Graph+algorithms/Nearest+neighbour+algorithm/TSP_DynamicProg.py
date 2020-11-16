import numpypy
import numpy as np
import math
import sys
import gc
from itertools import combinations

infinity = sys.maxint

def tsp(towns):
    # A dynamic programming algorithm for TSP with O((2^n)*(n^2)) running time.
    # Returns the cost of the optimal route.
    
    n = len(towns)
    
    # Initialize binomials for memoization
    global binomials
    binomials = [[None for _ in range(n+1)] for _ in range(n+1)]
    
    # Using NumPy float32 arrays (with no mapping dictionaries!)
    
    # For each m (m = |S|) we will erase all entries for (m-2),
    # i.e. we will alternate only between two arrays
    A0 = np.zeros((n, binomial(n, n/2)), dtype=np.float32) # For odd m's
    A1 = np.zeros((n, binomial(n, n/2)), dtype=np.float32) # For even m's
    
    # Memoization (~ dynamic programming table)
    def A_(S, j):
        if j == 0:
            if len(S) == 1 and S[0] == 0: return np.float32(0.0)
            else: return np.float32(infinity)
        else:
            if len(S) % 2: return A0[j][index(S)]
            else: return A1[j][index(S)]
            
    def update_A(S, j, val):
        if len(S) % 2:
            A0[j][index(S)] = val
        else:
            A1[j][index(S)] = val
         
    # The dynamic programming recurrence
    # NB: do not use sets, to save memory!
    for m in xrange(2, n+1):
        print('m = %f' % m)
        gc.collect()
        for S in combinations(range(n), m):
            if 0 not in S: continue
            for j in S:
                if j == 0: continue
                update_A(S, j, min([A_(excluded(S, j), k) + dist(towns, k, j) for k in S if k != j]))
              
    return min([A_(range(n), j) + dist(towns, j, 0) for j in range(1, n)])

#euclidean distance function
def dist(towns, i, j):
    return math.sqrt((towns[i][0]-towns[j][0])*(towns[i][0]-towns[j][0]) + (towns[i][1]-towns[j][1])*(towns[i][1]-towns[j][1]))
    
    
def index(S):
    # See http://en.wikipedia.org/wiki/Combinatorial_number_system for details
    # (Calculating binomials sadly make the actual running time a bit worse
    # than announced, but for n = 25: O(n) is still not that much).
    # [S = sorted(S)] - no need in sorting, since subsets are already sorted when generated!
    res = 0
    for i in range(len(S)):
        res += binomial(S[i], i+1)
    return res
    
    
def excluded(lst, elem):
    return filter(lambda x: x != elem, lst)
    
    
binomials = None
    
def binomial(n, k):
    if n < k: return 0
    if binomials[n][k]: return binomials[n][k]
    ntok = 1
    for t in range(min(k, n-k)):
        ntok = ntok*(n-t)//(t+1)
    binomials[n][k] = ntok
    return ntok
    
    
def main():
    #this function inputs the file
    #f = open('tsp.txt')
    n = int(f.readline())
    towns = [np.array([float(x) for x in line.split()], dtype=np.float32) for line in f]
    
    print(tsp(towns))


main()