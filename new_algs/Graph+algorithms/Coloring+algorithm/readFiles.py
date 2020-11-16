import numpy as np

# Read a given file and create a string with its contents


def readFile(filePath):
    f = open(filePath, "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
        return readMatrix(contents)
    return False


# Read a string and split its content on spaces
def readMatrix(matrixString):
    # Return a list with the edge locations
    edgeList = matrixString.split()
    # Remove 'p'
    del edgeList[0]
    # Return number of vertices
    numVertices = int(edgeList.pop(0))
    # Remove total number of edges
    del edgeList[0]
    return createMatrix(numVertices, edgeList), numVertices

# Creates the adjacency matrix


def createMatrix(numVertices, edgeList):
    # Create a square matrix filled with zeros
    matrix = np.zeros((numVertices, numVertices))
    while len(edgeList):
        # Takes edge location from list
         # Since vertices are named from 1 to n, subtracts 1 from each
        j = int(edgeList.pop(1)) - 1
        i = int(edgeList.pop(0)) - 1
        # Replaces '0' with '1' wherever there is an edge
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix
