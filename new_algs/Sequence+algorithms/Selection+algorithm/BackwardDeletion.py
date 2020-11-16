import LoadData
import Accuracy

def backwardDeletion(data):
	accuracy_at_level = []
	answer_set = []
	answer_accuracy = 0
	N = len(data)
	M = len(data[0])
	# start with all of the features
	features = list(range(1,M))	
	for count in range(1, M):
		best_num_wrong = float('inf')
		best_accuracy = 0
		feature_to_omit = -1
		for i in range(len(features)):
			# take out i'th feature
			temp = []
			if (i < len(features) - 1):
				temp = features[:i] + features[i+1:]		
			else:
				temp = features[:-1]
			temp_accuracy, num_wrong = Accuracy.Accuracy(data, N, temp, None, best_num_wrong)
			if (temp_accuracy > best_accuracy):
				best_accuracy = temp_accuracy
				feature_to_omit = i
				best_num_wrong = num_wrong
		print("Omitting feature", features[feature_to_omit])
		if (feature_to_omit < len(features) - 1):
			features = features[:feature_to_omit] + features[feature_to_omit+1:]
		else:
			features = features[:-1]	
		print("This leaves us with", features, "and an accuracy of ", best_accuracy)
		if (best_accuracy > answer_accuracy):
			answer_accuracy = best_accuracy
			answer_set = features
		accuracy_at_level.append(best_accuracy)
	return answer_set, answer_accuracy, accuracy_at_level
'''
# just to test
data = LoadData.loadData("../data/CS170_SMALLtestdata__80.txt")
LoadData.normalizeData(data)
N = len(data)
backwardDeletion(data)
'''
