# Counts how many steps it takes to go from one node to another.
# Doesn't show the path so you will have to extract it from the Dijkstra's
# adjacency matrix.

# This function keeps track of which vertexes have been selected 
# already. selected_indexes_array1 is an array of the indexes of 
# selected vertexes.


def selected_vertex_index(selected_vertex_index, selected_indexes_array1):
    selected_indexes_array1.append(selected_vertex_index)
    return selected_indexes_array1
    
# This function creates a matrix of directions for each node.
# array1 contains each node and for all nodes, a path matrix is 
# generated that tells which other nodes can be accessed to from a given 
# node. For array1[i], all possible directions are given by paths[i]


def path_matrix(from2, to2, array1, length1):
    list1 = from2 + to2
    common1 = max(set(list1), key=list1.count)
    
    # Declaring rows N and column M
    N = list1.count(common1)
    M = len(array1)
    
    # Initialize matrix of size N x M, fill it with -1 that represents 
    # empty slot. Vertex values always >= 0
    paths = [ [ -1 for i in range(N) ] for j in range(M) ] 
    
    # Allocates direction nodes to path matrix
    i = 0
    while i < length1:
        a = 0
        index1 = array1.index(from2[i])
        index2 = array1.index(to2[i])
        
        # Looks for empty slot and assigns direction vertex to each node
        # cond1 - slot is empty
        # cond2 - direction is not towards the node itself
        while a < N:     
            cond1 = paths[index1][a] < 0 
            cond2 = to2[i] != array1[index1] 
            if cond1 and cond2:
                paths[index1][a] = to2[i]
                break
            a += 1
        a = 0
        while a < N:
            cond3 = paths[index2][a] < 0
            cond4 = from2[i] != array1[index2]
            if cond3 and cond4:
                paths[index2][a] = from2[i]
                break
            a += 1 
        i += 1
    return paths, N

# from1 array to to1 array. If from1 = [0,0,1,2] and 
# to1 = [1,2,3,3], 0 is connected to 1 and 2, 1 is connected to
# 3, 2 is connected to 3. Locationa is the starting point and
# locationb is the destination.


def fastestroute(from1, to1, locationa, locationb):
    
    # Creates an array that contains all the nodes in the system
    # All nodes are saved only once in the array (cond1 and cond2)
    array = []
    length = len(from1)
    i = 0
    while i < length:
        cond1 = from1[i] not in array
        cond2 = to1[i] not in array
        if cond1:
            array.append(from1[i])
        if cond2:
            array.append(to1[i])
        i += 1
        
    # Infinity since platform uses python3.4 that doesn't contain math.inf
    INFINITY = 10000000 
    
    # Allocates directions to each node. Check path_matrix for 
    # detailed functionality.
    path, N1 = path_matrix(from1, to1, array, length)
    
    # Creates Adjacency Matrix for dijkstra's algorithm
    v_column = len(array)
    dijkstra = [ [ INFINITY for i in range(v_column) ] for j in range(2) ] 
    
    # row refers to row of Adjacency Matrix
    # selected_vertex is the selected vertex (index) for next node.
    # selected_indexes_array is the selected index matrix, tracks which
    # array indexes have been selected already (selected vertexes)
    row = 1
    selected_vertex = 0
    selected_indexes_array = []

    # Allocates nodes and steps to Adjacency Matrix for dijkstra's algorithm.
    # row = 1 goes to ELSE and the following ones go to IF
    while row >= 0: 
        cond0 = row > 1
        if cond0:
            
            # Creates a new row to the Adjacency Matrix and copies the  
            # previous row values to the new row
            dijkstra2 = [ [ INFINITY for i in range(v_column) ] for j in \
                          range(1) ] 
            dijkstra = dijkstra + dijkstra2
            dijkstra[row][:] = dijkstra[row - 1][:]
            
            # Assigns values (in the new row in the Adjacency Matrix)
            # to each vertex from previously selected vertex
            i = 0
            while i < N1:
                idx = selected_vertex
                cond3_1 = path[idx][i] >= 0
                if cond3_1:
                    idx2 = array.index(path[idx][i])
                    cond3 = dijkstra[row - 1][idx2] > dijkstra[row - 1][idx] + 1
                    cond4 = array[idx2] == locationb
                    if cond3:
                        dijkstra[row][idx2] = dijkstra[row - 1][idx] + 1
                    if cond4:
                        i = N1 + 1
                        row = -2 
                i += 1

            # Checks which vertex is selected as the following node.
            # Selects the minimum value while excluding nodes that have 
            # been already selected. selected_indexes_array tracks which 
            # nodes have been selected already
            temp_min = INFINITY
            i = 0
            while i < len(array):
                steps = dijkstra[row][i]
                cond5 = i not in selected_indexes_array
                cond6 = steps < temp_min
                if cond5 and cond6:
                    temp_min = steps
                    selected_vertex = i
                i += 1
            
            # Adds values to selected_indexes_array. If target node 
            # is reached, the program exits loop
            selected_indexes_array = selected_vertex_index(
                selected_vertex, selected_indexes_array)
            cond8 = array[selected_vertex] == locationb
            if cond8:
                row = -2
        
        # Assigns value 1 to Adjacency Matrix, meaning that 1 step to that 
        # vertex from node. If the vertex is the same as target location 
        # or locationb, the programs exits the loops by setting row=-2 and 
        # the end result is 1 step to target vertex
        else:
            i = 0
            idx = array.index(locationa)
            while i < N1:
                cond1 = path[idx][i] >= 0
                if cond1:
                    idx2 = array.index(path[idx][i])
                    dijkstra[row][idx2] = 1
                    cond1_1 = array[idx2] == locationb
                    if cond1_1:
                        i = N1 + 1
                        row = -2
                i += 1
            selected_vertex = dijkstra[1].index(min(dijkstra[1]))
            selected_indexes_array = selected_vertex_index(
                selected_vertex, selected_indexes_array)
        row = row + 1
        
        # Mainly for cases that do not have a connection between locationa
        # and locationb. Adjacency Matrix is still created but if the value 
        # is still infinity from starting node to end node, 
        # return value will be -1
        cond7 = len(selected_indexes_array) > len(array)
        if cond7:
            row = -2
    
    # Looks for return value. If value in the Adjacency Matrix is 
    # non-infinity, the return value is the amount of steps. 
    # Otherwise, it is -1.
    cond9 = dijkstra[-1][array.index(locationb)] != INFINITY
    if cond9:
        steps = dijkstra[-1][array.index(locationb)]
    else:
        steps = -1

    return steps


# Main function, this is an example.
# Means that the connections are 0<->1,0<->2,1<->3,2<->3,
# and starting point is 2, ending point is 3
def main():
    step = fastestroute([0, 0, 1, 2], [1, 2, 3, 3], 2, 3)
    print(step)


main()
