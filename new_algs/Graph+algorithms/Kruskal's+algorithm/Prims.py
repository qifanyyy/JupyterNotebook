# Matthew P. Burruss
# 4/4/2019
# CS 5250



import math
from DataGenerator import Adjacency_List,Edge,DataGenerator
# the elements of the minheap have a key-value pair
# the elements are sorted by the value and the key corresponds to 
# the vertex #
# the key-value pair represented by a tuple (vertex #, value)
class minHeapPrim():
    # initializes a minHeap where root (first node)
    # has value 0 and rest have value inf
    # Run-time of heapify: O(n)
    def __init__(self,vertices):
        self.list = []
        self.positions = [] # keeps track of vertex location in heap
        self.parents = []
        self.size = len(vertices)
        # list is indexed by vertex # and contains tuple (key value, index in heap)
        for i in range(len(vertices)):
            if (i == 0):
                self.list.append((0,0))
                self.positions.append(0)
                self.parents.append(-1)
            else:
                self.list.append((i,math.inf))
                self.positions.append(i)
                self.parents.append(-1)
        #self.printMe()
        self.totalCost = 0
    def printMe(self):
        for i in range(self.size):
            print("(v="+str(self.list[i][0])+" w=" + str(self.list[i][1])+") ",end='')
        print('')

    def setParent(self,vertex,parent):
        self.parents[vertex] = parent

    # returns smallest vertex-value pair and then restores heap O(lgn)
    def getMinNode(self,MST,addedVertices):
        smallest = self.list[0][0]
        #print mst
        if (self.parents[smallest] != -1 and addedVertices[smallest] == 0):
            MST.addEdge(Edge(self.parents[smallest],smallest,self.list[0][1]))
            addedVertices[smallest] = 1
        self.list[0] = self.list[self.size-1]
        self.positions[smallest] = -1
        self.positions[self.list[0][0]] = 0
        self.size = self.size - 1
        self.minHeapify(0)
        return smallest

    # takes O(logn)
    def minHeapify(self,index):
        # compare to children
        smallest = index
        # compare to children
        if (2*index + 1 < self.size and self.list[smallest][1] > self.list[2*index + 1][1]):
            smallest = 2*index + 1
        if (2*index + 2 < self.size and self.list[smallest][1] > self.list[2*index + 2][1]):
            smallest = 2*index + 2
        # stop if position found
        if (smallest != index):
            # swap elements in heap
            tmp = self.list[index]
            self.list[index] = self.list[smallest]
            self.list[smallest] = tmp
            # swap positions
            othervertex = self.list[smallest][0]
            myvertex = self.list[index][0]
            tmp = self.positions[myvertex]
            self.positions[myvertex] = self.positions[othervertex]
            self.positions[othervertex] = tmp
            # call heapify on smallest again
            self.minHeapify(smallest)

    # takes logn
    def decreaseKeyValue(self,index,vertex):
        positionFound = False
        while (not positionFound):
            # compare to parent
            parentWeight = self.list[int((index-1)/2)][1]
            parentIndex = int((index-1)/2)
            parentVertex = self.list[int((index-1)/2)][0]
            #print(parentIndex)
            mweight = self.list[index][1]
            if (parentWeight > mweight):
                # swap elements in heap
                tmp = self.list[index]
                self.list[index] = self.list[parentIndex]
                self.list[parentIndex] = tmp
                index = parentIndex
                # swap positions
                tmp = self.positions[vertex]
                self.positions[vertex] = self.positions[parentVertex]
                self.positions[parentVertex] = tmp
            else:
                positionFound = True


    # checks if list is empty
    # run-time is O(1)
    def isEmpty(self):
        return self.size == 0

    # returns the weight of an item in the list
    # run-time is O(1)
    def getWeight(self,vertex):
        return self.list[self.positions[vertex]][1]

    def updateHeap(self,vertex,weight):
        index = self.positions[vertex]
        self.list[index] = (vertex,weight)
        # bubble the index up
        self.decreaseKeyValue(index,vertex)
        

# takes in an adjacency list and vertices
# steps of algorithm that uses min heap to keep track of smallest distance connecting
# MST to nodes yet to be added to MST
# 1. Create a min heap of |V| with key value assigned
# inf to all nodes except node 0 (keyvalue = 0)
# 2. repeat
# 3.    find min value of node from min heap
# 4.    check all neighbors and see if not in T yet
# 5.    if not in T and weight > min node - itself, update

def Prim(Adj):
    # initialize array for prim
    vertices = Adj.getVertices()
    MST = Adjacency_List(vertices,[])
    # initialize array to keep track of what's been added
    addedVertices = [0 for i in range(len(vertices))]
    # create a heap... operation O(n)
    minheap = minHeapPrim(vertices)
    # while heap not empty... O(n)
    while(not minheap.isEmpty()):
        u = minheap.getMinNode(MST,addedVertices) # remove smallest (root) O(1) and add to MST if not there
        # update all neighbors of u
        for i in range(Adj.numberOfNeighborsTo(u)): # Check all neighbors in MST
            neighbor,weight = Adj.adjacentTo(u,i)
            # if neighbor not in MST and key > weight to MST
            if (addedVertices[neighbor] == 0 and minheap.getWeight(neighbor) > weight): # get weight and check if already added O(1)
                # update weight
                minheap.setParent(neighbor,u) # update parent O(1)
                minheap.updateHeap(neighbor,weight) # update heap O(lgn)
    return MST


if __name__ == '__main__':
    print("##########################")
    print("Original Adjacency list")
    print("##########################")
    dg = DataGenerator(100,0.1,method = 2)
    G = dg.generateData()
    G.printMe()
    MST = Prim(G)
    # print MST
    print("##########################")
    print("MST: Prim's Algorithm")
    print("##########################")
    MST.printMe()