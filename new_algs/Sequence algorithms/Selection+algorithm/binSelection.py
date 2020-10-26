import CorrelationMesures as cm
import util as ut
import numpy as np

#################################### STATIC (FORMULA) BIN SELECTION ####################################
def binStatic(X, y, measure=2):
	yBinSet = computeBinSetStatic(y)
	result = []
	binSize = []
	for i in range(0,X.shape[1]):
		xi = X[:,i]
		xiBinSet = computeBinSetStatic(xi)
		value =  computeValue(xi,y,xiBinSet, yBinSet, measure)	
		result.append(value[0])
		binSize.append(value[1])
	#print result
	return result

def computeValue(xi, y, xiBinSet, yBinSet, measure):
	binValueResult = []
	binSetResult = []
	binValue = 0
	maxValue = 0
	binResult = []
	for numbinx in xiBinSet:
		for numbiny in yBinSet:
			if(measure==0):
				binValue = round(cm.udv(xi,y,int(numbinx),int(numbiny)),2)
			elif(measure==1):
				binValue = round(cm.cdv(xi,y,int(numbinx),int(numbiny)),2)
			elif(measure==2):
				binValue = round(cm.ucmd(xi,y,int(numbinx),int(numbiny)),2)
			elif(measure==3):
				binValue = round(cm.MIC(xi,y),2)
			elif(measure==4):
				binValue = round(cm.MI(xi,y,int(numbinx),int(numbiny)),2)
			if(binValue>maxValue):
				maxValue=binValue
				binResult = [numbinx,numbiny]
	return [maxValue, binResult]

def computeBinSetStatic(f):
	binSet = []
	N = len(f)
	domainSize = float(len(set(f)))
	std = np.std(f)
	binSet.append(ut.computeStepV2(domainSize, N))
	binSet.append(round(pow(domainSize,0.5))) #Square Root
	binSet.append(round(np.log2(domainSize))) #Strugles
	binSet.append(round(2*pow(domainSize,0.3333))) #Rice
	binSet.append(round((3.5*std)/pow(domainSize,0.3333))) #Scott normal
	for i in range(0,len(binSet)):
		if(domainSize<(pow(N,0.5)/2)):
			binSet[i] = domainSize
		if(binSet[i] < 2):
			binSet[i] = 2
		if(binSet[i] > binSet[0]):
			binSet[i] = binSet[0]
	binSet = map(int,binSet)
	binSet = set(binSet)
	binSet = list(binSet)
	return binSet

#################################### DYNAMIC (Search) BIN SELECTION ####################################

def binarySearchBins(X, y, measure=0, split=0, useSteps=0, normalizeResult=False, debug=False):
	xbinsetList = []
	xValueList = []
	rangeY = float(len(set(y)))
	for i in range(0,X.shape[1]): #For each feature
		if(debug):
			print "------------------------feature: ", i
		xbinset = []
		explored = []
		repeated = False #flag of repeated bin size
		bestBin = 2
		maxValue = -1
		xi = X[:,i]
		rangeX = float(len(set(xi)))
		#defining range of bins
		if(useSteps==0):
			step = ut.computeStep(rangeX,rangeY,y.shape[0])
			domainx = step[0]
			numbiny = step[1]
		elif(useSteps==1):
			domainx = ut.computeStepNormalized(y.shape[0])
			numbiny = domainx
		elif(useSteps==2):
			domainx = ut.computeStepV2(rangeX,y.shape[0])
			numbiny = ut.computeStepV2(rangeY,y.shape[0])
		elif(useSteps==3):
			domainx = ut.computeStepV2(rangeX,y.shape[0])
			numbiny = rangeY
		elif(useSteps==4):
			domainx = rangeX
			numbiny = ut.computeStepV2(rangeY,y.shape[0])	
		else:
			domainx = rangeX
			numbiny = rangeY	
		
		########### Step 1: Initial Split ###########
		if(split==0):
			currentBins = ut.splitSize(domainx,pow(domainx,0.5),False)
		else:
			currentBins = ut.splitSize(domainx,split,False)
		if(debug):
			print currentBins, split
		while(not(repeated)): #Explore bins
			########### Step 2: Check greater ###########
			if(debug):
				print "currentBins: ", currentBins
			dependencyValues = []
			for numbinx in currentBins: #Compute dependency with each bin proposed
				if(measure==0):
					dependencyValues.append(round(cm.udv(xi,y,int(numbinx),int(numbiny)),2))
				elif(measure==1):
					dependencyValues.append(round(cm.cdv(xi,y,int(numbinx),int(numbiny)),2))
				elif(measure==2):
					dependencyValues.append(round(cm.ucmd(xi,y,int(numbinx),int(numbiny)),2))
				elif(measure==4):
					binValue = dependencyValues.append(round(cm.MI(xi,y,int(numbinx),int(numbiny)),2))
				if(numbinx in explored):
					repeated = True
				else:
					explored.append(numbinx)
			currentMaxPosition = ut.maxPosition(dependencyValues)
			currentMaxValue = dependencyValues[currentMaxPosition]
			if(currentMaxValue>maxValue):
				maxValue = currentMaxValue
				bestBin = currentBins[currentMaxPosition]
			########### Step 3: Get next bins ###########
			explored.sort()
			if(debug):
				print "values: ", dependencyValues
				print "currentMaxPosition: ", currentMaxPosition
				print "explored: ",explored
				print "bestBin:", bestBin
			#Adding try to avoid bin not found
			bbi = explored.index(bestBin) #best bin index
			if(debug):
				print "bbi: ", bbi
			
			#Calculating next inferior and superior limit
			if(len(currentBins)>2):
				if(bbi>=1):
					li = round((explored[bbi]+explored[bbi-1])/2)
				else:
					if(debug):
						print "inferior limit"
					li = round(((explored[bbi+1]+explored[bbi])/2 + 2)/2)
					
				if(bbi+1<len(explored)):
					ls = round((explored[bbi+1]+explored[bbi])/2)
				else:
					if(debug):
						print "superior limit"
					ls = round((li+explored[bbi])/2)
				
				currentBins = [li, ls]
			
			if(debug):
				print "***********"

		if(debug):
			print "maxValue: ", maxValue
			print "bestBin: ", bestBin
		xbinsetList.append(int(bestBin))
		xValueList.append(round(maxValue,2))
	if(normalizeResult):
		xValueList = ut.normalize(xValueList)
	return xValueList


def cuadratureSearchBins(X, measure=1, split=3, xjlist=False, consecutiveDepth=3, maxDepth=7, computeRepeated=False, Debug=False):
	xbinsetList = {}
	xValueList = {}
	
	if(xjlist==False):
		xjlist = range(0,X.shape[1])
	print "xjlist:",xjlist

	for i in range(0,X.shape[1]): #For each feature
		for j in xjlist:
			if(i<j):
				print "feature: ", i, ":", j
				xiBinset = []
				xjBinset = []
				xiExplored = []
				xjExplored = []				
				xiBestBin = 2
				xjBestBin = 2
				maxValue = -1
				currentDepth = 0
				totalDepth = 0
				continueFlag = True
				xi = X[:,i]
				xj = X[:,j]
				xiDomain = int(pow(len(set(xi)),1))+1 #domainSize
				xjDomain = int(pow(len(set(xj)),1))+1 #domainSize
				#Step 1: Initial Split
				if(split==0):
					xiCurrentBins = ut.splitSize(xiDomain,pow(xiDomain,0.7),False)
					xjCurrentBins = ut.splitSize(xjDomain,pow(xjDomain,0.7),False)
				else:
					xiCurrentBins = ut.splitSize(xiDomain,split,False)
					xjCurrentBins = ut.splitSize(xjDomain,split,False)
		
				while(continueFlag): #Explore bins
					print "xiCurrentBins: ", xiCurrentBins
					print "xjCurrentBins: ", xjCurrentBins
					currentDepth = currentDepth + 1
					totalDepth = totalDepth + 1					
					#Step 2: Check greater
					if((currentDepth <= consecutiveDepth) and (totalDepth <= maxDepth) ):
						dependencyValues = []
						for xiNumBin in xiCurrentBins: #Compute dependency with each bin proposed
							for xjNumBin in xjCurrentBins:
								if(measure==1):
									dependencyValues.append(round(cm.umd(xi,xj,int(xiNumBin),int(xjNumBin)),2))
								else:
									dependencyValues.append(round(cm.cmd(xi,xj,int(xiNumBin),int(xjNumBin)),2))
								if(xiNumBin not in xiExplored):
									xiExplored.append(xiNumBin)
								if(xjNumBin not in xjExplored):
									xjExplored.append(xjNumBin)
						currentMaxPosition = ut.maxPosition(dependencyValues)
						xicurrentMaxPosition = int(round(currentMaxPosition/split+0.49))
						xjcurrentMaxPosition = currentMaxPosition%split
						currentMaxValue = dependencyValues[currentMaxPosition]
						maxDepth = maxDepth + 1
						print "currentPositions:", currentMaxPosition, ":", xicurrentMaxPosition, ":", xjcurrentMaxPosition
						if(currentMaxValue>maxValue):
							maxValue = currentMaxValue
							xiBestBin = xiCurrentBins[xicurrentMaxPosition]
							xjBestBin = xjCurrentBins[xjcurrentMaxPosition]
							currentDepth = 1
						print "totalDepth:currentDepth", totalDepth, ":", currentDepth
					
						#Step 3: Get next bins
						xiExplored.sort()
						xjExplored.sort()
						print "values: ", dependencyValues
						print "xiExplored: ",xiExplored
						print "xjExplored: ",xjExplored						
						print "bestBins:", xiBestBin, ":", xjBestBin
						xibb = xiExplored.index(xiBestBin) #best bin index
						xjbb = xjExplored.index(xjBestBin) #best bin index
						print "bbindexes: ", xibb, ":", xjbb
						#xibins
						if(xibb>=1):
							xili = xiExplored[xibb-1]
						else:
							print "xi inferior limit"
							xili = xiExplored[xibb]
						if(xibb+1<len(xiExplored)):
							xils = xiExplored[xibb+1]
						else:
							print "xi superior limit"
							xils = xiExplored[xibb]
						#xjbins
						if(xjbb>=1):
							xjli = xjExplored[xjbb-1]
						else:
							print "xj inferior limit"
							xjli = xjExplored[xjbb]
						if(xjbb+1<len(xjExplored)):
							xjls = xjExplored[xjbb+1]
						else:
							print "xj superior limit"
							xjls = xjExplored[xjbb]
						xiCurrentBins = ut.intervalSplit(xili,xils,split,True)
						xjCurrentBins = ut.intervalSplit(xjli,xjls,split,True)
						print "******"
					else:
						continueFlag = False
				print "maxValue: ", maxValue
				print "bestBins:", xiBestBin, ":", xjBestBin
				xbinsetList[str(i)+":"+str(j)] = [xiBestBin,xjBestBin]
				xValueList[str(i)+":"+str(j)] = round(maxValue,2)
			print "----------------------------------------------------------------"	
	print "================================================================"
	s = sorted(xValueList, key=str.lower)
	for z in s:
		print z, ":", xValueList[z]
	return xbinsetList


def optimalRelevancyBins(X,y,measure=1):
	xbinsetList = []
	xValueList = []
	numbiny = float(len(set(y)))
	featureN = 1
	for i in range(0,X.shape[1]): #For each feature
		bestBin = 0
		maxValue = 0
		x = X[:,i]
		domainx = int(len(set(x)))
		domainx = int(pow(domainx,1.0))
		for numbinx in range(1,domainx):
			if(measure==1):
				currentValue = cm.umd(x,y,int(numbinx),int(numbiny))
			else:
				currentValue = cm.cmd(x,y,int(numbinx),int(numbiny))
			if(currentValue>maxValue):
				maxValue = currentValue
				bestBin = numbinx
		xbinsetList.append(int(bestBin))
		xValueList.append(round(maxValue,2))
	print "================================================================"
	print xbinsetList
	print xValueList

#################################### REDUNDANT ELIMINITATION ####################################
def removeRedundant(X, rank, measure=2, threshold=0.9):
	it = 0
	for i in rank:
		if (len(rank)>1):
			it = it+1
			rankj = rank[it:]
			for j in rankj:
				value = binfeatures(X[:,i],X[:,j],measure=measure)
				if(value>=threshold):				
					rank.remove(j)
	return rank

def binfeatures(xi, xj, measure=2):
	result = []
	binSize = []
	xiBin = computeBinSetStatic(xi)		
	xjBin = computeBinSetStatic(xj)
	value = computeValueRed(xi, xj, xiBin, xjBin, measure)[0]
	return value

def computeValueRed(xi, y, xiBinSet, yBinSet, measure):
	if(measure>4):
		measure=2
	binValueResult = []
	binSetResult = []
	binValue = 0
	maxValue = 0
	binResult = []
	for numbinx in xiBinSet:
		for numbiny in yBinSet:
			if(measure==0):
				binValue = round(cm.udmax(xi,y,int(numbinx),int(numbiny)),2)
			if(measure==1):
				binValue = round(cm.cdmax(xi,y,int(numbinx),int(numbiny)),2)
			if(measure==2):
				binValue = round(cm.ucmd(xi,y,int(numbinx),int(numbiny)),2)
			elif(measure==3):
				binValue = round(cm.MIC(xi,y),2)
			elif(measure==4):
				binValue = round(cm.MI(xi,y,int(numbinx),int(numbiny)),2)
			else:
				binValue = round(cm.ucmd(xi,y,int(numbinx),int(numbiny)),2)
			if(binValue>maxValue):
				maxValue=binValue
				binResult = [numbinx,numbiny]
	return [maxValue, binResult]