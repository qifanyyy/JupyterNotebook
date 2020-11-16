import os
import re
import sys
import time
import math

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(\\d+)")

def change_edge_matrix (edges):
    for v in range(0 , len(edges)):
        for e in range(0 , len(edges[v])):
            if type(edges[v][e]) is str:
                edges[v][e] = int(edges[v][e])

    return edges

def BellmanFord(G):
    pathPairs=[]
    edges = change_edge_matrix(G[1])

    val_infinity = edges[0][0]
    for n in range(0, len(G[0])): 

        one_node_to_rest = []
        
        # starting initialization here
        first_row = []
        
        for m in range(0, len(G[0])):
            if m == n:
                first_row.append(0)
            else:
                first_row.append(val_infinity)
        
        one_node_to_rest = first_row

        # done with initialization 
       
        for j in range(0, len(G[0])):
        
            if j > 0:
            
                new_row = []
                
                for i in range(0, len(edges)):
                    if i != n:
                        val_assign = one_node_to_rest[i]

                        for k in range(0, len(edges[i])):
                    
                            check_node_weight = edges[k][i]
                            check_node_weight_prev_val = one_node_to_rest[k]

                            if (check_node_weight != val_infinity) and (check_node_weight_prev_val != val_infinity):
                                if check_node_weight + check_node_weight_prev_val < val_assign:
                                        val_assign = check_node_weight + check_node_weight_prev_val
                                            
                        new_row.append(val_assign)

                    else:
                        new_row.append(0)

                one_node_to_rest = new_row
        pathPairs.append(one_node_to_rest)
        
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]

    # initializing here
    pathPairs= change_edge_matrix(G[1])
    for i in range(0, len(G[0])):
    	pathPairs[i][i] = 0

    for k in range(0, len(G[0])):
        for i in range(0, len(pathPairs)):
            for j in range(0, len(pathPairs[i])):
                result = pathPairs[i][k] + pathPairs[k][j]
                
                if result < pathPairs[i][j]:
                    pathPairs[i][j] = result
    return pathPairs

def readFile(filename):
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) >= len(vertices) or int(sink) >= len(vertices):
                print("Attempting to insert an edge between "+str(source)+" and "+str(sink)+" in a graph with "+str(len(vertices))+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)][int(sink)]=weight
    # TODO: Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def writeFile(lengthMatrix,filename):
    filename=os.path.splitext(os.path.split(filename)[1])[0]
    outFile=open('output/'+filename+'_output.txt','w')
    for vertex in lengthMatrix:
        for length in vertex:
            outFile.write(str(length)+',')
        outFile.write('\n')


def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    pathLengths=[]
    if algorithm == 'b' or algorithm == 'B':
        start=time.clock()
        pathLengths=BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))

    if algorithm == 'f' or algorithm == 'F':
        start=time.clock()
        pathLengths=FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Floyd-Warshall timing: "+str(FWTime))
    
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))
    writeFile(pathLengths,filename)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
