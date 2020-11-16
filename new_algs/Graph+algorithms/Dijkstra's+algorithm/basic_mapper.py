#!/usr/bin/python
# This is the first mapper, that we use to transform the initial matrix into something we can work with
# The end result consists in four columns, as follows:
# 1- A flag (0 if the departure node is the source and the line not treated yet, 1 otherwise), 2-, The distance between the two nodes,
# 3- The departure and arrival node, and 4- The optimal path to get to the last node
import sys

print("1,1\t%s\t1,1\t0" % str.rjust("0", 8)) # Print the first line (distance of 0 between the node 1 and 1, may be necessary)

for line in sys.stdin: # Split the sparse matrix into four columns:
    line = line.strip().split(';') # Departure node, arrival node, distance, and departure node again
 
    if line[0] == '1': # If the starting node is 1, print it as normal
        print("%s,%s\t%s\t%s,%s\t0" % (line[0], line[1], str.rjust(line[2], 8), line[0], line[1]))
        
    elif line[1] == '1': # Similar
        print("%s,%s\t%s\t%s,%s\t0" % (line[1], line[0], str.rjust(line[2], 8), line[1], line[0]))
        
    else:
        print("%s,%s\t%s\t%s,%s\t1" % (line[0], line[1], str.rjust(line[2], 8), line[0], line[1])) # We firstly print the line as normal
        #   We then add two lines that will be necessary for the initialisation of the Dijkstra algorithm.
        # Indeed, at the start, we need to set up the distance between the source and the nodes that aren't connected to it
        # to + infinity (9999 in our program).
        # We have no way from the start to know which nodes they are, so for every arc that do not involve the source, we print the following lines:
        print("1,%s\t%s\t1,%s\t0" % (line[1], str.rjust('9999', 8), line[1]))
        print("1,%s\t%s\t1,%s\t0" % (line[0], str.rjust('9999', 8), line[0]))
