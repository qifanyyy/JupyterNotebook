#step 1: Calculate Euclidean Distance.
#Step 2: Get Nearest Neighbors.
#Step 3: Make Predictions.
from math import sqrt


from tqdm import tqdm


def euclidean_distance(row1, row2):
	distance = 0.0
	for i in tqdm(range(len(row1)-1)):                  #i mentioned -1 coz thinking last element as my class label
		distance += (row1[i] - row2[i])**2
	return sqrt(distance)

print(euclidean_distance([1,2,3],[1,2,3]))         #prints zero

print(euclidean_distance([12,0],[0,12]))           #prints 12

dataset = [[2.7810836,2.550537003,0],              #test on a data set
	[1.465489372,2.362125076,0],
	[3.396561688,4.400293529,0],
	[1.38807019,1.850220317,0],
	[3.06407232,3.005305973,0],
	[7.627531214,2.759262235,1],
	[5.332441248,2.088626775,1],
	[6.922596716,1.77106367,1],
	[8.675418651,-0.242068655,1],
	[7.673756466,3.508563011,1]]
row0 = dataset[0]
for row in dataset:
	distance = euclidean_distance(row0, row)
	print(distance)

def get_neighbors(train, test_row, num_neighbors):
	distances = list()
	for train_row in tqdm(train):
		dist = euclidean_distance(test_row, train_row)
		distances.append((train_row, dist))              #apppending each of the distance
	distances.sort(key = lambda tup: tup[1])             #sorting based on distances
	neighbors = list()
	for i in tqdm(range(num_neighbors)):
		neighbors.append(distances[i][0])                #appending shortest distances based on sorted list
	return neighbors


# Test distance function
dataset = [[2.7810836,2.550537003,0],
	[1.465489372,2.362125076,0],
	[3.396561688,4.400293529,0],
	[1.38807019,1.850220317,0],
	[3.06407232,3.005305973,0],
	[7.627531214,2.759262235,1],
	[5.332441248,2.088626775,1],
	[6.922596716,1.77106367,1],
	[8.675418651,-0.242068655,1],
	[7.673756466,3.508563011,1]]
neighbors = get_neighbors(dataset, dataset[0], 3)
for neighbor in neighbors:
	print(neighbor)


def predict_classification(train, test_row, num_neighbors):
	neighbors = get_neighbors(train, test_row, num_neighbors)
	output_values = [row[-1] for row in neighbors]
	prediction = max(set(output_values), key=output_values.count)
	return prediction


