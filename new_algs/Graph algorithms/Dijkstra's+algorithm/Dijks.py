import tkinter as tk
import sys


class Dijkstra:  # Class for Dijkstra's algorithm

    def __init__(self):
        self.nodes = {} # holds user graph
        self.visited_nodes = {}  # holds all visited nodes
        self.distance_node = {}  # hold distance to nodes (visited nodes)
        self.start = None  # start node
        self.end = None  # end node
        self.shortest_path = [] # nodes in shortest path

    # Method sets up distances initially to all nodes
    # Undiscovered nodes are set to maxint so they can be updated when
    # a shorter path is found.
    def setup_distances(self):
        for node in self.nodes:
            if node == self.start:
                self.distance_node[node] = 0
            else:
                self.distance_node[node] = sys.maxsize

    def alternate_path(self, pq_key, pq_dict):  # Method to calculate alternate paths
        alt_path_value = None

        # For each neighbour in currently selected parent node , we must check all possible paths from it
        for neighbour in self.nodes[pq_key]:
            alt_path_value = self.nodes[pq_key][neighbour] + self.distance_node[pq_key]

            # If alt path is of shorter value that the path already exisiting , update values with new one.
            if alt_path_value < self.distance_node[neighbour]:
                self.distance_node[neighbour] = alt_path_value  # new shortest distance to neighbour node is alt path
                self.visited_nodes[neighbour] = pq_key  # neighbour node has been visited
                if alt_path_value < pq_dict[neighbour]:  # make changes to priority queue for new shorter length path
                    pq_dict[neighbour] = alt_path_value

    def create_path(self):  # Method to work out shortest path
        route_node = self.end
        found_start_node = False  # bool to check if start node has been found

        while not found_start_node:  # Tracing back from end node until start node found
            if self.visited_nodes[route_node] == self.start:
                self.shortest_path.append(route_node)  # adds penultimate node to sp
                self.shortest_path.append(self.visited_nodes[route_node])   # adds first node (start node)
                found_start_node = True
            else:
                self.shortest_path.append(route_node)
                route_node = self.visited_nodes[route_node]
        self.shortest_path = self.shortest_path[::-1]  # Reverse list as end node was 'start' node when tracing back

    def calc_shortest_path(self):  # Method that calculates shortest path through graph

        import Priorityqueue as PQ # Priority queue module imported

        self.setup_distances()  # calling member method

        pq = PQ.PriorityQueue()  # Priority queue class called using composition

        pq_dict = pq.setup_pq(self.nodes, self.start, self.end)  # holds dictionary that is priority queue

        while len(pq_dict) != 0:  # When pq is empty all nodes have been checked so algorithm has completed
            pq_key = pq.lowest_value()  # holds key of element that had highest priority
            self.alternate_path(pq_key, pq_dict)  # alt path method called

            if self.start == self.end:  # If start and end node are same then distance is zero and algorithm ends
                tk.messagebox.showinfo('title', "start and end vertex same so distance is zero")
                break

            if pq_key == self.end:  # If end node has been found algorithm can end as shortest path to it was found
                self.create_path()
                break
