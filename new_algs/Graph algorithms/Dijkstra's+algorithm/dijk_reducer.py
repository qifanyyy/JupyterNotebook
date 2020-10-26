#!/usr/bin/python
import sys
# For the last output, we put the third column (starting node, arrival node) first because we wanted to sort over it
# For every line, we check if the (starting node, arrival node) is equal to that of the previous line
# If it is the case, we keep the minimum distance between both arcs, along with the corresponding path
# Otherwise, we print the line as normal, and put the columns in their original order (to sort over our flag and over the distance).
last_line = None
for line in sys.stdin:
    line = line.strip().split('\t')
    if last_line == None: # If this is the first line in the algorithm
        last_line = line
    # For the next two 'elif' instructions: if the starting and the ending nodes are the same for two consecutive lines:    
    elif line[0] == last_line[0] and int(line[1]) < int(last_line[1]): # If the distance for the first line is higher:
        last_line = line # Do not print the first line
    elif line[0] == last_line[0] and int(line[1]) >= int(last_line[1]): # If the distance for the second line is higher:
        last_line[3] = 0
        continue
    else: # Otherwise, if the two consecutive lines have different starting or ending nodes:
        print("%s\t%s\t%s\t%s" % (last_line[3], str.rjust(str(last_line[1]), 4), last_line[0], last_line[2])) # Print line as normal
        last_line = line
else: # Do not forget to print the last line!
    print("%s\t%s\t%s\t%s" % (line[3], str.rjust(str(line[1]), 4), line[0], line[2]))