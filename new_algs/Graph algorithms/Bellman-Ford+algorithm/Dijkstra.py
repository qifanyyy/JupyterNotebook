## Implrementation of Dijsktra algoritm in Python

#function for priority queue
#on top of the gueue with priority is node with smallest value
def popmin(pqueue):
    lowest = 1000 
    keylowest = None
    for key in pqueue:
        if pqueue[key] < lowest:
            lowest = pqueue[key]
            keylowest = key
    del pqueue[keylowest]
    return keylowest
 
#function that implements algorithm
def dijkstra(graph, start):
    #pqueue follows the smallest value of distance from
    #start node to current node
    pqueue = {} # node: distance from start node
    dist = {}   # node: distance to start node
    pred = {}   # node: predecessor to the node
 
    # initialization
    for v in graph:
        dist[v] = 1000
        pred[v] = -1
    dist[start] = 0
    for v in graph:
       pqueue[v] = dist[v] # equivalent which is put i queue
 
    while pqueue:
        u = popmin(pqueue) # returns node with the smallest value 
        for v in graph[u].keys(): # for each neighboor of u
            w = graph[u][v] # w is distance from u to v
            newdist = dist[u] + w
            if (newdist < dist[v]): # if new distance is shorter than saved
                #distance, new distance is saved
                pqueue[v] = newdist
                dist[v] = newdist
                pred[v] = u
 
    return dist, pred
#example of the graph
graph = {
    0 : {1:6, 2:1, 3:4},
    1 : {4:3},
    2 : {1:-3, 3:2},
    3 : {4:-1},
    4 : {2:5},
}
 
dist, pred = dijkstra(graph, 0)

print ("Shortest distance from start node 0 to all other nodes is:")
for v in dist:
    print (v,'=',dist[v])

print ("Paths from start noe to all other nodes (predecessors of nodes):")
for v in pred:
    print (v,'=',pred[v])
