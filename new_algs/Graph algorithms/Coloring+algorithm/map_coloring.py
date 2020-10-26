import random
import numpy as np
import sys
import matplotlib.pyplot as plt
import networkx as nx
from copy import copy, deepcopy

##################################################
# Defaults
color_names = ['red', 'blue', 'yellow', 'green']
num_of_colors = len(color_names)
num_of_regions = 10
num_of_steps = 100
print_steps = 2

init_population_size = 20
mutation_chance = 10
max_population_size = 100
max_possible_score = 0
##################################################
# chromosome = list of integers that presents colors of regions
# population = list of chromosomes
##################################################

# Randomly initializing first population and adjencies of regions
def initiate_population():
	adjacency_matrix = [[0 for _ in range(num_of_regions)] for _ in range(num_of_regions)]
	for i in range(num_of_regions):
		for j in range(i+1, num_of_regions):
			adjacency_matrix[i][j] = np.random.randint(0, 2)
			adjacency_matrix[j][i] = adjacency_matrix[i][j]
	
	population = []
	for _ in range(init_population_size):
		population.append(list(np.random.randint(0, num_of_colors, num_of_regions)))
	
	return population, adjacency_matrix

# Calculating fitness gradres for each region set
def calculate_fitness(chromosome, neighborhood_matrix):
	fitness_score = 0
	for i in range(num_of_regions):
		for j in range(i+1, num_of_regions):
			if neighborhood_matrix[i][j] == 1 and chromosome[i] == chromosome[j]:
				fitness_score -= 10
	
	return fitness_score

# One point crossover
def one_point_crossover(first_chromosome, second_chromosome):
	spoint = np.random.randint(1, num_of_regions)
	first_set, second_set = copy(first_chromosome), copy(second_chromosome)
	first_set[spoint:], second_set[spoint:] = second_set[spoint:], first_set[spoint:]
	return first_set, second_set
		
# crossover with multipoints between two set
def multi_point_crossover(first_chromosome, second_chromosome):
	spoint_1 = np.random.randint(1, num_of_regions-1)
	spoint_2 = np.random.randint(spoint_1, num_of_regions)
	first_set, second_set = copy(first_chromosome), copy(second_chromosome)
	first_set[spoint_1:spoint_2], second_set[spoint_1:spoint_2] \
		= second_set[spoint_1:spoint_2], first_set[spoint_1:spoint_2]
	return first_set, second_set

# crossover with randomly selected indexes
def uniform_crossover(first_chromosome, second_chromosome):
	first_set, second_set = copy(first_chromosome), copy(second_chromosome)
	for i in range(num_of_regions):
		if np.random.randint(0, 1) == 1:
			first_set[i], second_set[i] = second_set[i], first_set[i]
	return first_set, second_set

# mutating chromosome
def mutation(chromosome):
	mutated_set = copy(chromosome)
	mutation_chance = np.random.randint(0, 100)
	random_index = np.random.randint(0, num_of_regions)
	random_color = np.random.randint(0, num_of_colors)
	mutated_set[random_index] = random_color
	return mutated_set

# drawing regions as graphs and edges
def draw_regions(chromosome, neighborhood):
	color_map = [color_names[x] for x in chromosome]	
	adjacency_matrix = np.array(neighborhood)
	rows, cols = np.where(adjacency_matrix == 1)
	edges = zip(rows.tolist(), cols.tolist())
	gr = nx.Graph()
	gr.add_edges_from(edges)
	nx.draw(gr, node_size=500, node_color=color_map, with_labels=True)
	plt.show()

# drawing best fit score change through iterations
def draw_scores(scores):
	_, ax = plt.subplots()
	ax.plot(list(range(num_of_steps)), scores)
	ax.set(xlabel='Step', ylabel='Fitness Score')
	plt.show()

# eliminating non-unique chromosomes
def select_uniques(population):
	uniques = dict()
	for chromo in population:
		hashable = tuple(chromo)
		if hashable not in uniques:
			uniques[hashable] = chromo
	return list(uniques.values())
	

# ----Algorithm running order----
# 1- initiate population
# 2- make selections and do crossovers
# 3- mutation
# 4- calculate fitness score and survive best
# 5- go back to 2, repeat n times

argc = len(sys.argv)
num_of_regions = int(sys.argv[1]) if argc >= 2 else num_of_regions
num_of_steps = int(sys.argv[2]) if argc >= 3 else num_of_steps
mutation_chance = int(sys.argv[3]) if argc >= 4 else mutation_chance
print_steps = int(sys.argv[4]) if argc >= 5 else mutation_chance

population, neighborhood = initiate_population()
fitness_scores = []
for step in range(num_of_steps):
	sz = len(population)

	# Step 2
	for i in range(sz):
		for j in range(i+1, sz):
			cross_rand = np.random.randint(0, 10)
			if cross_rand == 0:
				child_1, child_2 = one_point_crossover(population[i], population[j])
			elif cross_rand == 1:
				child_1, child_2 = multi_point_crossover(population[i], population[j])
			elif cross_rand == 2:
				child_1, child_2 = uniform_crossover(population[i], population[j])
			if cross_rand <= 2:
				population.append(child_1)
				population.append(child_2)

	# Step 3
	for i in range(sz):
		mutation_rand = np.random.randint(0, 100)
		if mutation_rand < mutation_chance:
			mutated = mutation(population[i])
			population.append(mutated)

	# Step 4
	population = select_uniques(population)
	population.sort(key=lambda chromo:calculate_fitness(chromo, neighborhood), reverse=True)
	population = population[:max_population_size]
	fitness_scores.append(calculate_fitness(population[0], neighborhood))

	if step % print_steps == 0:
		print("{0}. Step | Max. Fitness: {1}".format(step, fitness_scores[-1]))
	if fitness_scores[-1] == max_possible_score:
		print("Found optimal solution in {0} step".format(step))
		break

best_solution = population[0]
print("Fitness score of best solution: {0}".format(fitness_scores[-1]))
if fitness_scores[-1] != max_possible_score:
	print("Errors: ")
	for i in range(num_of_regions):
		for j in range(i+1, num_of_regions):
			if neighborhood[i][j] == 1 and best_solution[i] == best_solution[j]:
				print("\tRegion {0} and region {1} are connected and have same color : {2}".format(i, j, color_names[best_solution[i]]))

draw_regions(population[0], neighborhood)
draw_scores(fitness_scores)