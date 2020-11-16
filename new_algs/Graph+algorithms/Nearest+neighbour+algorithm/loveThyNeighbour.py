#k-nearest neighbours model for language classification

import csv
import re
from string import digits
import numpy as np
import math
import time

#Encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
startTime = time.time()

languageLabels = {'0': "Slovak",
				  '1': "French", 
				  '2': "Spanish", 
				  '3': "German", 
				  '4': "Polish"}

#How many examples in each language
exampleCounts = {'0': 14167,
		  		 '1': 141283,
		  		 '2': 69974,
		  		 '3': 37014,
		  		 '4': 14079}

#Language predicted for empty lines (French as it is the most common)
defaultPrediction = 1

#The number of nearest neighbours to pick the majority class from (i.e the "k" in kNN)
k = 5

#Percentage of training set for validation (i.e 100(1 - valPercent)% of the training data is used for training)
valPercent = 0.7

#Extract second column of train_set_x.csv as "examples", etc for labels and testData
examples = [item[1] for item in list(csv.reader(open("train_set_x.csv", 'rb')))[1:]]
labels = [item[1] for item in list(csv.reader(open("train_set_y.csv", 'rb')))[1:]]
testData = [item[1] for item in list(csv.reader(open("test_set_x.csv", 'rb')))[1:]]

#Put aside some data for validation/preventing overfitting
dividor = int(len(examples) * valPercent)

#TODO: Implement code on validation examples (and fix vectoriseSentence taking 20 highest chars)
valExamples = [examples[i] for i in range(0, dividor)]
valLabels = [labels[i] for i in range(0, dividor)]

trainExamples = [examples[i] for i in range(dividor, len(examples))]
trainLabels = [labels[i] for i in range(dividor, len(examples))]

totalExamples = len(trainExamples)
#Used for random projection approximation method for cosine distance
planeCount = 24

#Outputs a list of classifications/predictions for each example in the test set
def main(rawExamples, trainingLabels, rawTestData):
	#Preprocessing the training data
	examples = examplePreprocessing(rawExamples, False)

	#Training: -Building tf-idf scores for each character in each example
	#          -Converting each example to a 20-long list of the 20 highest tf-idf scores for the sentence
	#	       -Reducing the dimensionality of each vector to only store the expected value of their cosine distance from random hyperplanes
	trainingVectors, documentFrequencies = buildTF_IDFScores(examples, trainingLabels)
	#Calculate random hyperplanes of dimension 20 in a matrix of 1024 planes
	planes = np.random.randn(planeCount, 20)
	hashedTrainingVectors = {}
	for i in range(0, 5):
		hashedTrainingVectors[str(i)] = randomProjections(trainingVectors[str(i)], planes)

	#Preprocessing the testing data
	testData = examplePreprocessing(rawTestData, True)
	testVectors = []
	print("...Converting test examples to tf-idf vectors")
	for i in range(0, len(testData)):
		testVectors.append(vectoriseSentence(testData[i], documentFrequencies, True))
	hashedTestVectors = randomProjections(testVectors, planes)

	#TESTING: Approximating cosine distances and taking k-nearest neighbours
	predictions = []
	print("...Calculating nearest neighbours")
	for i in range(0, len(hashedTestVectors)):
		predictionStartTime = time.time()
		prediction = ""
		testee = hashedTestVectors[i]
		#Empty line indicated by [-1] return
		if testee == [-1]:
			prediction = str(defaultPrediction)
		else:
			prediction = kNearestNeighbours(testee, hashedTrainingVectors)
		predictions.append(prediction)
		print("Prediction Count: " + str(i))
		print("  --Prediction Time = " + str(time.time() - predictionStartTime))

	#Output
	print("...Outputting predictions")
	with open('knnPredictions.csv', 'wb') as output:
		writer = csv.writer(output)
		writer.writerow(['ID', 'Category'])
		for i in range(0, len(predictions)):
			writer.writerow([i, predictions[i]])

	#DEBUG
	#for (key, value) in hashedTrainingVectors.items():
	#	for j in value:
	#		print(key + " - " + str(j))
	#TODO: Come up with distance metric

	print (" --- Runtime (seconds): ~" + str((time.time() - startTime)) + " --- ")
	return None

#For each vector, returns a list of signatures representing the sign of the dot product between the vector and some hyper plane
#Uses bitwise arithmetic to increase performance in memory
def randomProjections(vectors, planes):
	#A list of bits where 0 represents "-1" (negative dot product with that random plane) and 
	# 					  1 represents "1" (positive dot product with that random plane)
	def signature(vector, planes):
		signature = 0
		for plane in planes:
			signature =  signature << 1
			if np.dot(vector, plane) >= 0:
				signature = signature | 1
		return signature

	print("...Reducing dimensionality of vectors")
	signatures = []
	for vector in vectors:
		#print(vector)
		if (vector == [-1]):
			signatures.append(vector)
			continue
		data = np.array(vector)
		dataSig = signature(data, planes)
		signatures.append(dataSig)
	return signatures

#Rturns approximations of cosine distances between data points, by 
# estimating the probability their bits (i.e +ve/-ve signs of their dot products with corresponding hyperplanes) equal
#Inspiration for this implementation was taken from http://www.bogotobogo.com/Algorithms/Locality_Sensitive_Hashing_LSH_using_Cosine_Distance_Similarity.php
#Prereq: vecASig, vecBSig have been generated by randomProjections() (see above)
def cosineDistanceApproximation(vecASig, vecBSig):
	#Count the number of 1's that are in both vectorA's signature and vectorB's signature
	def matchingBitCount(sigA, sigB):
		count = 0
		num = sigA ^ sigB
		while num:
			count += 1
			num = num & (num - 1)
		return count

	return (1 - (matchingBitCount(vecASig, vecBSig) / float(planeCount)))

#Distance metric: Cosine similarity between test example vectors and training example vectors
#Returns a list of (length k) of the cosine similarities with the k-nearest neighbours
#Test Vectors is a list of the vectors generated for each language for this test example
def kNearestNeighbours(testSig, trainingSigs):
	nearestDistances = [100 for i in range(0, k)]
	nnLabels = ["1" for i in range(0, k)]
	currentMaxIndex = 0
	for label in trainingSigs.keys():
		for j in trainingSigs[label]:
			distance = cosineDistanceApproximation(testSig, j)
			if distance <= nearestDistances[currentMaxIndex]:
				nearestDistances[currentMaxIndex] = distance
				nnLabels[currentMaxIndex] = label
				currMax, currMaxIndex = max((val, index) for (index, val) in enumerate(nearestDistances))
				currentMaxIndex = currMaxIndex
 
 	#Take the "majority class" (in this case the mode) for the prediction
	prediction = max(nnLabels, key=nnLabels.count)

	return prediction

#Remove digits, extra spaces, emojis, and URLS in the example
#Flatten the string into a list of characters
#Note: Empty line examples are not removed at this step.
#TODO: remove "-", "_", "."  --> Thought: does removing apostrophes lose information? i.e French
#"testing" --> = 0 if training, 1 if testing
def examplePreprocessing(examples, testing):
	cleanExamples = []
#	cleanLabels = []
	#A filter to get rid of all non-multilingual unicode characters (i.e emoji and others)
	characterFilter = re.compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=re.UNICODE)

	print("...Filtering examples")
	for i in range(0, len(examples)):
		noEmoji = characterFilter.sub('', unicode(examples[i]))
		flattened = ''.join(noEmoji.split())
		noDigits = str(flattened).translate(None, digits)
		#Check for URLS (check for "http" and if not found check for "www")
		noURLS = ""
		if testing:
			noURLS = noDigits
		else:
			indexOfURL = noDigits.find("http")
			if indexOfURL == -1:
				indexOfURL = noDigits.find("www")
			if indexOfURL != -1:
				noURLS = noDigits[:indexOfURL]
			else:
				noURLS = noDigits

		cleanExamples.append(noURLS)
		#print(str(cleanLabels[i]) + "- " + str(cleanExamples[i]))

	return cleanExamples

#Goes through and builds the tf-idf scores for every character in each language
#Outputs a list of five dictionaries (one for each language) where each list
# contains lists of the 20-highest tf-idf scores for the sentence 
#Precondition: examples is a list of sentences sanitised by examplePreprocessing()
def buildTF_IDFScores(examples, labels):
	print("...Converting training examples to tf-idf vectors")
	#A count of the total number of examples that contain the character
	documentFrequencies = {}
	sentenceCount = len(examples)
	for i in range(0, sentenceCount):
		sentence = examples[i]
		foundChars = []
		for j in range(0, len(sentence)):
			char = sentence[j]
			#Only want to count the first occurence of a character in a sentence
			if (char in foundChars):
				continue
			else:
				foundChars.append(char)
			if char in documentFrequencies.keys():
				documentFrequencies[char] += 1
			else:
				documentFrequencies[char] = 1

	listsOfTF_IDFS = {"0": [], "1": [], "2": [], "3": [], "4": []}
	#Get the char's frequency in each sentence and calculate TF-IDF for each char

	for i in range(0, sentenceCount):
		#Get a vector containing the sentence's 20 highest TF-IDF scores
		exampleVector = vectoriseSentence(examples[i], documentFrequencies, False)
		if exampleVector == [-1]:
			continue
		#sort in descending order and return
		listsOfTF_IDFS[labels[i]].append(exampleVector)

	return (listsOfTF_IDFS, documentFrequencies)

#Get the 20 highest character tf-idf scores (for that language) out of the sentence 
#If <20 characters in the training example then 
# 1) get the tf-idf scores of the n characters there
# 2) fill in the rest with the (20 - n) highest tf-idf scored characters for that language
#Precondition: sentence is a flattened list of chars outputted by examplePreprocessing()
#"testing" (boolean) = 0 if training example, 1 if test data
def vectoriseSentence(sentence, documentFrequencies, testing):
	sentenceLength = len(sentence)
	if (sentenceLength == 0):
		#store something here?
		#should empty lines be used in training at all?
		return [-1]

	#A count of the total frequency of the character within the sentence
	termFrequencies = {}
	for j in range(0, sentenceLength):
		if (sentence[j] in termFrequencies.keys()):
			termFrequencies[sentence[j]] += 1
		else:
			termFrequencies[sentence[j]] = 1

	#Calculate the list of tf-idfs for the sentence
	tf_idfs = []
	for j in range(0, sentenceLength):
		#TODO: Check if better performance with overall document count instead of per-language example count
		tf_idf = 0
		if testing:
			#Laplace smoothing for division by zero (i.e if this tested character does not appear at all in the language distribution)
			if (sentence[j] not in documentFrequencies.keys()):
				tf_idf = termFrequencies[sentence[j]] * math.log(totalExamples / 1)
			else:
				tf_idf = termFrequencies[sentence[j]] * math.log(totalExamples / documentFrequencies[sentence[j]])
		else:
			tf_idf = termFrequencies[sentence[j]] * math.log(totalExamples / documentFrequencies[sentence[j]])
		#regularise by multiplying by 20/sentenceLength
		tf_idf = tf_idf * (20.0 / sentenceLength)
		tf_idfs.append(tf_idf)
	#Fill in the rest of the characters with zeros
	#TODO: Think of possible better approach than appending zeros.
	if (sentenceLength < 20):
		for j in range(0, 20 - sentenceLength):
			tf_idfs.append(0)

	#If a training example, take the 20 largest tf-idfs for the vector and output in descending order
	#Otherwise we already have a 20-long vector due to the test set format
	output_tf_idfs = [0 for i in range(0, 20)]
	currentMinIndex = 0
	for j in range(0, len(tf_idfs)):
		if tf_idfs[j] > output_tf_idfs[currentMinIndex]:
			output_tf_idfs[currentMinIndex] = tf_idfs[j]
			#update min index
			currMin, currMinIndex = min((val, index) for (index, val) in enumerate(output_tf_idfs))
			currentMinIndex = currMinIndex
	return sorted(output_tf_idfs, reverse=True)


#Repeat by cross-validating and take an average of the predictions
#def crossValidationWeighting():
#	return None


main(trainExamples, trainLabels, testData)
