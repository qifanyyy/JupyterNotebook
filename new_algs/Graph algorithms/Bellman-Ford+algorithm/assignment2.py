import os
import re
import sys
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(\\d+)")

def BellmanFord(G):
    pathPairs=[]
    d = []

    for a in range(len(G[0])): # update every source node
        for b in range(len(G[0])):
            d.append(float("inf"))
        d[a] = 0
        for c in range(1, len(G[0])-1):
            for e in range(len(G[0])): #iterate nodes to find possible edges
                for f in range(len(G[0])):
                    if float(G[1][e][f]) < float("inf"): #This checks to see if an edge exists
                        if d[f] > d[e] + float(G[1][e][f]): #Then is checks to see if there is a better value
                            d[f] = int(d[e]) + int(float(G[1][e][f]))
        pathPairs.append(d)
        d = []
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs will contain a matrix of path lengths:
    #    0   1   2 
    # 0 x00 x01 x02
    # 1 x10 x11 x12
    # 2 x20 x21 x22
    # Where xij is the length of the shortest path between i and j
   
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    d = []
    
    for a in range(len(G[0])): # update every node to be inf
        drow = []
        for b in range(len(G[0])):
            drow.append(float("inf"))
        d.append(drow)
            
    for c in range(len(G[0])):
        for e in range(len(G[0])):
            if c == e:
                d[c][c] = 0
            elif float(G[1][c][e]) < float("inf"):
                d[c][e] = int(float(G[1][c][e]))
            else:
                d[c][e] = float("inf")
                
    for c in range(len(G[0])):
        for a in range(len(G[0])):
            for b in range(len(G[0])):
                if d[a][b] < d[a][c] + d[c][b]:
                    d[a][b] = d[a][b]
                else:
                    d[a][b] = d[a][c] + d[c][b]
    pathPairs.append(d)
    print(d)
    # Fill in your Floyd-Warshall algorithm here
    # The pathPairs will contain a matrix of path lengths:
    #    0   1   2 
    # 0 x00 x01 x02
    # 1 x10 x11 x12
    # 2 x20 x21 x22
    # Where xij is the length of the shortest path between i and j
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

    return (vertices,edges)

def writeFile(lengthMatrix,filename):
    filename=os.path.splitext(os.path.split(filename)[1])[0]
    outFile=open('output/'+filename+'_output.txt','w+')
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
        pathLengths=BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        pathLengths=FloydWarshall(G)
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
    writeFile(pathLengths,filename)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
