import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from deap import creator, base, tools, algorithms
from scoop import futures
import random
import numpy
from scipy import interpolate
import matplotlib.pyplot as plt
import sys
import time


dfData = pd.read_csv(sys.argv[1], sep=',', low_memory=False)
le = LabelEncoder()
le.fit(dfData['Label'])
allClasses = le.transform(dfData['Label'])
allFeatures = dfData.drop(['Label'], axis=1)


# Form training, test, and validation sets
X_trainAndTest, X_validation, y_trainAndTest, y_validation = train_test_split(allFeatures, allClasses, test_size=0.20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_trainAndTest, y_trainAndTest, test_size=0.20, random_state=42)



# Feature subset fitness function
def getFitness(individual, X_train, X_test, y_train, y_test, evaluation=False):

	cols = [index for index in range(len(individual)) if individual[index] == 0]
	X_trainParsed = X_train.drop(X_train.columns[cols], axis=1)
	X_trainOhFeatures = pd.get_dummies(X_trainParsed)
	X_testParsed = X_test.drop(X_test.columns[cols], axis=1)
	X_testOhFeatures = pd.get_dummies(X_testParsed)

	# Remove any columns that aren't in both the training and test sets
	sharedFeatures = set(X_trainOhFeatures.columns) & set(X_testOhFeatures.columns)
	removeFromTrain = set(X_trainOhFeatures.columns) - sharedFeatures
	removeFromTest = set(X_testOhFeatures.columns) - sharedFeatures
	X_trainOhFeatures = X_trainOhFeatures.drop(list(removeFromTrain), axis=1)
	X_testOhFeatures = X_testOhFeatures.drop(list(removeFromTest), axis=1)

	# Apply logistic regression on the data, and calculate accuracy
	clf = LogisticRegression()
	clf.fit(X_trainOhFeatures, y_train)
	predictions = clf.predict(X_testOhFeatures)
	accuracy = accuracy_score(y_test, predictions)

	if evaluation == False:	
		return (accuracy,)

#	results = confusion_matrix(y_test, predictions)
	precision = precision_score(y_test, predictions)
	recall = recall_score(y_test, predictions)
	return (accuracy, precision, recall)

# Create Individual/Classes
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Create Toolbox/Base Class
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(dfData.columns) - 1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", getFitness, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, evaluation=False)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def getHof():
	# Initialize variables to use eaSimple
	numPop = 10
	numGen = 10
	pop = toolbox.population(n=numPop)
	hof = tools.HallOfFame(numPop * numGen)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)
	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=numGen, stats=stats, halloffame=hof, verbose=False)
	return hof

def getMetrics(hof):

	testAccuracyList = []
	validationAccuracyList = []
	individualList = []
	for individual in hof:
		testAccuracy = individual.fitness.values
		validationAccuracy = getFitness(individual, X_trainAndTest, X_validation, y_trainAndTest, y_validation, evaluation=False)
		testAccuracyList.append(testAccuracy[0])
		validationAccuracyList.append(validationAccuracy[0])
		individualList.append(individual)
	testAccuracyList.reverse()
	validationAccuracyList.reverse()
	return testAccuracyList, validationAccuracyList, individualList


if __name__ == '__main__':

	individual = [1 for i in range(len(allFeatures.columns))]
	start = time.time()
	testAccuracy, precision, recall = getFitness(individual, X_train, X_test, y_train, y_test, evaluation=True)
	end = time.time()
	validationAccuracy = getFitness(individual, X_trainAndTest, X_validation, y_trainAndTest, y_validation, evaluation=False)
	print('Test accuracy with all features: \t' + str(testAccuracy))
	print('Validation accuracy with all features: \t' + str(validationAccuracy[0]))
	print("Test time : " + str(end-start))
	print('Precision : \t' + str(precision) + '\tRecall : ' + str(recall))
	print("Number of Features : " + str(len(individual)))

	build_start = time.time()
	hof = getHof()
	testAccuracyList, validationAccuracyList, individualList = getMetrics(hof)
	build_end = time.time()
	# Get a list of subsets that performed best on validation data
	maxValAccSubsetIndicies = [index for index in range(len(validationAccuracyList)) if validationAccuracyList[index] == max(validationAccuracyList)]
	maxValIndividuals = [individualList[index] for index in maxValAccSubsetIndicies]
	maxValSubsets = [[list(allFeatures)[index] for index in range(len(individual)) if individual[index] == 1] for individual in maxValIndividuals]


	# WORKING ON HOF
	count = [0 for i in range(len(allFeatures.columns))]
	for subset in hof :
		i = 0
		for feature in subset :
			if feature :
				count[i] += 1
			i += 1
	hof_feature_count = []
	for index in range(len(count)) :
		hof_feature_count.append([ list(allFeatures)[index], count[index] ])
	print (hof_feature_count)

	#Rank Features
	count = [0 for i in range(len(allFeatures.columns))]
	rank =  [i for i in range(len(allFeatures.columns))]
	for subset in individualList :
		i = 0
		for count_index in subset :
			count[i] += count_index
			i += 1
	for i in range(len(count)): 
		max_idx = i
		for j in range(i+1, len(count)):
			if count[max_idx] < count[j]:
				max_idx = j
		count[i], count[max_idx] = count[max_idx], count[i]
		rank[i], rank[max_idx] = rank[max_idx], rank[i]

	best_features = [list(allFeatures)[index] for index in rank[:10]]
	print("\n---Best Informative Features---")
	for i in range(len(best_features)) :
		print("\t" + str(i+1) + ". " + best_features[i])

	#Print Features Subsets
	print('\n---Optimal Feature Subset(s)---\n')
	for index in range(len(maxValAccSubsetIndicies)):

		start = time.time()
		testAccuracy, precision, recall = getFitness(maxValIndividuals[index], X_train, X_test, y_train, y_test, evaluation=True)
		end = time.time()

		print('Number Features In Subset: \t' + str(len(maxValSubsets[index])))
		print('Test Time: ' + str(end-start))
		print('Test Accuracy: \t\t' + str(testAccuracy))
		print('Validation Accuracy: \t\t' + str(validationAccuracyList[maxValAccSubsetIndicies[index]]))
		print('Precision : \t' + str(precision) + '\tRecall : ' + str(recall))
		#print('Individual: \t' + str(maxValIndividuals[index]))
		print('Feature Subset: ' + str(maxValSubsets[index]) + '\n')

	print("---BUILD TIME : " + str(build_end-build_start) + " ---\n")

	input()
