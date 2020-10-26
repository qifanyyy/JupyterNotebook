import os
import sys
import json

version = "New"

def clusterParser( logFile ):
	cluster = []
	for line in logFile:
		if 'Number of colors:' in line or 'Average number of nodes' in line or 'end_used_colors' in line:
			break
		itms = line.split( sep = ' ' )
		nn = int( itms[1] )
		cluster.append(nn)
	return line, cluster

def lineParser( logFile ):
	tempDict = {}
	for line in logFile:
		if 'Color histogram:' in line:
			line, tempDict["colorClusters"] = clusterParser( logFile )
		if 'Max deg:' in line:
			tempDict["maxDeg"] = int( line.split(sep = ' ')[2] )
			tempDict["minDeg"] = int( line.split(sep = ' ')[6] )
			tempDict["avgDeg"] = float( line.split(sep = ' ')[10] )
		if 'Nodes:' in line:
			tempDict["nnodes"] = int( line.split(sep = ' ')[1] )
			tempDict["nedges"] = int( line.split(sep = ' ')[4] )
		if 'Edge probability' in line:
			tempDict["edgeProb"] = float( line.split(sep = ' ')[6] )
		if 'Repetition:' in line:
			tempDict["repet"] = int( line.split(sep = ' ')[1] )
		if 'Iteration performed:' in line:
			tempDict["performedIter"] = int( line.split(sep = ' ')[2] )
		if 'Max iteration' in line:
			if 'no' in line:
				tempDict["convergence"] = True
			else:
				tempDict["convergence"] = False
		if 'Execution time:' in line:
			tempDict["execTime"] = float( line.split(sep = ' ')[2] )
		if 'Number of colors:' in line:
			tempDict["numColors"] = int( line.split(sep = ' ')[3] )
		if 'Used colors:' in line:
			tempDict["usedColors"] = int( line.split(sep = ' ')[7] )
		if 'Color ratio:' in line:
			tempDict["colorRatio"] = float( line.split(sep = ' ')[2] )
		if 'Average number' in line:
			tempDict["avgNodesPerColor"] = float( line.split(sep = ' ')[7] )
		if 'Variance:' in line:
			tempDict["varNodesPerColor"] = float( line.split(sep = ' ')[1] )
		if 'StD:' in line:
			tempDict["stdNodesPerColor"] = float( line.split(sep = ' ')[1] )
	return tempDict

def mcmcGpuLineParser( logFile ):
	tempDict = {}
	iterCount = 0
	for line in logFile:
		if 'max_iteration_reached' in line:
			if 'no' in line:
				tempDict["convergence"] = True
			else:
				tempDict["convergence"] = False
			line, tempDict["colorClusters"] = clusterParser( logFile )
		if 'time ' in line:
			tempDict["execTime"] = float( line.split(sep = ' ')[1] )
		if 'iteration_' in line:
			iterCount = iterCount + 1
		if 'numCol ' in line:
			tempDict["numColors"] = int( line.split(sep = ' ')[1] )
		if 'numColorRatio' in line:
			tempDict["colorRatio"] = float( line.split(sep = ' ')[1] )
		if 'end_used_colors' in line:
			tempDict["usedColors"] = int( line.split(sep = ' ')[1] )
		if 'end_average' in line:
			tempDict["avgNodesPerColor"] = float( line.split(sep = ' ')[1] )
		if 'end_variance' in line:
			tempDict["varNodesPerColor"] = float( line.split(sep = ' ')[1] )
		if 'end_standard_deviation' in line:
			tempDict["stdNodesPerColor"] = float( line.split(sep = ' ')[1] )

	tempDict["performedIter"] = iterCount
	return tempDict

def parseDirs( baseDir ):
	s = os.sep
	basePath = baseDir
	subDir = os.listdir( basePath )
	totResLuby = {}
	totResMCMC_CPU = {}
	totResMCMC_GPU = {}
	for currDir in subDir:
		if os.path.isfile( basePath + s + currDir ):
			continue
		filesInDir = os.listdir( basePath + s + currDir )
		lubyRes = []
		mcmcCpuRes = []
		mcmcGpuRes = []
		colorRatio = currDir.split(sep = '-')[2]
		for currLog in filesInDir:
			numNodes = currLog.split( sep='-' )[0]
			prob = currLog.split( sep='-' )[1]


			if 'LUBY' in currLog:
				with open( basePath + s + currDir + s + currLog ) as logFile:
					tempItem = lineParser( logFile )
					tempItem["algo"] = "LUBY"
					lubyRes.append( tempItem )
			if 'MCMC' in currLog:
				with open( basePath + s + currDir + s + currLog ) as logFile:
					tempItem = lineParser( logFile )
					tempItem["algo"] = "MCMC_CPU"
					mcmcCpuRes.append( tempItem )
			if 'resultsFile' in currLog:
				with open( basePath + s + currDir + s + currLog ) as logFile:
					tempItem = mcmcGpuLineParser( logFile )
					tempItem["repet"] = int( (currLog.split( sep = '-')[3]).split( sep = '.')[0] )
					tempItem["algo"] = "MCMC_GPU"
					mcmcGpuRes.append( tempItem )

		if lubyRes:
			totResLuby[str(numNodes) + '-' + str(prob) + '-' + str(colorRatio)] = lubyRes
		if mcmcCpuRes:
			totResMCMC_CPU[str(numNodes) + '-' + str(prob) + '-' +  str(colorRatio)] = mcmcCpuRes
		if mcmcGpuRes:
			totResMCMC_GPU[str(numNodes) + '-' + str(prob) + '-' +  str(colorRatio)] = mcmcGpuRes

	with open( basePath + s + 'outLuby.json', "w") as outFile:
		json.dump( totResLuby, outFile )
	with open( basePath + s + 'outMCMC_CPU.json', "w") as outFile:
		json.dump( totResMCMC_CPU, outFile )
	with open( basePath + s + 'outMCMC_GPU.json', "w") as outFile:
		json.dump( totResMCMC_GPU, outFile )

def avgCalc( exp, item, discardNotConvergent = True ):
	itemAccum = 0
	itemCounter = 0
	for expRun in exp:
		if discardNotConvergent:
			if expRun["convergence"]:
				itemAccum += expRun[item]
				itemCounter += 1
		else:
			itemAccum += expRun[item]
			itemCounter += 1
	if itemCounter > 0:
		return itemAccum / itemCounter
	else:
		return None

def statMakerFromJson( baseDir ):
	s = os.sep
	basePath = baseDir
	with open( basePath + s + "outLuby.json", "r" ) as read_file:
		dataLuby = json.load( read_file )
	with open( basePath + s + "outMCMC_CPU.json", "r") as read_file:
		dataMcmcCpu = json.load( read_file )
	with open( basePath + s + "outMCMC_GPU.json", "r") as read_file:
		dataMcmcGpu = json.load( read_file )

	results = {}

	for exxp in dataLuby:
		lubyAvg = {}
		graphs = []
		lubyAvg["numColors"] = avgCalc(dataLuby[exxp], "numColors", discardNotConvergent = False)
		lubyAvg["execTime"] = avgCalc(dataLuby[exxp], "execTime", discardNotConvergent = False)
		lubyAvg["avgNodesPerColor"] = avgCalc(dataLuby[exxp], "avgNodesPerColor", discardNotConvergent = False)
		lubyAvg["varNodesPerColor"] = avgCalc(dataLuby[exxp], "varNodesPerColor", discardNotConvergent = False)
		lubyAvg["stdNodesPerColor"] = avgCalc(dataLuby[exxp], "stdNodesPerColor", discardNotConvergent = False)
		for exp in dataLuby[exxp]:
			graphDict = {}
			graphDict["nNodes"] = exp["nnodes"]
			graphDict["nEdges"] = exp["nedges"]
			graphDict["edgeProb"] = exp["edgeProb"]
			graphDict["maxDeg"] = exp["maxDeg"]
			graphDict["minDeg"] = exp["minDeg"]
			graphDict["avgDeg"] = exp["avgDeg"]
			graphs.append(graphDict)

		results[exxp] = {}
		results[exxp]["graphs"] = graphs
		results[exxp]["Luby"] = {}
		results[exxp]["Luby"]["Exp"] = dataLuby[exxp]
		results[exxp]["Luby"]["Avg"] = lubyAvg
		for ee in results[exxp]["Luby"]["Exp"]:
			ee.pop("nnodes")
			ee.pop("nedges")
			ee.pop("maxDeg")
			ee.pop("minDeg")
			ee.pop("avgDeg")
			ee.pop("edgeProb")

	for exp in dataMcmcCpu:
		results[exp]["MCMC_CPU"] = {}
		results[exp]["MCMC_CPU"]["Exp"] = dataMcmcCpu[exp]
		for ee in results[exp]["MCMC_CPU"]["Exp"]:
			ee.pop("nnodes")
			ee.pop("nedges")
			ee.pop("maxDeg")
			ee.pop("minDeg")
			ee.pop("avgDeg")
			ee.pop("edgeProb")
			if version == "Old":
				if int( ee["performedIter"] ) >= float( ee["numColors"] ):
					ee["convergence"] = False
				else:
					ee["convergence"] = True

		mcmcDict = {}
		mcmcDict["numColors"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "numColors")
		mcmcDict["usedColors"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "usedColors")
		mcmcDict["execTime"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "execTime")
		mcmcDict["avgNodesPerColor"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "avgNodesPerColor")
		mcmcDict["varNodesPerColor"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "varNodesPerColor")
		mcmcDict["stdNodesPerColor"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "stdNodesPerColor")
		mcmcDict["performedIter"] = avgCalc(results[exp]["MCMC_CPU"]["Exp"], "performedIter")
		results[exp]["MCMC_CPU"]["Avg"] = mcmcDict

	for exp in dataMcmcGpu:
		results[exp]["MCMC_GPU"] = {}
		results[exp]["MCMC_GPU"]["Exp"] = dataMcmcGpu[exp]

		for ee in results[exp]["MCMC_GPU"]["Exp"]:
			if version == "Old":
				if int( ee["performedIter"] ) >= float( ee["numColors"] ):
					ee["convergence"] = False
				else:
					ee["convergence"] = True

		mcmcDict = {}
		mcmcDict["numColors"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "numColors")
		mcmcDict["usedColors"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "usedColors")
		mcmcDict["execTime"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "execTime")
		mcmcDict["avgNodesPerColor"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "avgNodesPerColor")
		mcmcDict["varNodesPerColor"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "varNodesPerColor")
		mcmcDict["stdNodesPerColor"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "stdNodesPerColor")
		mcmcDict["performedIter"] = avgCalc(results[exp]["MCMC_GPU"]["Exp"], "performedIter")
		results[exp]["MCMC_GPU"]["Avg"] = mcmcDict

	if version == "New":
		colorRatiosSet = set()
		finalDict = {}
		for exp in results:
			colorRatiosSet.add( exp.split(sep = '-')[2] )
		for rs in colorRatiosSet:
			expList = []
			for exp in results:
				if exp.split(sep = '-')[2] == rs:
					expList.append( results[exp] )

			finalDict[rs] = expList

		for rs in finalDict:
			colorRatio = float( rs )
			invColorRatio = 1 / float( rs )
			for exp in finalDict[rs]:
				exp["colorRatio"] = colorRatio
				exp["invColorRatio"] = invColorRatio
				exp["edgeProb"] = exp["graphs"][0]["edgeProb"]
				exp["nNodes"] = exp["graphs"][0]["nNodes"]
	else:
		finalDict = results

	with open( basePath + s + 'finalRes.json', "w") as outFile:
		json.dump( finalDict, outFile )

if __name__ == '__main__':
	baseDir = sys.argv[1]
	if len( sys.argv ) > 2:
		version = sys.argv[2]
	if version not in ["Old", "New"]:
		version = "New"
	if not baseDir:
		exit()
	parseDirs( baseDir )
	statMakerFromJson( baseDir )
