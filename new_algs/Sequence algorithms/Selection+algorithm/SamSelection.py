import LoadData
import Accuracy
import random
import ForwardSelection

'''
Delete 5%
'''
def samSelection(data):
	d1 = []
	d2 = []
	d3 = []
	d4 = []
	d5 = []
	for i in range(len(data)):
		rand = random.randrange(1)
		if (rand < .15):
			d1.append(data[i][:])
		
	for i in range(len(data)):
		rand = random.randrange(1)
		if (rand < .15):
			d2.append(data[i][:])
		
	for i in range(len(data)):
		rand = random.randrange(1)
		if (rand < .15):
			d3.append(data[i][:])
		
	for i in range(len(data)):
		rand = random.randrange(1)
		if (rand < .15):
			d4.append(data[i][:])
		
	for i in range(len(data)):
		rand = random.randrange(1)
		if (rand < .15):
			d5.append(data[i][:])
	
	answer_set_1, answer_accuracy_1, accuracy_at_level = ForwardSelection.forwardSelection(data)		
	
	answer_set_2, answer_accuracy_2, accuracy_at_level = ForwardSelection.forwardSelection(data)

	answer_set_3, answer_accuracy_3, accuracy_at_level = ForwardSelection.forwardSelection(data)

	answer_set_4, answer_accuracy_4, accuracy_at_level = ForwardSelection.forwardSelection(data)
	
	answer_set_5, answer_accuracy_5, accuracy_at_level = ForwardSelection.forwardSelection(data)

	answer_sets = [answer_set_1,answer_set_2,answer_set_3,answer_set_4,answer_set_5]
	accuracies = [answer_accuracy_1, answer_accuracy_2, answer_accuracy_3, answer_accuracy_4, answer_accuracy_5]
	seen = {}

	for answer_set in answer_sets:
		for num in answer_set:
			if (num in seen):
				seen[num] += 1
			else:
				seen[num] = 1
	for num in seen:
		print(num, "is seen", 100*(seen[num]/5),"percent of time.")

	print(answer_set_1)
	print(answer_set_2)
	print(answer_set_3)
	print(answer_set_4)
	print(answer_set_5)

	max_accuracy = 0
	max_accuracy_pos = 0
	for i in range(len(accuracies)):
		if (accuracies[i] > max_accuracy):
			max_accuracy = accuracies[i]
			max_accuracy_pos = i
	
	max_set = answer_sets[max_accuracy_pos]
	return max_set, max_accuracy	
		
'''	
data = LoadData.loadData("../data/CS170_SMALLtestdata__80.txt")
LoadData.normalizeData(data)
samSelection(data)
'''






