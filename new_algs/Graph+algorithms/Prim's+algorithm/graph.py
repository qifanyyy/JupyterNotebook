import pandas as pd


class Graph:

    def __init__(self, graph):
        self.graph = graph

    def show_graph(self):
        print("Grafo :\n", self.graph)

    def prim(self):
        print("\n------------ALGORITMO DE PRIM------------\n")
        min_graph = {}
        aux_graph = {}

        node, adj_nodes_list = next(iter(self.graph.items()))

        aux_graph[node] = adj_nodes_list

        min_edge, next_node = self.min_edge_and_node(adj_nodes_list)

        min_graph[node] = {next_node: min_edge}
        min_graph[next_node] = {node: min_edge}

        aux_graph[next_node] = self.graph[next_node]

        print("VERTICE INICIAL : {}".format(node))

        while len(aux_graph) < len(self.graph):

            edges = {}

            for node, nodes_adj in aux_graph.items():
                count = 0

                for node_adj, adj_value in nodes_adj.items():

                    if node_adj in aux_graph:
                        continue

                    if count == 0:
                        edges[node] = {node_adj: adj_value}
                        count += 1
                    else:
                        edges[node][node_adj] = adj_value

            min_edge = 999
            next_node = ''
            node_to = ''

            for node, nodes_adj in edges.items():

                for node_adj, adj_value in nodes_adj.items():
                    if adj_value < min_edge:
                        if node_adj in aux_graph.keys():
                            continue
                        min_edge = adj_value
                        next_node = node_adj
                        node_to = node

            aux_graph[next_node] = self.graph[next_node]

            min_graph[node_to].update({next_node: min_edge})

            min_graph[next_node] = {node_to: min_edge}

        print("ARVORE MINIMA : \n", pd.DataFrame(min_graph).fillna('.'))

    @staticmethod
    def min_edge_and_node(adj_nodes_list):

        min_edge = 999
        best_node = ''

        for adj_node, value in adj_nodes_list.items():

            if value < min_edge:
                min_edge = value
                best_node = adj_node

        return min_edge, best_node

    def dijkstra(self):
        print("\n------------ALGORITMO DE DIJKSTRA------------\n")
        accumulated_distances = { key: float('inf') for key in self.graph.keys()}
        expanded = {key: False for key in self.graph.keys()}
        previous = {}

        print("CIDADES:", self.graph.keys())

        origin = (input("Digite a cidade de origem:")).upper()
        destiny = (input("Digite a cidade de destino:")).upper()

        accumulated_distances[origin] = 0

        city = origin

        while city != destiny:

            for adj_city, adj_city_cost in self.graph[city].items():

                if expanded[adj_city] is True:
                    continue

                if (accumulated_distances[city] + adj_city_cost) < accumulated_distances[adj_city]:
                    accumulated_distances[adj_city] = adj_city_cost

                    previous[adj_city] = city

            expanded[city] = True
            if accumulated_distances[city] == 0:
                accumulated_distances[city] = float('inf')

            min_value = float('inf')
            next_city = ''
            for new_city, value in accumulated_distances.items():

                if expanded[new_city] is True:
                    continue

                if value < min_value:
                    min_value = value
                    next_city = new_city

            city = next_city

        print("\nEXPANDIDOS : \n", pd.DataFrame([expanded]).to_string(index=False))
        print("\nDISTANCIA ACUMULADA: \n", pd.DataFrame([accumulated_distances]).to_string(index=False))
        print("\nANTERIORES: \n", pd.DataFrame([previous]).to_string(index=False))
