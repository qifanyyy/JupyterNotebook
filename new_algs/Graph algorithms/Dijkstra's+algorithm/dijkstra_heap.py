from Min_heap.minheap import Minheap

'''
* Author: Tomoya Tokunaga(mailto: ttokunag@ucsd.edu)
*
* About this file:
* This file implements Dijkstra's shortest path algorithm with a binary MIN-HEAP
* Complexity: O((V + E)*logV) time | O(1) space (this stores node & distance pair
* to a list, so it takes a space)
'''
class graph_node(object):
    '''
    * a graph node constructor
    * @param val: the value of the node
    * @param adjacents: a list of its adjacent nodes
    '''
    def __init__(self, val, adjacents=[]):
        # val is the value of a vertex. it can be location names,
        # server names, intersections in real life applications
        self.val = val
        self.prev_pointer = None
        self.distance = float('inf')
        # its adjacent nodes are stored in an array
        # this array contains tuple pair, (adjacent_node, weight)
        self.adjacents = adjacents
    
    # a method to set a previous pointer
    def set_prev(self, node):
        self.prev_pointer = node
        
    # a method to add an adjacent node
    def set_adjacent(self, node, weight):
        self.adjacents.append((node, weight))
    
    # a method to set a distance from the start node
    def set_distance(self, dist):
        self.distance = dist


class graph_heap(object):
    '''
    * a constructor of a graph structure
    * @param vertices: a list of vertices which belong to the graph
    '''
    def __init__(self, vertices):
        # heapify the given list regarding to 
        # the distance of each node from the start node
        self.unvisited = Minheap(vertices)

    '''
    * a method to find a shortest path from the given start node
    * to the given destination using Dijkstra's algorithm
    * @param start: a node which one want to know the distance from
    * @param dest: a node which one want to know the distance from the start
    '''
    def dijkstra(self, start, dest):
        # the distance from the start to the start is 0
        # (this follows the Dijkstra's algorithm)
        start.set_distance(0)
        curr_node = None

        while self.unvisited.size() != 0:
            # min-heap's root at this point is the start node
            curr_node = self.unvisited.peek()
            
            # updates adjacent nodes distance
            if curr_node and curr_node.adjacents:
                for adj in curr_node.adjacents:
                    if curr_node.distance + adj[1] < adj[0].distance:
                        adj[0].set_distance(curr_node.distance + adj[1])
                        adj[0].set_prev(curr_node)
            
            # pop the minimum item, and heapify the queue
            self.unvisited.heappop()
    
        
    