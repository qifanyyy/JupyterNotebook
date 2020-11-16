#!/usr/bin/python3

import itertools
import heapq
from scipy.sparse.csgraph import minimum_spanning_tree as min_tree
from TSPClasses import *
import numpy as np
import time
from munkres import Munkres
from which_pyqt import PYQT_VER
from heapq import *
import sys


if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None
        self.start_time = 0
        self.time_allowance = 0

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    def greedy(self, time_allowance=60.0):
        # Greedy algorithm to find a first tour fast that is near the optimal
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        bssf = None
        start_time = time.time()
        start_node = 0
        # Loop until a tour is found or we time out
        while time.time() - start_time < time_allowance and start_node < ncities:
            badTour = False
            current_matrix = self.generateInitialMatrix()
            route = []
            # Start at the current start node, this will loop through every possible node as a start until a valid tour
            # is found or we time out
            current_node = start_node
            route.append(cities[current_node])
            current_matrix = blockCol(current_matrix, current_node)
            # We loop through enough times to create the length of a tour
            for i in range(ncities - 1):
                # From our current node grab the index for the smallest cost
                current_node = self.findMinIndex(current_matrix, current_node)
                # if our current_node is infinite then that means the lowest cost was infinite so this won't be a valid tour
                if current_node == np.inf:
                    badTour = True
                    break
                # append the node to the route and update the matrix so we don't revisit
                route.append(cities[current_node])
                current_matrix = blockCol(current_matrix, current_node)
            # create a TSPSolution based on our tour, if we had a bad tour or if the cost is infinite then it is not valid
            # so throw it out and try the next node as our starting position
            cur_tour = TSPSolution(route)
            if badTour:
                cur_tour.cost = np.inf
            if bssf is None:
                if cur_tour.cost < np.inf:
                    bssf = cur_tour
                    foundTour = True
            else:
                if cur_tour.cost < bssf.cost:
                    bssf = cur_tour
                    foundTour = True
            start_node += 1
        self._global_bssf = bssf
        end_time = time.time()
        print("greedy", len(self._scenario.getCities()), end_time - self.start_time, bssf.cost)
        results['cost'] = bssf.cost if foundTour else np.inf
        results['time'] = end_time - start_time
        results['count'] = None
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    def branchAndBound(self, time_allowance=60.0):
        cities = self._scenario.getCities()
        ncities = len(cities)
        # Get graph from cities
        G = self.create_cities_matrix()
        # Reduce initial matrix and get reduction cost
        reduced_matrix, cost = self.get_cost(G)
        # Initialize path
        path = np.array([], dtype=int)
        # Initialize root
        root = Node(reduced_matrix, 0, -1, path, 0)
        root.path = path
        root.set_cost(cost)
        # Initialize Priority Queue and push root onto it
        pq = []
        heappush(pq, root)
        # Initialize best solution
        best_solution = None
        best_cost = np.inf
        # Initialize tracking variables
        nodes_created = 0
        nodes_pruned = 0
        max_pq_size = 0
        bssf_updates = 0

        # Track start time as to not go over time allowance
        start_time = time.time()
        # While the Priority Queue is not empty and we are within the time allowance
        while len(pq) > 0 and time.time() - start_time < time_allowance:
            # Check for max Priority Queue size
            if max_pq_size < len(pq):
                max_pq_size = len(pq)
            # Pop from Priority Queue and examine Node
            current_node = heappop(pq)

            # If cost is greater than the best solution, prune
            if current_node.cost >= best_cost:
                nodes_pruned = nodes_pruned + 1
                continue

            # Check if Node it a leaf
            if current_node.visited_num == ncities:
                # If node is a leaf:
                # Set it to best solution if its cost is less than the current best solution or no best solution exists yet
                if best_solution is None or current_node.cost < best_solution.cost:
                    best_solution = current_node
                    best_cost = current_node.cost
                    bssf_updates = bssf_updates + 1
                    continue

            # Loop through all paths connected to current city where the cost is not infinity
            # This excludes cities that have already been visited
            i = current_node.city_num
            for j in range(ncities):
                if current_node.reduced_matrix[i, j] != np.inf:
                    # If the cost of the current city plus the path to the next one is more than the best solution, prune
                    if current_node.cost + current_node.reduced_matrix[i, j] >= best_cost:
                        nodes_pruned = nodes_pruned + 1
                        continue

                    # Create Node for current city
                    next_node = Node(current_node.reduced_matrix, i, j, current_node.path, current_node.visited_num + 1)
                    nodes_created = nodes_created + 1
                    # Create reduced matrix for current Node
                    new_reduced_matrix, cost = self.get_cost(next_node.reduced_matrix)
                    next_node.reduced_matrix = new_reduced_matrix
                    # Set cost and priority for current Node
                    next_node.set_cost(current_node.cost + current_node.reduced_matrix[i, j] + cost)

                    # If cost of current Node is greater than the best solution, prune
                    if next_node.cost >= best_cost:
                        nodes_pruned = nodes_pruned + 1
                        continue

                    # If it makes it here, Node is still valid
                    # Push Node onto Priority Queue
                    heappush(pq, next_node)

        # Populate results
        results = {}
        foundTour = False
        count = 0
        route = []
        bssf = None
        # Now build the route using the BSSF
        if best_solution is not None:
            for i in range(ncities):
                route.append(cities[best_solution.path[i]])
            count += 1
            bssf = TSPSolution(route)
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True

        end_time = time.time()
        print("branch", len(self._scenario.getCities()), " ", end_time - self.start_time, " ", bssf.cost)
        results['cost'] = bssf.cost if count > 0 else math.inf
        results['time'] = end_time - start_time
        results['count'] = bssf_updates
        results['soln'] = bssf
        results['max'] = max_pq_size
        results['total'] = nodes_created
        results['pruned'] = nodes_pruned
        return results

    def get_cost(self, G):
        # Copy the matrix passed in so that it doesn't affect other states
        reduced_matrix = G.copy()

        # Reduce rows
        reduced_matrix, row_cost = self.row_reduction(reduced_matrix)
        # Reduce columns
        reduced_matrix, col_cost = self.column_reduction(reduced_matrix)

        # Return reduced matrix and the cost to reduce the matrix
        return reduced_matrix, (row_cost + col_cost)

    def row_reduction(self, G):
        # Initialize variables
        cities = self._scenario.getCities()
        ncities = len(cities)
        reduced_matrix = G
        infinity = np.inf

        # Initialize values from reduction to be infinity
        reduced_row = np.full(ncities, infinity)
        # Get the smallest number from each row
        for i in range(ncities):
            for j in range(ncities):
                if reduced_matrix[i, j] < reduced_row[i]:
                    reduced_row[i] = reduced_matrix[i][j]
                    # If 0 is in row, no need to check the rest of the row
                    if reduced_row[i] == 0:
                        break

        # Subtract the smallest number from each row
        for i in range(ncities):
            # If 0 or infinity, no need to subtract from row
            if reduced_row[i] == infinity or reduced_row[i] == 0:
                reduced_row[i] = 0
            else:
                new_row = np.subtract(reduced_matrix[i], reduced_row[i])
                reduced_matrix[i] = new_row

        # Return the matrix with the reduced values and the sum of all smallest values from each row
        return reduced_matrix, np.sum(reduced_row)

    def column_reduction(self, G):
        # Initialize variables
        cities = self._scenario.getCities()
        ncities = len(cities)
        reduced_matrix = G
        infinity = np.inf

        # Initialize values from reduction to be infinity
        reduced_col = np.full(ncities, infinity)
        # Get the smallest number from each column
        for i in range(ncities):
            for j in range(ncities):
                if reduced_col[j] > reduced_matrix[i, j]:
                    reduced_col[j] = reduced_matrix[i, j]

        # Subtract the smallest number from each column
        for i in range(ncities):
            for j in range(ncities):
                # If 0 or infinity, no need to subtract from cell
                if reduced_col[j] == 0 or reduced_col[j] == infinity:
                    reduced_col[j] = 0
                else:
                    reduced_matrix[i, j] = reduced_matrix[i, j] - reduced_col[j]

        # Return the matrix with the reduced values and the sum of all smallest values from each column
        return reduced_matrix, np.sum(reduced_col)

    def create_cities_matrix(self):
        cities = self._scenario.getCities()
        ncities = len(cities)

        # Initialize cities matrix ncities x ncities with infinity in all cells
        cities_matrix = []
        for i in range(ncities):
            row = []
            for j in range(ncities):
                row.append(np.inf)
            cities_matrix.append(row)

        # Populate the matrix by getting the cost of all edges
        for i in range(ncities):
            for j in range(ncities):
                city1 = cities[i]
                city2 = cities[j]
                cities_matrix[i][j] = city1.costTo(city2)

        # Convert to NumPy array
        return_array = np.array(cities_matrix)
        return return_array

    def generateInitialMatrixBranch(self):
        i = 0
        j = 0
        cities = self._scenario.getCities()
        ncities = len(cities)
        matrix = np.empty([ncities, ncities])
        for i in range(ncities):
            for j in range(i,ncities):
                matrix[i, j] = cities[i].costTo(cities[j])
        return matrix

    def fancy(self, time_allowance=60.0):
        sys.setrecursionlimit(1500)
        results = {}
        self.start_time = time.time()
        self.time_allowance = time_allowance
        initial_matrix = self.generateInitialMatrix()
        # print("initial matrix:")
        # print(time.time()-self.start_time)
        # print("{}\n".format(initial_matrix))
        min_tree = self.minTree(initial_matrix)
        # print("min_tree:")
        # print(time.time()-self.start_time)
        # print("{}\n".format(min_tree))
        odd_verts = self.getOddVerts(min_tree)
        # print("oddverts:")
        # print(time.time()-self.start_time)
        # print("percent odd" + str(len(odd_verts) * 100 / initial_matrix.shape[0]))
        # perfect = self.perfectMatchNetwork(odd_verts,initial_matrix,min_tree)
        perfect = self.perfectMatchGreedy(odd_verts, initial_matrix.copy())
        # print("perfectGreedy:")
        # print(time.time()-self.start_time)
        multigraph, num_edges = self.multigraph(min_tree, perfect)
        # self.convert_to_dir_graph(multigraph)
        # num_edges = self.getEdges(multigraph)
        # if len(self.getOddVerts(multigraph)) != 0:
            # print("Uneven nodes!!!")
        # print("multigraph:")
        # print(time.time()-self.start_time)
        # print("{}\n".format(multigraph))
        # print(num_edges)
        euclidGraph = self.hierholzer(multigraph, num_edges, len(initial_matrix))
        # print("euclidian:")
        # print(time.time()-self.start_time)
        # print(euclidGraph)
        tour, tracker = self.shortcut(euclidGraph)
        # print(tracker)
        christof_aprox = TSPSolution(tour)
        end_time = time.time()
        print("fancy", len(self._scenario.getCities()), " ", end_time - self.start_time, " ", christof_aprox.cost)
        results['cost'] = christof_aprox.cost
        results['time'] = end_time - self.start_time
        results['count'] = None
        results['soln'] = christof_aprox
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    def generateInitialMatrix(self):
        i = 0
        j = 0
        cities = self._scenario.getCities()
        ncities = len(cities)
        matrix = np.empty([ncities, ncities])
        for i in range(ncities):
            for j in range(ncities):
                matrix[i, j] = cities[i].costTo(cities[j])
        return matrix

    def getOddVerts(self, matrix):
        odds = []
        for i in range(matrix.shape[0]):
            size = 0
            for j in range(matrix.shape[0]):
                if matrix[i, j] > 0:
                    size += 1
            for k in range(matrix.shape[0]):
                if matrix[k, i] > 0:
                    size += 1
            if (size % 2) != 0:
                odds.append(i)
        return odds

    def minTree(self, matrix):
        min_matrix = min_tree(matrix)
        min_matrix = min_matrix.toarray().astype(float)
        return min_matrix

    def findMinIndex(self, matrix, row):
        minIndex = np.inf
        min = np.inf
        for i in range(matrix.shape[1]):
            if matrix[row, i] < min:
                minIndex = i
                min = matrix[row, i]
        return minIndex

    # Source: https://github.com/sonph/pygraph/blob/master/pygraphalgo.py
    def hierholzer(self, graph, num_edges, node_count):
        # Initialize variables
        start_vertex = 0
        circuit = [start_vertex]
        edges_visited = 0
        current_node_index = 0
        # Loop through all vertices in the circuit and make sure they don't have any unvisited edges
        while edges_visited <= num_edges:
            # Initialize current path to be updated from following the edge to the next vertex
            curr_path = []
            edges_visited = self.search_new_vertex(
                graph, circuit[current_node_index], curr_path, start_vertex, node_count, edges_visited)
            current_node_index += 1
            insert_index = current_node_index
            # Add the new path to the current circuit
            for i in range(len(curr_path)):
                circuit.insert(insert_index, curr_path[i])
                insert_index += 1
            if current_node_index >= len(circuit):
                break

        return circuit

    def convert_to_dir_graph(self, graph):
        # Loop through every cell and make sure that its inverse cell is equal to it
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[i, j] != np.inf and graph[i, j] != graph[j, i]:
                    graph[j, i] = graph[i, j]

    def search_new_vertex(self, graph, u, curr_path, starting_vertex, node_count, edges_visited):
        # Loop through all edges that connect to the current vertex (u)
        for v in range(node_count):
            small = u
            big = v
            if small > big:
                small = v
                big = u
            # If an edge exists and it hasn't been visited
            if (small, big) in graph and graph[(small, big)] > 0:
                # Mark as visited
                edges_visited += 1
                graph[(small, big)] -= 1
                # Add it to the current path
                curr_path.append(v)
                # If we have completed the circuit, return; else, keep searching until the circuit is completed
                if v == starting_vertex:
                    break
                else:
                    edges_visited = self.search_new_vertex(
                        graph, v, curr_path, starting_vertex, node_count, edges_visited)
                    break
        return edges_visited
    #Utilizes the base algorithm found in the Christofides module
    def perfectMatchNetwork(self, vertices, matrix, min_matrix):
        newmatrix = np.zeros(min_matrix.shape)
        bipartite_set = [set(i) for i in itertools.combinations(set(vertices), len(vertices) // 2)]
        bipartite_graphs = self.bipartite_Graph(matrix, bipartite_set, vertices)
        indexes = self.min_Munkres(matrix, bipartite_graphs)
        for pair in indexes:
            newmatrix[pair[0]][pair[1]] = matrix[pair[0]][pair[1]]
        return newmatrix

    def bipartite_Graph(self, M, bipartite_set, odd_vertices):
        """
        """
        bipartite_graphs = []
        vertex_sets = []
        for vertex_set1 in bipartite_set:
            vertex_set1 = list(sorted(vertex_set1))
            vertex_set2 = []
            for vertex in odd_vertices:
                if vertex not in vertex_set1:
                    vertex_set2.append(vertex)
            matrix = [[np.inf for j in range(len(vertex_set2))] for i in range(len(vertex_set1))]
            for i in range(len(vertex_set1)):
                for j in range(len(vertex_set2)):
                    if vertex_set1[i] < vertex_set2[j]:
                        matrix[i][j] = M[vertex_set1[i]][vertex_set2[j]]
                    else:
                        matrix[i][j] = M[vertex_set2[j]][vertex_set1[i]]
            bipartite_graphs.append(matrix)
            vertex_sets.append([vertex_set1, vertex_set2])
        return [bipartite_graphs, vertex_sets]

    def min_Munkres(self,M, bipartite_graphs):
        """Implements the Hungarian problem or the Assignment problem to
        find Minimum Cost Perfect Matching(MCPM).

        """
        m = Munkres()
        minimum = np.inf
        for index, bipartite_graph in enumerate(bipartite_graphs[0]):
            Munkres_indexes = m.compute(bipartite_graph)
            cost = self.Munkres_cost(Munkres_indexes, bipartite_graph)
            if cost < minimum:
                minimum = cost
                min_index = index
                min_Munkres_indexes = Munkres_indexes
        Munkres_indexes = [[] for i in range(len(min_Munkres_indexes))]
        for index, vertex_set in enumerate(min_Munkres_indexes):
            Munkres_indexes[index].append(bipartite_graphs[1][min_index][0][vertex_set[0]])
            Munkres_indexes[index].append(bipartite_graphs[1][min_index][1][vertex_set[1]])
        return Munkres_indexes

    def Munkres_cost(self, indexes, bipartite_graph):
        """Returns cost of the edges in Munkres_indexes

        """
        cost = 0
        for index in indexes:
            cost = cost + bipartite_graph[index[0]][index[1]]
        return cost

    def perfectMatchGreedy(self, vertices, matrix):
        newmatrix = np.zeros(matrix.shape)
        numvertices = len(vertices)
        # mark distances to all even degree vertexes as infinity
        for i in range(matrix.shape[0]):
            if i not in vertices:
                matrix[i] = math.inf
                for j in range(matrix.shape[1]):
                    matrix[j][i] = math.inf
        while len(vertices) != 0:
            # there should always be an even number of vertices
            if len(vertices) == 1:
                print("this should never happen")
            else:
                pos = np.argmin(matrix)
                cols = matrix.shape[0]
                # calculate location of smallest edge
                y = np.mod(pos, cols)
                x = pos // matrix.shape[0]
                # check if both vertices are in still in contention
                if x in vertices and y in vertices:
                    #removed check for minMatrix
                    if matrix[x][y] != np.inf:
                        # print("adding match edge --> y (col) = {}, x (row) = {}".format(y, x))
                        # print("{}\n".format(matrix))
                        #when a position is found, remove the two vertices from the array
                        vertices.remove(x)
                        vertices.remove(y)
                        newmatrix[x][y] = matrix[x][y]
                        matrix[x] = np.inf
                        matrix[y] = np.inf
                    #once a position has been considered, mark it as infinity so that the next one can be found
                    matrix[x][y] = math.inf
                    matrix[y][x] = math.inf
                    if not vertices:
                        return newmatrix
                else:
                    matrix[x][y] = math.inf
                    matrix[y][x] = math.inf
                    continue
        return newmatrix

    def checkPerfect(self, matrix, numvertices):
        # get the minimum values of each column
        min = matrix.max(1)
        # if vertices // 2 edges have been added, it is a perfect match
        if np.count_nonzero(min) == numvertices // 2:
            return True
        else:
            return False

    def multigraph(self, matrix, perfectMatrix):
        returnedDict = {}
        numEdges = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0]):
                if i < j:
                    start = i
                    end = j
                else:
                    start = j
                    end = i
                if matrix[i][j] != 0 or perfectMatrix[i][j] != 0:
                    if (start, end) not in returnedDict:
                        returnedDict[(start, end)] = 1
                    else:
                        returnedDict[(start, end)] += 1
                    if matrix[i][j] != 0 and perfectMatrix[i][j] != 0:
                        returnedDict[(start, end)] += 1
                        numEdges += 1
                    numEdges += 1
        return returnedDict, numEdges

    def shortcut(self, circuit):
        # follow Eulerian circuit adding vertices on first encounter
        cities = self._scenario.getCities()
        Tour = []
        tracker = []
        for vert in circuit:
            if vert not in tracker:
                tracker.append(vert)
                Tour.append(cities[vert])

        return Tour, tracker

    def getEdges(self, matrix):
        toReturn = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0]):
                if matrix[i][j] != np.inf:
                    toReturn += 1
        return toReturn
