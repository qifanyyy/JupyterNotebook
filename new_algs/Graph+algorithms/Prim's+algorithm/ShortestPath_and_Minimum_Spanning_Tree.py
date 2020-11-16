import sys
import numpy as np
import pandas as pd
import time
import warnings

#supresses Future Warnings for pandas (used at .getvalues())
warnings.simplefilter(action='ignore', category=FutureWarning)

sum_for_mst = 0
default_file_location = 'Input1.txt'


# **************Reading Input from file**************#
def getInput(InputfileLocation):
    array = []
    try:
        input = open(InputfileLocation)
    except:
        input = open(default_file_location)

    for line in input:
        a = line.strip()
        array.append(a)

    return array


# **************Adjacency Matrix Code**************#

def create_matrix(row, col):
    zero_matrix = np.zeros(shape=(row, col))
    return zero_matrix


def convertToAdjacencyMatrix(inputarray):
    # gets no of vertices, source vertex from input array
    components = inputarray[0].split(' ')
    v = int(components[0])
    dir_undir = (components[2])
    adj_mat = create_matrix(v, v)
    source_vertex = (inputarray[len(inputarray) - 1])

    vertices = []
    # gets a list of vertices in the input array
    for i in range(1, len(inputarray) - 1):
        parts = inputarray[i].split(' ')
        vertex1 = parts[0]
        try:
            vertex2 = parts[1]
            if vertex2 not in vertices:
                vertices.append(vertex2)
        except:
            continue
        if vertex1 not in vertices:
            vertices.append(vertex1)
        vertices.sort()

    # names rows and columns with vertex names
    adj_mat = pd.DataFrame(adj_mat, columns=vertices, index=vertices)

    # creates adjacency matrix depending on the type of edges
    if dir_undir == 'D':
        for i in range(1, len(inputarray) - 1):
            part = inputarray[i].split(' ')
            row = part[0]
            column = part[1]
            value = part[2]
            adj_mat[column][row] = value

    if dir_undir == 'U':
        for i in range(1, len(inputarray) - 1):
            part = inputarray[i].split(' ')
            row = part[0]
            column = part[1]
            value = part[2]

            adj_mat[column][row] = value
            adj_mat[row][column] = value


    return adj_mat, vertices, source_vertex


# **************Minimum distance Code for Prim's and Djikstra's**************#
def min_distance_djk(distance, queue):
    # Initialize min value as infinite
    min = float("Inf")
    min_index = -1

    # code to pick the least value from the distance array
    for i in range(len(distance)):
        if distance[i] < min and i in queue:
            min = distance[i]
            min_index = i
    return min_index


def min_distance_Prim(key, mst, V):
    # Initilaize min value
    min = float("Inf")

    for v in range(V):
        if key[v] < min and mst[v] == False:
            min = key[v]
            min_index = v

    return min_index


# **************Code of Print Functions**************#
def print_path_djk(parent, j):
    if parent.get_value(j, 0) == -1:
        print(j)
        return
    print(j)
    p = print_path_djk(parent, parent.get_value(j, 0))
    return p


def print_djk(distance, parent, vertices, source_vertex, dict):
    distance = pd.DataFrame(distance, index=vertices)
    parent = pd.DataFrame(parent, index=vertices)
    print("Vertex \t\tdistance from Source\t")
    for i in (vertices):
        print("\n%s - %s \t\t%d \t\t" % (dict[source_vertex], i, distance.get_value(i, 0))),
        print("Path : ")
        print_path_djk(parent, i)


def print_prim(parent, adj_mat, V, dict):

        global sum_for_mst

        print("Edge \tWeight")
        for i in range(1, V):
            print(dict[parent[i]], "-", dict[i], "\t", adj_mat[parent[i]][i])
            sum_for_mst += adj_mat[parent[i]][i]
        return sum_for_mst


# **************Djikstra's shortest path algorithm**************#
def djk(adj_mat, source_vertex, vertices):
    row = len(adj_mat)
    col = len(adj_mat)
    dict = {}

    # converts the input vertex names into integers for easier calculations
    queue = []
    for i in range(col):
        queue.append(i)
        dict[i] = vertices[i]
        if vertices[i] == source_vertex:
            source_vertex = i

    # distance array with values initialized as infinite
    distance = [float("Inf")] * row

    # Initializing Parent array
    parent = [-1] * row

    distance[source_vertex] = 0

    # Code to get the shortest path from minimum distanceance function
    while queue:
        u = min_distance_djk(distance, queue)
        queue.remove(u)

        for i in range(col):

            # updates distance and parent array if smaller path is found
            if adj_mat[u][i] and i in queue:
                if distance[u] + adj_mat[u][i] < distance[i]:
                    distance[i] = distance[u] + adj_mat[u][i]

                    try:
                        parent[i] = dict[u]
                    except:
                        print("Exception")
    # prints output
    print_djk(distance, parent, Vertices, source_vertex, dict)


# **************Prim's algorithm for Minimum Spanning Tree**************#
def prim(V, adj_mat, vertices):
    col = len(adj_mat)
    dict = {}

    # converts to integers for easier calculations
    for i in range(col):
        dict[i] = vertices[i]

    # Key values used to pick minimum weight edge in cut
    key = [sys.maxsize] * V
    parent = [None] * V
    key[0] = 0
    mstSet = [False] * V

    parent[0] = -1

    for vertex in range(V):

        # gets vertex at shortest distance
        u = min_distance_Prim(key, mstSet, V)

        mstSet[u] = True

        # updates distance if a shorter distance is found
        for v in range(V):

            # Updates the key  if value at [u][v] is smaller than key[v]
            if adj_mat[u][v] > 0 and mstSet[v] == False and key[v] > adj_mat[u][v]:
                key[v] = adj_mat[u][v]
                parent[v] = u

    A = print_prim(parent, adj_mat, V, dict)
    return A


# **************Input File From User**************#
B = input("Enter the location of the input File: ")
graph_from_input = getInput(B)

print("_________________________________________________________________________________\n")

# **************To get Adjacency Matrix from given file input**************#

adj_mat_input = convertToAdjacencyMatrix(graph_from_input)
Matrix_input = adj_mat_input[0].values
Vertices = adj_mat_input[1]
source_vertex = adj_mat_input[2]

# **************To get output for Djikstra's Algorithm**************#
print("Shortest Path Algorithm: \n")
start_time_djikstra = time.time()
djk(Matrix_input, source_vertex, Vertices)
print("\nTime taken to find the shortest Path: %s seconds" % (time.time() - start_time_djikstra))

print("_________________________________________________________________________________\n")

# **************To get output for Prim's Minimum Spanning Tree Algorithm**************#
print("Minimum Spanning Tree: \n")
start_time_Prim = time.time()
sum_of_edges = prim(len(Vertices), Matrix_input, Vertices)
print("\n Total Sum = ", sum_of_edges)
print("\nTime taken to find the Minimum Spanning Tree using Prim's algorithm is : %s seconds " % (
            time.time() - start_time_Prim))

print("_________________________________________________________________________________\n")
