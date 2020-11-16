import networkx as nx


class GraphViz:
    def __init__(self, G, only_way=False):
        self.G = G
        self.DG = nx.DiGraph()
        self.edge_colors = []
        self.node_pos = {}
        self.ONLY_WAY = only_way
        self.n = len(G)
        self.__init_graph()
        self.edge_labels = nx.get_edge_attributes(self.DG, 'route')
        self.edge_colors2 = nx.get_edge_attributes(self.DG, 'color')
        self.pos = nx.shell_layout(self.DG)

    def __init_graph(self):
        def get_indexes(n):
            for i in range(n):
                for j in range(n):
                    yield i, j
        if self.ONLY_WAY:
            [self.__initEdge(i, j, self.G[i][j].flow, self.G[i][j].cup) for i, j in
             get_indexes(self.n) if self.G[i][j].cup > 0 and self.G[i][j].flow > 0]
        else:
            [self.__initEdge(i, j, self.G[i][j].flow, self.G[i][j].cup) for i, j in
             get_indexes(self.n) if self.G[i][j].cup > 0 and self.G[i][j].flow >= 0]

    def __getEdgeColor(self, flow, cup):
        def get_str_hex(value):
            if value >= 255:
                return 'FF'
            result = str(hex(value))[2:4].rjust(2, '0')
            return result
        if flow < 0: return '#000000'
        delimiter = 6
        RGB = [1, 20, 1]
        cf = int(flow / (cup / delimiter) + 1) * 2
        return '#{}{}{}'.format(get_str_hex(RGB[0] * (cf // 2)), get_str_hex(RGB[1] * cf), get_str_hex(RGB[2]))

    def __drawEdges(self):
        nx.draw_networkx_edge_labels(self.DG, self.pos, edge_labels=self.edge_labels, clip_on=False)

    def __drawNodes(self):
        nx.draw_networkx_nodes(self.DG, self.node_pos)

    def draw(self):
        self.__drawEdges()
        nx.draw_shell(self.DG, with_labels=True, edge_color=self.edge_colors2.values(), width=2.5)

    def __initEdge(self, x, y, flow, cup):
        edge_label = "{0}/{1}".format(flow, cup)
        self.DG.add_edge(x, y, route=edge_label, color=self.__getEdgeColor(flow, cup))
        self.edge_colors.append(self.__getEdgeColor(flow, cup))
