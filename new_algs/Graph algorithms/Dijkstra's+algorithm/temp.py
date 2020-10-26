import sys
import json

class Graph:

    ttime=0

    def minDist(self,dist,queue):
        min = float("Inf")
        index = -1

        for i in range(len(dist)):
            if dist[i] < min and i in queue:
                min = dist[i]
                index = i
        return index

    def printpath(self,previous,j):
        if previous[j] == -1:
            print(j,end=' ')
            return
        self.printpath(previous,previous[j])
        print(j,end=" ")
        self.ttime += time*density[previous[j]][j]

    def printSol(self,dist,previous,src):
        print("Vertex\t\tDistance\tPath\t\tTime")
        for i in range(len(dist)):
            self.ttime= 0
            print("\n",src,"->",i,"\t",dist[i],end = "\t\t")
            self.printpath(previous,i)
            print("\t\t",self.ttime,end=" ")


    def dijkstra(self,graph,src):
        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row

        previous = [-1] * row
        dist[src] = 0

        queue = []
        for i in range(row):
            queue.append(i)
        #add every node in the queue

        while queue:

            u = self.minDist(dist,queue)
            queue.remove(u)

            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        previous[i] = u
        self.printSol(dist,previous,src)

def removelink(i,j):
    graph[i][j]=graph[j][i] = 0
    density[i][j] = density[j][i] = 0


g = Graph()

with open('input.json') as infile:
    data = json.load(infile)
    graph = data['graph']
    density = data['density']
    node = data['node']
    time = data['time']

# graph = [
#         [0, 4, 0, 0, 0, 0, 0, 8, 0], 
# 		[4, 0, 8, 0, 0, 0, 0, 11, 0], 
# 		[0, 8, 0, 7, 0, 4, 0, 0, 2], 
# 		[0, 0, 7, 0, 9, 14, 0, 0, 0], 
# 		[0, 0, 0, 9, 0, 10, 0, 0, 0], 
# 		[0, 0, 4, 14, 10, 0, 2, 0, 0], 
# 		[0, 0, 0, 0, 0, 2, 0, 1, 6], 
# 		[8, 11, 0, 0, 0, 0, 1, 0, 7], 
# 		[0, 0, 2, 0, 0, 0, 6, 7, 0] 
# 		] 
# node = 4
# time = 0.2
# density=[
#         [0, 40, 0, 0, 0, 0, 0, 80, 0], 
# 		[40, 0, 80, 0, 0, 0, 0, 110, 0], 
# 		[0, 80, 0, 70, 0, 40, 0, 0, 20], 
# 		[0, 0, 70, 0, 90, 140, 0, 0, 0], 
# 		[0, 0, 0, 90, 0, 1000, 0, 0, 0], 
# 		[0, 0, 40, 140, 1000, 0, 20, 0, 0], 
# 		[0, 0, 0, 0, 0, 20, 0, 10, 60], 
# 		[80, 110, 0, 0, 0, 0, 10, 0, 70], 
# 		[0, 0, 20, 0, 0, 0, 60, 70, 0] 
#         ]

g.dijkstra(graph,node) 

removelink(1,2)
print()
g.dijkstra(graph,node)