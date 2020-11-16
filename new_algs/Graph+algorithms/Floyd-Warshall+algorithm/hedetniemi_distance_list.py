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



##******** Implementation: list ********##
##**** Construct distance matrix ****##

@timeout_decorator.timeout(10800)
def distance_matrix_list(graph, n):
  ## calculate distance matrix
  INF = float('inf')
  dist_mtx = [[INF] * n for i in range(n)]
  for g in graph:
    i = g[0] - 1
    j = g[1] - 1
    d = g[2]
    dist_mtx[i][j] = d
    dist_mtx[j][i] = d

  ## set diagonal to 0
  for i in range(n):
    dist_mtx[i][i] = 0.0
 
  return dist_mtx



##**** Calculate Hedetniemi Matrix Sum ****##

@timeout_decorator.timeout(10800)
def hede_distance_list(matrix, n):
  INF = float('inf')
  mtx_a_t = [[INF] * n for i in range(n)]
  mtx_a_t_1 = copy.deepcopy(matrix)

  for p in range(n):
    for i in range(n):
      a = mtx_a_t_1[i]      
      for j in range(n):
        b = [row[j] for row in matrix] 
        mtx_a_t[i][j] = min([a[k] + b[k] for k in range(n)])
    
    if mtx_a_t == mtx_a_t_1:
      break
    else:
      mtx_a_t_1 = copy.deepcopy(mtx_a_t)  
  
  return mtx_a_t




##******** Main ********##

with open('hedet_results_list.csv', 'w') as fw:
  fw.write('nodes,degree,list_t1,list_t2\n')
  fw.flush()
    
  for i in nodes:
    for j in degree:
      data = locals()['data_n' + str(i) + '_d' + str(j)]
      
      ## List t1
      try:
        start = default_timer()
        dist_mtx_list = distance_matrix_list(data, i)
        stop = default_timer()
        list_t1 = stop - start
      except:
        list_t1 = float('inf')
      
      ## List t2
      try:
        start = default_timer()
        mtx_a_t_list = hede_distance_list(dist_mtx_list, i)
        stop = default_timer()
        list_t2 = stop - start
        ## print shortest path matrix
        with open('hede_dist_list' + '_n' + str(i) + '_d' + str(j) + '.txt', 'w') as f:
            f.write('\n'.join(['\t'.join([str(round(cell,2)) for cell in row]) for row in mtx_a_t_list]))
      except:
        list_t2 = float('inf')

      fw.write(str(i) + ',' + str(j) + ',' + str(list_t1) + ',' + str(list_t2) + '\n')

      fw.flush()
fw.close()
