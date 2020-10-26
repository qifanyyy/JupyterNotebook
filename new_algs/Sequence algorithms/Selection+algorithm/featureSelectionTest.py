import model as ml
import featureSelection as fs
import util as ut
from pandas import read_csv, np
import time

def artificialTest():
	dataType = 1 #0 syntetic, 1 real
	modelType = 1 #0 classification, 1 regression
	dataPath = "data/"
	dataSets = ut.constructDatasetNames(dataType,modelType,dataPath)
	#dataSets = dataSets[22:24]
	#print dataSets
	i=0
	verboseClassifiers = True
	for f in dataSets:
		maxAcc = 1000000*modelType
		bestRun = False
		data = read_csv(f)
		#data = data[0:2000]
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print f
		startTime = time.time()
		acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
		endTime = time.time()
		if(modelType==0):
			print "original:", str(acc*100)+"%", "#"+str(X.shape[1]), "n:"+str(X.shape[0]), str(round(endTime-startTime,3))+"s"
		else:
			print "original:", "e: "+str(acc), "#"+str(X.shape[1]), "n:"+str(X.shape[0]), str(round(endTime-startTime,3))+"s"
		for minRed in [0,1]:#range(0,2):
			for binMethod in [0]:#range(0,2):
				for cutMethod in [3]:#range(0,4):
					for measure in [0,1,2,3,4]:#range(0,6):
						startTime = time.time()
						rank = fs.featureSelection(X=X,y=y, modelType=modelType, runs=3, processes=0, measure=measure, binMethod=binMethod, cutMethod=cutMethod, minRed=minRed, rrThreshold=0.9, debug=False)							
						endTime = time.time()
						timefs = round(endTime-startTime,3)
						X = np.array(data.ix[:,rank])
						startTime = time.time()
						acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
						endTime = time.time()
						timecf = round(endTime-startTime,3)
						if(modelType==0):		
							print "[",minRed, binMethod, cutMethod, measure, "]", str(acc*100)+"%", str(timefs)+"s", str(timecf)+"s", "#"+str(len(rank)), rank[0:10]			
							bestRun = True if acc>maxAcc else False 
						else:
							print "[",minRed, binMethod, cutMethod, measure, "]", "e: "+str(acc), str(timefs)+"s", str(timecf)+"s", "#"+str(len(rank)), rank[0:10]
							bestRun = True if acc<maxAcc else False 
						if(bestRun):							
							maxAcc = acc
							maxRank = rank
							maxTimefs = timefs
							maxTimecf = timecf
							configuration = [minRed,binMethod,cutMethod,measure]
							bestRun = False
						X = np.array(data.ix[:,0:-1])
		if(modelType==0):
			print "best:", configuration, str(maxAcc*100)+"%", str(maxTimefs)+"s", str(maxTimecf)+"s", "#"+str(len(maxRank)), maxRank[0:10]
		else:
			print "best:", configuration, "e: "+str(maxAcc), str(maxTimefs)+"s", str(maxTimecf)+"s", "#"+str(len(maxRank)), maxRank[0:10]

if __name__ == '__main__':
	artificialTest()
