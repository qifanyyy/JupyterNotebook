#!/usr/bin/python
import sys
# With the previous mapper, we sort our input over the columns 'flag' and 'distance'.
# This means that the first line is going to be the node with the shortest distance to the source,
# that has not yet been treated in the algorithm.
current_node = None
for line in sys.stdin:
    line = line.strip().split('\t')
    line[1] = int(line[1]) # This line is necessary to add two distances together (a bit later)
    if current_node == None and line[0] == '0': # If the line is the first line, and the node was not treated by the algorithm yet
        current_node = line[2].split(',')[-1] # Set the current node to the first node (once for the whole mapper)
        distance = line[1]
        path = line[3]
        print("%s\t%s\t%s\t1" % (line[2], line[1], line[3]))
    elif line[2].split(',')[0] == current_node and line[0] == '1': # If the first node is equal to the current node:
        print("1,%s\t%s\t%s\t1" % (line[2].split(',')[1], line[1] + distance, path + ',' + line[3].split(',')[-1])) # Add distance and modify the path
    elif line[2].split(',')[1] == current_node and line[0] == '1': # If the second node is equal to the current node (since the graph is non-directed):
        print("1,%s\t%s\t%s\t1" % (line[2].split(',')[0], line[1] + distance, path + ',' + line[3].split(',')[0]))
    else:
        print("%s\t%s\t%s\t%s" % (line[2], line[1], line[3], line[0])) # If the line is 'normal', print it without any modification
