import multiprocessing
import binSelection as bs
from functools import partial

def splitArray(number, size):
	ss = number/float(size)
	indexes = []
	current = 0
	while (current<=number):
		indexes.append(current)
		current += ss
	for i in range(0,len(indexes)):
		indexes[i] = int(indexes[i])
	if((number-1)>indexes[-1]):
		indexes.append(number)
	elif(indexes[-1]>=(number-1)):
		indexes[-1] = number
	indexes = list(set(indexes))
	indexes.sort()
	return indexes

def tuplesPoolGenerator(size,nsplits):
	sArray = splitArray(size,nsplits)
	tl = []
	for i in range(0,len(sArray)-1):
		tl.append([sArray[i],sArray[i+1]])
	return tuple(tl)

def splitInformation(info,nsplits):
	tl = tuplesPoolGenerator(int(info.shape[1]),nsplits)
	sInfo = []
	for i in tl:
		sInfo.append(info[:,i[0]:i[1]])
	return tuple(sInfo)

def splitInformationRows(info,nsplits):
	tl = tuplesPoolGenerator(int(info.shape[0]),nsplits)
	sInfo = []
	for i in tl:
		sInfo.append(info[i[0]:i[1],:])
	return tuple(sInfo)

#################################### RELEVANCE IDENTIFICATION ####################################

def binStatic(X, y, processes=0, measure=2):
	cores = multiprocessing.cpu_count()
	nfeat = X.shape[1]
	pareval = int(nfeat*pow(len(list(set(y))),0.7)*pow(cores,0.5)*len(y)*2)
	if(pareval>1000000):
		if(processes==0):
			jobs = cores
			if(cores>nfeat):
				jobs = nfeat
		else:	
			jobs=processes
		pool = multiprocessing.Pool(processes=jobs)
		info = splitInformation(X,jobs)
		pbs=partial(bs.binStatic, y=y, measure=measure)
		presults = pool.map(pbs, info)
		results = [item for sublist in presults for item in sublist]
		pool.close()
		pool.join()
		return results
	else:
		return bs.binStatic(X,y,measure=measure)
	

def binarySearchBins(X, y, processes=0, measure=0, split=0, useSteps=0, normalizeResult=False, debug=False):
	if(measure==3):
		return binStatic(X,y,0,3)
	cores = multiprocessing.cpu_count()
	nfeat = X.shape[1]
	pareval = int(nfeat*pow(len(list(set(y))),0.7)*pow(cores,0.5)*len(y)*2)
	if(pareval>1000000): 
		if(processes==0):
			jobs = cores
			if(cores>nfeat):
				jobs = nfeat
		else:	
			jobs=processes
		pool = multiprocessing.Pool(processes=jobs)
		info = splitInformation(X,jobs)
		pbs=partial(bs.binarySearchBins, y=y, measure=measure, split=split, useSteps=useSteps, normalizeResult=normalizeResult, debug=debug)
		presults = pool.map(pbs, info)
		results = [item for sublist in presults for item in sublist]
		pool.close()
		pool.join()
		return results
	else:
		return bs.binarySearchBins(X, y=y, measure=measure, split=split, useSteps=useSteps, normalizeResult=normalizeResult, debug=debug)

#################################### REDUNDANT ELIMINITATION ####################################
def parallelRemoveRedundant(X, rank, processes=0, measure=2, threshold=0.9):
	cores = multiprocessing.cpu_count()
	samples = X.shape[0]
	if(processes==0):
		jobs = cores
		if(cores>samples):
			jobs = samples
	else:	
		jobs=processes	
	pool = multiprocessing.Pool(processes=jobs)
	info = splitInformationRows(X,jobs)
	pbs=partial(bs.removeRedundant, rank=rank, measure=measure, threshold=threshold)
	results = pool.map(pbs, info)
	removeSet = set(rank) - set(results[0])
	for r in results[1:]:
		removeSet = removeSet & (set(rank) - set(r))
	for s in removeSet:
		rank.remove(s)
	pool.close()
	pool.join()
	return rank