
from operator import itemgetter
from Graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
import json

## finds the minimum spanning tree by KRUSKAL
def KRUSKAL(g):
    parent = {} 
    MST = Graph()
    
    for key,value in g.vertices.items():
        MST.addVertex(key,value[0],value[1])
        parent[key] = key #MAKE - SET (v)
    
    edges =list(g.edges)
    edges.sort(key=itemgetter(2)) ## by w - > (v,u,w) 
    
    for v,u,w in edges:
        if findParent(parent,v) != findParent(parent,u):
            MST.addEdge(v,u,w)
            union(parent,v,u)

    return MST

## makes the parent of v to u 
def union(parent,v,u):
    parentV = findParent(parent,v)
    parentU = findParent(parent,u) ##
    if parentV != parentU:
        parent[parentU] = parentV ## Does not matter who will be the parent 
    
# finds the parent of v in the parent list
def findParent(parent,v):

    if parent[v] != v :
        return findParent(parent,parent[v])
    else:
        return v

# 
def Christofides(g,root):
    MST = KRUSKAL(g);     

    MWPM = mimumWeightPerfectMatching(g,MST); 
    
    multiGraph = graphUnion(MST,MWPM)

    eulerianCircut = formEulerCircut(multiGraph,root); 
 
    hamlitonianCircut = formHamiltonianCircut(eulerianCircut)
 
    TSP_Graph = finalTSPgraph(hamlitonianCircut,g.weights)

    return TSP_Graph[0], TSP_Graph[1] , hamlitonianCircut


def finalTSPgraph(hPath, weights):
    
    TSP_graph = nx.Graph();
    cost = 0; 

    for i in range(len(hPath)-1):
        v = hPath[i]
        u = hPath[i+1]
        w = weights[(u,v)]
        cost+= w; 
        TSP_graph.add_edge(hPath[i],hPath[i+1], weight = w)

    return TSP_graph,cost
## every vertex of the graph is incident to exactly one edge of the matching
def mimumWeightPerfectMatching(g,MST):
    odds = findOdds(MST)
    minWeightPM = Graph() ## minWeightPM : Mim Weight Perfect Matching
    minWeightPM.vertices = g.vertices
    minWeightPM.weights = g.weights
    while len(odds) > 0: ## While not empty
        v = odds.pop()
        minimum = float("inf") ## Closest at first is infinity
        for u in odds: ## Find closest Vertex to v
            if( (v,u) not in g.weights):
                continue; 
            if g.weight(v,u) < minimum: ## if closest
                minimum = g.weight(v,u)
                closest = u ## set closest <- u
          
        minWeightPM.addEdge(closest,v,minimum) ## add edge between it's closest neighbor
        odds.remove(closest)
  
        
    return minWeightPM




#counts the degree of each vertex and returns the odd vertrices.
def findOdds(g):
    oddVertices = []
    
    vertrices = g.vertices
    edges = g.edges

    counts = {} ##

    for v in vertrices:
        counts[v] = 0; 

    for v,u,w in edges:
        counts[v] += 1
        counts[u] += 1

    for v in counts:
        if(counts[v] %2 == 1):
            oddVertices.append(v)
    return oddVertices

# with help of networkx library, it unites matching and spanning tree to give us a multiGraph (allows multiple edges)
def graphUnion(g1,g2):
    multiGraph = nx.MultiGraph();
    vertices1 = g1.vertices
    vertices2 = g2.vertices

    for v,u,w in g1.edges:
            multiGraph.add_edge(v,u,weight = w)

    for v,u,w in g2.edges:
            multiGraph.add_edge(v,u,weight = w)
    
    return multiGraph
        
# path that visits every edge exactly once    
def formEulerCircut(multiGraph,root):

    curVertex = root; 
    stack = [curVertex]
    path = []
    while len(stack) != 0:
        
        curNeighbors = list(multiGraph.neighbors(curVertex)) ## Takes first neighbor as nextVertex 
        if (len(curNeighbors) == 0): ## if curVertex has no neighbouurs 
             path.append(curVertex) ## add it to the path
             curVertex = stack.pop() ## Set last visited vertex as curVertex
             continue;
        nextVertex = curNeighbors[0]; ## take first neighbor as nextVertex 
        multiGraph.remove_edge(curVertex,nextVertex) ## Remove the edge between them
        stack.append(curVertex) 
        curVertex = nextVertex; ## move to the neighbor after deleting the edge.
    return path; 
        

    
# Removes repeated vertices
def formHamiltonianCircut(euler_path):

    TSP_path = []
    visted = set() 
    
    for v in euler_path:
        if(v not in visted):
            TSP_path.append(v)
            visted.add(v)

    TSP_path.append(TSP_path[0])

    return TSP_path
    

# helper....
def readJson(inp):
    g = Graph()
    for v in inp["vl"]:
        
        g.addVertex(v,inp["vl"][v]["x"],inp["vl"][v]["y"])

    for v in  inp["vl"]:
        for u in inp["vl"]:
            if(u != v):
                g.addEdge(v,u)
    return g;

