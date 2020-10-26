"""

*** find the number of nodes away from specified point in graph using Breadth First Search ***

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
		[7,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0] #15
		]

def notVisited(array, num):
	if array[num] > 0: 
		
		return False #has been visited already, don't add to queue
	else:
		return True #add to queue
		
def BFS(start):
	          #0. 1. 2. 3. 4. 5. 6. 7  8  9. 0. 1. 2. 3. 4. 5 
	visited = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #1 for visited, 0 for not 
	queue = []
	nodesAway = [0] *16
	queue.append(start)
	visited[start] = 1 #first node starts as 'visited'

	while queue:
		for i in range(16): #loop thru sublist of queue[0] in myMap
			if myMap[queue[0]][i] > 0: #if element in sublist is > 0, representing a vertice 
				if notVisited(visited, i): #check if element has not been seen before
					queue.append(i) #add the unvisited node to the queue
					
					visited[i] = 1 #record node has been visited
					nodesAway[i] = nodesAway[queue[0]] + 1 #record distance by adding 1 to the distance of the node's parent
					
		queue.pop(0)
		
	return nodesAway
		
startingNode = 12 #<--- change starting node here
answer = BFS(startingNode) #myMap[12] (point M) as the starting point

point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

print("Number of nodes away from node", point_names[startingNode])
print("")
print("Using Breadth-First Search Algorithm:")

for i in range(len(answer)):
	print(point_names[i] + ":", str(answer[i]), "nodes away")