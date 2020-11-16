# Reads a coordinate file and parses the results into an array of coordinates.
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from matplotlib.collections import LineCollection
from scipy import spatial
import time
import math
"""
# initial values
FILENAME = "SampleCoordinates.txt"
START_NODE = 0
END_NODE = 5
RADIUS = 0.08

"""
#Germany
FILENAME = "GermanyCities.txt"
START_NODE = 1573
END_NODE = 10584
RADIUS = 0.0025


def mercator_projection(latitude, longitude):

    r = 1
    x = r * math.pi * longitude / 180
    y = r * math.log(math.tan(np.pi / 4 + math.pi * latitude / 360))
    return x, y


def read_coordinate_file(filename):
    t = time.time()
    coordinates = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip('{}\n').split(sep=',')
            latitude = float(line[0])
            longitude = float(line[-1])
            coord = mercator_projection(latitude, longitude)
            coordinates.append(coord)
    print('Read_coordinate_file: {:4.3f}s'.format(time.time() - t))
    return np.array(coordinates)


def plot_points(coord_list, indices, path):
    t = time.time()
    fig = plt.figure()
    ax = fig.gca()

    city_connections = coord_list[indices]
    cheapest_route = coord_list[path]

    # Size for marker:
    # Sample City: 4, Hungary: 1, Germany: 0.1
    ax.plot(coord_list[:, 0], coord_list[:, 1], 'r.', markersize=0.1)                   # dotted cities
    ax.plot(cheapest_route[:, 0], cheapest_route[:, 1], 'b', linewidth=1)               # cheapest path route
    line_segments = LineCollection(city_connections, colors='grey', linewidths=0.2)     # city connections
    ax.add_collection(line_segments)
    ax.axis('equal')
    plt.title("Optimal Path")
    print('Plot_points excluding plt.show {:4.3f}s'.format(time.time() - t))
    plt.show()


def euclidean_norm(p1, p2):
    # calculates distance between point p1 and p2 with Euclidean norm
    """
    calculates distance between point p1 and p2 with Euclidean norm

    :param p1: [x,y] coordinate
    :param p2: [x,y] coordinate
    :return: distance
    """
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def construct_graph_connections(coord_list, radius):
    # Computes all connections between all points in coord_list within radius
    # Returns: Connections between all neighbouring cities and the cost of traveling between these cities
    t = time.time()
    cost = []
    city_connections = []

    for start, start_coord in enumerate(coord_list):
        for end, next_coord in enumerate(coord_list[start + 1:], start + 1):
            distance = euclidean_norm(start_coord, next_coord)
            if distance <= radius:
                cost.append(math.pow(distance, 9/10))
                city_connections.append([start, end])
    np_cost = np.array(cost)
    np_connections = np.array(city_connections)
    print('construct_graph_connections: {:4.3f}s'.format(time.time() - t))
    return np_connections, np_cost


def construct_fast_graph_connections(coord_list, radius):
    t = time.time()
    tree = spatial.cKDTree(coord_list)
    # returns a list of neighbors within the given radius of each node.
    start_ends = tree.query_ball_point(coord_list, radius)
    city_connections, cost = [], []
    # removing city connection doublets
    for start, ends in enumerate(start_ends):
        for end in ends:
            if start < end:
                distance = euclidean_norm(coord_list[start], coord_list[end])
                city_connections.append([start, end])
                cost.append(math.pow(distance, 9/10))

    np_connections = np.array(city_connections)
    np_cost = np.array(cost)
    print('construct_fast_graph_connections: {:4.3f}s'.format(time.time() - t))
    return np_connections, np_cost


def construct_graph(indices, costs, N):
    t = time.time()
    i = indices[:, 0]
    j = indices[:, 1]
    data = costs

    # At [i,j] in the sparse matrix, the cost of this route between i and j can be found.
    graph = csr_matrix((data, (i, j)), shape=(N, N))    # N is equal to amount of cities in coord_list
    print('construct_graph: {:4.3f}s'.format(time.time() - t))
    return graph


def cheapest_path(sparse_graph, start_node):
    """
    creates cheapest path represented by a distance matrix with cost of travel between nodes,
    and predecessor which  are used to reconstruct cheapest path.

    :param sparse_graph: sparse matrix [i, j], representing cost of route between i and j
    :param start_node: starting node, which the path should be computed for
    :return: distance as a  matrix with cheapest distance from node i, to node j through the graph.
            Predecessor as a matrix [i,j] of the shortest paths from point i. Each index  in predecessor[i,j] consists
             previous node which was passed when traveling from the start node i to node j through the graph.
    """
    # csgraph=sparse_graph, which is a matrix consisting distance between node i and j as described in documentation
    # directed=false, since the shortest path can be found from node i -> j, and j -> i.
    # indicies=start_node, which the path should be computed for
    # return_predecessors=True, since we need to reconstruct the shortest path later on. Described in documentation.
    distance, predecessor = dijkstra(csgraph=sparse_graph, directed=False, indices=start_node, return_predecessors=True)
    return distance, predecessor


def compute_path(predecessor, start_node, end_node):
    """
    computes path by going through predecessor list, FROM end node until start_node is found.

    :param predecessor: predecessor matrix [i,j] which is used to reconstruct the cheapest path from i to j
    :param start_node: starting node
    :param end_node: end node
    :return: cheapest path, FROM start node, TO end node
    """
    # start computation from end node
    current_pos = end_node
    # add first node (end node) to path, since this is the "start" of the computation
    path = [end_node]

    # loops throuh predecessor list as long as predecessor[current_pos] != starting node
    while current_pos != start_node:
        # predecessor[current_pos] represents the cheapest path to current_pos
        current_pos = predecessor[current_pos]
        # adds the current position to path
        path.append(current_pos)
    print("The cheapest path from {} to {}: {}".format(start_node, end_node, path[::-1]))
    # path is reversed, since the computation goes from end node -> start node,
    return path[::-1]


def print_cost_cheapest_path(dist, end_node):
    total_cost = dist[end_node]
    print("Total Cost: {}".format(total_cost))


t1 = time.time()
coordinate_list = read_coordinate_file(FILENAME)
# Slow version
# connections, travel_cost = construct_graph_connections(coordinate_list, RADIUS)
# Fast version
connections, travel_cost = construct_fast_graph_connections(coordinate_list, RADIUS)
constructed_graph = construct_graph(connections, travel_cost, N=len(coordinate_list))
dist_matrix, predecessor_matrix = cheapest_path(constructed_graph, START_NODE)
calculated_path = compute_path(predecessor_matrix, START_NODE, END_NODE)
t2 = time.time()
print_cost_cheapest_path(dist_matrix, END_NODE)
print('Task 6+7: {:4.3f}s'.format(time.time() - t2))
print('whole program: {:4.3f}s'.format(time.time() - t1))
plot_points(coordinate_list, connections, calculated_path)


