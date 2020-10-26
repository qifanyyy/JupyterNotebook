from Roulette import *
import networkx as nx  # Generating of graphs

class Ga:
    def __init__(self):
        self.settings = self.get_settings()
        self.popsize = self.settings[0]
        self.crossover = self.settings[1]
        self.mutation = self.settings[2]
        self.generations = self.settings[3]
        self.selection = self.settings[4]
        self.stop_criterion = self.settings[5]
        self.percentage = self.settings[6]
        self.tournament_size = self.settings[7]
        self.crossover_method = self.settings[8]
        self.number_of_colors = self.settings[9]
        self.mutation_method = self.settings[10]
        self.graph = self.settings[11]

    @staticmethod
    def get_settings():
        path = "settings.txt"
        settings = []
        with open(path, "r") as f:
            line = f.readline()
            while line:
                settings.append(line.strip().split(": ")[1])
                line = f.readline()
        return settings


    # Why static method?
    def run(self, popsize, crossover, mutation, generations, selection_method, stop_criterion,
            percentage, tournament_size, crossover_method, number_of_colors, mutation_method, graph):

        my_graph = nx.Graph()
        edges = nx.read_edgelist(graph)
        my_graph.add_edges_from(edges.edges())

        number_nodes = my_graph.number_of_nodes()
        adjacency_list = my_graph.edges()

        # Process adjacency list in a format that is easier, int format and with [ ]
        adjacency_list = [list(int(x) for x in tup) for tup in adjacency_list]

        # I know this part of the code sucks...
        G = nx.Graph()
        G.add_edges_from(adjacency_list)

        population = Population(G, popsize, number_nodes, number_of_colors, adjacency_list)
        population.print_me(0)

        # Loop through generations
        for x in range(generations):

            population.sort(True)
            print("Generation " + str(x) + " with fitness = " + str(population.individual_list[0].fitness) + ", " + str(population.individual_list[0].wrong_connections)  +" Wrong Edges")

            # Selection
            if selection_method == 'roulette_selection':
                roulette = Roulette(population)
                selected = roulette.rouletteSelection(G, population.number_of_colors)
            elif selection_method == 'sus_selection':
                roulette = Roulette(population)
                selected = roulette.SUS(G, population.number_of_colors)
            elif selection_method == 'tournament_selection_with_replacement':
                selected = population.tournamentWithReplacement(G, tournament_size)
            elif selection_method == 'tournament_selection_without_replacement':
                selected = population.tournamentSelectionWithoutReplacement(G, tournament_size)
            elif selection_method == 'truncation_selection':
                selected = population.truncationSelection(G, percentage)

            new_individuals = []

            # Crossover
            for j in range(0, len(selected.individual_list), 2):

                # first with second, third with forth...
                r = random.random()
                first_individual = selected.individual_list[j]
                second_individual = selected.individual_list[j + 1]

                if crossover_method == 'onepoint_crossover':
                    cross_result = first_individual.onePointCrossover(second_individual)
                elif crossover_method == 'uniform_crossover':
                    cross_result = first_individual.uniformCrossover(second_individual)
                elif crossover_method == 'cycle_crossover':
                    cross_result = first_individual.cycleCrossover(second_individual)

                # if crossover was allowed...
                if r < crossover:
                    new_individuals.append(cross_result[0])
                    new_individuals.append(cross_result[1])
                else:
                    new_individuals.append(first_individual)
                    new_individuals.append(second_individual)

            # Mutation
            for i in range(len(new_individuals)):
                individual = new_individuals[i]

                if mutation_method == 'adjacent_color':
                    individual.color_mutate2(mutation)
                elif mutation_method == 'valid_color':
                    individual.mutate_valid_color(mutation, population.color_list)
                elif mutation_method == 'random_color':
                    individual.color_mutate(mutation)

                new_individuals[i] = individual

            # print(len(new_individuals))
            population = Population(G, '', '', number_of_colors, '', new_individuals)

            if stop_criterion == '1':
                population.sort(True)
                if population.individual_list[0].wrong_connections == 0:
                    print("Generation " + str(x+1) + " with fitness = " + str(
                        population.individual_list[0].fitness) + ", " + str(
                        population.individual_list[0].wrong_connections) + " Wrong Edges")
                    return population, x+1, True

        # Return population after n generations
        population.sort(True)
        # Third argument means it wasnt possible to reach max fitness
        return population, generations, False
