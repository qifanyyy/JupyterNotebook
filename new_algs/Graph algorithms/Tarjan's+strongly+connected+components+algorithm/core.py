class Node(object):
    """
    Represents a node in a graph.

    """
    pass


class NamedNode(Node):
    """
    Represents a named node in a graph.

    """
    name = str

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class ComponentNode(Node):
    """
    Represents a component in a graph.

    """

    nodes = set

    def __init__(self, nodes = None):
        if nodes is None: nodes = set()
        self.nodes = nodes

    def __str__(self):
        return "__".join([str(x) for x in self.nodes])


class ByteNodeMatrix(object):
    matrix = dict

    def __init__(self):
        self.matrix = dict()

    def set(self, i, j, b):
        """
        @i: Node
        @j: Node
        @b: anything

        Sets given byte to edge i -> j

        """

        if i not in self.matrix:
            self.matrix[i] = dict()

        self.matrix[i][j] = b

    def get(self, i, j):
        """
        @i: Node
        @j: Node

        Gets value for edge i -> j, or -1 if the matrix does not contain such edge.

        """

        if i in self.matrix and j in self.matrix[i]:
            return self.matrix[i][j]
        else:
            return -1


class Digraph(object):
    nodes    = dict
    nodemap  = None
    incoming = dict

    def __init__(self):
        self.nodes = dict()
        self.incoming = dict()

    def add_edge(self, from_node, to_node):
        self.add_node(from_node)
        self.add_node(to_node)

        self.nodes[from_node].add(to_node)
        self.incoming[to_node].add(from_node)

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()
            self.incoming[node] = set()

    def has_edge(self, from_node, to_node):
        return from_node in self.nodes and to_node in self.nodes[from_node]

    def remove_edge(self, from_node, to_node):
        self.nodes[from_node].remove(to_node)
        self.incoming[to_node].remove(from_node)

    def edges(self):
        edges = set()

        for node in self.nodes:
            for adjacent_node in self.nodes[node]:
                edges.add( (node, adjacent_node) )

        return edges

    def nodes_set(self):
        return set(self.nodes.keys())

    def to_dot(self):
        dot = "digraph {\n"

        for v in self.nodes_set():
            if len(self.nodes[v]) == 0:
                dot += "\t%s;\n" % str(v)
            else:
                for w in self.nodes[v]:
                    dot += "\t%s -> %s;\n" % (str(v), str(w))

        dot += "}\n"

        return dot

    def subgraph(self, v):
        """
        Creates a subgraph by performing DFS in the current digraph
        for node v and taking any nodes and edges traversed to the
        subgraph.

        returns Digraph

        """

        from pygraph.algorithms.traversal import NodeVisitor, dfs


        class Visitor(NodeVisitor):
            def __init__(self, result):
                self.result = result

            def visit_node(self, dg, v):
                self.result.add_node(v)

            def visit_edge(self, dg, v, w):
                self.result.add_edge(v, w)

        dg = Digraph()
        visitor = Visitor(dg)

        dfs(self, v, visitor)
        return dg

    def copy(self):
        dg          = Digraph()
        dg.nodes    = self.nodes.copy()
        dg.nodemap  = self.nodemap.copy()
        dg.incoming = self.incoming.copy()

        return dg

    def revert(self):
        tmp = self.nodes
        self.nodes = self.incoming
        self.incoming = tmp

    @staticmethod
    def from_file(filename):
        f = None
        dg = Digraph()

        try:
            f = open(filename, "r")

            for line in f.readlines():
                parts = line.split(":")

                node_name = ""
                edge_target_list_str = ""

                if len(parts) > 1:
                    node_name, edge_target_list_str = parts
                else:
                    node_name = parts[0]

                if len(node_name) > 0:
                    dg.add_node(NamedNode(node_name))
                    for edge_target_name in edge_target_list_str.strip().split(" "):
                        edge_target_name = edge_target_name.strip()
                        
                        if len(edge_target_name) > 0:
                            dg.add_edge(NamedNode(node_name), NamedNode(edge_target_name))
        finally:
            if f:
                f.close()

        return dg