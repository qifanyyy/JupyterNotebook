import subprocess
import model as ml
from pandas import read_csv, np
import time
import cuts

def parseInformation(info):
	info = info.replace(" ", "")
	info = info.replace("\r\n", "\t")
	info = info.replace("\t\t\t", "\t")
	info = info.replace("\t\t", "\t")
	info = info.split("\t")
	featureSet = []
	correlationSet = []
	for i in range(0,len(info)):
		if(i%4==1):
			value = info[i].replace(" ", "")
			featureSet.append(int(value)-1)

		elif(i%4==3):
			value = info[i].replace(" ", "")
			correlationSet.append(float(value))
	return [featureSet,correlationSet]

def rankExtraction(filepath, method=0): #method 0 = relevance, methodo 1 = mrmr
	execution = ["mrmr.exe", "-i" , filepath, "-t", "1"]
	output = subprocess.Popen(execution, stdout=subprocess.PIPE).communicate()[0]
	output = output[273:-476]
	#print output
	output2 = output.split("*** mRMR features ***")
	rel = output2[0][:-4]
	mrmr = output2[1][31:]	
	if(method==0):
		[rank,corr] = parseInformation(rel)
	elif(method==1):
		[rank,corr] = parseInformation(mrmr)
	return [rank,corr]
	

def mrmrTest(cutMethod=1, method=0, runs=3):
	#Artifial Datasets
	files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv','data1000-f1-r500.csv','data5000-f1-r500.csv','data20000-f1-r500.csv']
	buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14]]	
	modelsType = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#Real Datasets
	#files = ['real/sonar_scale.csv', 'real/splice_scale.csv', 'real/colon-cancer.csv', 'real/leu.csv', 'real/duke.csv', 'real/BH20000.csv', 'real/madelon-test.csv']
	#buenos = [['?'],['?'],['?'],['?'],['?'],['?'],['?']]
	#modelsType = [0,0,0,0,0,0,0]
	i=0
	verboseClassifiers = True
	for f in files:
		modelType = modelsType[i]
		filepath = 'Data/'+f		
		filepath2 = 'Data2/'+f				
		data = read_csv(filepath)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print filepath, buenos[i]
		startTime = time.time()
		if(modelType==0):
			acc = ml.clasificationJudge(X=X,y=y, testPerc=0.5, runs=runs)
		else:
			acc = ml.regresionJudge(X=X,y=y, testPerc=0.5, runs=runs)
		endTime = time.time()
		print "original:", acc, X.shape[1], str(round(endTime-startTime,3))+"s"
		#try:
		startTime = time.time()
		[rank,featureImportance] = rankExtraction(filepath2,method)
		if(cutMethod==0):
			cutpos = cuts.greatestDiffCut(weights=featureImportance)
		elif(cutMethod==1):
			cutpos = cuts.monotonicValidationCut(X=X, y=y, modelType=modelType, rank=rank, consecutives=5, runs=runs)
		
		rank = rank[0:cutpos]
		endTime = time.time()
		timefs = round(endTime-startTime,3)
		X = np.array(data.ix[:,rank])
		startTime = time.time()
		if(modelType==0):
			acc = ml.clasificationJudge(X=X,y=y, testPerc=0.5, runs=runs)
		else:
			acc = ml.regresionJudge(X=X,y=y, testPerc=0.5, runs=runs)
		endTime = time.time()
		timeml = round(endTime-startTime,3)
		print "result: ",acc, timefs, timeml, len(rank), rank[0:5]
		print 	
		#except Exception as inst:
		#	X = np.array(data.ix[:,0:-1])
		#	print "error"

if __name__ == '__main__':
	mrmrTest(1,1,3)