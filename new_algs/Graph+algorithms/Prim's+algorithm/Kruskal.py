# Matthew P. Burruss
# 4/12/2019
# CS 5250

import math
from DataGenerator import Adjacency_List,Edge,DataGenerator

class UnionFind:
    # init
    # create |vertices| trees each with a single item and size 1
    def __init__(self,numVertices):
        # initialize n trees
        self.trees = []
        for i in range(numVertices):
            self.trees.append(Node(i,None))
    # find() operation takes O(logn) time
    # given a node i, follow it to its root and return root
    # implement tree compression which doubles the time of find
    def find(self,i):
        path = []
        root = self.trees[i].getRoot(path)
        for nodes in path:
            nodes.parent = root
        return root
    # union() operation takes O(1) time
    # if size of setX < size of setY, make y point to x
    # keep track of rank or height
    def union(self,rootX,rootY,edge,MST):
        MST.addEdge(edge)
        if (rootX.rank <= rootY.rank):
            rootY.makeChildOf(rootX)
            rootY.rank = rootY.rank+1
        else:
            rootX.makeChildOf(rootY)
            rootX.rank = rootX.rank+1

class Node:
    def __init__(self,vertex,parent):
        self.vertex = vertex # vertex of node
        self.parent = parent # parent of node
        if (parent == None):
            self.rank = 1   # if root, set level of node to 1
        else:
            self.rank = self.parent.rank + 1 # if not root, set level to parent level + 1
    def getRoot(self,path):
        if (self.parent == None): # we are root, return self
            return self
        else:
            path.append(self)
            root = self.parent.getRoot(path) # climb up tree to find root node
            return root
    def printMeUpToParent(self):
        if (self.parent == None):
            return
        else:
            print(str(self.vertex)+ "--",end='')
            self.parent.printMeUpToParent()
    def makeChildOf(self,parent):
        self.parent = parent

# takes an array of Edge objects and returns sorted version
# runs in mlogn
def mergeSort(edges,low,high):
    if (low < high):
        middle = low+(high-low)/2
        mergeSort(edges,int(low),int(middle))
        mergeSort(edges,int(middle+1),int(high))
        merge(edges,int(low),int(middle),int(high))
def merge(edges,low,middle,high):
    left = middle - low + 1
    right = high - middle
    # create tmp arrays
    left_array = []
    right_array = []
    for i in range(left):
        left_array.append(edges[low+i])
    for j in range(right):
        right_array.append(edges[middle+1+j])
    i = j = 0
    k = low
    while(i < left and j < right):
        if (left_array[i].weight <= right_array[j].weight):
            edges[k] = left_array[i]
            i = i +1
        else:
            edges[k] = right_array[j]
            j = j +1
        k = k +1
    # copy remaining
    while(i < left):
        edges[k] = left_array[i]
        i = i +1
        k = k +1
    while(j < right):
        edges[k] = right_array[j]
        j = j +1
        k = k +1

# takes in an adjacency list and vertices
# Psuedo
# Sort edges increasing: O(|E|log|E|) 
# Look at every edge in sorted list: O(|E|)
#   select next smallest edge O(1)
#   see if vertex u and vertex v on different components (find(u) != find(v)): 2m times of log(|V|)
#       combine sets: union(u,v): n-1 unions of O(1) time
# Total running time
# ElogE + 2|E|log|V|~= ElogV

# However, because tree compression was acheived, it runs in O(|E|*alpha(|V|)) where
# alpha(|V|) is the inverse Ackermann function
def Kruskal(Adj):
    # initialize array for kruskal
    MST = Adjacency_List(Adj.getVertices(),[])
    # initialize union find
    UF = UnionFind(Adj.getNumberOfVertices())
    # initialize array to keep track of what's been added
    # sort edges of input
    edges = Adj.getEdges()
    mergeSort(edges,0,len(edges)-1) # takes |E|log|E|
    for edge in edges:
        #edge.printMe()
        setX = UF.find(edge.u)
        setY = UF.find(edge.v)
        if (setX.vertex != setY.vertex):
            UF.union(setX,setY,edge,MST)
    return MST


if __name__ == '__main__':
    print("##########################")
    print("Original Adjacency list")
    print("##########################")
    dg = DataGenerator(100,0.1,method = 2)
    G = dg.generateData()
    G.printMe()
    MST = Kruskal(G)
    # print MST
    print("##########################")
    print("MST: Kruskal Algorithm")
    print("##########################")
    MST.printMe()