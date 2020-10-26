#########################################################################################
#
#   File:       bellmanford-floydwarshall.py
#   Author:     David Weber (dwebe003)
#   Date:       6/05/2017
#   Version:    1.0
#
#   Algorithms: Bellman-Ford Algorithm
#               Floyd-Warshall Algorithm
#
#   Contents:   This program implements two 'shortest path' algorithms given a graph G
#               of vertices connected by (u,v) edges. The Floyd-Warshall constructs a
#               uxv matrix with each entry being the shortest distance from u to v.
#               The Bellman-Ford algorithm is a single-source shortest path algorithm
#               that calculates the shortest path from a source vertex s to every
#               other other vertex in the graph. By implementing the single-source
#               function on each vertex, it accomplishes the same as the Floyd-Warshall
#               but not nearly as efficient.
#
#########################################################################################

import sys
import re
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]
E=[]
pathPairs = []

#
# initializes array of vertices, edges, matrix E, and set of pairs
#

###########################################################################################################################

def BellmanFord(G):
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    
    #initializes diagonal of E to 0 and prints the matrix
    print "\nOriginal: "
    for i in range(len(vertices)):
        E[i][i] = 0
        print E[i]
    
    #Utilizes Single-Source BellmanFordSS(G, s) function for each vertex 0, 1, ..., n
    print "\nResult: "
    for i in range(len(vertices)):
        x = BellmanFordSS(G, i)
        E[i] = x[0]
    
    #for numVertices, for numVertices
    for u in range(len(vertices)):
        for v in range(len(vertices)):
            if x[0][v] > x[0][u] + float(E[u][v]):
                return false
            else:
                pathPairs.append( ((u, v), E[u][v]) )

    print "\npathPairs: "
    for i in pathPairs:
        print(i)
    
    return pathPairs

###########################################################################################################################

def BellmanFordSS(G, s):
    
    #initialize source to 0, all other entries to INF
    d = []
    for i in range(len(vertices)):
        d.append(float("inf"))
    d[s] = 0
    
    #Bellman-Ford algorithm implementation
    for i in range(len(vertices) - 1):
        for u in range(len(vertices)):
            for v in range(len(vertices)):
                
                if d[v] > d[u] + float(E[u][v]):
                    d[v] = d[u] + int(E[u][v])


    print d
    return d, pathPairs

###########################################################################################################################

def FloydWarshall(G):
    
    pathPairs=[]
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    
    #initializes diagonal to 0 and prints matrix
    print "\nOriginal: "
    for i in range(len(vertices)):
        edges[i][i] = 0
        print edges[i]
    
    #Floyd-Warshall algorithm implementation
    for k in range(len(vertices)):
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                
                if edges[i][k] == float("inf") or edges[k][j] == float("inf"):
                    continue
                
                if edges[i][j] > float(edges[i][k]) + float(edges[k][j]):
                    edges[i][j] = int(edges[i][k]) + int(edges[k][j])
            #end for
        #end for
    #end for


    #this prints the matrix
    print "\nResult: "
    for i in range(len(vertices)):
        print edges[i]

    #this populates pathPairs with every vertex pair (i.e. edge) along with its weight.
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            pathPairs.append( ((i, j), edges[i][j]) )

    print "\npathPairs: "
    for i in pathPairs:
        print(i)

    return pathPairs

###########################################################################################################################

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    
    #open file, read in line
    inFile=open(filename,'r')
    line1=inFile.readline()
    
    #graphMatch will be true if format of input is correct (i.e. 2 numbers)
    graphMatch=graphRE.match(line1)
    
    #if false, print error, quit
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    
    #creates list with index i=0, 1,..., n based on first number (i.e. # elements)
    vertices=list(range(int(graphMatch.group(1))))

    edges=[]

#constructs matrix of INF.
    #i = 0, 1, 2, 3
    for i in range(len(vertices)):
        
        row=[]
        
        #j = 0, 1, 2, 3
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
        E.append(row)

#Fills in matrix with weight values (if any)
    for line in inFile.readlines():
        line = line.strip()
        
        #makes sure 3 numbers supplied
        edgeMatch=edgeRE.match(line)
        
        if edgeMatch:
            #source vertices
            source=edgeMatch.group(1)
            
            #destination verticies
            sink=edgeMatch.group(2)
            
            if int(source) >= len(vertices) or int(sink) >= len(vertices):
                print "Attempting to insert an edge between ", source, " and ", sink, " in a graph with ", len(vertices), " vertices"
                quit(1)
            #weights
            weight=edgeMatch.group(3)
            
            edges[int(source)][int(sink)]=int(weight)
            E[int(source)][int(sink)]=int(weight)

    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

###########################################################################################################################

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    s = float("inf")
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        FloydWarshall(G)
        start=time.clock()
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
