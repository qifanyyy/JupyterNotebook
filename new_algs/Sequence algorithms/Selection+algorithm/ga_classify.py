import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from operator import itemgetter
from k_nn import get_accuracy

if len(sys.argv) != 7:
    print "Invalid number of arguments!\nUsage: \npython ", sys.argv[0], " <TRAINING_DATA> <TEST_DATA> <GENERATIONS> <K> <POPULATION_SIZE> <SELECTION_SIZE>\n"
    quit()

def get_table_subset(table, columns):
	return table[columns]

def get_fitness(solution):
	limited_test_data = get_table_subset(test_data, train_data.columns[np.append(np.nonzero(solution)[0],[-1])])
	limited_train_data = get_table_subset(train_data, train_data.columns[np.append(np.nonzero(solution)[0],[-1])])
	correct_dict, incorrect_dict = get_accuracy(limited_train_data, limited_test_data, k)
	correct_count = sum(correct_dict.values())
	incorrect_count = sum(incorrect_dict.values())
	return 1.0*correct_count/(correct_count+incorrect_count)

def get_random_solution(feature_size, prob_feature_selection):
	solution = []
	for i in range(feature_size):
		if np.random.random()<prob_feature_selection:
			solution.append(True)
		else:
			solution.append(False)
	fitness = get_fitness(solution)
	return [fitness, solution]

def get_random_population(population_size, feature_size, prob_feature_selection):
	population = []
	for i in range(population_size):
		population.append(get_random_solution(feature_size, prob_feature_selection))
	return population

def get_stochastic_element(population):
	prob = np.random.random()
	fitness_vals = [x[0] for x in population]
	fitness_sum = sum(fitness_vals)
	fitness_vals = [x*1.0/fitness_sum for x in fitness_vals]
	val = 0
	j = -1
	while val < prob:
		j += 1
		val += fitness_vals[j]
	return population[j]

def select_population(selection_model, current_population, selection_size):
	if selection_model == 'Elitist':
		return current_population[:selection_size]
	elif selection_model == 'Roulette':
		new_population = []
		for i in range(selection_size):
			new_population.append(get_stochastic_element(current_population))
		return new_population
	return None

def perform_crossover(parent1, parent2, crossover_type):
	child1 = parent1[:]
	child2 = parent2[:]
	if crossover_type == 'Single':
		crossover_point = np.random.randint(0, len(parent1))
		child1[0:crossover_point] = parent2[0:crossover_point]
		child2[0:crossover_point] = parent1[0:crossover_point]
	elif crossover_type == 'Double':
		rand = np.random.randint(0, len(parent1), 2)
		crossover_point1 = min(rand)
		crossover_point2 = max(rand)
		child1[crossover_point1:crossover_point2] = parent2[crossover_point1:crossover_point2]
		child2[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]
	return child1, child2

def crossover_selection(current_population, next_population, probability_crossover, crossover_type):
	while len(next_population) < len(current_population):
		parent1 = get_stochastic_element(current_population)[1]
		parent2 = get_stochastic_element(current_population)[1]
		if np.random.random() < probability_crossover:
			child1, child2 = perform_crossover(parent1, parent2, crossover_type)
			child1_fitness = get_fitness(child1)
			child2_fitness = get_fitness(child2)
			next_population.append([child1_fitness, child1])
			next_population.append([child2_fitness, child2])
	return next_population

def population_mutation(population, probability_mutation):
	for i in range(len(population)):
		if np.random.random() < probability_mutation:
			mutation_point = np.random.randint(0, len(population[i][1]))
			population[i][1][mutation_point] = not(population[i][1][mutation_point])
	return population

def genetic_algorithm(init_population, num_generations, selection_model):
	current_generation = 1
	current_population = init_population
	best = []
	mean = []
	worst = []

	while current_generation<num_generations:
		current_population.sort(key=itemgetter(0), reverse=True)
		best.append(current_population[0][0])
		worst.append(current_population[-1][0])
		mean.append(np.mean([x[0] for x in current_population]))
		next_population = select_population(selection_model, current_population, selection_size)
		next_population = crossover_selection(current_population, next_population, probability_crossover, crossover_type)
		next_population = population_mutation(next_population, probability_mutation)
		current_population = next_population
		current_generation += 1

	return current_population[0], best, worst, mean

train_data = pd.read_csv(sys.argv[1])
test_data = pd.read_csv(sys.argv[2])
target_attribute = train_data.columns[-1]

num_generations = int(sys.argv[3])
k = int(sys.argv[4])
population_size = int(sys.argv[5])
selection_size = int(sys.argv[6])
features = train_data.columns

# probability of feature being selected
prob_feature_selection = 0.08
probability_mutation = 0.01
probability_crossover = 0.9
crossover_type = 'Single'
selection_model = 'Elitist'
population = get_random_population(population_size, len(features)-1, prob_feature_selection)
solution, best_fitness, worst_fitness, mean_fitness = genetic_algorithm(population, num_generations, selection_model)
print "Best solution is ", train_data.columns[np.nonzero(solution[1])[0]]
print "Fitness is ", solution[0]

plt.figure(1)
plt.subplot(311)
plt.plot(best_fitness)

plt.subplot(312)
plt.plot(worst_fitness)

plt.subplot(313)
plt.plot(mean_fitness)

plt.show()