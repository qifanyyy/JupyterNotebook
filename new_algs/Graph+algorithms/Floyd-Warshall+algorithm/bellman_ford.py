import sys
import re
import time

import itertools # to generate permutations
import math # to use infinity

################################################################################
################################################################################
###
### Bellman-Ford:     'python bellman_ford.py -b input1.txt'
### Floyd-Warshall:   'python bellman_ford.py -bf input1.txt'
### Both:             'python bellman_ford.py -both input1.txt'
###
################################################################################
################################################################################


graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

#################################################################

def BellmanFord(G):
    pathPairs=[]
    # The pathPairs list will contain the list of vertex 
    # pairs and their weights [((s,t),w),...]
    
    print("\nEntered BellmanFord")
    
    # print("")
    # for i in G:
    #     print(i)
    
    V = G[0]
    E = G[1]
    # print("\nV")
    # print(V)
    # print("\nE")
    # print(E)
    # print("\nlength of E")
    # print(len(E))
    
    # # create a list of permutations of V
    # print("\npermutations of V ")
    x = list(itertools.permutations(V,2))
    # for i in x:
    #     print(i)
    
    # to access each permutation, do x[i]
    # to access first element of x[i], do x[i][0]
    # to access second element of x[i], do x[i][1]
    
    # print("\n")
    # print(x[1][1])
    
    inf = float('inf')
        
    
    
    #####################################################
    #####################################################
    #####################################################
    
    for i in range(len(V)):
        
        dist = [inf] * len(V)
        # rotate through each of the vertices 
        # of V
        index = V[i]
        dist[index]=0
        
        # print("\nindex: " + str(index))
        # print("dist before: ")
        # for i in dist:
        #     print(i)
        
        # print("\nlength(x)")
        # print(len(x))
        # print("\n###########################################")
        
        # print("u and v combinations: \n")
        
        # print("|V|")
        # print(len(V))
        # print("\n")
        
        
        for j in range(1, len(V)): # do this |V|-1 times
            # print("\n#################\nj: " + str(j))
            for i in range(len(x)):
                u = x[i][0]
                v = x[i][1]
                # print("u: " + str(u) + "   v: " + str(v))
                # print(u)
                # print("v:")
                # print(v)
                # print("weight: " + str(E[u][v]))
                # print(E[u][v]) #################
                # print("########\n")
                if (dist[v] > dist[u] + float(E[u][v])):
                    dist[v] = dist[u] + float(E[u][v])
        
        # # print("\n")
        # print("\nindex: " + str(index))
        # print("dist after: ")
        # for i in dist:
        #     print(i)
            
        # print("\nChecking if negative cycle exists: ")
        negCycle = False
        for i in range(len(x)):
            u = x[i][0]
            v = x[i][1]
            # print("u: " + str(u) + "   v: " + str(v))
            # print("weight: " + str(E[u][v]))
            # print("########\n")
            if (dist[v] > dist[u] + float(E[u][v])):
                # dist[v] = dist[u] + float(E[u][v])
                negCycle = True
        
            
        for i in range(len(V)):
            # print(i)
            if dist[i] != float('inf'):
                dist[i] = int(dist[i])
            new = ((str(index),str(V[i])),str(dist[i]))
            pathPairs.append(new)
        
        
    #####################################################
    #####################################################
    #####################################################
    
    print("\npathPairs")
    print(pathPairs)
    
    if(negCycle):
        print("\nNote: A negative cycle exists")
    else:
        print("\nNote: No negative cycles exist")
    
    
    # print("\n")
    print("\nExiting BellmanFord\n")
    # print("\n")
    
    
    
    return pathPairs

#################################################################

def FloydWarshall(G):
    pathPairs=[]
    # The pathPairs list will contain the list of vertex 
    # pairs and their weights [((s,t),w),...]
    
    print("\nEntered FloydWarshall")
    
    # print("")
    # for i in G:
    #     print(i)
    
    V = G[0]
    E = G[1]
    # print("\nV")
    # print(V)
    # print("\nE")
    # print(E)
    # print("\nlength of E")
    # print(len(E))
    # print("\nlength of V")
    # print(len(V))
    
    inf = float('inf')
    
    # print("\nV")
    # for i in V:
    #     print(i)
    
    # # Creates a list containing 5 lists, each of 8 items, all set to 0
    # w, h = 4, 4;
    # dist = [[inf for x in range(w)] for y in range(h)] 
    dist = E
    
    for i in V:
        for j in V:
            dist[i][j] = float(dist[i][j])
    
    # print("\ndist")
    # print(dist)
    
    for v in V:
        dist[v][v]=0
    
    # print("\ndist")
    # print(dist)
    
    
    for k in V:
        for i in V:
            for j in V:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # print("\ndist")
    # print(dist)
    
    # print(dist[0][1])
    
    # index = V[i]
    
    # for i in range(len(V)):
    #     # print(i)
    #     new = ( (str(index),str(V[i])) , str(dist[i]) )
    #     pathPairs.append(new)
    
    for i in V:
        for j in V:
            if dist[i][j] != float('inf'):
                dist[i][j] = int(dist[i][j])
            new = ( (str(i), str(j)) , str(dist[i][j]) )
            pathPairs.append(new)
    
    print("\npathPairs")
    print(pathPairs)
    
    print("\nExiting FloydWarshall\n")
    
    return pathPairs

#################################################################

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r') # 'r' mode for reading
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
        
    # print("num vertices: ")
    # print(graphMatch.group(1)) # print num vertices
    # print("num edges: ")
    # print(graphMatch.group(2)) # print num edges
    # print("num both vertices and edges: ")
    # print(graphMatch.group(0)) # print both num vertices and edeges
    
    # creates a list from 0 to (num vertices -1)
    # i.e., if num veritices is 4, creates list from 0 to 3
    vertices=list(range(int(graphMatch.group(1))))
    
    # print("\nvertices: ")
    # print(vertices)
    # print("len(vertices): ")
    # print(len(vertices))
    # print("\n")
    
    # create a list of rows, where each row is a list with
    # 'inf' in it, used to hold the weights from each vertex
    # to the adjacent vertices, where inf means the vertices
    # are not adjacent
    # print("##############################################")
    edges=[]
    for i in range(len(vertices)):
        # print("#######################")
        # print("outer for loop")
        row=[]
        for j in range(len(vertices)):
            # print("#############")
            # print("inner for loop")
            row.append(float("inf"))
            # print("\nrow")
            # print(row)
        edges.append(row)
        # print("\nedges: ")
        # print(edges)
    # print("##############################################")
    # print("\n")
    
    for line in inFile.readlines():
        
        line = line.strip()
        # .strip() removes all whitespace at the start and end, 
        # including spaces, tabs, newlines and carriage returns
        
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            
            # print("\nsource: " + source + "\nsink: " + sink)
            # print("\nsink: " + sink)
            
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            
            weight=edgeMatch.group(3)
            
            
            # tempSource = str(int(source)-1)
            # tempSink = str(int(sink)-1)
            # print("\nint(source)-1:  " + tempSource + "\nint(sink)-1:  " + tempSink)
            
            
            # edges[int(source)-1][int(sink)-1]=weight
            edges[int(source)][int(sink)]=weight
            
    
    # #Debugging
    # for i in vertices:
    #     print(i)
    
    # print("\n")
    
    print("\nvertex    edges")
    for i in range(len(edges)):
        print(str(vertices[i]) + "         " + str(edges[i]))
        # print("            ")
        # print(edges[i])
        # for j in range(0,len(i)):
        #     print(i[j])
        
    print("")    
        
    return (vertices,edges)

#################################################################

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and 
    # a list of the edges in the format ((source,sink),weight)
    
    # G[0] holds the list of vertices [0, 1, 2, 3]
    # G[1] holds the list of edges/weights, so to get vertex 0's edges,
    # type G[1][0], to get the first edge of vertex 0, type G[1][0][0]
    
    # print("\n")  
    
    # print(G[0])
    
    # print("\n")  
    
    # print(G[1][0][0])
    
    # print("\n")  
    
    # for i in G:
    #     print(i)
    
    # print("\nalgorithm: ")
    # print(algorithm)
    
    if algorithm == 'b' or algorithm == 'B':
        # print("\nabout to call BellmanFord")
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        print("\nBellman-Ford timing: "+str(BFTime)+"\n")
        # print("\ncalled BellmanFord\n")
    if algorithm == 'f' or algorithm == 'F':
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Floyd-Warshall timing: "+str(FWTime))
    if algorithm == "both":
        
        print("##############################################")
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        
        print("##############################################")
        
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        
        print("##############################################")
        # print("\n")
        print("\nBellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime)+"\n")
        # print("\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2], sys.argv[1])
    #   (filename   , algorithm  )

#################################################################