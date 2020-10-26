import random
import numpy as np

class MapIndividual:
    def __init__(self, colors, adjacency_list, G):
        self.adjacency_list = adjacency_list
        self.colors = list(colors)
        self.n_nodes = len(self.colors)
        self.graph_nx = G
        self.fitness, self.wrong_connections = self.createGraph(self.colors)


    def createGraph(self, colors):
        counter = 0  # edges with wrong colors
        number_of_edges_twice = 0

        # Paint all nodes first
        iter = 0
        for u, v in self.graph_nx.nodes(data=True):
            self.graph_nx.nodes[u]['color'] = colors[iter]
            iter = iter + 1

        # Calculate fitness based on wrong connections
        for u, v in self.graph_nx.nodes(data=True):
            neighbours = list(self.graph_nx.neighbors(u))

            for neighbour in neighbours:

                number_of_edges_twice += 1

                if self.graph_nx.nodes[u]['color'] == self.graph_nx.nodes[neighbour]['color']:
                    counter += 1

        fitness = number_of_edges_twice - counter

        return fitness, counter

    def onePointCrossover(self, individual_2):
        r = random.random()
        cut = round(individual_2.n_nodes * r)
        adjacency_list = individual_2.adjacency_list

        child1_colors = []
        child2_colors = []

        for x in range(individual_2.n_nodes):
            if x <= cut:
                child1_colors.append(self.colors[x])
                child2_colors.append(individual_2.colors[x])
            else:
                child1_colors.append(individual_2.colors[x])
                child2_colors.append(self.colors[x])

        child1 = MapIndividual(child1_colors, adjacency_list, self.graph_nx)
        child2 = MapIndividual(child2_colors, adjacency_list, self.graph_nx)
        childs = [child1, child2]
        return childs

    def cycleCrossover(self, individual2):
        adjacency_list = individual2.adjacency_list

        cycles = [-1] * self.n_nodes
        cycle_no = 1
        cyclestart = (i for i, v in enumerate(cycles) if v < 0)

        for pos in cyclestart:

            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                if individual2.colors[pos] in self.colors:
                    pos = self.colors.index(individual2.colors[pos])
                else:
                    pos = -1

            cycle_no += 1

        child1_colors = [self.colors[i] if n % 2 else individual2.colors[i] for i, n in enumerate(cycles)]
        child2_colors = [individual2.colors[i] if n % 2 else self.colors[i] for i, n in enumerate(cycles)]

        child1 = MapIndividual(child1_colors, adjacency_list, self.graph_nx)
        child2 = MapIndividual(child2_colors, adjacency_list, self.graph_nx)
        childs = [child1, child2]
        return childs

    def uniformCrossover(self, individual2):
        r = random.random()
        adjacency_list = individual2.adjacency_list

        child1_colors = []
        child2_colors = []
        for x in range(individual2.n_nodes):
            r = random.random()
            if r <= 0.5:
                child1_colors.append(self.colors[x])
                child2_colors.append(individual2.colors[x])
            else:
                child1_colors.append(individual2.colors[x])
                child2_colors.append(self.colors[x])
        child1 = MapIndividual(child1_colors, adjacency_list, self.graph_nx)
        child2 = MapIndividual(child2_colors, adjacency_list, self.graph_nx)
        childs = [child1, child2]
        return childs

    # Change the colors of each node with probability p
    def color_mutate(self, p):
        for x in range(self.n_nodes):
            r = random.random()
            if r < p:
                color = np.random.choice(list(self.colors), self.n_nodes)
                color_string = list(color)
                self.colors = color_string

    def color_mutate2(self, p):
        r = random.random()

        if r < p:
            for u, v in self.graph_nx.nodes(data=True):
                node_color = self.graph_nx.nodes[u]['color']
                neighbours = self.graph_nx.neighbors(u)
                adjacentColors = []
                for neighbour in neighbours:
                    neighbor_color = self.graph_nx.nodes[neighbour]['color']
                    adjacentColors.append(neighbor_color)

                # same color...
                if node_color in adjacentColors:
                    k = random.randint(0, len(self.colors) - 1)
                    newColor = self.colors[k]
                    self.graph_nx.nodes[u]['color'] = newColor


    def mutate_valid_color(self, p, colors):

        r = random.random()

        if r < p:
            for u, v in self.graph_nx.nodes(data=True):
                node_color = self.graph_nx.nodes[u]['color']
                neighbours = self.graph_nx.neighbors(u)
                adjacentColors = []
                for neighbour in neighbours:
                    neighbor_color = self.graph_nx.nodes[neighbour]['color']
                    adjacentColors.append(neighbor_color)

                # same color...
                if node_color in adjacentColors:
                    validColors = [item for item in self.colors if item not in set(adjacentColors)]
                    if len(validColors) > 0:
                        k = random.randint(0, len(validColors) - 1)
                        newColor = validColors[k]
                        self.graph_nx.nodes[u]['color'] = newColor


