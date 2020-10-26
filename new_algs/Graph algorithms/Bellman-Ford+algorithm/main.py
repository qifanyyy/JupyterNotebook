"""
***Note***
The output will be placed within the output.txt file so it is easier to read. 
The dictionaries that will contain the ADT graph data will be found within json files
The program uses a library called mpu that allows a streamlined reading and writing process involving json files.
"""



import pdb
import json
import sys 

#output function that has no return
#it will accept the algorithm data it is outputting and place it into the output file 'output.txt'
def outputDistances(typeOfOutput, dictForOutput, f, source): 
    
    #Printing the type of algorithm 
    print("{" + typeOfOutput, "Distances}", file = f, end = "\n\n")

    string = "|starting location| " + " |ending location| " + "        |distance| "
    print(string, file = f)

    for i in range(len(string)): 
        print("_", file = f, end ="")

    print("\n", file = f)



    #Looping through the distances found in the algorithm 
    for i in output['Distances']: 

        #formatting the ouput
        print(source, end = "   ", file = f)
        print('{:<30}{:>}'.format(i, output['Distances'][i]), end = "\n", file = f)
    
    print("\n\n\n\n", file = f)
        
#Will trace pathways back to the original source via backtracking from the final node to the source node. 
def outputPathways(typeOfOutput, dictForPath, f, source):
    print("{" + typeOfOutput, "Pathways}", file = f, end = "\n\n")

    for i in dictForPath:
        path = [] 
        #Path to", i + ":"
        
        print('{:<32}'.format("path to " + i + ":"), end = " ", file = f)
        j = dictForPath[i]
        path.append(dictForPath[i])
        if (j == None): 
            path.append(None)
        else: 
            while(j != source): 
                path.append(dictForPath[j])
                j = dictForPath[j]
        if(i == source ):
            print ("N/A", file = f, end = "\n")
            continue
        else: 
            for k in reversed(path): 
                print(k, "--->", file = f, end = " ")
            #print("\n", file = f)
        print(i, file = f)
    print("\n\n\n", file = f)

#findMin will find the minimum distanced node definition within the "queue" and return the index of it
#This was necessary to prevent using repeating values
def findMin(queue, dist, graph):
    try: 
        minimumIndex = float('inf')
        maximumName = ""
        for i in queue: 
            if (dist[i] < minimumIndex): 
                minimumIndex = dist[i]
                maximumName = i
        return queue.index(maximumName)
    except: 
        print("Incorrect Source")
        #pdb.set_trace()

#dijkstra's algortihm
def dijkstra(graph,src, dist = {}, previous = {}):
    #initializing the vertecies within the graph
    for vertex in graph: 
        dist[vertex] = float('inf')
        previous[vertex] = None
    
    #setting the source node to zero
    dist[src] = 0

    #initializing the queue
    queue = []
    for i in graph: 
        queue.append(i)
    
    while len(queue) != 0: 
        #pops the minimum value in the q and places it in u
        u = queue.pop(findMin(queue, dist, graph))

        #will check each node connected to the u node
        for neighbor in graph[u]: 
            #checking condition to see how we will organize the queue
            if dist[neighbor] > dist[u] + graph[u][neighbor]:
                dist[neighbor] = dist[u] + graph[u][neighbor]
                previous[neighbor] = u

                #since I used a pseudo-queue, this will represent the decreaseKey(H, v) function
                temp = queue.pop(queue.index(neighbor)) #popping the neighbor into temp
                queue.insert(0, temp) #placing the popped value to the front of the queue

    returningDict = {} #simple dictionary that will hold the return values 

    returningDict['Distances'] = dist #dist key
    returningDict['Previous'] = previous   #previous key

    return returningDict

#Used in the Bellman-Ford algorithm to update the values based on the current edge. 
def updateE (graph, e, dist, previous): 
    if dist[e[1]] > dist[e[0]] + graph[e[0]][e[1]]: 
        dist[e[1]] = dist[e[0]] + graph[e[0]][e[1]]
        previous[e[1]] = e[0]

#Bellman Ford Algorithm
def bellmanFord (graph, edges, src, dist = {}, previous = {}): 

    #initializing values
    for vertex in graph: 
        dist[vertex] = float('inf')
        previous[vertex] = None
    
    #initializing source
    dist[src] = 0

    #Will iterate over the produced list of values mag(V) - 1 or |V| - 1
    for i in range(len(dist) - 1): 
        for e in edges: 
            updateE(graph, e, dist, previous)

    #Creates a returnable dictionary that will be used to print out the findings of the algorithm
    returnDict = {}
    returnDict["Distances"] = dist   #Creates the "distances" section of the returnable key
    returnDict["Previous"] = previous#Creates the previous seciton of the returnable key
    return returnDict

#Simple function that will be used to create a list of n = 2 arrays that will hold the nodes associated with the edges
def initializeEdges(graph): 
    edges = []
    f = open('testingOutput.txt', 'w')
    for i in graph: 
        for u in graph[i]: 
            edges.append((i, u))

    print(edges, file = f)
    return edges

#Used to get user input and check wether the user input is viable
def getUserInput(question): 
    yORn = input(question) 
    yORn = str(yORn.lower())
    while ((yORn != "yes") and (yORn != "no")): 
        yORn = input("Please enter a valid response (yes or no): ")
    return yORn

#Will get a list of all viable nodes in the algorithm so they can be checked against user input. 
def checkingListOfKeys(testGraph): 
    listOfKeys = []
    for i in testGraph: 
        listOfKeys.append(i)
    return listOfKeys



mpuYesOrNo = getUserInput("Do you have mpu (Martin Python Utilities) installed? (yes or no): ")


if (mpuYesOrNo == 'no'): 
    print("Loading dictionary...")
    with open('key.json', 'r') as jFile: 
        testGraph = json.load(jFile)

elif (mpuYesOrNo == 'yes'): 
    import mpu.io as mi 
    testGraph = mi.read('key.json')

else: 
    print("Something went wrong... Terminating program")
    sys.exit(1)
    
#pdb.set_trace()
yORn = getUserInput("Are you using \"Math-Comp Science\" as your source node? (yes or no): ")

if (yORn == 'no'): 
    checker = bool(1)
    listToCheck = checkingListOfKeys(testGraph)
    while checker: 
        source = input("Please enter your source: ")
        if (source in listToCheck): 
            checker = bool(0)
        else: 
            print("Please enter a valid source")
        
else: 
    source = 'Math-Comp Science'


output = dijkstra(testGraph, source)
#

#creating the output file
f = open('output.txt', 'w')

#Printing the distances found in the dijkstra algorithm and..
#Printing the pathways found in the dijkstra algorithm
outputDistances("Dijkstra's Algorithm", output['Distances'], f, source)
outputPathways("Dijkstra's Algorithm", output['Previous'], f, source)

#initialize edges for Bellman-Ford Algorithm
edges = initializeEdges(testGraph)
outputFord = bellmanFord(testGraph, edges, source)

#

outputDistances ("Bellman-Ford Algorithm", outputFord['Distances'], f, source)
outputPathways ("Bellman-Ford Algorithm", outputFord['Previous'], f, source)
yORn = getUserInput("Would you like the 'distance' and 'previous' dictionaries written to seperate .json files? (yes or no): ")



if(yORn == 'yes'): 
    if (mpuYesOrNo == 'yes'): 
        mi.write('outPutBellmanFord.json', outputFord)
        mi.write('outputForDijkstra.json', output)
        print('Dijkstra Results: outputForDijkstra.json\nBellman-Ford Results: outPutBellmanFord.json')

    elif (mpuYesOrNo == 'no'): 
        with open('outPutBellmanFord.json', 'w') as wj: 
            json.dump(outputFord, wj, indent = 10)
        with open('outputForDijkstra.json', 'w') as wj: 
            json.dump(output, wj, indent = 10)
        print('Dijkstra Results: outputForDijkstra.json\nBellman-Ford Results: outPutBellmanFord.json')



yORn = getUserInput("Would you like the output to also be written to the console? (yes or no): ")
f.close()

if (yORn == 'yes'): 
    f = open('output.txt', 'r')
    for line in f: 
        print(line, end = "")
else: 
    pass
