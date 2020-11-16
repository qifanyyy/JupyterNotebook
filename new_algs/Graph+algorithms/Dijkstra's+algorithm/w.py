import csv
from heapdict import heapdict
import numpy as np

# Instantiate a 2D array
datafile = 'stage2.csv'
data = np.array(list(csv.reader(open(datafile))))

# Get number of rows and columns
numR = len(data)
numC = len(data[0])

# Setup data array for edge weight math
data[data == ''] = 0 
for i in range(numR):
    for j in range(numC):
        if (data[i,j]).isdigit() == True:
            data[i,j] = int(data[i,j])+1

# Find where start and finish are
s = np.where(data == str('FD'))
sR = int(s[0])
sC = int(s[1])

e = np.where(data == str('KS'))
eR = int(e[0])
eC = int(e[1])

# Declare arrays. Mark unexplored distances as inf in pursuit of the best path
dist = np.array([[float('inf') for x in range(numC)] for y in range(numR)])
visited = np.array([[False for x in range(numC)] for y in range(numR)])
prev = {(x,y):0 for x in range(numC) for y in range(numR)}

# Provide cardinal directions
dr = [-1, +1, 0, 0]
dc = [0, 0, +1, -1]

# Add priority queue data structure. Use key-value pairs (node index, dist)
hd = heapdict()

# Add first node and mark it visisted with no distance weight
dist[sR,sC] = 0
hd[sR,sC] = 0
visited[sR,sC] = True

reached_end = False

def explore(r, c):
    for i in range (0,4):
        rr = r + dr[i]
        cc = c + dc[i]

        if rr < 0 or cc < 0: continue 
        if rr >= numR or cc >= numC: continue
        if visited[rr,cc]: continue
        if data[rr,cc] == 'W': continue
        if data[rr,cc] == 'F': continue

        # Save parent node for use in path reconstruction
        node = (r,c)
        prev[rr,cc] = node 

        # Keep exploring until the end is reached
        if (rr,cc) == (eR, eC):
            global reached_end
            reached_end = True 
            break 

        # The core of Dijkstras Algorithm
        d = int(dist[r,c]) + int(data[rr,cc])
        hd[rr,cc] = d
        dist[rr,cc] = d

        visited[rr,cc] = True

def reconstruct():
    path = []
    xy = (eR, eC) 
    path.append(xy)
    while xy != s:
        path.append(prev[xy]) 
        xy = prev[xy]
    path.reverse()
    return path

# MAIN

while reached_end == False:
    # Tells you which node to visit next based on which key-value pair has the lowest value
    a = hd.popitem()
    r, c = a[0]
    explore(r, c)
print(reconstruct())
