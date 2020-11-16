#! /usr/bin/python3
import sys, os
from os import path

# Parse input file
def parseInput(infile):
    # edges = list of edges, weight, and label
    # Format: [label, v1, v2, weight]
    edges = []
    numVertices = -1
    numEdges = -1

    # If input file does not exist, exit program
    if not path.exists("./" + infile):
        sys.exit('Error: Cannot find input file name: %s' % infile)
    
    # Open input file for reading
    f = open('./' + infile, 'r')
    line = f.readline()
    ln = 1
    while line: # Parse file line by line
        if line == '\n':
            break
        elif ln == 1: # First line is number of vertices
            numVertices = line.strip()
        elif ln == 2: # Second line is number of edges
            numEdges = line.strip()
        else: # lines > 2 contain edges and their respective weights
           v1, v2, w = line.strip().split(' ')
        #    print(float(int(w)))
           edges.append([ln-2,int(v1),int(v2),float(int(w))])

        line = f.readline()
        ln += 1

    # Close input file stream
    f.close()
    return numVertices, numEdges, edges

# Write to output file
def writeOutput(outfile, mwst):

    # Open output file for writing
    f = open(outfile, "w")

    totalWeight = 0.0
    for label, v1, v2, weight in mwst:
        f.write("%4d: (%d, %d) %.1f\n" % (label, v1, v2, round(weight, 1)))
        totalWeight += weight

    f.write("Total Weight = %.1f\n" % round(totalWeight,1))

    # Close output fule stream
    f.close

# Get adjacent vertices of a vertex given a list of edges
def getAdjacent(vertex, edges):
    # List of adjacent vertices
    adjacents = []

    # Check for vertex in edges
    for _, v1, v2, _ in edges:
        if vertex == v1: # If vertex is source, get destination vertex
            adjacents.append(v2)
        elif vertex == v2: # If vertex is destination, get source vertex
            adjacents.append(v1)

    return adjacents


# Check if adding the new edge to a graph makes it cyclic
def isCyclic(edges, newEdge):
    newEdges = edges.copy()
    newEdges.append(newEdge)

    # Get source and destination vertices of new edge
    _, nv1, nv2, _ = newEdge

    # List of unvisited vertices, add the vertices of new edge to it
    # Used for checking unconnected graphs
    unvisited = [nv1,nv2]

    # Then add all vertices in current graph to unvisited
    for _, v1, v2, _ in edges:
        if v1 not in unvisited:
            unvisited.append(v1)
        if v2 not in unvisited:
            unvisited.append(v2)

    # List of vertices to check next
    stack = []
    # List of vertices visited
    visited = []

    for v in unvisited:
        # Check if v is already visited
        if v not in visited:
            # Add v to stack
            stack.append(v)

            while stack:
                # Pop the vertex at top of stack
                top = stack.pop()
                # Visit that vertex
                visited.append(top)

                # Get the adjacent vertices of top
                adjacents = getAdjacent(top, newEdges)
                # Add all adjacent vertices of top to stack
                for av in adjacents:
                    if av in stack: # Vertex already in stack, there is a cycle
                        return True
                    elif av not in visited: # Vertex not visited yet, so push to stack
                        stack.append(av)
                    # Else, vertex is already visited so do nothing
    return False

# Kruskal's algorithm
def Kruskal(edges):
    # Sort edges by weight, smallest first
    edges.sort(key = lambda x: x[3])
    
    # List of marked vertices
    marked = []
    # List of the edges of the MWST, with label and weight
    minEdges = []

    # For each edge, mark it if it's addition does not make the MWST cyclic
    for e in edges:
        if e not in marked and not isCyclic(minEdges, e): 
            marked.append(e) # Mark the edge
            minEdges.append(e) # Append edge to MWST

    # Return minEdges, which is a MWST
    return minEdges

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Error: Incorrect usage: ./mwst.py [infile] [outfile]')

    # Get input and output files from command line
    infile = sys.argv[1]
    outfile = sys.argv[2]

    # Parse input file
    numVertices, numEdges, edges = parseInput(infile)

    # Call Kruskal's algorithm
    mwst = Kruskal(edges)

    # Write to output file
    writeOutput(outfile, mwst)