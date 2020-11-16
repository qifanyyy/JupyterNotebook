class AlonColoring:
    def __init__(self, graph, coloring=None, color_counter=None):
        self.graph = graph
        self.coloring = coloring
        self.color_counter = color_counter

    def __call__(self, *args, **kwargs):
        return self.alon_coloring_root()

    def alon_coloring_root(self):
        return self.alon_color()

    def alon_color(self, graph, coloring=None, color_counter=None):

        if coloring is None:
            number_of_colors = graph.max_degree('degree')
            coloring = {color: [] for color in range(number_of_colors)}
        if color_counter is None:
            color_counter = [0]

        if graph.max_degree('degree') % 2 != 0:
            if graph.max_degree('degree') == 1:
                m_covering_edges = [(node, graph.incident[node][0]) for node in graph.incident if len(graph.incident[node]) > 0]
            else:
                m_covering_edges = graph.find_matching_alon()

            coloring[color_counter[0]] = m_covering_edges
            color_counter[0] += 1

            for edge in m_covering_edges:
                graph.remove_edge(edge[0], edge[1])

            if graph.has_no_edges():
                return

            AlonColoring.alon_color(self, graph, coloring, color_counter)

        else:
            euler_split_1, euler_split_2 = graph.euler_split_without_copy()

            AlonColoring.alon_color(self, euler_split_1, coloring, color_counter)
            AlonColoring.alon_color(self, euler_split_2, coloring, color_counter)

        return coloring