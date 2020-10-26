import util as ut
import cuts
import parallel as p

#modelType = 0 # classification
#modelType >= 1 # regression
#modelType >= 2 # explore if it is classification or reression
#binMethod 0 = Relevancy with total static bin selection
#binMethod 1 = Relevancy with dynamic bin selection
#measure 0 = ud
#measure 1 = cd
#measure 2 = (umd+cmd)/2
#measure 3 = MIC
#measure 4 = MI
#measure 5 = vote (ud + cd)
#measure 6 = vote (ud + cd + mic + mi)
#cutMethod -1 = top20
#cutMethod 0 = greatestDiffCut
#cutMethod 1 = monotonicValidationCut
#cutMethod 2 = fullValidationCut
#cutMethod 3 = searchValidationCut

def featureSelection(X,y, modelType=0, runs=3, processes=0, measure=1, binMethod=0, cutMethod=1, minRed=0, rrThreshold=0.9, debug=False):
	
	if(measure<=4):
		corrMethod = measure
	elif(measure==5):
		measure = [0,1]
	elif(measure==6):
		measure = [1,3,4]
	wlist = []
	if(measure<=4):
		if(binMethod==0):
			weights = p.binStatic(X=X,y=y,processes=processes,measure=corrMethod)
		elif(binMethod==1):
			weights = p.binarySearchBins(X=X, y=y, processes=processes, measure=corrMethod, split=0, useSteps=2, normalizeResult=False, debug=False)			
	else:
		for corrMethod in measure: 	
			if(binMethod==0):
				wlist.append(p.binStatic(X=X,y=y,processes=processes,measure=corrMethod))
			elif(binMethod==1):
				wlist.append(p.binarySearchBins(X=X, y=y, processes=processes, measure=corrMethod, split=0, useSteps=2, normalizeResult=False, debug=False))
		weights = (ut.sumMixedCorrelation(wlist))
	#print weights
	rank = ut.getOrderRank(weights)
	orank = set(rank)
	if(cutMethod==-1):
		rank = rank	[0:20]
	if(cutMethod==0):
		rank = rank[0:cuts.greatestDiffCut(weights=weights)]
	elif(cutMethod==1):
		rank = rank[0:cuts.monotonicValidationCut(X=X, y=y, modelType=modelType, rank=rank, consecutives=5, runs=runs)]
	elif(cutMethod==2):
		#rank = rank[0:cuts.monotonicValidationCut(X=X, y=y, modelType=modelType, rank=rank, consecutives=X.shape[1], runs=runs)]
		[rank,originalRankPositions] = cuts.searchValidationCut(X=X, y=y, modelType=modelType, rank=rank, consecutives=X.shape[1], runs=runs)
	elif(cutMethod==3):
		[rank,originalRankPositions] = cuts.searchValidationCut(X=X, y=y, modelType=modelType, rank=rank, consecutives=5, runs=runs)
	if(debug):
		print "cutted",rank
	if(minRed==1):
		rank = p.parallelRemoveRedundant(X=X, rank=rank, processes=processes, measure=measure, threshold=rrThreshold)
	if(debug):
		print "mrmr",rank
	#print "weights:",
	#for i in rank:
	#	print weights[i],
	#print
	return rank