import random
import networkx as nx
import numpy as np
import numba
import timeout_decorator
import copy
from timeit import default_timer


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




##******** Implementation: numpy ********##
##**** Construct distance matrix ****##

@timeout_decorator.timeout(10800)
def distance_matrix_np(graph, n):
  ## calculate distance matrix
  dist_mtx = np.full((n,n), np.inf)
  for g in graph:
    i = int(g[0]) - 1
    j = int(g[1]) - 1
    d = g[2]
    dist_mtx[i,j] = d
    dist_mtx[j,i] = d

  ## set diagonal to 0
  np.fill_diagonal(dist_mtx, 0)
 
  return dist_mtx



##**** Calculate Hedetniemi Matrix Sum ****##

@timeout_decorator.timeout(10800)
def hede_distance_np(matrix, n):
  mtx_a_t = np.full((n,n), np.inf)
  mtx_a_t_1 = matrix.copy()
  
  for p in range(n):
    for i in range(n):
      a = mtx_a_t_1[i]
      for j in range(n):
        b = matrix[:,j]
        mtx_a_t[i,j] = np.amin([a[k] + b[k] for k in range(n)])
    
    if np.array_equal(mtx_a_t, mtx_a_t_1):
      break
    else:
      mtx_a_t_1 = mtx_a_t.copy()   
  
  return mtx_a_t



##******** Main ********##

with open('hedet_results_np.csv', 'w') as fw:
  fw.write('nodes,degree,np_t1,np_t2\n')
  fw.flush()
    
  for i in nodes:
    for j in degree:
      data = locals()['data_n' + str(i) + '_d' + str(j)]
          
      ## Numpy t1
      try:
        start = default_timer()
        dist_mtx_np = distance_matrix_np(np.array(data), i)
        stop = default_timer()
        np_t1 = stop - start
      except:
        np_t1 = float('inf')
          
      ## Numpy t2
      try:
        start = default_timer()
        mtx_a_t_np = hede_distance_np(dist_mtx_np, i)
        stop = default_timer()
        np_t2 = stop - start
        ## print shortest path matrix
        with open('hede_dist_np' + '_n' + str(i) + '_d' + str(j) + '.txt', 'w') as f:
          f.write('\n'.join(['\t'.join([str(round(cell,2)) for cell in row]) for row in mtx_a_t_np.tolist()]))                
      except:
        np_t2 = float('inf')
        
      fw.write(str(i) + ',' + str(j) + ',' + str(np_t1) + ',' + str(np_t2) + '\n')

      fw.flush()
fw.close()
