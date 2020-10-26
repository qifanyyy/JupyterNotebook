import csv
import sys
import collections
import numpy as np
import util as util
#import collections
#from sklearn.metrics import precision_score
#from sklearn.metrics import log_loss
#from sklearn.model_selection import train_test_split



#### read and structure data

def getRawData(infile):
	rawData = []
	with open(infile) as f:
		reader = csv.reader(f)
		for row in reader:
			rawData.append(row)
	return rawData

def convertRawDataToFeatures(rawData):
	columnsNumber = len(rawData[0])
	dataSet = []
	for i in range(0,columnsNumber):
		dataSet.append(zip(*rawData)[i])
	return dataSet 

def getFeaturesData(infile,hasHeader=1): 
	trainData = getRawData(trainPath)
	trainDataSet = convertRawDataToFeatures(trainData)
	features = {}
	if(hasHeader):
		for column in trainDataSet:
			features.update({column[0]:column[1:]})
	else:
		counter = 0		
		for column in trainDataSet:
			features.update({counter:column})
			counter += 1
	return features

def sepDataAndLabel(features, labelName):
	data = {}
	label = {}
	for f in features:
		if(f!=labelName):
			data.update({f:features[f]})
		else:
			label.update({f:features[f]})
	return [data,label]

def getData(infile,labelName=False,hasHeader=1): #if label Name  = False means has not label
	features = getFeaturesData(trainPath,hasHeader)
	if(labelName!=False):
		return sepDataAndLabel(features, labelName)
	else:
		return features

#normalize and transform data

def mapVector(vector):
	domain = set(vector)
	domain = list(domain)
	dictVector = {}
	for i in range(0,len(domain)):
		dictVector.update({domain[i]:i+1})
	return dictVector

def convertIntegerVector(vector):
	newVector = []
	dictVector = mapVector(vector)
	for e in vector:
			newVector.append(dictVector[e])
	return newVector

def dataToInteger(data): #convert and order feature to integer 
	integerData = {}
	for featureName in data:
		featureInt = convertIntegerVector(data[featureName])
		integerData.update({featureName:featureInt})
	return integerData

#write Data
def writeCSV(rawData,filepath):
	myfile = open(filepath,'w')
	for row in rawData:
		stringRow=''
		for c in row:
			stringRow+=str(c)
		stringRow = stringRow.translate(None,"\'")
		stringRow = stringRow.translate(None,"]")
		stringRow = stringRow.translate(None,"[")
		stringRow = stringRow.translate(None," ")
		myfile.write(stringRow+"\n")
	myfile.close()	


#Numpy commons
def compareDif(y,pred):
	diff = 0
	for i in range(0,len(y)):
		diff += abs(y[i]-pred[i])
	result = round(1 - (float(diff)/len(y)),4)
	return result

def compareDif2(y,pred):
	diff = 0
	diff0 = 0
	diff1 = 0
	count0 = 0
	count1 = 0
	result = {}
	for i in range(0,len(y)):
		if(pred[i]>1 or pred[i]<0):
			print (pred[i])
			pred[i] = 0.5
			#print "PUTA MADRE VERGA COLA"
		if(y[i]==0):
			diff0  += abs(y[i]-pred[i])
			count0 += 1
		elif(y[i]==1):
			diff1  += abs(y[i]-pred[i])
			count1 += 1
		diff += abs(y[i]-pred[i])
	result['0'] = round(1 - (float(diff0)/count0),4)
	result['1'] = round(1 - (float(diff1)/count1),4)
	#print diff0, diff1, diff, count0, count1, result['0'], result['1']
	result['t'] = round(1 - (float(diff)/len(y)),4)
	result['w'] = round( (result['0']+result['1'])/2, 4)
	result['l'] = round(log_loss(y, pred), 4)
	#print predr
	predr = np.round(pred)
	result['p'] = round(precision_score(y, predr, average='macro'),4)
	result['sumy'] = sum(y)
	result['sump'] = round(sum(pred),1)
	result['z'] = False
	#results = collections.OrderedDict(sorted(result.items()))
	return result

def readNumpyOLD(filepath,label=False, castToNumber=True):
	features = getRawData(filepath)
	headers = features[0]
	label = util.removeColumnByName(features,label,1)

	if(castToNumber):
		features = [map(float, row) for row in features]
		label = map(float, label)
		label = map(int, label)		
	X = np.asarray(features)
	y = np.asarray(label)
	return [X, y, headers]

def readNumpy(filepath, label=False, castToNumber=True):
	features = getRawData(filepath)
	headers = features[0]
	label = util.removeColumnByName(features,label)

	if(castToNumber):
		features = [map(float, row) for row in features]
		try:
			label = map(float, label)
			label = map(int, label)
		except ValueError:
			True
			#print "no se puedo transformar el label"
	X = np.asarray(features)
	y = np.asarray(label)
	return [X, y, headers]


def joinColumns(original,extra,unique=False):
	nfeatures = original.shape[1]
	#print extra
	if(unique):
		original = np.insert(original, nfeatures, extra, axis=1)
	else:
		xfeatures = extra.shape[1]
		for f in range(0,xfeatures):
			original = np.insert(original, nfeatures, extra[:,f], axis=1)
			nfeatures = nfeatures + 1
	return original

def batchName(headers,mstr,number):
	lstr = []
	for n in range(0,number):
		headers.append(mstr+str(n))
	return lstr

def transposeDataFile(inFile,outFile):
	data = getRawData(inFile)
	data = util.transposeMatrix(data)
	write = []
	for row in data:
		line = ', '.join([str(x) for x in row])
		write.append(line)
	writeCSV(write,outFile)

def filterFeatures(X, featureSet=-1):
	if(featureSet != -1):
		if isinstance(featureSet, int):
			X = X[:,[featureSet]]
		else:
			X = X[:,featureSet]
	return X

def separateData(X, y, testPerc, random_state=42):
	X_tra, X2, y_tra, y2 = train_test_split(X, y, test_size=testPerc, random_state=42)
	X_val, X_tst, y_val, y_tst = train_test_split(X2, y2, test_size=0.5, random_state=42)
	return [X_tra, X_val, X_tst, y_tra, y_val, y_tst]

def mergeLog(a,b,f):
	return round(((a+b) + pow((f*(a-b)),2))/2,4)
	#return round((a+b)/2,4)
def mergeSum(a,b,f):
	return round(((a+b) - pow((f*(a-b)),2))/2,4)
	#return round((a+b)/2,4)

def mergeResults(dict1, dict2, f1=2.5, f2=2.5):
	dict3 = {}
	f1 = 5
	f2 = 5
	for key in dict1:
		#print key
		if(key=='l'):
			dict3[key] = mergeLog(dict1[key],dict2[key],f1)
			#print dict1[key],dict2[key],dict3[key]
		elif(key=='sump' or key=='sumy'):
			dict3[key] = round((dict1[key]+dict2[key])/2,2)
		else:
			dict3[key] = mergeSum(dict1[key],dict2[key],f2)
			#if(dict3[key]>=0.8):
			#	print dict1[key],dict2[key],dict3[key]
	return dict3

#[X,y,headers] = readNumpy("datasets/extrafet-b6.csv",'label')
#[X,y,headers] = readNumpy("datasets/trainningSet12.csv",'label')
#print X[0]
#print y
