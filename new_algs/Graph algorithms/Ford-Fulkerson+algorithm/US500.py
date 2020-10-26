import networkx as nx
from collections import defaultdict
import LongestPath as LP
import EdmondKarp as EK
import time

"""
Instructions to execute the code
run as : python3 US500.py

The purpose of this file is to run the algorithm on US airports dataset
"""

if __name__ == '__main__':
    # Start the execution time to check performance
    start_time = time.time()

    # read the list of edges in networkx graph object
    G = nx.read_weighted_edgelist('datasets/USAirport_500.txt', delimiter=' ', nodetype=int)

    # calculate capacity matrix from the graph
    capMat = defaultdict(list)  # [[0]*mygraph.number_of_nodes()]*mygraph.number_of_nodes()

    for each in G.edges():
        capMat[each[0]].append(each[1])

    # run the function from LongestPath file to get the longest path in the graph
    all_paths, max_len, max_paths = LP.run_the_algo(capMat)
    all_flows=[]
    start_time = time.time();

    # If there are multiple longest paths calculate max flow for all 
    for eachLongPath in max_paths:
        print("--------------------------------------------------------------------")
        print(eachLongPath[0],"---",eachLongPath[-1])
        all_flows.append(EK.save_to_txt_and_read(nxGraph=G, weightLabel="weight", s=eachLongPath[0],t=eachLongPath[-1]))

    print("Maximum of all--->",max(all_flows))
    print('Number of augmenting paths: %s' % str(EK.numberOfPaths - 1))
    print("--- %s seconds ---" % (time.time() - start_time))
    #printableMatrix = nx.to_numpy_matrix(G, weight="weight")

#print(printableMatrix[1])