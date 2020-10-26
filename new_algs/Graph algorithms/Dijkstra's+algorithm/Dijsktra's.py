import math
import copy
import time




def searchForLeastCost(costs, processed):
    lowestCost = math.inf
    lowestCostNode = None
    for node in costs:
        cost = costs[node]
        #check if cheapest
        if cost < lowestCost and node not in processed:
            lowestCost = cost
            lowestCostNode = node
    return(lowestCostNode)

def formulate(graph, startNode):
    costs = {}
    parents = {}
    processed = []
    #making costs
    for w in graph:
        costs[w] = math.inf
    #adding costs from start node
    costs[startNode] = 0
    for x in graph[startNode]:
        costs[x] = graph[startNode][x]
    #creating parents
    for y in graph:
        parents[y] = None
    #adding parents from start node
    parents[startNode] = 0
    for z in graph[startNode]:
        parents[z] = startNode
    #creating processed
    processed.append(startNode)
    return(parents, costs, processed)

def dijkstra(graph, startNode):
    parents, costs, processed = formulate(graph, startNode)
    node = searchForLeastCost(costs, processed)
    #if while loop over nodes all processed
    while node is not None:
        #get all neighbours from node & their total costs
        cost = costs[node]
        neighbours = graph[node]
        for n in neighbours:
            newCost = cost + neighbours[n]
            #if newcost less than previous noted 'shortest' cost...
            if costs[n] > newCost:
                #then update costs and parents to say so
                costs[n] = newCost
                parents[n] = node
        #now all neighbours noted node has been processed
        processed.append(node)
        #find next node
        node = searchForLeastCost(costs, processed)
    return(parents, costs, processed)
        
def main():
    '''
    target = "End"
    #make graph
    graph = {}
    #nodes
    graph["Start"] = {}
    graph["A"] = {}
    graph["B"] = {}
    graph["End"] = {}
    #node connections
    graph["Start"]["A"] = 6
    graph["Start"]["B"] = 2
    graph["A"]["End"] = 1
    graph["B"]["A"] = 3
    graph["B"]["End"] = 5
    '''
    
    #travelling salesman
    #make graph
    graph = {}
    #nodes
    graph["A"] = {}
    graph["B"] = {}
    graph["C"] = {}
    graph["D"] = {}
    graph["E"] = {}
    graph["F"] = {}
    #node connections
    graph["A"]["B"] = 5
    graph["A"]["C"] = 3
    graph["A"]["D"] = 3
    graph["B"]["A"] = 5
    graph["B"]["F"] = 2
    graph["C"]["A"] = 3
    graph["C"]["F"] = 3
    graph["C"]["E"] = 3
    graph["D"]["A"] = 3
    graph["D"]["E"] = 2
    graph["E"]["C"] = 3
    graph["E"]["D"] = 2
    graph["F"]["B"] = 2
    graph["F"]["C"] = 3
    
    graphList = []
    for v in graph:
        graphList.append(v)
    graphString = ", ".join(graphList)
    print("The nodes are", graphString)
    inputLoop = True
    while inputLoop == True:
        startNode = input("Please enter the start node: \n").upper()
        targetNode = input("Please enter the target node: \n").upper()
        if startNode in graph and targetNode in graph:
            print("\n")
            target = targetNode
            inputLoop = False
        else:
            print("\nPlease enter a nodes in the graph")
            

    #Start the clock!
    startTime = time.time()
    #use dijkstras                              
    parents, costs, processed = dijkstra(graph, startNode) # Node must be in graph
    #Stop the clock!
    endTime = time.time() - startTime
    #give answer
    travelList = [target]
    parent = parents[target]
    if parent == 0:
        pass
    else:
        travelList.insert(0, parent)
    while parent != 0:
        parent = parents[parent]
        if parent == 0:
            pass
        else:
            travelList.insert(0, parent)
    #formatting the answers
    print("The path of "+", ".join(travelList)+" was taken")
    print("With a total cost of "+str(costs[target]))
    print("The nodes were processed in the order "+", ".join(parents))
    
    print("The program took", endTime , "second/s")

mainLoop = True
print("----------- Welcome To Dijsktra's Algorithm -----------")
while mainLoop == True:
    main()
    print("\n")
    userSelect = input("Please press enter to continue, or E to exit")
    if userSelect == "e" or userSelect == "E":
        mainLoop = False
    
    
        
    
    


















