import csv
from collections import deque
import numpy as np 

# Instantiate a 2D array
datafile = 'stage1.csv'
data = np.array(list(csv.reader(open(datafile))))

# Get number of rows and columns
numR = len(data)
numC = len(data[0])

# Find where start and finish are
s = np.where(data == str('FD'))
sR = int(s[0])
sC = int(s[1])

e = np.where(data == str('KS'))
eR = int(e[0])
eC = int(e[1])

# Declare arrays
visited = np.array([[False for x in range(numC)] for y in range(numR)])
prev = {(x,y):0 for x in range(numC) for y in range(numR)}

#Provide cardinal directions
dr = [-1, +1, 0, 0]
dc = [0, 0, +1, -1]

# Use queue data structure to keep track of row and column coordinates. 
# Using one queue for each dimension. Can sub with position pairs	
rq = deque([])
cq = deque([])

# Add first node and mark it visisted
rq.append(sR)
cq.append(sC)
visited[sR,sC] = True

reached_end = False

def explore(r, c):
	for i in range (0,4):
		rr = r + dr[i]
		cc = c + dc[i]

		if rr < 0 or cc < 0: continue
		if rr >= numR or cc > numC: continue
		if visited[rr,cc]: continue
		if data[rr,cc] == 'W': continue
		if data[rr,cc] == 'F': continue

		# Save parent node for use in path reconstruction
		node = (r,c)
		prev[(rr,cc)] = node 

		# Add adjacent unvisited neighbors to the queue
		rq.append(rr)
		cq.append(cc)

		visited[rr,cc] = True

	
def reconstruct_path():
	path = []
	xy = (eR, eC)
	path.append(xy) 
	while xy != s:
		path.append(prev[xy])
		xy = prev[xy] 
	path.reverse()
	return path


# MAIN

while len(rq) > 0 or len(cq) > 0: # Keep repeating until there are no nodes with unexplored edges
	# Remove the node you're about to explore the edges of
	r = rq.popleft()
	c = cq.popleft()
	if (r,c) == (eR,eC):
		reached_end = True
		break
	explore(r, c)
print(reconstruct_path())

