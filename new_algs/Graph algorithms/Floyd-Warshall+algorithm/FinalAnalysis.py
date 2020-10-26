import random
import sys
import time

import matplotlib.pyplot as plt
import networkx as nx
from scipy.interpolate import interp1d
from graph import *


class Algorithms:
    def __init__(self):
        self.v = 0

    def floydWarshal(self, graph):
        dist = []
        self.v = len(graph)

        for i in range(self.v):
            ls = []
            for j in range(self.v):
                ls.append(0)
            dist.append(ls)

        for i in range(0, self.v):
            for j in range(0, self.v):
                dist[i][j] = graph[i][j]

        for k in range(0, self.v):
            for i in range(0, self.v):
                for j in range(0, self.v):
                    if float(dist[i][k] + dist[k][j]) < dist[i][j]:
                        dist[i][j] = float(dist[i][k] + dist[k][j])
                    obj=XYZ(data)


        self.printsolution(dist)

    def printsolution(self, farness):
        for i in range(0, self.v):
            for j in range(0, self.v):
                if farness[i][j] == float('infinity'):
                    print("INF\t", end='')
                else:
                    print(str(farness[i][j]) + "\t", end='')
            print()
        print()
    def MinimumDistance(self, distance, shortestPathTreeSet, verticesCount):
        min = sys.maxsize
        minIndex = 0

        for v in range(0, verticesCount):
            if (shortestPathTreeSet[v] == False and distance[v] <= min):
                min = distance[v]
                minIndex = v

        return minIndex

    def printDisjkstra(self,froom, distance, verticesCount):
        print('Distance from :',froom)

        print('Vertex\tDistance from source')
        for i in range(0, verticesCount):
            print(str(i) + '\t\t\t' + str(distance[i]))


    def dijkstra(self, graph):

        verticesCount = len(graph)

        l=0

        for source in range(0, verticesCount):

            distance = [sys.maxsize] * verticesCount
            shortestPathTreeSet = [False] * verticesCount

            distance[source] = 0

            for count in range(0, verticesCount - 1):
                u = self.MinimumDistance(distance, shortestPathTreeSet, verticesCount)
                shortestPathTreeSet[u] = True

                for v in range(0, verticesCount):
                    if shortestPathTreeSet[v] == False and (
                            bool(graph[u][v]) and
                            distance[u] != sys.maxsize and
                            distance[u] + graph[u][v] < distance[v]):
                        distance[v] = distance[u] + graph[u][v]

            self.printDisjkstra(l,distance, verticesCount)
            l+=1


vlist = []
lst1 = []
lst2 = []

listofgraph=[]


for i in range(5): #no of graph
    print('                                                                                                    :', i)
    while True:
        v = random.randint(4,8)
        if v not in vlist:
            vlist.append(v)
            break

    G = nx.DiGraph() #G = graph obj

    data = \
        [
            [
                random.randint(1, 1000) for x in range(v)
            ]
            for y in range(v)
        ]


    print(v)

    for t in range(v):
        for u in range(v):
            if t == u:
                data[t][u] = 0


    for t in range(v):
        for u in range(v):
            if data[t][u] != 0:
                G.add_edges_from([(t, u)], weight=data[t][u])
    print('pring length of edges:',len(G.edges))

    #Randomly edges bht sary thy tu hamny is logic sy more then 50% ko remove kia h randomly
    c=len(G.edges)/1.1
    print(c)
    for i in range(int(c)):
        row = random.randint(0, v - 1)
        col = random.randint(0, v - 1)
        if G.has_edge(row,col):
            G.remove_edge(row,col)
        # data[row][col] = 0
        # data[col][row] = 0

    print('Lenght of Remaning Edges :',len(G.edges))

    #graph working
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])

    #graph choose
    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, pos, with_labels=True, node_size=1500, edge_color='black', edge_cmap=plt.cm.Reds)
    plt.show()



    #myFile = open('Graph_Input.csv', 'a')
    #with myFile:
    #    writer = csv.writer(myFile)
    #    writer.writerows(data)

    temp = Algorithms()


    start_time = time.time()
    temp.floydWarshal(data)
    elapsed_time = time.time() - start_time
    lst1.append(elapsed_time)

    start_time1 = time.time()
    temp.dijkstra(data)
    elapsed_time1 = time.time() - start_time1
    lst2.append(elapsed_time1)

    print("Floyd : ", elapsed_time)

    print("Dijkstra : ", elapsed_time1)

lst2.sort()
lst1.sort()
vlist.sort()

f = interp1d(vlist, lst1)
ff = interp1d(vlist, lst2)

f2 = interp1d(vlist, lst1, kind='cubic')
ff2 = interp1d(vlist, lst2, kind='cubic')

plt.plot(vlist, lst1, 'o', vlist, f(vlist), '-', vlist, f2(vlist), '-')
plt.plot(vlist, lst2, 'o', vlist, ff(vlist), '-', vlist, ff2(vlist), '-')

plt.legend(['Floyd','','Floyd Line','Dijkstra','','Dijkstra Line'], loc='best')
plt.show()
plt.close()
