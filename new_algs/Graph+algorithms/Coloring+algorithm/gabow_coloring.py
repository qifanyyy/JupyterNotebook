from graph_impl.regular_bipartite_multigraph import RegularBipartiteGraph


class GabowColoringSplitMatching:

    def __init__(self, graph, coloring=None, color_counter=None):
        self.graph = graph
        self.coloring = coloring
        self.color_counter = color_counter

    def __call__(self, *args, **kwargs):
        return self.gabow_color_root()

    def gabow_color_root(self):
        return self.gabow_color(self.graph)

    def gabow_color(self, graph, coloring=None, color_counter=None):

        if coloring is None:
            number_of_colors = graph.max_degree('degree')
            coloring = {color: [] for color in range(number_of_colors)}
        if color_counter is None:
            color_counter = [0]

        if graph.max_degree('degree') % 2 != 0:
            if graph.max_degree('degree') == 1:
                m_covering_edges = [(node, graph.incident[node][0]) for node in graph.incident if len(graph.incident[node]) > 0]
            else:
                m_covering_edges = graph.find_cole_hopcroft_covering_matching()

            coloring[color_counter[0]] = m_covering_edges
            color_counter[0] += 1

            for edge in m_covering_edges:
                graph.remove_edge(edge[0], edge[1])

            if graph.has_no_edges():
                return

            GabowColoringSplitMatching.gabow_color(self, graph, coloring, color_counter)

        else:
            euler_split_1, euler_split_2 = graph.euler_split(False)

            GabowColoringSplitMatching.gabow_color(self, euler_split_1, coloring, color_counter)
            GabowColoringSplitMatching.gabow_color(self, euler_split_2, coloring, color_counter)

        return coloring


class GabowColoringDFSMatching:

    def __init__(self, graph, coloring=None, color_counter=None):
        self.graph = graph
        self.coloring = coloring
        self.color_counter = color_counter

    def __call__(self, *args, **kwargs):
        return self.gabow_color_root()

    def gabow_color_root(self):
        return self.gabow_color(self.graph)

    def gabow_color(self, graph, coloring=None, color_counter=None):

        if coloring is None:
            number_of_colors = graph.max_degree('degree')
            coloring = {color: [] for color in range(number_of_colors)}
        if color_counter is None:
            color_counter = [0]

        if graph.max_degree('degree') % 2 != 0:

            if graph.max_degree('degree') == 1:
                m_covering_edges = [(node, graph.incident[node][0])
                                    for node in graph.incident if len(graph.incident[node]) > 0]
            else:
                mulgraph = RegularBipartiteGraph(graph=graph)
                m_covering_edges = mulgraph.get_matchings()
                if len(m_covering_edges) == 0:
                    m_covering_edges = [(node, mulgraph.incident_weighted[node][0][0])
                                        for node in mulgraph.incident_weighted]

            assert len(m_covering_edges) > 0
            coloring[color_counter[0]] = m_covering_edges
            color_counter[0] += 1

            for edge in m_covering_edges:
                graph.remove_edge(edge[0], edge[1])

            if graph.has_no_edges():
                return

            GabowColoringDFSMatching.gabow_color(self, graph, coloring, color_counter)

        else:
            euler_split_1, euler_split_2 = graph.euler_split(with_graph_copy=False)

            GabowColoringDFSMatching.gabow_color(self, euler_split_1, coloring, color_counter)
            GabowColoringDFSMatching.gabow_color(self, euler_split_2, coloring, color_counter)

        return coloring