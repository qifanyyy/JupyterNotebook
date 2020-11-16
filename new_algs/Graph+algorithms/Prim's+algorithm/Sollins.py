# Matthew P. Burruss
# 4/11/2019
# CS 5250

import math
from DataGenerator import Adjacency_List,Edge,DataGenerator

class Node:
    def __init__(self,vertex,parent):
        self.vertex = vertex # vertex of node
        self.parent = parent # parent of node
        self.rank = 1
    def makeChildOf(self,parent):
        self.parent = parent
    def getRoot(self,path):
        if (self.parent == None): # we are root, return self
            return self
        else:
            path.append(self)
            root = self.parent.getRoot(path) # climb up tree to find root node
            return root
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


# Psuedo
# Initialize a forest of |V| trees or components
# Repeat while components greater than 1
#   init array of components to edges of infinity to indicate cheapest edge connecting separate components called cheapEdge[] at most O(V)
#   for each edge (u,v) in G O(E)
#       if u and v are in different components (perform two find operations so 2log(V))
#           If (u,v) < cheapEdge[u]: cheapEdge[u] = (u,v)
#           If (u,v) < cheapEdge[v]: cheapEdge[v] = (u,v)
#   for each component at most O(V)
#       if cheapEdge != 'None': perform two find operations log(V) add edge to MST and merge components with union O(1)

# Therefore, the run-time is O(ELogV) when E > V
def Sollins(Adj):
    # initiallize empty MST
    MST = Adjacency_List(Adj.getVertices(),[])
    # initialize union find interface |V| number of vertices
    UF = UnionFind(Adj.getNumberOfVertices())
    numberOfComponents = Adj.getNumberOfVertices()
    # while there is more than one component
    while (numberOfComponents > 1):
        cheapEdge = []
        # set cheapest edge of each component to INF
        for i in range(Adj.getNumberOfVertices()):
            cheapEdge.append(Edge(-1,-1,math.inf))
        # visit every edge in G
        for edge in Adj.getEdges():
            # see what set each edge belongs to
            setX = UF.find(edge.u)
            setY = UF.find(edge.v)
            if (setX != setY): # see if they belong to the same set
                if (cheapEdge[setX.vertex].weight >= edge.weight): # if the cheapest edge in the setX is greater than this edge, change cheapest edge
                    cheapEdge[setX.vertex] = edge
                if (cheapEdge[setY.vertex].weight >= edge.weight): # same as 2 lines above but for setY
                    cheapEdge[setY.vertex] = edge
        for edge in cheapEdge: # for all 
            if (edge.weight != math.inf):
                setX = UF.find(edge.u)
                setY = UF.find(edge.v)
                if (setX != setY):
                    UF.union(setX,setY,edge,MST)
                    numberOfComponents = numberOfComponents - 1
    return MST


if __name__ == '__main__':
    print("##########################")
    print("Original Adjacency list")
    print("##########################")
    dg = DataGenerator(100,0.1,method = 2)
    G = dg.generateData()
    G.printMe()
    MST = Sollins(G)
    # print MST
    print("##########################")
    print("MST: Sollin's Algorithm")
    print("##########################")
    MST.printMe()