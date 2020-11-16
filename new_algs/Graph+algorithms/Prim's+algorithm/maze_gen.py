'''
Cian McDonnell 2020
A program that generates a maze using Prim's algorithm.
'''
import matplotlib.pyplot as plt
import numpy as np
import random
import time

start = time.time()


class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def dist(self,p):
		return np.sqrt((self.x-p.x)**2+(self.y-p.y)**2)

points = []

xwidth = 20 #width/height of maze. Graphing works best for square mazes
ywidth = 20

for i in range(0,xwidth):
	for j in range(0,ywidth):
		points.append(Point(i,j))

connections = [[[] for j in range(0,ywidth)] for i in range(0,xwidth)]

for point in points:
        x_coord = point.x
        y_coord = point.y
        connections[x_coord][y_coord].append(0) #initialise all our connections to 0 - this is equivalent to initialising our maze to be completely made of walls.
        connections[x_coord][y_coord].append(0)
        connections[x_coord][y_coord].append(0)
        connections[x_coord][y_coord].append(0)

#let the 0th element in 4 element array be 1 for a connection to right
#1st element for connection to bottom
#2nd element for connection to left
#3rd element for connection to top
        
tree = [points[0]] #make a new list called tree, with one point in it. This will be the "seed" point from which the tree grows.
random.shuffle(points) #shuffle the points to ensure that there is no bias in how the tree grows -otherwise we may get a boring maze full of straight lines


min_point_indices = [0,0] #array to store the indices in the "points" list current pair of points fulfilling the conditions:
                                #(a) one is in the tree, one not in the tree and (b) the distance between them is the smallest distance between two such points.
min_points = [] #array to store the two points above, not just their indices
min_dist = 1000 #big distance to start off at to ensure that we do get the minimum distance between the points above.

plt.figure(figsize=(8,8))
ax = plt.axes()

plt.xlim(-1,xwidth) #set the limits of the plot to contain the whole maze.
plt.ylim(-1,ywidth)

for i in range(0,len(points)):
	min_dist = 1000
	min_point_indices = [0,0]
	min_points = []
	for point in points: #trying to find the closest distance between (a) a point in the tree and (b) a point not in tree
				if point not in tree: #find a point not in tree; compare the distance between it and a point in tree to the current "min_dist":
						for point2 in tree: 
                                                        if point.dist(point2)<= min_dist:
                                                                min_dist = point.dist(point2)
                                                                min_point_indices = [points.index(point2),points.index(point)] #record which points are at the minimum.
					
	min_points = [points[min_point_indices[0]],points[min_point_indices[1]]] #get the minimum points
	tree.append(min_points[1]) #add the new point to the tree and plot a line between it and the other point
	
	orig_x = min_points[0].x #just defining new variables to save typing/readability
	orig_y = min_points[0].y
	new_x = min_points[1].x
	new_y = min_points[1].y
	
	if(orig_x - new_x == 1):
		connections[orig_x][orig_y][2] = 1 # record that the two points are connected (i.e. one has a wall at the right, the other one at left)
		connections[new_x][new_y][0] = 1
        # we need "elif" to ensure that diagonally adjacent are not recorded as "connected".
	elif(orig_x - new_x == -1):
		connections[orig_x][orig_y][0] = 1 # same as other if statement, but for connections at other side
		connections[new_x][new_y][2] = 1
	elif(orig_y - new_y == 1):
		connections[orig_x][orig_y][1] = 1 # connections at bottom/top
		connections[new_x][new_y][3] = 1
	elif(orig_y - new_y == -1):
		connections[orig_x][orig_y][3] = 1 # connections at top/bottom
		connections[new_x][new_y][1] = 1
end = time.time()

for point in points: #plot walls if a particular point has no connection on a certain side.
        if(connections[point.x][point.y][0]==0):
                plt.plot([point.x+0.5,point.x+0.5],[point.y-0.5,point.y+0.5],color="#689a71")
        if(connections[point.x][point.y][1]==0 and not (point.x == xwidth-1 and point.y == 0)):
                plt.plot([point.x-0.5,point.x+0.5],[point.y-0.5,point.y-0.5],color="#689a71")
        if(connections[point.x][point.y][2]==0):
                plt.plot([point.x-0.5,point.x-0.5],[point.y-0.5,point.y+0.5],color="#689a71")
        if(connections[point.x][point.y][3]==0 and not (point.x == 0 and point.y == ywidth-1)): #add an extra condition to get an entry hole
                plt.plot([point.x-0.5,point.x+0.5],[point.y+0.5,point.y+0.5],color="#689a71")


elapsed = round(end-start,3)
print(str(elapsed) + " s")
file = open("times.txt",'a')
file.write(str(xwidth)+","+str(elapsed)+"\n")
file.close()
plt.show()



