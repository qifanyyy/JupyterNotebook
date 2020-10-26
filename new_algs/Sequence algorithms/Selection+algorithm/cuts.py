import model as ml

def greatestDiffCut(weights):
	maxdiff=0
	cutpos=0
	for i in range(0,len(weights)-1):
		diff = weights[i]-weights[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

def monotonicValidationCut(X,y,rank,modelType=0,consecutives=5,runs=3):
	bestScore = 0
	cutpos = 0
	counter = 0
	for i in range(1,len(rank)):
		if(modelType==0):
			score = ml.modelJudge(X=X[:,rank[0:i]], y=y, testPerc=0.4, runs=runs)
		else:
			score = 1/(ml.modelJudge(X=X[:,rank[0:i]], y=y, testPerc=0.4, runs=runs)+1)
		#print bestScore, score, cutpos
		if(bestScore >= score):
			counter = counter + 1
			if(counter>=consecutives):
				cutpos = i-consecutives			
				break
		else:
			counter = 0
			bestScore = score
			cutpos = i
	if(cutpos<=0):
		cutpos=1
	return cutpos

def searchValidationCut(X,y,rank,modelType=0,consecutives=7,runs=3):
	bestScore = 0
	rankPositions = []
	featuresAccepted = []
	counter = 0
	for i in range(0,len(rank)):
		rankPositions.append(i)
		featuresAccepted.append(rank[i])
		if(modelType==0):
			score = ml.modelJudge(X=X[:,featuresAccepted], y=y, modelType=modelType, testPerc=0.4, runs=runs)
		else:
			score = 1/(ml.modelJudge(X=X[:,featuresAccepted], y=y, modelType=modelType, testPerc=0.4, runs=runs)+1)
		if(bestScore >= score):
			rankPositions.remove(i)
			featuresAccepted.remove(rank[i])
			counter = counter + 1
			if(counter>=consecutives):
				break
		else:
			bestScore = score
			counter = 0
	return [featuresAccepted, rankPositions]