"""
Title: Implementation of Girvan-Newman Algorithm and Network Modularity
for Unweighted and Undirected Graphs

Course: MSBD5008 - Introduction to Social Computing (Assignment 1)

Author: Rohini BANERJEE (Student ID: 20543577)

"""

"""Import necessary libraries"""
import pandas as pd
import networkx as nx

# Uncomment the following two lines to save the console information onto a textfile
# import sys
# sys.stdout = open('output.txt','wt')

"""Function to obtain the degree of each node in a network from its adjacency matrix.
Degree is defined as the number of neighbors a node is connected to."""
def get_node_degree(adjacent_matrix):
    #Index of the degree list will correspond to network node name
    degree = []
    for row in adjacent_matrix:
        degree.append(sum(x!=0 for x in row))
    return degree

"""Function to get the cross product of two dataframes."""
def get_cartesian_product(left, right):
    #This assigns a temporary key called 'key' to merge the dataframes
    return (left.assign(key=1).merge(right.assign(key=1), on='key').drop('key', 1))

"""Function to obtain the shortest path between any two nodes via Breadth First Search."""
def get_shortest_path(graph, node_src, node_dst):
    visited = [] #maintain list of visited nodes
    Q = [[node_src]] #queue of paths to be checked during BFS
    #Check all possible paths between the two nodes
    while len(Q)!=0:
        bfs_path = Q.pop(0) #start the path
        node = bfs_path[-1] #get the last node to check all neighbors
        if node not in visited:
            successors = graph[node] #get all connected neighbors of the node
            #Search all un-visited neighboring nodes
            for successor in successors:
                shortest_path = list(bfs_path)
                shortest_path.append(successor) #append neighboring nodes to existing path
                Q.append(shortest_path) #add path to the queue
                if successor == node_dst:
                    return shortest_path #return the shortest path when final node is reached
            visited.append(node) #mark node visit as complete
    return [] #no path was found between the two nodes, hence append null set

"""Function to calculate the edge betweenness of a network."""
def get_edge_betweenness(graph):
    #Initialize all edges to have 0 betweenness
    betweenness =  {tuple(k): 0 for k in graph.edges()}
    #Get the shortest paths for all the node combinations found via their cross product
    all_shortest_paths = []
    for row in ALL_NODE_COMBINATIONS:
        all_shortest_paths.append(get_shortest_path(graph, row[0],row[1]))
    #Calculate betweenness for the required (i.e., existing) edges only
    for key in betweenness:
        for path in all_shortest_paths:
            #Count the number of times the two nodes occur in various shortest paths
            if (key[0] in path) and (key[1] in path):
                betweenness[key] += 1.0
    return betweenness

"""Function to obtain the maximum betweenness of a network."""
def get_max_edge_betweenness(betweenness):
    max_edge_betweenness = []
    #Obtain the highest betweenness in a network
    max_betweenness = max(betweenness.items(), key=lambda x: x[1])[1]
    #Find the corresponding node pair (i.e, key) for the highest betweenness (i.e., value)
    for edge,betwn in betweenness.items():
        if betwn == max_betweenness:
            max_edge_betweenness.append(edge)
    #Return all the node pairs having maximum edge betweenness
    return max_edge_betweenness

"""Function to calculate the modularity of a network from its adjacency matrix."""
def get_community_modularity(adjacent_matrix,clusters):
    modularity = 0 #initilize to 0
    num_clus = len(clusters)
    #Formula: Mod = (summation of S (summation for i, j in S of Aij - ki*kj/2m))
    #Where: ki and kj are the degrees of node i and node j in the original network
    #and m is the total number of edges in the original network
    for cluster in clusters:
        for node_i in cluster:
            for node_j in cluster:
                temp_var = (NETWORK_DEGREE[node_i]*NETWORK_DEGREE[node_j])/(2.0*NUM_EDGES)
                modularity += adjacent_matrix[node_i][node_j] - temp_var
    modularity /= 2.0*NUM_EDGES
    #Directly append number of clusters and corresponding modularity to the global variable
    CLUSTER_MODULARITY.append([num_clus,modularity])

"""Function to perform the Girvan-Newman hierarchical decompostion of a given network."""
def GN_hierarchical_decomposition(graph):
    G = graph.copy()
    all_decomposition = [] #will store all the decompositions
    #Find the Girvan-Newman decomposition of the network till no edges are left
    while G.number_of_edges():
        gn_decomposition = []
        #Find edge betweenness of the network
        betweenness = get_edge_betweenness(G)
        #Find and remove the edges with maximum edge betweenness
        max_edge_betweenness = get_max_edge_betweenness(betweenness)
        G.remove_edges_from(max_edge_betweenness)
        #Obtain all connected components of the network
        clusters = nx.connected_components(G)
        for cluster in clusters:
            gn_decomposition.append(list(cluster))
        #Sort by reverse length so that output comes in the required format
        #i.e., the clusters with more nodes are printed out first
        gn_decomposition.sort(key=len, reverse=True)
        print(tuple(gn_decomposition))
        #Calculate modularity for the decomposed clusters
        adj = nx.to_numpy_matrix(G).tolist() #change to adjacency matrix first!
        get_community_modularity(adj,gn_decomposition)
        #Store all the hierarchical network decompositions
        all_decomposition.append(gn_decomposition)
    return all_decomposition


"""----------------------------------------MAIN------------------------------------------------"""
#Reading the file with the adjacency matrix (first line reflects number of nodes)
#NOTE: File format must be maintained (delimiter is assumed to be space - change if required)
data = pd.read_csv("input.txt", skiprows=1, header=None, delimiter=" ")

#Directly obtain the number of nodes from the length of the adjacent matrix
NUM_NODES = len(data.index.tolist())

#Build a graph from the pandas adjacency matrix
network = nx.from_pandas_adjacency(data)

#Find the following for the modularity formula:
#(1)Degree of each node in the original network
#(2)Number of edges in the original network
NETWORK_DEGREE = get_node_degree(data.values)
NUM_EDGES = network.number_of_edges()

#Get a list of all possible combinations of nodes to find the shortest paths between them
node_df = pd.DataFrame(list(network.nodes()), columns=['node_name'])
node_cartesian = get_cartesian_product(node_df, node_df) #get a cross product between all nodes
#Remove rows with same nodes (i.e, [[0,0],[1,1]] etc.) from the cross product
node_cartesian = node_cartesian.query("node_name_x != node_name_y")
node_cartesian = node_cartesian.values.tolist()
#As the graph is undirected, remove duplicates, i.e., [0,1] and [1,0] are considered to be same
ALL_NODE_COMBINATIONS = list(set([tuple(sorted(x)) for x in node_cartesian]))
ALL_NODE_COMBINATIONS = [list(x) for x in ALL_NODE_COMBINATIONS]

#Save cluster number and corresponding modularity e.g. [[3,0.4563],[5,0.8765]]
CLUSTER_MODULARITY = []

#Get the Girvan-Newman hierarchical decomposition of the network
print("\nnetwork decomposition:")
all_possible_communities = GN_hierarchical_decomposition(network)
print("\n")

#Get the number of clusters & modularity for each decomposition of the above GN algorithm
for row in CLUSTER_MODULARITY:
    print(row[0],"clusters: modularity",round(row[1],4)) #round off modularity to 4 decimal places

#Get the index for the maximum modularity to get the optimal number of clusters
max_modularity_idx = CLUSTER_MODULARITY.index(max(CLUSTER_MODULARITY, key=lambda x: x[1]))
#Output the corresponding optimal community structure of the network
print("\noptimal structure:",tuple(all_possible_communities[max_modularity_idx]))