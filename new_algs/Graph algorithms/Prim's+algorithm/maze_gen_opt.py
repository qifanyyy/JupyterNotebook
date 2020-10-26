'''
Cian McDonnell 2020
A program that generates a maze using Prim's algorithm.
The algorithm used here is more efficient than the one used in maze_gen.py. 
It takes advantage of the fact that the points in the maze are on a square grid, so the shortest distance
between a point in the tree and a point not in the tree will always be one.
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
        return ((self.x-p.x)+(self.y-p.y))


xwidth = 50 #width/height of maze. Graphing works best for square mazes
ywidth = 50

points = np.empty([xwidth,ywidth],dtype=Point)
for i in range(0,xwidth):
    for j in range(0,ywidth):
        points[i][j] = Point(i,j)

connections = [[[] for j in range(0,ywidth)] for i in range(0,xwidth)]

for column in points:
    for point in column:
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
randx = random.randint(0,xwidth-1)
randy = random.randint(0,ywidth-1)           
tree = [points[randx][randy]] #make a new list called tree, with one point in it. This will be the "seed" point from which the tree grows.

#since the tree grows from the initial point, it is best to randomize the initial point as the solution usually ends up passing near there

v_points = points.flatten() #make a 1D array of the points - this makes it easier to choose them at random and makes the final maze less predictable
random.shuffle(v_points)

min_point_indices = [] #array to store the indices in the "points" list current pair of points fulfilling the conditions:
                                #(a) one is in the tree, one not in the tree and (b) the distance between them is the smallest distance between two such points.
min_points = [] #array to store the two points above, not just their indices
min_dist = 1000 #big distance to start off at to ensure that we do get the minimum distance between the points above.

if(xwidth<=ywidth):
    plt.figure(figsize=(8,int(8*(ywidth/xwidth))))
else:
    plt.figure(figsize=(int(8*(xwidth/ywidth)),8))
ax = plt.axes()

plt.xlim(-1,xwidth) #set the limits of the plot to contain the whole maze.
plt.ylim(-1,ywidth)

for i in range(0,(len(points)*len(points[0]))):
    min_dist = 1000
    min_point_indices = []
    min_points = []
    for point in v_points:
        if point not in tree:
            connect_list = [False,False,False,False] #this algorithm is more efficient as it considers that the closest point that is IN the tree will always be a neighbour of the current point
            found_connection = False
            if(point.x<xwidth-1):
                if points[point.x+1][point.y] in tree:
                    connect_list[0] = True #this flag indicates that the point to the RIGHT of the current point is in the tree.
                    found_connection = True
            if(point.y<ywidth-1):
                if points[point.x][point.y+1] in tree:
                    connect_list[1] = True #indicates the point to the top is in the tree.
                    found_connection = True
            if(point.x>0):
                if points[point.x-1][point.y] in tree:
                    connect_list[2] = True #indicates the point to the left is in the tree.
                    found_connection = True
            if(point.y>0):
                if points[point.x][point.y-1] in tree:
                    connect_list[3] = True #indicates the point to the bottom is in the tree.
                    found_connection = True
                    
            if(found_connection):
                choice = random.randint(0,3) #choose randomly between all of the point's neighbours that are in the tree. This prevents the maze from looking too predictable.
                while(connect_list[choice] == False):
                    choice = random.randint(0,3) 
                if(choice==0):
                    tree.append(point)
                    connections[point.x][point.y][0]= 1
                    connections[point.x+1][point.y][2] = 1
                if(choice==1):
                    tree.append(point)
                    connections[point.x][point.y][3]= 1
                    connections[point.x][point.y+1][1] = 1
                if(choice==2):
                    tree.append(point)
                    connections[point.x][point.y][2]= 1
                    connections[point.x-1][point.y][0] = 1
                if(choice==3):
                    tree.append(point)
                    connections[point.x][point.y][1]= 1
                    connections[point.x][point.y-1][3] = 1      
                    
            


for column in points:
    for point in column: #plot walls if a particular point has no connection on a certain side.
            if(connections[point.x][point.y][0]==0):
                    plt.plot([point.x+0.5,point.x+0.5],[point.y-0.5,point.y+0.5],color="#af73a1")
            if(connections[point.x][point.y][1]==0 and not (point.x == xwidth-1 and point.y == 0)): #add extra condition to get exit hole
                    plt.plot([point.x-0.5,point.x+0.5],[point.y-0.5,point.y-0.5],color="#af73a1")
            if(connections[point.x][point.y][2]==0):
                    plt.plot([point.x-0.5,point.x-0.5],[point.y-0.5,point.y+0.5],color="#af73a1")
            if(connections[point.x][point.y][3]==0 and not (point.x == 0 and point.y == ywidth-1)): #add an extra condition to get an entry hole
                    plt.plot([point.x-0.5,point.x+0.5],[point.y+0.5,point.y+0.5],color="#af73a1")

end = time.time()
elapsed = round(end-start,3)
print(str(elapsed) + " s") #print the time taken

file = open("opt_times.txt",'a') #output the time taken to generate a maze of this size to a file. (Assumes a square maze)
file.write(str(xwidth)+","+str(elapsed)+"\n")
file.close()
plt.show()