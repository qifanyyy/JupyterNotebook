from pygraph.core import *

def quotient(dg):
    return TarjansAlgorithm(dg).quotient()


class TarjansAlgorithm(object):
    digraph    = Digraph
    stack      = list
    index      = 0
    lowlinks   = dict
    indexes    = dict
    nodemap    = dict
    quotient   = Digraph
    in_stack   = set
    components = set

    def __init__(self, digraph):
        self.digraph = digraph

    def run(self):
        self.stack      = list()
        self.lowlinks   = dict()
        self.indexes    = dict()
        self.index      = 0
        self.components = set()
        self.in_stack   = set()
        self.nodemap    = dict()

        for node in self.digraph.nodes_set():
            if node not in self.indexes:
                self.__strong_connect(node)

    def __strong_connect(self, v):
        self.indexes[v]  = self.index
        self.lowlinks[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.in_stack.add(v)

        for w in self.digraph.nodes[v]:
            if w not in self.indexes:
                self.__strong_connect(w)
                self.lowlinks[v] = min(self.lowlinks[v], self.lowlinks[w])
            elif w in self.in_stack:
                self.lowlinks[v] = min(self.lowlinks[v], self.indexes[w])

        if self.lowlinks[v] == self.indexes[v]:
            component_nodes = set()
            while True:
                w = self.stack.pop()
                self.in_stack.remove(w)
                component_nodes.add(w)

                if w == v:
                    break

            component = ComponentNode(component_nodes)
            for node in component_nodes:
                self.nodemap[node] = component

            self.components.add(component)

    def quotient(self):
        self.run()

        quotient = Digraph()
        quotient.nodemap = self.nodemap.copy()

        for c in self.components:
            quotient.add_node(c)

            for v in c.nodes:
                for w in self.digraph.nodes[v]:
                    c2 = self.nodemap[w]
                    if c2 != c:
                        quotient.add_edge(c, c2)


        return quotient