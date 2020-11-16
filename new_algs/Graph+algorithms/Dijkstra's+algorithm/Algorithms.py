"""
Dijkstra's Algorithm
takes in a 2D array
This was my initial version of Dijkstra's Algorithm.
However, i had to modify it to visualise it (i.e. move to another loop).
So i copied a chunk of this code into Shortest_Path_Visualiser.py
"""
#Import system to link to other py files
import sys
sys.path.append(".")
#Import min heap data structure from Structures to decrease run time of algorithm
from Structures import min_heap


def check_surroundings(arr, absorbed_nodes, current_node, size):
    """
    Function, given a node, will determine the neighbouring nodes.
    Inputs:  arr: given grid structure
             absorbed_ nodes: Nodes that are used in the algo. list of tuples (x,y)
             current_node: Node whose neighbours are to be determined. Tuple (x,y)
             size: size of arr
    Returns: List of available neighbouring nodes 
    """
    x, y = current_node
    surrounding_nodes = []

    if(x>0 and arr[x-1][y] != None and (x-1,y) not in absorbed_nodes):        #Left Node
        surrounding_nodes.append((x-1,y))

    if(y<size-1 and arr[x][y+1] != None and (x,y+1) not in absorbed_nodes):   #Top Node
        surrounding_nodes.append((x, y+1))

    if(x<size-1 and arr[x+1][y] != None and (x+1,y) not in absorbed_nodes):   #Right Node
        surrounding_nodes.append((x+1, y))

    if(y>0 and arr[x][y-1] != None and (x,y-1) not in absorbed_nodes):        #Bottom Node
        surrounding_nodes.append((x, y-1))

    return surrounding_nodes


def d_algo(arr, start_node, end_node, size):
    """
    Dijkstra's algorithm main function
    Inputs: arr: initialised 2D array
            start_node: start point, should be a tuple
            end_node: end point, should be a tuple
            size: size of 2D square array
    Returns: 0 if found a shortest path, -1 otherwise
    """
    start_x, start_y = start_node

    arr[start_x][start_y] = 0                   #Initialise start node in array
    current_node = (start_x, start_y)           #Initialise current_node (x,y)
    absorbed_nodes = [current_node]             #Initialise absorbed nodes [(x,y)]
    heap = min_heap([])                         #Initialise heap structure

    while(current_node != end_node):
        current_x, current_y = current_node         #x,y coordinates of current node
        current_value = arr[current_x][current_y]   #Value of current node

        #Obtain list of nodes that are surrounding current nodes
        surrounding_nodes = check_surroundings(arr, absorbed_nodes, current_node, size)

        #For each surrounding node, check if it is in heap and check if it needs updating
        for node in surrounding_nodes:
            x, y = node             #x,y coordinates of surrounding_nodes

            #Node has not been added to heap before, so we add it in, and we update in arr
            if arr[x][y] == float("inf"):
                arr[x][y] = current_value + 1       #Updates arr
                node_with_value = (x, y, arr[x][y])
                heap.heap_insert(node_with_value)       #Updates heap

            #Value of node <= value of current_node + 1, then we leave it alone
            elif arr[x][y] <= current_value + 1:
                pass

            #Value of node > value of current_node + 1, then we want to update node value in heap
            else:
                node_with_value = (x, y, arr[x][y])
                heap_index = heap.find_index(node_with_value)
                #Update the heap_index with appropriate value
                heap.update_heap(heap_index, current_value + 1)
        
        min_node = heap.extract_min()               #Obtain smallest node
        if min_node == -1:                          #Checks if there are any remaining nodes
            return -1
        current_node = (min_node[0], min_node[1])   #update current_node
        absorbed_nodes.append(current_node)         #Update absorbed_nodes
    
    #If while loop condition is met, it means the current_node == end_node, and we found the shortest path
    return 0
