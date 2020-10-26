# Python libraries to use
from time import time
from array import *
from copy import deepcopy
from random import randint, choice, shuffle

# Get minimum paths for all pairs
def FloydWarshall(edgeMatrix):
    #initialize empty array 
    Paths = newIntegerGraph(N, [])

    #make local copy of edges because it will change throughout the algorithm (want to keep original)
    E = deepcopy(edgeMatrix)
    #for each > = zero degree edge, add path [a, b] to pathMatrix
    for a in range(0, N):
        for b in range(0, N):
            if (E[a][b] >= 0):
                Paths[a][b].append(a+1)
                if a != b:
                    Paths[a][b].append(b+1)

    #for each inclusion-candidate node D...
    for D in range(0, N):
        #go through and change matrix:
        #(Don't do this on any paths from a to D or D to b)
        operatingEdges = [f for f in range(0, N) if f != D]
        for a in operatingEdges:
            for b in operatingEdges:
                #- if path between a and b can be improved by going through n, update the spot
                #- skip the case where the path with node D included is infinity (using -1 as infinity)
                if not (a == b or E[a][D] == -1 or E[D][b] == -1):
                    withNode = E[a][D] + E[D][b]
                    if (E[a][b] > withNode) or (E[a][b] == -1):
                        E[a][b] = withNode
                        #-update path for a:b, using saved values for a:D, and D:b
                        Paths[a][b] = Paths[a][D][:-1] + Paths[D][b] 
          #move on to next D (inclusion-candidate node)

    return Paths, E

def GetEdgeLoads(originalEdgeWeights, minPaths, Flows):

    Loads = newIntegerGraph(N, 0)

    #using the flow for each edge pair, calculate individual edge Loads.
    for i in range(0, N):
        for j in range(0, N):
            if (i+1, j+1) in Flows:
                #for each edge in the path, add the flow
                for k in range(0, len(minPaths[i][j]) - 1):
                    a = minPaths[i][j][k] - 1
                    b = minPaths[i][j][k+1] - 1
                    Loads[a][b] += Flows[(i+1, j+1)]
            if originalEdgeWeights[i][j] == -1:
                if Loads[i][j] != 0:
                    print("Load found for nonexistent edge! Details: ", i+1, ":", j+1, minPaths[i][j])
                Loads[i][j] = -1

    return Loads

def GetPathHopLengths(Paths):
    hops = newIntegerGraph(N, -1)
    
    for i in range(0, N):
        for j in range(0, N):
            hopCount = len(Paths[i][j])
            hops[i][j] = hopCount - 1
    return hops

# Generate Graph and Flows based on a percentage of "flowiness" and density
# where complete "flowiness" has a flow amount from each node to every other node
# So for 100 percent, there are N*(N-1) flows.
def GenerateTestData(size, density, flowiness):
    global N
    N = size
    Matrix = newIntegerGraph(size, -1)
    Flows = dict()
    nodes = list(range(1, N+1))
    shuffle(nodes)

    Matrix[nodes[N-1]-1][nodes[0]-1] = randint(1, 10)
    for i in range(0, N-1):
        Matrix[nodes[i]-1][nodes[i+1]-1] = randint(1, 10)
    
    edgesAdded = 0
    while edgesAdded < int((N*(N-1))*density):
        i = randint(0, N-1)
        j = randint(0, N-1)
        if i!= j:
            if Matrix[i][j] == -1:
                Matrix[i][j] = randint(1, 20)
                edgesAdded += 1
            
    flowsAdded = 0
    while flowsAdded < int((N*(N-1))*flowiness):
        i = randint(1, N)
        j = randint(1, N)
        
        if i != j:
            if not ((i, j) in Flows):
                Flows[(i, j)] = randint(1, 10)
                flowsAdded += 1
    return Matrix, Flows

# File input function - returns edge weight matrix and a Flows map, with nodes (a, b) as keys.
def ReadDataFromFile(file):
    global N
    firstLine = file.readline().split(",")
    N, start, end = int(firstLine[0].strip()), int(firstLine[1].strip()), int(firstLine[2].strip())

    Matrix = newIntegerGraph(N)
    Flows = dict()

    for L in file:
        L = L.strip()
        if L != "":
            items = L.split(",")
            type = items[0].strip()
            from_node = int(items[1].strip())
            to_node =  int(items[2].strip())
            quantity = int( items[3].strip())
            if type == "E":
                Matrix[from_node-1][to_node-1] = quantity
            elif type == "F":
                Flows[(from_node, to_node)] = quantity
    return Matrix, Flows, start, end

# Get the min or max edge of each path, by traffic
def GetPathEdgeMinMax(Paths, Loads, type):

    MinMaxEdges = newIntegerGraph(N, [])
    MinMaxVals = newIntegerGraph(N, -1)

    for i in range(0, N):
        for j in range(0, N):
            cmp = -1
            for k in range(0, len(Paths[i][j]) - 1):
                a = Paths[i][j][k] - 1
                b = Paths[i][j][k+1] - 1
                if type == "min":
                    if Loads[a][b] < cmp or cmp == -1:
                        cmp = Loads[a][b] 
                        MinMaxVals[i][j] = cmp
                        MinMaxEdges[i][j] = [a+1,b+1]
                elif type == "max":
                    if Loads[a][b] > cmp:
                        cmp = Loads[a][b]
                        MinMaxVals[i][j] = cmp
                        MinMaxEdges[i][j] = [a+1,b+1]
    return MinMaxEdges, MinMaxVals

# Get the average Traffic per edge for each path
def GetPathEdgeAvg(PathHops, PathWeights):

    Avgs = newIntegerGraph(N, [])
    for i in range(0, N):
        for j in range(0, N):
            totalWeight = PathWeights[i][j]
            numHops = PathHops[i][j]
            if numHops > 0 and totalWeight >= 0:
                Avgs[i][j] = round(totalWeight/numHops, 3)
            else:
                Avgs[i][j] = -1
    return Avgs

# Print utility function
def prettyMatrix(M, colWidth = 15):
    s = "\n"
    for i in range(0, N):
        line = []
        for j in range(0, N):
            if M[i][j] == -1:
                line.append("-")
            else:
                line.append(str(M[i][j]))
        s += (("{: >"+ str(colWidth)+"}") * N).format(*line) + "\n"
    return s

# Utility function for empty array list (for integers) or List of dynamic Lists (for paths)
def newIntegerGraph(size, default = -1):    
    G = []
    for i in range(0, size):
        if default == []:
            row = []
            for j in range(0, size):
                row.append([])
            G.append(row)
        else:
            G.append(array('i', [default]*size))
            G[i][i] = 0
    return G

# Function for timing the algorithm on a range of N sizes
def functionTimer(startN, endN, increment):

    #create results file
    outf = open("results.txt", "w")

    for GraphSize in range(startN, endN, increment):
        t1 = time()
        EdgeWeights, Flows = GenerateTestData(GraphSize, 0.3, 0.3)
    
        MinWeightPaths, MinPathWeights = FloydWarshall(EdgeWeights)
        SneakyPaths, TrafficEncountered = FloydWarshall(Loads)
        SneakyPathHops = GetPathHopLengths(SneakyPaths)
        t2= time()

        print("size: ", GraphSize, " - Full time elapsed: ", t2-t1)
        outf.write(str(GraphSize) + ", " + str(round((t2-t1)*1000, 4)) + "\n")


##### MAIN SECTION ############

Data = open("Input6.txt")
EdgeWeights, Flows, Start, End = ReadDataFromFile(Data)
Data.close()

Start = Start - 1
End = End - 1

MinWeightPaths, MinPathWeights = FloydWarshall(EdgeWeights)
#print("Minimum Paths by Edge Weight (Distance): ", prettyMatrix(MinWeightPaths))
#print("Minimum Path Weights: ", prettyMatrix(MinPathWeights, 7))

MinWeightHops = GetPathHopLengths(MinWeightPaths)
#print("Hops for these paths (number of edges): ", prettyMatrix(MinWeightHops, 7))

Loads = GetEdgeLoads(EdgeWeights, MinWeightPaths, Flows)
#print("Edge Loads: ", prettyMatrix(Loads, 7))

SneakyPaths, TrafficEncountered = FloydWarshall(Loads)
print("Sneaky Path from ", Start+1, " to ", End+1, ": ", SneakyPaths[Start][End])
print("Traffic encountered on Sneaky Path: ", TrafficEncountered[Start][End])

SneakyPathHops = GetPathHopLengths(SneakyPaths)
print("Hops for this path (number of edges): ", SneakyPathHops[Start][End])

MinEdgesOnSneakyPath, MinValsOnSneakyPath = GetPathEdgeMinMax(SneakyPaths, Loads, "min")
print("Edge on Sneaky Path with lowest number of cars: ", MinEdgesOnSneakyPath[Start][End])
print("Traffic on this Edge: ", MinValsOnSneakyPath[Start][End])

MaxEdgesOnSneakyPath, MaxValsOnSneakyPath = GetPathEdgeMinMax(SneakyPaths, Loads, "max")
print("Edge on Sneaky Path with highest number of cars: ", MaxEdgesOnSneakyPath[Start][End])
print("Traffic on this Edge: ", MaxValsOnSneakyPath[Start][End])

AvgEdgesOnSneakyPath = GetPathEdgeAvg(SneakyPathHops, TrafficEncountered)
print("Avg number of cars per hop: ", AvgEdgesOnSneakyPath[Start][End])

   
