import LoadData
import Accuracy

'''
INPUT
data in the form of a 2d array

OUTPUT
answer_set of feature numbers
answer_accuracy for this feature set
'''

def forwardSelection(data):
	accuracy_at_level = []
	answer_accuracy = 0
	answer_set = []
	N = len(data)
	M = len(data[0])
	current_features = []
	for i in range(1, M):
		print("On search-tree level number", i)
		feature_to_add = -1
		best_accuracy = 0
		best_num_wrong = float('inf')
		
		for j in range(1, M):
			if (j not in current_features):
				print("Considering feature number ", j)	
				accuracy, num_wrong = Accuracy.Accuracy(data, N, current_features, j, best_num_wrong)
				if (accuracy > best_accuracy):
					best_accuracy = accuracy
					feature_to_add = j
					best_num_wrong = num_wrong
		if (feature_to_add == -1):
			print("ERROR: feature to add is -1")
			exit()
		else:
			current_features.append(feature_to_add)
			print("On level", i, "I added feature", feature_to_add, "which gave an accuracy of", best_accuracy)
		if (best_accuracy > answer_accuracy):
			answer_accuracy = best_accuracy
			answer_set = current_features[:]	
		accuracy_at_level.append(best_accuracy)
	return answer_set, answer_accuracy, accuracy_at_level
	
'''
# just to test
data = LoadData.loadData("../data/CS170_SMALLtestdata__80.txt")
LoadData.normalizeData(data)
N = len(data)
forwardSelection(data)
'''
