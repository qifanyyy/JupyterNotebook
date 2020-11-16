from adjacencymatrix import *
from minheap import *

class dijkstra:
    def __init__(self, am, nv):
        self.numVertices = nv
        self.priorityQueue = binaryHeap()
        self.visited = []
        self.distances = []
        self.parent = [-1] * self.numVertices
        self.adjacencyMatrix = am
        
    def run(self, start):
        minNode = None
        #Set all node distances to infinity - each index of list = node number
        for i in range(0, self.numVertices):
            self.distances.append(math.inf)
        #Set start node distance to zero
        self.distances[start] = 0
        
        #Make priority queue with all vertices contained in it
        for i in range(0, len(self.distances)):
            self.priorityQueue.insertKeyValue(self.distances[i], i)
            self.parent.append(None)
        while not self.priorityQueue.isEmpty():
            minNode = self.priorityQueue.popMin()
            self.visited.append(minNode.value)
            neighbors = self.adjacencyMatrix.findNeighbors(minNode.value)
            for neighbor in neighbors:
                if neighbor[1][1] not in self.visited and self.distances[neighbor[1][1]] > minNode.key + neighbor[0]:
                    self.distances[neighbor[1][1]] = minNode.key + neighbor[0]
                    self.priorityQueue.decreaseKey(minNode.key + neighbor[0], neighbor[1][1])
                    self.parent[neighbor[1][1]] =  minNode.value

    #Print the constructed distance list
    def displaySolution(self):
        src = 0
        print("Vertex \t\tDistance from Source\tPath")
        print("src -> dest")
        for i in range(1, len(self.distances)):
            print("\n%d -> %d \t\t%d \t\t\t" % (src, i, self.distances[i]), end=' ')
            self.displayPath(self.parent,i)

    #Print shortest path from source to j using parent list
    def displayPath(self, parent, j):
        if parent[j] == -1:
            print(j, end=' ') 
            return
        self.displayPath(parent , parent[j])
        print(j, end=' ')
             
     
    
