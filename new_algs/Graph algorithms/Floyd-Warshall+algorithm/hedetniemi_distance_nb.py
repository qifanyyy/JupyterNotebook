import random
import networkx as nx
import numpy as np
import numba
import timeout_decorator
import copy
from timeit import default_timer

print(numba.config.NUMBA_NUM_THREADS)
print(numba.config.NUMBA_DEFAULT_NUM_THREADS)

##******** Read graph data ********##

## Number of nodes (100/1,000/10,000/100,000/1,000,000)
nodes = [100, 1000, 10000, 100000, 1000000]
print('Nodes: ', nodes)
## Total degree
degree = [3, 4, 5]
print('Degree: ', degree)

for i in nodes:
    for j in degree:        
        locals()['data_n' + str(i) + '_d' + str(j)] = []
        with open('graph_n' + str(i) + '_d' + str(j) + '.txt', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                l = line.split()
                item = [int(l[0]), int(l[1]), float(l[2])]
                locals()['data_n' + str(i) + '_d' + str(j)].append(item)

        print(locals()['data_n' + str(i) + '_d' + str(j)][0])



##******** Implementation: numba (njit) ********##
##**** Construct distance matrix ****##

@timeout_decorator.timeout(10800)
@numba.njit
def distance_matrix_nb(graph, n):
  ## calculate distance matrix
  dist_mtx = np.full((n,n), np.inf)
  for g in numba.prange(graph.shape[0]):
    i = int(graph[g,0]) - 1
    j = int(graph[g,1]) - 1
    d = graph[g,2]
    dist_mtx[i,j] = d
    dist_mtx[j,i] = d

  ## set diagonal to 0
  np.fill_diagonal(dist_mtx, 0)
 
  return dist_mtx



##**** Calculate Hedetniemi Matrix Sum ****##

@timeout_decorator.timeout(10800)
@numba.njit
def hede_distance_nb(matrix, n):
  mtx_a_t = np.full((n,n), np.inf)
  mtx_a_t_1 = matrix.copy() 
  
  for p in numba.prange(n):
    for i in numba.prange(n):
      a = mtx_a_t_1[i]
      for j in numba.prange(n):
        b = matrix[:,j]
        mtx_a_t[i,j] = np.amin(np.array([a[k] + b[k] for k in range(n)]))
    
    if np.array_equal(mtx_a_t, mtx_a_t_1):
      break
    else:
      mtx_a_t_1 = mtx_a_t.copy()   
  
  return mtx_a_t



##******** Compile ********##
d = [[1, 2, 30], [1, 4, 30], [1, 9, 40],
        [2, 3, 25], [2, 4, 40], [3, 4, 50],
        [4, 5, 30], [4, 6, 20], [5, 7, 25],
        [6, 7, 20], [6, 9, 20], [7, 8, 25],
        [8, 9, 20]]
n = 9

dist_mtx = distance_matrix_nb(np.array(d), n)
mtx_a_t = hede_distance_nb(dist_mtx, n)



##******** Main ********##

with open('hedet_results_nb.csv', 'w') as fw:
  fw.write('nodes,degree,nb_t1,nb_t2\n')
  fw.flush()
    
  for i in nodes:
    for j in degree:
      data = locals()['data_n' + str(i) + '_d' + str(j)]
          
      ## Numba (njit) t1
      try:
        start = default_timer()
        dist_mtx_nb = distance_matrix_nb(np.array(data), i)
        stop = default_timer()
        nb_t1 = stop - start
      except:
        nb_t1 = float('inf')
      
      ## Numba (njit) t2
      try:
        start = default_timer()
        mtx_a_t_nb = hede_distance_nb(dist_mtx_nb, i)
        stop = default_timer()
        nb_t2 = stop - start
        ## print shortest path matrix
        with open('hede_dist_nb' + '_n' + str(i) + '_d' + str(j) + '.txt', 'w') as f:
          f.write('\n'.join(['\t'.join([str(round(cell,2)) for cell in row]) for row in mtx_a_t_nb.tolist()]))                
      except:
        nb_t2 = float('inf')
          
      fw.write(str(i) + ',' + str(j) + ',' + str(nb_t1) + ',' + str(nb_t2) + '\n')

      fw.flush()
fw.close()
