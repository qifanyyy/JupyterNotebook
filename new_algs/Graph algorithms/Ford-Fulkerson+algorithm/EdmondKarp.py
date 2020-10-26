import decimal
import networkx as nx
import numpy as np
import time
import LongestPath as LP
from collections import defaultdict
from memory_profiler import profile

# To compute number of sugmenting paths needed for computing max flow
numberOfPaths = 0

"""
Instructions to execute the code
run as : python3 EdmondKarp.py

The purpose of this file is to run the algorithm on neural network dataset 
and also to use it as library for edmond karp implementation
"""

"""
The variables used throughout the code are:
    G : It is the networkX graph object
    s : It is the source of the graph
    t : It is the sink of the graph
    C : This is a 2D capacity matrix
    adj: This variable stores the adjacent vertices of each vertex
    flow_list : This variable is used to store the flows for each edge

This function performs the following steps:
    1)  Looks for an augmenting path using BFS
    2)  If present adds the flow to the cumulative flow
    3)  Then increases or decreases the flow along the augmenting path
        this is the residual graph part
    4)  Returns the cumulative flow and the flow list
"""
#@profile   #Used for memory profiling
def EdmondsKarp(C, adj, s, t):
  #initialise cumulative flow and length
  cumulative_flow = 0
  length = len(C)

  # Get the flow for each edge
  flow_list = [[0 for i in range(length)] for j in range(length)]

  #Till there is an augmenting path keep looking for increase in flow
  while True:
    # Using breadth first search, look for a path
    #path variable stores the explored nodes of the source i.e. the BFS path
    flow, path = BreadthFirstSearch(C, adj, flow_list, s, t)
    
    # To compute number of sugmenting paths needed for computing max flow
    global numberOfPaths
    numberOfPaths += 1

    # max flow for each augmenting path
    print('max: %s' %flow)

    if flow == 0:
      break

    # Add the flow returned by that path to the cumulative flow
    cumulative_flow = cumulative_flow + flow
    v = t
    while v != s:
      u = path[v]
      #increase flow in the edge
      flow_list[u][v] = flow_list[u][v] + flow
      #decrease the flow
      flow_list[v][u] = flow_list[v][u] - flow
      v = u
  return (cumulative_flow, flow_list)

"""
The purpose of this function is return an augmenting path using BFS traversal

This function performs the following steps:
    1)  Creates a set of explored nodes to keep track for BFS (explored variable)
    2)  Search for all adjacent vertices starting from source
    3)  Then increase or redirect the flow along the path if capacity is available
    4)  Select min weight from the edges of the path and store in M
    5)  Return min weight as M[t] and path as explored
"""
def BreadthFirstSearch(C, adj, flow_list, s, t):
  length = len(C)
  #maintain a set of explored nodes
  explored = [-1 for i in range(length)]
  # make sure source is not rediscovered
  explored[s] = -2 

  # To store the capacity to node i in M
  M = [0 for i in range(length)]
  # Make the capacity infinity to skip garbage value
  M[s] = decimal.Decimal('Infinity')

  # maintain a queue of nodes
  queue = []
  queue.append(s)
  while queue:
    u = queue.pop(0)
    for v in adj[u]:
      # If v is not seen and capacity is available
      if C[u][v] - flow_list[u][v] > 0 and explored[v] == -1:
        explored[v] = u
        # it will work because at the beginning M[u] is Infinity
        M[v] = min(M[u], C[u][v] - flow_list[u][v]) # try to get minimum weight
        if v != t:
          queue.append(v)
        else:
          return M[t], explored
  return 0, explored

# This function parses the file to create a capacity matrix and adjacent vertices of each vertex
def ParseGraph(file):
  file_object = open(file, "r")
  # store capacity of edges
  C = []
  adj = {} # neighbors include reverse direction neighbors
  for line in file_object.readlines():
    C.append([int(i) for i in line.split(',')])
  for vertex in range(len(C)):
    adj[vertex] = []
  for vertex, flow_list in enumerate(C):
    #adjacent variable stores the adjacent node for the nodes in the flow
    for adjacent, flow in enumerate(flow_list):
      if flow > 0:
        adj[vertex].append(adjacent)
        adj[adjacent].append(vertex) # reverse path may be used
  # return the capacity matrix and adjacecncy matrix
  return C, adj

# This function converts the networkx digraph to weighted capacity matrix
def save_to_txt_and_read(nxGraph,weightLabel,s,t):
  # Convert the Networkx MultiDIGraph to weighted capacity matrix
  printableMatrix = nx.to_numpy_matrix(nxGraph, weight=weightLabel)

  file_name = 'output.txt'

  #Save it to a text file for the program to read it
  np.savetxt(file_name, X=printableMatrix, delimiter=',', fmt="%d")

  #Parse the file
  C, adj = ParseGraph(file_name)
  
  #Run EdmondKarp to get the max flow and the flow paths
  flow, flow_list = EdmondsKarp(C, adj, s, t)
  print('Max flow: %s' % flow)

  return flow

# Driver code for the program
#The purpose of this driver code is to run the algorithm on neural network dataset
if __name__ == "__main__":

  # read the gml data in networkx graph object
  mygraph = nx.read_gml("datasets/unoriginal.gml")

  # calculate capacity matrix from the graph
  C = defaultdict(list)  # [[0]*mygraph.number_of_nodes()]*mygraph.number_of_nodes()

  for each in mygraph.edges():
    C[each[0]].append(each[1])

  # run the function from LongestPath file to get the longest path in the graph
  all_paths, max_len, max_paths = LP.run_the_algo(C)
  s_time = time.time()
  all_flows=[]

  # If there are multiple longest paths calculate max flow for all 
  for eachLongPath in max_paths:
    print("--------------------------------------------------------------------")
    print(eachLongPath[0], "---", eachLongPath[-1])
    all_flows.append(save_to_txt_and_read(nxGraph=mygraph, weightLabel="value", s=eachLongPath[0], t=eachLongPath[-1]))

  print('Number of augmenting paths: %s' % str(numberOfPaths - 1))
  print("--- %s seconds ---" % (time.time() - s_time))
