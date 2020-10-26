#https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
# Author - Neelam Yadav
#Bilal  Naazir
import random
from collections import defaultdict
import numpy as np
import time

class MaxFlowAlgo:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)
        # self.COL = len(gr[0])

    '''Returns true if there is a path from source 's' to sink 't' in 
    residual graph. Also fills parent[] to store the path '''

    def BFS(self, s, t, parent):

        # Mark all the vertices as not visited
        visited = [False] * (self.ROW)

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

                    # If we reached sink in BFS starting from source, then return
        # true, else false
        return True if visited[t] else False
    x=1
    thePath = []
    pathFlow= []
    def funct1(self, a):
        self.thePath.append(a)
        #print(self.thePath)
        return self.thePath
    # Returns tne maximum flow from s to t in the given graph
    def FordFulkerson(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * (self.ROW)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.BFS(source, sink, parent):
            #The nodes visited
            nodes = []
            #The nodes visited in accending order
            orderedNodes = []
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
                nodes.append(s)
                # Add path flow to overall flow
            max_flow += path_flow
            for i in reversed(nodes):
                orderedNodes.append(i)
            orderedNodes.append(sink)

            self.funct1(orderedNodes)
            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
            # print("graph" , self.x, "=")
            # print(np.asarray(self.graph))
            # print("+", path_flow)
            # print("=", max_flow)
            self.pathFlow.append(path_flow)
            self.x+=1

        return max_flow

    # Create a graph given in the above diagram


#Creating a graph with a  random number of nodes between 4 to 10 excluding the sink and source
flowGraph = [[]]
count = random.randint(6, 10)
print(count)

index = count - 1
print(index)
for i in range(count):
    flowGraph.append([])
    for j in range(count):
        # Appending 0s to the last row
        if i == index:
            flowGraph[i].append(0)
        else:
            #populating the rows with random values from 0 to 20
            flowGraph[i].append(random.randint(0, 20))
    # Making the diagonal values 0
    flowGraph[i][i] = 0
    # making the first column of every row 0
    flowGraph[i][0] = 0;




del flowGraph[count]
flowGraph[0][index] = 0;
print("Flow network graph: ")
print(np.asarray(flowGraph))

g = MaxFlowAlgo(flowGraph)

source = 0
sink = index



import networkx as nx
import matplotlib.pyplot as plt

plt.savefig("simple_path.png") # save as png
plt.show() # display

P=nx.DiGraph()
whole=[]
for i in range(len(flowGraph)):
    whole.append(i)

evenList = []
oddList = []

for i in range(len(whole)):
    if (i % 2 == 0):
        evenList.append(i)
    else:
        oddList.append(i)
del evenList[0]
evenList.reverse()




P.add_node(0)
for i in range(len(oddList)):
    P.add_node(oddList[i])


for i in range(len(evenList)):
    P.add_node(evenList[i])


for i in range(len(flowGraph)):
    for j in range(len(flowGraph[i])):
        if(flowGraph[i][j]!=0):
            P.add_edge(i, j, capacity =flowGraph[i][j])


pos = nx.circular_layout(P)

nx.draw(P, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(P,'capacity')
nx.draw_networkx_edge_labels(P, pos, edge_labels=edge_labels, label_pos=0.3)
plt.show()
start = time.time()
print("The maximum possible flow is %d " % g.FordFulkerson(source, sink))
end = time.time()
print("time taken",end - start)
print("The paths: ",g.thePath)

for i in range(len(g.thePath)):
    Y = nx.DiGraph()
    Y.add_node(0)
    for a in range(len(oddList)):
        Y.add_node(oddList[a])

    for a in range(len(evenList)):
        Y.add_node(evenList[a])


    for j in range(len(g.thePath[i])-1):

        Y.add_edge(g.thePath[i][j],g.thePath[i][j+1], capacity = g.pathFlow[i])

    pos = nx.circular_layout(Y)
    nx.draw(Y, pos, with_labels=True)
    edgeLabel= nx.get_edge_attributes(Y,'capacity')
    nx.draw_networkx_edge_labels(Y,pos,edge_labels=edgeLabel)


    plt.show()


print("residual graph ",flowGraph)
print("the path flow: ",g.pathFlow)

