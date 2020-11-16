from FileReadLib import get_data
from FloydWarshallLib import floyd_warshall

n_graphs = 3

for i_graph in range(n_graphs):

    print("Working on graph %s..." % (i_graph + 1))

    filename = "g" + str(i_graph+1)
    n_nodes, n_edges, edges = get_data(filename)

    shortest_shortest_path = [[] for x in range(n_graphs)]

    # To determine the shortest shortest path, run the Floyd-Warshall algorithm
    shortest_paths, neg_cycle_exists = floyd_warshall(n_nodes, n_edges, edges)

    if neg_cycle_exists:
        print("Graph %s has at least one negative cycle." % (i_graph+1))
    else:
        sh_sh_path = shortest_paths.min()
        print("Graph %s has at no negative cycles and the shortest shortest path has length %s."
              % (i_graph + 1), sh_sh_path)


