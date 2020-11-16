# =============================================================================
# Name: Tony Praveen Jesuthasan
# IIT ID: 2018596
# UoW ID: w1743058/8
# Referenced Sources: https://medium.com/100-days-of-algorithms/day-49-ford-fulkerson-e70045dafd8b
#                     https://networkx.github.io/
#                     https://matplotlib.org/api/pyplot_api.html
# =============================================================================
import time                                                      #Library used to measure time taken for the program to excecute
import networkx as nx                                            #Library imported to draw the graphs
import matplotlib.pyplot as plt                                  #Library used to plot the graphs
import random

#Implementing the Ford-Fulkerson Algorithm to solve the Maximum-Flow Problem.
def FordFulkerson(maxFlowGraph,source,sink,debug=None):                 #debug is the default value of this method.
    flow,flowPath=0,True
    
    #searching for paths with flow reserve. The flow path is returned from the depth-first function
    #The flow will increase by the amount of flow reserve found during the depth-first search.
    while flowPath:
        flowPath,flowReserve=DepthFirstSearch(maxFlowGraph,source,sink)
        flow+=flowReserve
    
        #increasing the flow along the path. The current node is in flowPath and the next node is in flowPath[1:]
        for currentNode, nextNode in zip(flowPath,flowPath[1:]):
            if maxFlowGraph.has_edge(currentNode,nextNode):
                maxFlowGraph[currentNode][nextNode]['flow']+=flowReserve
            else:
                maxFlowGraph[nextNode][currentNode]['flow']-=flowReserve
        
        #to display results each time there is a flow path.
        if callable(debug):
            debug(maxFlowGraph,flowPath,flowReserve,flow)
        
#Implementing the Depth-First Search
def DepthFirstSearch(maxFlowGraph, source, sink):
    undirected= maxFlowGraph.to_undirected()        #NetworkX function to return an undirected copy of a graph.
    visited={source}                                #Adding the source node to the visted dictionary since the search should begin from the source.

    stack=[(source,0,dict(undirected[source]))]     #The stack that would be used for the depth-first search. dict(undirected[source]) is a dictionary that holds--- 
                                                    #---the value of the capacity flowing from the source into the nodes that are attached to the source.
    
    while stack:                                    
        currentNode,_,adjacentNodes= stack[-1]      #The value of the current node, a null pointer and the adjacent node is added last to the list.
        if currentNode==sink:                       
            break
        
        #searching the adjacent node               
        while adjacentNodes:                       
            nextNode,cf= adjacentNodes.popitem()    #The next node identifier and the capacity and flow of the node is taken from the last value in the dictionary
            if nextNode not in visited:              
                break
        
        else:                                       #If no adjacent nodes, it will be removed from the stack. 
            stack.pop()
            continue
    
        #The flow and the capacity of the edge
        hasEdge=maxFlowGraph.has_edge(currentNode,nextNode)         #NetworkX function that returns if there are edges between two nodes.
        flow= cf['flow']                                            #The flow value in the cf dictionary is the flow between the two nodes.
        capacity=cf['capacity']                                     #The capacity value in the cf dictionary is the capacity between the two nodes.
        adjacentNodes=dict(undirected[nextNode])                    #The capacity and flow of the next node is added into the adjacentNodes dictionary.
        
        #increase and redirect flow at edge
        if hasEdge and flow<capacity:
            stack.append((nextNode,capacity-flow,adjacentNodes))    #if a node is present and the capacity is greater than the flow, the next node, difference--- 
                                                                    #---between capacity and flow and the adjacentNode dictionary is appended into the stack
            visited.add(nextNode)                                   
        elif not hasEdge and flow:                                  
            stack.append((nextNode,flow,adjacentNodes))             #if there is no edge or flow the nextnode, flow and adjacentnodes dictionary is appeneded to the stack.
            visited.add(nextNode)
    
    #This is to calculate the flow reserve and to find out the path taken by the flow.
    flowReserve= min((i for _,i,_ in stack[1:]),default=0)         
    flowPath= [currentNode for currentNode,_,_ in stack]            #returns the path taken.
    
    return flowPath,flowReserve

    
print("------------------------------------------------------------------------------")

def flow_debug(maxFlowGraph,flowPath,flowReserve,flow):
    if flowPath!=[]:
        print("The Flow has expanded by", flowReserve,"in the path",flowPath,"\nThe Current Flow is: ",flow)
    elif flowPath==[]:
        print("-------------------------------------------------------------------")
        print("THE Maximum Flow is:",flow)

#This time code surrounding the Ford-Fulkerson method call is used to show calculate the time taken to excecute this method.
start_time = time.time()

#This section of code creates the digraph and adds egde (starting node and ending node), their capacities and their flow.
#A DiGraph stores nodes and edges with optional data, or attributes.

#for i in range(100):
maxFlowGraph = nx.DiGraph()
maxFlowGraph.add_nodes_from('ABCDEF')
maxFlowGraph.add_edges_from([
        ('A', 'B', {'capacity': 10, 'flow': 0}),
        ('A', 'C', {'capacity': 8, 'flow': 0}),
        ('B', 'C', {'capacity': 5, 'flow': 0}),
        ('B', 'D', {'capacity': 5, 'flow': 0}),
        ('C', 'B', {'capacity': 4, 'flow': 0}),
        #('C', 'E', {'capacity': 10, 'flow': 0}),
        ('D', 'C', {'capacity': 7, 'flow': 0}),
        #('D', 'E', {'capacity': 6, 'flow': 0}),
        ('D', 'F', {'capacity': 3, 'flow': 0}),
        #('E', 'D', {'capacity': 10, 'flow': 0}),
        #('E', 'F', {'capacity': 14, 'flow': 0}),
])

FordFulkerson(maxFlowGraph,'A','F',flow_debug)
    
end_time = time.time()
print(end_time-start_time)

