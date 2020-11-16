import random


class MinCut:
    """
    Compute the minimum cut of a connected graph using Karger's algorithm
    with edge contraction
    """

    def __init__(self, graph, runs=lambda n: 2*n):
        """
        Compute the minimum cut for a given graph,
        with number of iterations defined by runs function
        """

        self._graph = graph
        self._mincut = None

        for i in range(runs(graph.v())):
            cut = self._find_mincut()
            if self._mincut is None or self._mincut > cut:
                self._mincut = cut

    def _find_mincut(self):
        """
        Run the contraction algorithm for a given graph and return the
        mincut found
        """

        v = self._graph.v()
        edges = list(self._graph.edges())

        while v > 2:
            # pick a random edge and contract
            p, q = random.choice(edges)
            # replace p--q connections with r--q ones
            for i in range(len(edges)):
                edge = edges[i]
                if p in edge:
                    r = edge[0] if edge[0] != p else edge[1]
                    edges[i] = r, q

            # remove self-loops (v--v)
            edges = [x for x in edges if x[0] != x[1]]

            v -= 1

        return len(edges)

    def mincut(self):
        """
        Return the mincut
        """

        return self._mincut
    name = "../data/KargerMinCut.txt"
    graph_file = open(filename)
    graph = {}
    global cuts
    cuts = []
    edge_num = 0
    edge_list = []
    # print "Loading from", filename
    for line in graph_file:
        node = int(line.split()[0])
        edges = []
        for edge in line.split()[1:]:
            edges.append(int(edge))
        graph[node] = edges
        edge_num = edge_num + len(edges)
        edge_list.append(len(edges))
    graph_file.close()

    f = open('../data/matrix.txt', 'w')
    for j in range(1, len(graph) + 1):
        for i in range(1, 201):
            if i not in graph[j]:
                f.write('0 ')
            else:
                f.write('1 ')
        f.write('\n')
    f.close()

    # # print the general info of the graph.
    count = 200
    i = 0
    while i < count:
        graph1 = copy.deepcopy(graph)
        g = MinCut(graph1, 2)
        # g = FastMinCut(graph1)
        i += 1

    print("Total edges:     ", edge_num / 2)
    print("Total vertices:  ", len(graph))
    print("Maximum degree:  ", max(edge_list))
    print("Minimum degree:  ", min(edge_list))
    print("average degree:  ", sum(edge_list) / len(edge_list))
    print("Runing times:    ", len(cuts))
    # print() cuts
    # print() "Maxcut is", max(cuts)
    print("Mincut is        ", min(cuts))


if __name__ == '__main__':
    main()
