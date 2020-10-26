import json
import sys
from math import sqrt, ceil
import matplotlib.pyplot as plt
import numpy as np

# Draws balancing index graphs
# Feed me a json file in the 'Old' format (fixed density)

def balIdxEval( clusters, mu, k ):
	balIdx = 0
	for nodesInColor in clusters:
		balIdx += ((nodesInColor - mu) * (nodesInColor - mu))
	balIdx /= k
	return sqrt( balIdx )

def readBalIdxFromJson( filenm ):
	with open( filenm, "r" ) as read_file:
		dataFromJson = json.load( read_file )

	balIdxList = []

	for exp in dataFromJson:
		n = dataFromJson[exp]["graphs"][0]["nNodes"]
		p = dataFromJson[exp]["graphs"][0]["edgeProb"]
		k = n * p
		mu = n / k
		MCPU_balIdxs = []
		MGPU_balIdxs = []
		Luby_balIdxs = []

		for rept in dataFromJson[exp]["MCMC_CPU"]["Exp"]:
			if not rept["convergence"]:
				continue
			colorClusters = rept["colorClusters"]
			balIdx = balIdxEval( colorClusters, mu, k )
			MCPU_balIdxs.append( balIdx )
		for rept in dataFromJson[exp]["MCMC_GPU"]["Exp"]:
			if not rept["convergence"]:
				continue
			colorClusters = rept["colorClusters"]
			balIdx = balIdxEval( colorClusters, mu, k )
			MGPU_balIdxs.append( balIdx )
		for rept in dataFromJson[exp]["Luby"]["Exp"]:
			colorClusters = rept["colorClusters"]
			balIdx = balIdxEval( colorClusters, mu, k )
			Luby_balIdxs.append( balIdx )

		tempDict = {
			"nNodes": n,
			"edgeProb": p,
			"mu": mu,
			"k": k,
			"MCPU_balIdxs": MCPU_balIdxs,
			"MGPU_balIdxs": MGPU_balIdxs,
			"Luby_balIdxs": Luby_balIdxs,
		}

		balIdxList.append( tempDict )

	return balIdxList

def drawBalIdxGraphs( balIdxList, prob ):
	x = []
	yLuby = []
	yMCPU = []
	yMGPU = []
	for elem in balIdxList:
		if elem["edgeProb"] != prob:
			continue
		yLuby.append( sum(elem["Luby_balIdxs"]) / float( len(elem["Luby_balIdxs"]) ) )
		yMCPU.append( sum(elem["MCPU_balIdxs"]) / float( len(elem["MCPU_balIdxs"]) ) )
		yMGPU.append( sum(elem["MGPU_balIdxs"]) / float( len(elem["MGPU_balIdxs"]) ) )
		x.append( elem["nNodes"] )

	#avgCPU = sum(yMCPU) / float( len(yMCPU) )
	avgGPU = sum(yMGPU) / float( len(yMGPU) )

	x = np.array( x )
	yLuby = np.array( yLuby )
	yMCPU = np.array( yMCPU )
	yMGPU = np.array( yMGPU )

	ii = np.argsort( x )
	x = x[ii]
	yLuby = yLuby[ii]
	yMCPU = yMCPU[ii]
	yMGPU = yMGPU[ii]

	# Convert x ticks in string: 25000 -> 25k
	xlabels = [str(ceil(a / 1000)) + 'k' for a in x]

	fig = plt.figure()
	plt.plot( x, yLuby, label='Luby', color='b', linestyle='-', marker='o' )
	plt.plot( x, yMCPU, label='MCMC CPU', color='g', linestyle='-', marker='o' )
	plt.plot( x, yMGPU, label='MCMC GPU', color='r', linestyle='-', marker='o' )
	plt.legend()
	plt.grid( True )
	plt.xticks( x, labels = xlabels )
	plt.xlabel( 'nodes' )
	plt.ylabel( 'Balance Index' )
	plt.title( 'Balance Index - prob. ' + str( prob ) )
	plt.annotate( 'Average = {:.2f}'.format(avgGPU), xy=(x[3] + (x[4] - x[3]) / 2, yMCPU[3]),
		xytext=(x[2], yLuby[2] / 3.5), arrowprops = dict(arrowstyle='->'), )
	plt.show()


##########################
if __name__ == '__main__':
	filename = sys.argv[1]

	balIdxList = readBalIdxFromJson( filename )
	drawBalIdxGraphs( balIdxList, 0.001 )
	drawBalIdxGraphs( balIdxList, 0.005 )
