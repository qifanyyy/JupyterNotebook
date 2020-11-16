"""
Points as index in myMap
A = 0
B = 1 
C = 2
D = 3 
E = 4
F = 5
G = 6
H = 7
I = 8
J = 9
K = 10
L = 11
M = 12
N = 13
O = 14
P = 15

Example: myMap[0][15] returns 7, signifing a connection between point A and point P, 
which has a distance of 7. A return of 0 means there is no connection between 
points.
"""

import collections
from queue import PriorityQueue

#adjacency matrix of weighted edged graph (see diagram.png)

		#0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 
myMap = [
        [0,10,7,0,0,0,0,0,0,0,0,0,0,0,0,7], #0
	[10,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0], #1
	[7,0,0,6,0,0,0,0,0,0,0,0,7,0,0,0],  #2 
	[0,5,6,0,9,8,0,0,0,0,0,0,0,0,0,0],  #3 
	[0,0,0,9,0,4,0,0,0,0,0,0,0,0,0,0],  #4 
	[0,0,0,8,4,0,4,0,0,6,0,0,0,0,0,0],  #5 
	[0,0,0,0,0,4,0,2,5,0,0,0,0,0,0,0],  #6  
	[0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],  #7 
	[0,0,0,0,0,0,5,0,0,9,8,0,0,0,0,0],  #8
	[0,0,0,0,0,6,0,0,9,0,6,0,5,0,0,0],  #9 
	[0,0,0,0,0,0,0,0,8,6,0,9,0,0,0,0],  #10 
	[0,0,0,0,0,0,0,0,0,0,9,0,6,0,8,0],  #11 
	[0,0,7,0,0,0,0,0,0,5,0,6,0,6,0,0],  #12
	[0,0,0,0,0,0,0,0,0,0,0,0,6,0,12,7], #13
	[0,0,0,0,0,0,0,0,0,0,0,8,0,12,0,13],#14
	[7,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0]  #15
	]
				 
def notVisited(array, num):
	if array[num] > 0: 
		return False #has been visited already, don't add to queue
	else:
		return True #add to queue
	
		
def prim(start, totalNodes):

	visited = [0] * totalNodes #keep track of visited nodes
	visited[start] = 1 #mark starting node as visited
	
	treeEdges = totalNodes - 1
	msTree = [0] * treeEdges #intialize MST
	edgeCount = 0 
	totalCost = 0
	
	#(cost/distance, starting node, ending node)
	pqueue = PriorityQueue() #intialize Priority queue in this ^^ format
	
	for i in range(15): #add the starting node's neighbors to the pqueue
		if myMap[start][i] > 0:
			pqueue.put((myMap[start][i], start, i))
			
			
	while pqueue:
		if pqueue.empty() and treeEdges == edgeCount: #loop does not break without this for some reason
			break 
		else: 
			
			edgeVal, nodeStart, nodeEnd = pqueue.queue[0] #get values from pqueue
			x = pqueue.get()
		
			if notVisited(visited, nodeEnd): #check if the node has not been visited
				#if no, continue below
				if edgeCount == 0:
					msTree[0] = (edgeVal, nodeStart, nodeEnd) #mark the first branch of the tree on the MST
				else:
					msTree[edgeCount] = (edgeVal, nodeStart, nodeEnd) #Mark the subsequent branches
					
				edgeCount = edgeCount + 1
				totalCost = totalCost + edgeVal #update the total distance of paths 
				visited[nodeEnd] = 1 #add the node to the visited list
				
				for i in range(16): #loop through the nodes neighbors 
					if myMap[nodeEnd][i] > 0:
						if notVisited(visited, i):
							pqueue.put((myMap[nodeEnd][i], nodeEnd, i))
					#if there is a connection and it has not been visited, add to pqueue
				
	return (totalCost, msTree)



def namePoint(name): 
	point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 
	'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

	return point_names[name]
	

totalDistance, answer = prim(12, 16) #12 (myMap[12]/node M) is the starting point to do the MST. 16 to identify how many points are there in the graph



print("Find the minimum spanning tree of graph using Prim's algorithm")
print("")
print("Connections:")

for i in range(15): #loop through the MST
	distance, point1, point2 = answer[i] #get the values
	point1 = namePoint(point1) #convert number representation to its node names
	point2 = namePoint(point2) #same as above
	
	print(point1, "and", point2, '(' + str(distance), "units)") #print results
	
print("")
print("Total distance of", totalDistance, "units")
