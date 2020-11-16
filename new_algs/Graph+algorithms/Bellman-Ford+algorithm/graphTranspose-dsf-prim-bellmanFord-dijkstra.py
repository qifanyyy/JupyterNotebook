# -*- coding: utf-8 -*-
"""
Topic: Graph theory, minimal spanning tree, shortest path, greedy algorithms
Implementation: graph transpose, in & out degree, depth-first-search
            prim's algorithm, bellman-ford algorithm, and dijkstra's algorithm
Name: Xiaolou Huang
Date: 11/12/2019
"""

import sys


# =============================================================================

class Graph(object):
    """docstring for Graph"""
    user_defined_vertices = []
    dfs_timer = 0

    def __init__(self, vertices, edges):
        super(Graph, self).__init__()
        n = len(vertices)
        self.matrix = [[0 for x in range(n)] for y in range(n)]
        self.vertices = vertices
        self.edges = edges
        for edge in edges:
            x = vertices.index(edge[0])
            y = vertices.index(edge[1])
            self.matrix[x][y] = edge[2]

    def display(self):
        print(self.vertices)
        for i, v in enumerate(self.vertices):
            print(v, self.matrix[i])

    def transpose(self):
        n = len(self.vertices)  # length of vertices
        for x in range(n):
            for y in range(x, n, 1):
                temp = self.matrix[x][y]
                self.matrix[x][y] = self.matrix[y][x]
                self.matrix[y][x] = temp

    def in_degree(self):
        n = len(self.vertices)  # length of vertices
        degree = [0 for i in range(n)]  # initialize 'degree' list
        for y in range(n):  # check every column (every vertex's in-degree)
            count = 0
            # check every row, if there is a 1, in-degree count + 1
            for x in range(n):
                if self.matrix[x][y] == 1:
                    count = count + 1
            degree[y] = count
        print("In degree of the graph:")
        self.print_degree(degree)

    def out_degree(self):
        n = len(self.vertices)  # number of vertices
        degree = [0 for i in range(n)]  # initialize 'degree' list
        for x in range(n):  # check every row (every vertex's out-degree)
            count = 0
            # check every column, if there is a 1, out-degree count + 1
            for y in range(n):
                if self.matrix[x][y] == 1:
                    count = count + 1
            degree[x] = count
        print("Out degree of the graph:")
        self.print_degree(degree)

    def dfs_on_graph(self):
        n = len(self.vertices)  # number of vertices
        discover = [0 for i in range(n)]
        finish = [0 for i in range(n)]

        # meaning of each field in list_v:
        # [vertex_name, order_number, color, discover_time, finish_time]
        list_v = []
        for x in range(n):
            list_v.append([self.vertices[x], x, "white", 0, 0])

        # visit every vertex in the graph
        self.dfs_timer = 0
        for i in range(n):
            if list_v[i][2] == "white":
                self.dfs_visit(list_v, i)

        # put discover time and finish time into two lists,
        # and print final results
        for i in range(n):
            discover[i] = list_v[i][3]
            finish[i] = list_v[i][4]
        self.print_discover_and_finish_time(discover, finish)

    # Helper function for dfs_on_graph().
    # param list_v: is a data structure contains necessary fields for a vertex.
    # param i: which vertex in list_v
    def dfs_visit(self, list_v, i):
        n = len(self.vertices)
        self.dfs_timer = self.dfs_timer + 1
        list_v[i][3] = self.dfs_timer  # record discover time of this vertex
        list_v[i][2] = "gray"

        # check all adjacency vertices
        for x in range(n):
            if self.matrix[list_v[i][1]][x] == 1 and list_v[x][2] == "white":
                self.dfs_visit(list_v, list_v[x][1])

        list_v[i][2] = "black"
        self.dfs_timer = self.dfs_timer + 1
        list_v[i][4] = self.dfs_timer  # record finish time of this vertex

    def prim(self, root):
        n = len(self.vertices)

        # prim_list stores fields needed for information about each iteration
        # prim_list fields:
        # [vertex_name, vertex_number, distance/weight/key/d, parent/pi]
        iteration = 0
        prim_list = []
        for i in range(n):
            if self.vertices[i] == root:  # for root, set distance to 0
                prim_list.append([self.vertices[i], i, 0, "None"])
            else:
                prim_list.append([self.vertices[i], i, sys.maxsize, "None"])

        # queue_list stores fields needed for remaining vertices to explore.
        # queue_list fields: [vertex_name, vertex_number, distance/weight/key]
        queue_list = []
        for i in range(n):
            if self.vertices[i] == root:   # for root, set distance to 0
                queue_list.append([self.vertices[i], i, 0])
            else:
                queue_list.append([self.vertices[i], i, sys.maxsize])

        # Initial output for self.print_d_and_pi()
        count = 0
        iteration = "Initial"
        d = []
        pi = []
        for v in prim_list:
            if v[2] == sys.maxsize:
                d.append("inf")
            else:
                d.append(v[2])
            pi.append(v[3])
        self.print_d_and_pi(iteration, d, pi)

        while queue_list:
            # get the vertex list from remaining queue_list with min value
            u = self.extract_min_prim(queue_list)
            for i in range(n):  # length of self.vertices
                # check if it's an adjacency vertex
                if self.matrix[u[1]][i] != 0:

                    # if this vertex in queue_list(the remaining vetices list),
                    # and the edge weight is greater than 0
                    # and less than the compared vertex weight,
                    # then reassign the parent and weight
                    for j in range(len(queue_list)):
                        if prim_list[i][0] == queue_list[j][0] \
                                and prim_list[i][2] > self.matrix[u[1]][i] > 0:
                            prim_list[i][3] = u[0]  # update parent
                            prim_list[i][2] = self.matrix[u[1]][i]  # update key
                            queue_list[j][2] = self.matrix[u[1]][i]  # update key in queue_list

            # format the output for self.print_d_and_pi()
            d = []
            pi = []
            iteration = count
            count = count + 1
            for v in prim_list:
                if v[2] == sys.maxsize:
                    d.append("inf")
                else:
                    d.append(v[2])
                pi.append(v[3])
            self.print_d_and_pi(iteration, d, pi)

    # Helper function for prim().
    # Return vertex in remaining list with min value
    def extract_min_prim(self, queue_list):
        u = []
        min_v = sys.maxsize
        for i in range(len(queue_list)):
            if queue_list[i][2] < min_v:
                u = queue_list[i]
                min_v = queue_list[i][2]
        queue_list.remove(u)
        return u

    def bellman_ford(self, source):
        n = len(self.vertices)

        # bellman_list stores the information about vertices for output results
        # bellman_list fields:
        # {vertex_name, vertex_order, distance/key/d, parent/pi}
        bellman_list = []
        for i in range(n):
            if self.vertices[i] == source:
                bellman_list.append({"name": self.vertices[i],
                                     "order": i,
                                     "key": 0,
                                     "pi": "None"})
            else:
                bellman_list.append({"name": self.vertices[i],
                                     "order": i,
                                     "key": sys.maxsize,
                                     "pi": "None"})
        # print(bellman_list)

        # initial formatted output for print_d_and_pi()
        count = 0
        d = []
        pi = []
        iteration = "Initial"
        for x in range(n):
            if bellman_list[x]["key"] == sys.maxsize:
                d.append("inf")
            else:
                d.append(bellman_list[x]["key"])
            pi.append(bellman_list[x]["pi"])
        self.print_d_and_pi(iteration, d, pi)

        # will relax edges in this order
        relax_list = [('t', 'x'),
                      ('t', 'y'),
                      ('t', 'z'),
                      ('x', 't'),
                      ('y', 'x'),
                      ('y', 'z'),
                      ('z', 'x'),
                      ('z', 's'),
                      ('s', 't'),
                      ('s', 'y')]

        for i in range(n - 1):  # in each iteration
            for j in range(len(relax_list)):  # for each edge in relax_list
                u = []
                v = []
                w = 0
                for k in range(n):  # for each sub-list in bellman_list
                    if bellman_list[k]["name"] == relax_list[j][0]:  # find vertex u
                        u = bellman_list[k]
                    elif bellman_list[k]["name"] == relax_list[j][1]:  # find vertex v
                        v = bellman_list[k]
                w = self.matrix[u["order"]][v["order"]]  # find w(u, v)
                self.relax(u, v, w)  # relax the edge

            # format output for print_d_and_pi()
            iteration = count
            count = count + 1
            for x in range(n):
                if bellman_list[x]["key"] >= sys.maxsize - 99999:
                    d[x] = "inf"
                else:
                    d[x] = bellman_list[x]["key"]
                pi[x] = bellman_list[x]["pi"]
            self.print_d_and_pi(iteration, d, pi)

        # check if there is a negative weight cycle
        for j in range(len(relax_list)):  # for each edge in relax_list
            u = []
            v = []
            w = 0
            for k in range(n):  # for each sub-list in bellman_list
                if bellman_list[k]["name"] == relax_list[j][0]:  # find vertex u
                    u = bellman_list[k]
                elif bellman_list[k]["name"] == relax_list[j][1]:  # find vertex v
                    v = bellman_list[k]
            w = self.matrix[u["order"]][v["order"]]  # find w(u, v)
            if v["key"] > u["key"] + w:
                return False
        return True

    # Helper function for bellman_ford() and dijkstra().
    # param u, v are vertices to check if need relax
    # param w is the weight of (u, v)
    def relax(self, u, v, w):
        if v["key"] > u["key"] + w:
            v["key"] = u["key"] + w  # update d/key
            v["pi"] = u["name"]  # update parent

    def dijkstra(self, source):
        n = len(self.vertices)

        # dijkstra_list stores information to output the results
        # dijkstra_list fields:
        # {vertex_name, vertex_order, if_visited, key/distance/d, parent/pi}
        dijkstra_list = []
        for i in range(n):
            if self.vertices[i] == source:
                dijkstra_list.append(
                    {"name": self.vertices[i],
                     "order": i,
                     "visited": "F",
                     "key": 0,
                     "pi": "None"})
            else:
                dijkstra_list.append(
                    {"name": self.vertices[i],
                     "order": i,
                     "visited": "F",
                     "key": sys.maxsize,
                     "pi": "None"})

        # vertices need to iterate through
        queue_list = list(self.vertices)

        # initial formatted output results for print_d_and_pi()
        iteration = "Initial"
        count = 0
        d = []
        pi = []
        for i in range(n):
            if dijkstra_list[i]["key"] == sys.maxsize:
                d.append("inf")
            else:
                d.append(dijkstra_list[i]["key"])
            pi.append(dijkstra_list[i]["pi"])
        self.print_d_and_pi(iteration, d, pi)

        # finding the shortest path for every vertex
        while queue_list:
            u = self.extract_min_dijkstra(dijkstra_list)  # u from dijkstra_list
            queue_list.remove(u["name"])
            u["visited"] = "T"
            for i in range(n):  # check adjacency matrix for adj[u]
                w = self.matrix[u["order"]][i]  # w is the weight of (u, v)
                if w != 0:  # if there is an edge from u to v
                    v = dijkstra_list[i]
                    self.relax(u, v, w)

            # format output results for print_d_and_pi()
            iteration = count
            count = count + 1
            for i in range(n):
                if dijkstra_list[i]["key"] == sys.maxsize:
                    d[i] = "inf"
                else:
                    d[i] = dijkstra_list[i]["key"]
                pi[i] = dijkstra_list[i]["pi"]
            self.print_d_and_pi(iteration, d, pi)

    # Get vertex with min value from unvisited vertices.
    def extract_min_dijkstra(self, dijkstra_list):
        u = []
        min_v = sys.maxsize
        for i in range(len(dijkstra_list)):
            if min_v > dijkstra_list[i]["key"] \
                    and dijkstra_list[i]["visited"] == "F":
                u = dijkstra_list[i]
                min_v = dijkstra_list[i]["key"]
        return u

    # Print out steps for prim algorithm.
    # param d, distance between two vertices
    # param pi, parent vertex
    def print_d_and_pi(self, iteration, d, pi):
        assert ((len(d) == len(self.vertices)) and
                (len(pi) == len(self.vertices)))

        print("Iteration: {0}".format(iteration))
        for i, v in enumerate(self.vertices):
            print("Vertex: {0}\td: {1}\tpi: {2}".format(v, 'inf' if d[i] == sys.maxsize else d[i], pi[i]))

    def print_discover_and_finish_time(self, discover, finish):
        assert ((len(discover) == len(self.vertices)) and
                (len(finish) == len(self.vertices)))
        for i, v in enumerate(self.vertices):
            print("Vertex: {0}\tDiscovered: {1}\tFinished: {2}".format(
                v, discover[i], finish[i]))

    def print_degree(self, degree):
        assert ((len(degree) == len(self.vertices)))
        for i, v in enumerate(self.vertices):
            print("Vertex: {0}\tDegree: {1}".format(v, degree[i]))


def main():
    # Thoroughly test your program and produce useful output.
    #  # Q1 and Q2
    graph = Graph(['1', '2'], [('1', '2', 1)])
    graph.display()
    graph.transpose()
    graph.display()
    graph.transpose()
    graph.display()
    graph.in_degree()
    graph.out_degree()
    graph.print_d_and_pi(1, [1, sys.maxsize], [2, None])
    graph.print_degree([1, 0])
    graph.print_discover_and_finish_time([0, 2], [1, 3])

    # # Q3
    graph = Graph(['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                  [('q', 's', 1),
                   ('s', 'v', 1),
                   ('v', 'w', 1),
                   ('w', 's', 1),
                   ('q', 'w', 1),
                   ('q', 't', 1),
                   ('t', 'x', 1),
                   ('x', 'z', 1),
                   ('z', 'x', 1),
                   ('t', 'y', 1),
                   ('y', 'q', 1),
                   ('r', 'y', 1),
                   ('r', 'u', 1),
                   ('u', 'y', 1)])
    graph.display()
    graph.dfs_on_graph()

    # # Q4 - Prim
    graph = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                  [('A', 'H', 6),
                   ('H', 'A', 6),
                   ('A', 'B', 4),
                   ('B', 'A', 4),
                   ('B', 'H', 5),
                   ('H', 'B', 5),
                   ('B', 'C', 9),
                   ('C', 'B', 9),
                   ('G', 'H', 14),
                   ('H', 'G', 14),
                   ('F', 'H', 10),
                   ('H', 'F', 10),
                   ('B', 'E', 2),
                   ('E', 'B', 2),
                   ('G', 'F', 3),
                   ('F', 'G', 3),
                   ('E', 'F', 8),
                   ('F', 'E', 8),
                   ('D', 'E', 15),
                   ('E', 'D', 15)])
    graph.prim('G')
    #
    # # Q5
    graph = Graph(['s', 't', 'x', 'y', 'z'],
                  [('t', 'x', 5),
                   ('t', 'y', 8),
                   ('t', 'z', -4),
                   ('x', 't', -2),
                   ('y', 'x', -3),
                   ('y', 'z', 9),
                   ('z', 'x', 7),
                   ('z', 's', 2),
                   ('s', 't', 6),
                   ('s', 'y', 7)])
    graph.bellman_ford('z')
    #
    # # Q5 alternate
    graph = Graph(['s', 't', 'x', 'y', 'z'],
                  [('t', 'x', 5),
                   ('t', 'y', 8),
                   ('t', 'z', -4),
                   ('x', 't', -2),
                   ('y', 'x', -3),
                   ('y', 'z', 9),
                   ('z', 'x', 4),
                   ('z', 's', 2),
                   ('s', 't', 6),
                   ('s', 'y', 7)])
    graph.bellman_ford('s')
    #
    # # Q6
    graph = Graph(['s', 't', 'x', 'y', 'z'],
                  [('s', 't', 3),
                   ('s', 'y', 5),
                   ('t', 'x', 6),
                   ('t', 'y', 2),
                   ('x', 'z', 2),
                   ('y', 't', 1),
                   ('y', 'x', 4),
                   ('y', 'z', 6),
                   ('z', 's', 3),
                   ('z', 'x', 7)])
    graph.dijkstra('s')
    #
    graph = Graph(['A', 'B', 'C', 'D', 'E'],
                    [('A', 'B', -1),
                     ('A', 'C', 4),
                     ('B', 'C', 3),
                     ('B', 'D', 2),
                     ('B', 'E', 2),
                     ('D', 'B', 1),
                     ('D', 'C', 5),
                     ('E', 'D', -3)])
    graph.bellman_ford('A')

if __name__ == '__main__':
    main()
