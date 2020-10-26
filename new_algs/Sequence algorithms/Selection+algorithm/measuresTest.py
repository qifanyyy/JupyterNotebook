import featureSelection as fs
import util as ut
from pandas import read_csv, np
import time

def measureTest():
	dataType = 0 #0 syntetic, 1 real
	modelType = 0 #0 classification, 1 regression
	dataPath = "data/"
	dataSets = ut.constructDatasetNames(dataType,modelType,dataPath)
	i=0
	verboseClassifiers = True
	for f in dataSets:
		print f
		data = read_csv(f)
		for samples in [20000,2000,200]:#range(0,2):
			data = data[0:samples]
			X = np.array(data.ix[:,0:-1])
			y = np.array(data.ix[:,-1])
			for minRed in [0,1]:
				for binMethod in [0]:#range(0,2):
					for measure in [0,1,2,3,4]:#range(0,6):
						startTime = time.time()
						rank = fs.featureSelection(X=X,y=y, modelType=modelType, runs=3, processes=0, measure=measure, binMethod=binMethod, cutMethod=-1, minRed=minRed, rrThreshold=0.9, debug=False)							
						endTime = time.time()
						timefs = round(endTime-startTime,3)
						print "[",samples, minRed, binMethod, measure, "]", str(timefs)+"s", "#"+str(len(rank)), rank[0:20]
					
if __name__ == '__main__':
	measureTest()
