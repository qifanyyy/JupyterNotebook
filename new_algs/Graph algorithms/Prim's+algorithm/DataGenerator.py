# Matthew P. Burruss
# 4/12/2019
# CS 5250

import random
import math

# Adjacency list class for graphs with weighted, undirected edges
class Adjacency_List:
    # initialize a simple adjacency list.
    # Requires vertices are known at init
    def __init__(self,vertices,edges):
        self.adj = [[] for i in range(len(vertices))]
        self.vertices = vertices
        self.edges = edges
        for edge in edges:
            self.adj[edge.u].append((edge.v,edge.weight))
            self.adj[edge.v].append((edge.u,edge.weight))
    # add an edge to the adjacency list
    def addEdge(self,edge):
        self.edges.append(edge)
        self.adj[edge.u].append((edge.v,edge.weight))
        self.adj[edge.v].append((edge.u,edge.weight))
    # print adjacency list and associated edges
    def printMe(self):
        node = 0
        for list in self.adj:
            print("%d:" %node,end='')
            node = node + 1
            for edge in list:
                print(" (%d:%0.2f)" % (edge[0],edge[1]),end='')
            print('')
    # return a specified neighbor of vertex u and that edge's weight
    def adjacentTo(self,u,index):
        # returns neighbor,weight
        return self.adj[u][index][0],self.adj[u][index][1]
    # return the number of neighbors vertex u
    def numberOfNeighborsTo(self,u):
        return len(self.adj[u])
    #get number of vertices
    def getNumberOfVertices(self):
        return len(self.vertices)
    # get array representation of all edges and vertices
    def getEdges(self):
        return self.edges
    def getVertices(self):
        return self.vertices

# undirected weighted edge between vertex u and v with specified weight
class Edge:
    def __init__(self,u,v,weight):
        self.u = u
        self.v = v
        self.weight = weight
    def printMe(self):
        print("edge:(" + str(self.u) + "--" + str(self.v) + ") with weight " + str(self.weight))

# Used to generate the data for the graphs
class DataGenerator:
    # PARAMETERS
    # n = number of vertices
    # p = probability of edge between any two vertices
    # method = select method of data generation
    # weightMax = sets weight for method 1
    # xlim = 0...xlim marks boundary of x axis for method 2
    # ylim = 0...xylim marks boundary for y axis for method 2 and with xlim defines plane
    # seed = random seed

    # There is also a seed that you can choose
    """
    Generate random data sets on reasonble size inputs as follows. Decide
    whether x is adjacent to y is by picking a random number in the range 1-10k, 
    and making these adjacent if the randum number is less than or equal to k.

    For these edges, generate edge weights in 2 different ways. In method 1, edge 
    weights are random numbers over the range 1..n, In the other, points 
    are placed randomly on the plane, and the edges are the distance between these 
    points.

    Your writeup should compare the performance of each of the algorithms on the
    data, and make appropriate conclusions.
    """
    def __init__(self,n,p,method=1,weightMax = 30,xlim=100,ylim=100,seed = 3141):
        self.n = n
        self.p = p
        self.method = method
        self.weightMax = 30
        self.xlim = xlim
        self.ylim = ylim
        random.seed(seed)
    # call this to return a MST tree
    def generateData(self):
        if (self.method == 1):
            return self.method1()
        elif(self.method == 2):
            return self.method2()
        else:
            print("Method not defined")
            return Adjacency_List([],[])

    def method1(self):
        vertices = []
        for i in range(self.n):
            vertices.append(i)
        edges = []
        for i in range(self.n):
            for j in range(i+1,self.n):
                randomNumber = random.randint(1,10001)
                if (randomNumber <= self.p*10000):
                    randomWeight = random.randint(1,self.weightMax+1)
                    edges.append(Edge(i,j,randomWeight))
        return Adjacency_List(vertices,edges)

    def method2(self):
        vertices = []
        x = [] 
        y = []
        for i in range(self.n):
            vertices.append(i)
            x.append(random.randint(1,self.xlim+1))
            y.append(random.randint(1,self.ylim+1))
        edges = []
        for i in range(self.n):
            for j in range(i+1,self.n):
                randomNumber = random.randint(1,10001)
                if (randomNumber <= self.p*10000):
                    weight = math.sqrt((x[i]-x[j])**2 +(y[i]-y[j])**2)
                    edges.append(Edge(i,j,weight))
        return Adjacency_List(vertices,edges)
