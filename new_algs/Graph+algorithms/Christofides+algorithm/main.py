import os
from os import listdir
from os.path import isfile, join
import sys
import numpy as np
import time
import matplotlib.pyplot as plt
from copy import copy, deepcopy

from TSPFile import TSPFile
from primalgorithm import PrimAlgorithm
from tabusearch import TabuSearch
from grasp import grasp
from ils import ils

# Flag that controls if intermediary plots showing each steps of the 
# Christofides should be printed or not
# Flag que controle se gráficos intermediários mostrando cada etapa do 
# algortimo de Christofides devem ser exibidos ou não
show_intermediary_steps_graphs = False
source_indexes_visited = []
best_destiny_indexes_visited = []

def main():
    # Read all instances and store it in an array of TSPFile objects
    tsp_files = compute_tsp_instances()

    # For each instance apply some heuristic based on christofides algorithm
    for tsp_file in tsp_files:
        # Set of expensive edges visited
        pairs_visited = [False] * tsp_file.dimension
        for i in range(tsp_file.dimension):
            pairs_visited[i] = [False] * tsp_file.dimension
        
        # Set of root nodes visited
        roots_visited = [False] * tsp_file.dimension

        # Capture the initial time
        start_time = time.time()

        # Get the cycle by christofides's algorithms
        euler_cycle = christofides(tsp_file)

        # Apply a Variable Neighborhood Descent metaheuristic to improve the current solution
        euler_cycle = variable_neighborhood_descent(tsp_file, euler_cycle, 100, pairs_visited, roots_visited)

        # Apply a Tabu Search metaheuristic to improve the current solution
        memory_size = tsp_file.dimension
        tabu_search_algorithm = TabuSearch(memory_size, tsp_file, euler_cycle)
        euler_cycle = tabu_search_algorithm.tabu_search()

        # # Apply a Greedy Randomized Adaptative Search Procedure Meteheuristic to improve current solution
        grasp_instance = grasp(tsp_file, euler_cycle)
        euler_cycle = grasp_instance.grasp()

        # Apply a Iterated Local Search Meteheuristic to improve current solution.
        # The perturbation function works 2 minutes in an attempt to improve current solution.
        # It apply a cut with a fixed length in current solution and apply a nearest neighborhood 
        # heuristic in the nodes inside that cut.
        ils_instance = ils(tsp_file, euler_cycle)
        euler_cycle = ils_instance.ils()

        # Capture the final time
        elapsed_time = time.time() - start_time

        # Present the final solution for the user
        show_final_solution(tsp_file, euler_cycle, elapsed_time)

def compute_tsp_instances():
    tsp_files = np.array([])

    mypath = 'Instances/EUC_2D'
    tsp_files = np.append(tsp_files, [read_files_in_directory(mypath)])

    mypath = 'Instances'
    tsp_files = np.append(tsp_files, [read_files_in_directory(mypath)])

    return tsp_files

def read_files_in_directory(mypath):
    tsp_files = np.array([])
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in filenames:
        tsp_file = TSPFile()
        name, ext = os.path.splitext(filename)
        if ext == '.tsp':
            filepath = mypath + '/' + filename
            f = open(filepath)
            line = f.readline()
            while line:
                param = ''
                value = ''
                if ':' in line:
                    [param, value] = line.split(':')
                else :
                    param = line
                tsp_file.fill_props(param, value)
                line = f.readline()
            f.close()
            # After closing the file the adjacency matrix should be computed
            # Após fechar o arquivo a matriz de adjacência deve ser computada
            tsp_file.compute_adjacency_matrix()
            tsp_files = np.append(tsp_files, [tsp_file])
    return tsp_files

def christofides(tsp_file):
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 1 - Calculate minimum spanning tree T
    # 1 - Calculo da árvore geradora mínima através do algoritmo de PRIM
    minimum_spanning_tree = compute_minimum_spanning_tree(tsp_file)
    
    if show_intermediary_steps_graphs == True:
        plt.scatter(tsp_file.x_coord, tsp_file.y_coord)
        for i in range(tsp_file.dimension):
            plt.annotate(str(i), (tsp_file.x_coord[i], tsp_file.y_coord[i]))
            if minimum_spanning_tree[i] != -1:
                plt.plot([tsp_file.x_coord[i], tsp_file.x_coord[minimum_spanning_tree[i]]],[tsp_file.y_coord[i], tsp_file.y_coord[minimum_spanning_tree[i]]],'k-')
        plt.title(tsp_file.name + ' - MST')
        plt.figure()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 2 -  Calculate the set of vertices O with odd degree in T
    odd_degree_nodes = find_odd_degree_nodes(tsp_file, minimum_spanning_tree)

    if show_intermediary_steps_graphs == True:
        for i in range(tsp_file.dimension):
            if i in odd_degree_nodes:
                plt.plot(tsp_file.x_coord[i], tsp_file.y_coord[i], 'ro')
                plt.annotate(str(i), (tsp_file.x_coord[i], tsp_file.y_coord[i]))
        plt.title(tsp_file.name + ' - Odd Degree')
        plt.figure()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 3 - Form the subgraph of G using only the vertices of O
    subgraph_odd_degree_nodes = subgraph_only_odd_degree_nodes(tsp_file, odd_degree_nodes)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 4 - Construct a minimum-weight perfect matching M in this subgraph
    matching  = construct_minimum_weight_perfect_matching(tsp_file, subgraph_odd_degree_nodes)
    
    if show_intermediary_steps_graphs == True:
        for i in range(tsp_file.dimension):
            if i in odd_degree_nodes:
                plt.plot(tsp_file.x_coord[i], tsp_file.y_coord[i], 'ro')
                plt.annotate(str(i), (tsp_file.x_coord[i], tsp_file.y_coord[i]))
                for j in range(tsp_file.dimension):
                    if matching[i][j] == True:
                        plt.plot([tsp_file.x_coord[i], tsp_file.x_coord[j]],[tsp_file.y_coord[i], tsp_file.y_coord[j]],'k-')
        plt.title(tsp_file.name + ' - Perfect Matching')
        plt.figure()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 5 - Unite matching and spanning tree T ∪ M to form an Eulerian multigraph
    spanning_tree_union_matching = minimum_matching_union_spanning_tree(tsp_file, matching, minimum_spanning_tree)

    if show_intermediary_steps_graphs == True:
        for i in range(tsp_file.dimension):
            plt.plot(tsp_file.x_coord[i], tsp_file.y_coord[i], 'ro')
            plt.annotate(str(i), (tsp_file.x_coord[i], tsp_file.y_coord[i]))
            for j in range(tsp_file.dimension):
                if spanning_tree_union_matching[i][j] == True:
                    plt.plot([tsp_file.x_coord[i], tsp_file.x_coord[j]],[tsp_file.y_coord[i], tsp_file.y_coord[j]],'k-')
        plt.title(tsp_file.name + ' - MST U Perfect Matching')
        plt.figure()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 6 - Calculate Euler tour and Remove repeated vertices
    euler_cycle  = compute_euler_tour(tsp_file, spanning_tree_union_matching)

    return euler_cycle

def variable_neighborhood_descent(tsp_file, euler_cycle, neighborhoods_max, pairs_visited, roots_visited):
    # Initialize control parameters and get the cost of the christofides solution
    n = 0 
    i = 0
    current_cost = 0
    best_cost = euler_tour_cost(tsp_file, euler_cycle)

    # Perform a given number of tries to improve the current solution
    # Another neighborhods are visited and only those which improve the current solution are 
    # accepted
    while n <= neighborhoods_max:
        n += 1
        euler_cycle_neighbor = choose_most_improving_neighbour(tsp_file, euler_cycle, n, pairs_visited, roots_visited)
        current_cost = euler_tour_cost(tsp_file, euler_cycle_neighbor)
        if current_cost < best_cost:
            best_cost = current_cost
            euler_cycle = euler_cycle_neighbor
            
    return euler_cycle

def euler_tour_cost(tsp_file, euler_cycle):
    cost = 0
    for i in range(tsp_file.dimension):
        for j in range(tsp_file.dimension):
            if euler_cycle[i][j] == True:
                cost += tsp_file.adjacency_matrix[i][j]
    return cost

# That function always choose the most expensive edge not already visited to improve
# It removes that connection and connect the root node (root_node_worst_edge) with the best node to him
# than it removes the antepenult connection to the (best_node_root_node)
# Than it connects the root node of the removed connection (best_node_root_node_next) with the node destiny of the
# most expensive edge (destiny_node_worst_edge) and connects the destiny node of the removed connection (best_node_root_node_next_next)
# with the node previos of the best node of the root node 
# If that move improves the solution it is accepted as current solution
def choose_most_improving_neighbour(tsp_file, euler_cycle, current_iteration, pairs_visited, roots_visited):
    root_node_worst_edge = 0
    destiny_node_worst_edge = 0
    best_node_root_node = 0
    
    max_distance = 0
    for i in range(tsp_file.dimension):
        for j in range(tsp_file.dimension):
            if i != j and (euler_cycle[i][j] == True) and (max_distance < tsp_file.adjacency_matrix[i][j]) and roots_visited[i] == False:
                max_distance = tsp_file.adjacency_matrix[i][j]
                root_node_worst_edge = i
                destiny_node_worst_edge = j

    min_distance_index_1 = sys.maxsize
    for j in range(tsp_file.dimension):
        if root_node_worst_edge != j and (euler_cycle[root_node_worst_edge][j] == False) and (tsp_file.adjacency_matrix[root_node_worst_edge][j] < min_distance_index_1) and (pairs_visited[root_node_worst_edge][j] == False):
            min_distance_index_1 = tsp_file.adjacency_matrix[root_node_worst_edge][j]
            best_node_root_node = j

    euler_cycle_neighbor = deepcopy(euler_cycle)
    euler_cycle_neighbor[root_node_worst_edge][destiny_node_worst_edge] = False
    euler_cycle_neighbor[root_node_worst_edge][best_node_root_node] = True

    best_node_root_node_source = 0
    best_node_root_node_destiny = 0
    for i in range(tsp_file.dimension):
        for j in range(tsp_file.dimension):
            if i != j and (best_node_root_node == i) and (euler_cycle[i][j] == True):
                best_node_root_node_destiny = j
            if i != j and (best_node_root_node == j) and (euler_cycle[i][j] == True):
                best_node_root_node_source = i

    best_node_root_node_next = 0
    for j in range(tsp_file.dimension):
        if euler_cycle_neighbor[best_node_root_node][j] == True:
           best_node_root_node_next = j 

    best_node_root_node_next_next = 0
    for j in range(tsp_file.dimension):
        if euler_cycle_neighbor[best_node_root_node_next][j] == True:
           best_node_root_node_next_next = j

    euler_cycle_neighbor[best_node_root_node_next][best_node_root_node_next_next] = False
    euler_cycle_neighbor[best_node_root_node_source][best_node_root_node] = False
    euler_cycle_neighbor[best_node_root_node_source][best_node_root_node_next_next] = True
    euler_cycle_neighbor[best_node_root_node_next][destiny_node_worst_edge] = True

    pairs_visited[root_node_worst_edge][best_node_root_node] = True

    if current_iteration == tsp_file.dimension:
        roots_visited[root_node_worst_edge] = True

    return euler_cycle_neighbor

def show_final_solution(tsp_file, euler_cycle, elapsed_time):
    cost = 0
    for i in range(tsp_file.dimension):
        plt.plot(tsp_file.x_coord[i], tsp_file.y_coord[i], 'ro')
        plt.grid(True)
        plt.annotate(str(i), (tsp_file.x_coord[i], tsp_file.y_coord[i]))
        for j in range(tsp_file.dimension):
            if euler_cycle[i][j] == True:
                cost += tsp_file.adjacency_matrix[i][j]
                plt.plot([tsp_file.x_coord[i], tsp_file.x_coord[j]],[tsp_file.y_coord[i], tsp_file.y_coord[j]],'k-')
    plt.title(tsp_file.name + ' - Algorithm\'s output (Cost = '+ str(cost) + '| Elapsed time = ' + str(round(elapsed_time, 5)) + ')')
    print('Instance: ' + str(tsp_file.name) + '- Cost: ' + str(cost) + ' - Elapsed time = ' + str(round(elapsed_time, 5)))
    #plt.show()

def compute_minimum_spanning_tree(tsp_file):
    prim_algorithm = PrimAlgorithm(tsp_file.adjacency_matrix)
    minimum_spanning_tree = prim_algorithm.primMST()
    del prim_algorithm
    return minimum_spanning_tree

def find_odd_degree_nodes(tsp_file, minimum_spanning_tree):
    odd_degree_nodes = []
    for i in range(tsp_file.dimension):
        count_degree = 0
        for j in range(tsp_file.dimension):
            if (minimum_spanning_tree[j] == i) or (minimum_spanning_tree[i] == j):
                count_degree += 1
        if (count_degree % 2) == 1:
            odd_degree_nodes.append(i)
    return odd_degree_nodes

def subgraph_only_odd_degree_nodes(tsp_file, odd_degree_nodes):
    subgraph_odd_degree_nodes = [0] * tsp_file.dimension
    for i in range(tsp_file.dimension):
        subgraph_odd_degree_nodes[i] = [0] * tsp_file.dimension

    for i in range(tsp_file.dimension):
        for j in range(tsp_file.dimension):
            if (i not in odd_degree_nodes) or (j not in odd_degree_nodes):
                subgraph_odd_degree_nodes[i][j] = 0
                subgraph_odd_degree_nodes[j][i] = subgraph_odd_degree_nodes[i][j]
            else:
                subgraph_odd_degree_nodes[i][j] = tsp_file.adjacency_matrix[i][j]
    return subgraph_odd_degree_nodes

def construct_minimum_weight_perfect_matching(tsp_file, subgraph_odd_degree_nodes):
    matching  = [False] * tsp_file.dimension
    for i in range(tsp_file.dimension):
        matching[i] = [False] * tsp_file.dimension

    for i in range(tsp_file.dimension):
        min = sys.maxsize
        match_node = -1
        for j in range(tsp_file.dimension):
            if subgraph_odd_degree_nodes[i][j] > 0 and subgraph_odd_degree_nodes[i][j] < min and matching[i][j] == False:
                min = subgraph_odd_degree_nodes[i][j]
                match_node = j
        if match_node > 0:
            matching[i][match_node] = True
    return matching

def minimum_matching_union_spanning_tree(tsp_file, matching, minimum_spanning_tree):
    spanning_tree_union_matching = [False] * tsp_file.dimension
    for i in range(tsp_file.dimension):
        spanning_tree_union_matching[i] = [False] * tsp_file.dimension

    for i in range(tsp_file.dimension):
        for j in range(tsp_file.dimension):
            if matching[i][j] == True:
                spanning_tree_union_matching[i][j] = True
            if (minimum_spanning_tree[i] == j):
                spanning_tree_union_matching[i][j] = True
    return spanning_tree_union_matching

def compute_euler_tour(tsp_file, spanning_tree_union_matching):
    euler_cycle  = [False] * tsp_file.dimension
    for i in range(tsp_file.dimension):
        euler_cycle[i] = [False] * tsp_file.dimension

    nodes_already_visited = np.array([]).astype(int)
    current_node = 0
    i = 0
    while i < tsp_file.dimension:
        nodes_already_visited = np.append(nodes_already_visited, [current_node])
        min_distance = sys.maxsize
        node_min_distance = -1
        for j in range(tsp_file.dimension):
            if (current_node != j) \
            and (spanning_tree_union_matching[current_node][j] == True \
                or spanning_tree_union_matching[j][current_node] == True) \
            and tsp_file.adjacency_matrix[current_node][j] < min_distance \
            and (j not in nodes_already_visited):
                min_distance = tsp_file.adjacency_matrix[current_node][j]
                node_min_distance = j
        if node_min_distance != -1:
            euler_cycle[current_node][node_min_distance] = True
            current_node = node_min_distance
        else:
            min_distance = sys.maxsize
            node_min_distance = -1
            for j in range(tsp_file.dimension):
                if (current_node != j) \
                and tsp_file.adjacency_matrix[current_node][j] < min_distance \
                and (j not in nodes_already_visited):
                    min_distance = tsp_file.adjacency_matrix[current_node][j]
                    node_min_distance = j
            if node_min_distance != -1:
                euler_cycle[current_node][node_min_distance] = True
                current_node = node_min_distance
            else:
                euler_cycle[current_node][0] = True
                current_node = 0
        i += 1
    return euler_cycle

if __name__ == '__main__':
    main()