import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from k_nn import get_accuracy

def get_table_subset(table, columns):
	return table[columns]

def get_initial_solution(feature_size, selected_features):
	sol = np.random.choice(range(feature_size), size=selected_features)

def get_neighbor(current_solution, feature_size, temperature):
	all_features = range(feature_size)
	selected = current_solution
	not_selected = np.setdiff1d(all_features, selected)

	# swap one selected feature with one non-selected feature
	num_swaps = int(min(np.ceil(np.abs(np.random.normal(0, 0.1*len(selected)*temperature))), np.ceil(0.1*len(selected))))
	feature_out = np.random.randint(0, len(selected), num_swaps)
	feature_in = np.random.randint(0, len(not_selected), num_swaps)

	selected = np.delete(selected, feature_out)
	selected = np.append(selected, not_selected[feature_in])
	return list(selected), num_swaps

def get_cost(solution):
	limited_test_data = get_table_subset(test_data, train_data.columns[np.append(solution,[-1])])
	limited_train_data = get_table_subset(train_data, train_data.columns[np.append(solution,[-1])])
	correct_dict, incorrect_dict = get_accuracy(limited_train_data, limited_test_data, k)
	correct_count = sum(correct_dict.values())
	incorrect_count = sum(incorrect_dict.values())
	return 1.0*incorrect_count/(correct_count+incorrect_count)

def get_probability(temperature, delta_cost):
	return np.exp(delta_cost/temperature)

def simulated_annealing(init_soln, init_temp, max_iterations, alpha):
	temperature = init_temp
	solution = init_soln
	cost = get_cost(solution)

	best_solution = solution
	best_cost = cost

	iteration = 0
	temp_history = [temperature]
	cost_history = [cost]
	prob_history = [0]
	swaps_history = [0]
	best_history = [best_cost]

	while (iteration < max_iterations):
		next_solution, swaps = get_neighbor(solution, len(features)-1, temperature)
		next_cost = get_cost(next_solution)

		probability = 0
		if (next_cost > cost):
			probability = get_probability(temperature, cost-next_cost)
		if (next_cost < cost or np.random.random()<probability):
			cost = next_cost
			solution = next_solution
		if (cost < best_cost):
			best_cost = cost
			best_solution = solution
		iteration += 1 
		temperature *= alpha

		temp_history.append(temperature)
		cost_history.append(cost)
		prob_history.append(probability)
		swaps_history.append(swaps)
		best_history.append(best_cost)
	return best_solution, best_cost, temp_history, cost_history, prob_history, swaps_history, best_history


if len(sys.argv) != 7:
    print "Invalid number of arguments!\nUsage: \npython ", sys.argv[0], " <TRAINING_DATA> <TEST_DATA> <ITERATIONS> <K> <NUM_FEATURES> <alpha>\n"
    quit()

train_data = pd.read_csv(sys.argv[1])
test_data = pd.read_csv(sys.argv[2])
target_attribute = train_data.columns[-1]

max_iterations = int(sys.argv[3])
k = int(sys.argv[4])
selected_features = int(sys.argv[5])
alpha = float(sys.argv[6])
features = train_data.columns

random_solution = np.random.random_integers(0, len(features)-2, selected_features)
init_temp = 1.0
solution, cost, temp_history, cost_history, prob_history, swaps_history, best_history = simulated_annealing(random_solution, init_temp, max_iterations, alpha)
print "Best solution is ", train_data.columns[solution]
print "Cost is ", cost

plt.figure(1)
plt.subplot(511)
plt.plot(temp_history)

plt.subplot(512)
plt.plot(best_history)

plt.subplot(513)
plt.plot(cost_history)

plt.subplot(514)
plt.plot(prob_history)

plt.subplot(515)
plt.plot(swaps_history)

plt.show()