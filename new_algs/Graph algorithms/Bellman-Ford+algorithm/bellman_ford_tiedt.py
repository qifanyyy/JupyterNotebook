''' 
 Tyler Tiedt
 4/1/19
 Bellman Ford Algorithm
 CPCS 447
'''

import sys
# sets up the bellman ford algorithm
def init(graph, start_node):
  dist = {}
  prevNode = {}
  for node in graph:
    dist[node] = sys.maxsize
    prevNode[node] = None
  dist[start_node] = 0
  return dist, prevNode

# performs bellman ford algorithm
def bellman_ford(graph, start_node):
  dist, prevNode = init(graph, start_node)
  path = []
  cnt = 0
  # iterate algorithm nodes-1 times
  while(cnt < len(graph) - 1):
    # loop over every node
    for node in graph:
      # loop over every neighbor node
      for next_node in graph[node]:
        # if the distance to the node is less then the curent distance
        # reassign the distance and reassign the shortest path node
        if(dist[node] + graph[node][next_node] < dist[next_node]):
          dist[next_node] = dist[node] + graph[node][next_node]
          prevNode[next_node] = node
    cnt += 1
  # loop to get the path from every node to z
  for node in graph:
    path.append(get_path(prevNode, node, 'z'))
  return dist, path

# get the shortest path
def get_path(prevNode, start_node, end_node):
  path = []
  # this basiclly reassigns start node until it reaches end node
  # this will give us the path to each node from end node
  while(start_node is not end_node):
    path.append(start_node)
    start_node = prevNode[start_node]
  path.append(end_node)
  return path 

# Main
# create graph
graph = {
  'z': {'x': 2, 'v': 6},
  'x': {'v': 3, 'y': 3},
  'v': {'u': 1},
  'y': {'u': 2},
  'u': {}
  }
# run algorithm
distance, path = bellman_ford(graph, 'z')
# print the cost from z to every node
print('Cost from z:')
print('Node | Cost')
print('-----|-----') 
for dist in distance:
  print('  %s  |  %d' % (dist, distance[dist])) 
print()  

# print the forwarding table from z to every node
print('Forwarding Table:')
print('Node | Forward')
print('-----|--------')
for nodes in path:
  if(len(nodes) != 1):
    print('  %s  |  z, %s' % (nodes[0], nodes[len(nodes) - 2]))
