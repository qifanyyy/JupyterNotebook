import random
import networkx as nx
import numpy as np
import timeout_decorator
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



##**** Calculate Dijkstra distance ****##

INF = float('inf')

@timeout_decorator.timeout(10800)
def dijkstra_list(source, distmatrix, n):
  dist = [INF if i!=source else 0 for i in range(n)]
  Q = list(range(n))
  while len(Q)>0:
    u = get_remove_min_list(Q, dist)
    U = get_neighbor_list(u, distmatrix, n)
    for v in U:
      newd = dist[u] + distmatrix[u][v]
      if newd < dist[v]:
        dist[v] = newd
  return dist


def get_remove_min_list(Q, dist):
  dmin = INF
  imin = -1
  for i in Q:
    if dist[i] < dmin:
      dmin = dist[i]
      imin = i
  Q.remove(imin)
  return imin


def get_neighbor_list(u, d, n):
  neighbors = [i for i in range(n) if d[i][u]!=INF and i!=u]
  return neighbors



##******** Main ********##

source = 1

with open('dijkstra_results_list.csv', 'w') as fw:
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
        mtx_a_t_list = dijkstra_list(source, dist_mtx_list, i)
        stop = default_timer()
        list_t2 = stop - start
        ## print shortest path matrix
        with open('dijkstra_dist_list' + '_n' + str(i) + '_d' + str(j) + '.txt', 'w') as f:
            f.write('\t'.join([str(round(cell,2)) for cell in mtx_a_t_list]))
      except:
        list_t2 = float('inf')
          
          
      fw.write(str(i) + ',' + str(j) + ',' + str(list_t1) + ',' + str(list_t2) + '\n')

      fw.flush()
fw.close()
