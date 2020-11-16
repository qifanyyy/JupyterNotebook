from GraphReadLib import get_graph
from KosarajuLib import kosaraju

import numpy as np

def get_scc_sizes(graph_name, nLargest):
    graph = get_graph(graph_name)

    # sort graph
    sortOrder = np.argsort(graph[:, 0])
    graph = graph[sortOrder, :]

    # Perform the Kosaraju algorithm to get the leaders for each node.
    # (the nodes reporting a shared leader will belong to the same SCC).
    leaders = kosaraju(graph)
    nLeaders = leaders.max()+1
    SCC_sizes = np.bincount(leaders)
    SCC_sizes[::-1].sort()

    return SCC_sizes[:nLargest]

def run_tests():
    # Do tests on small networks to check code
    results = np.zeros(4,dtype=bool)
    for iTest in [1,2,3,4]:
        t =  get_scc_sizes("SCCsmall" + str(iTest),5)
        correct_ans = np.load("SCCsmall" + str(iTest)+"ans.npy")
        results[iTest-1] = np.array_equal(correct_ans,t)

    print("Tests successful: " + str(min(results)))

run_tests()

# Calculate SCC sizes for large graph
res = get_scc_sizes("SCC",5)
print(res)

print('all done.')

