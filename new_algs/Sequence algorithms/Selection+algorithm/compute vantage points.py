import sys
import json
import time
import argparse
import random
from histogram_sql import *
from vantage_point_utils import *

def parse_args():
    parser = argparse.ArgumentParser()
    # This is a CAIDA AS topology.
    parser.add_argument("--initial_vantage_point",
                        default="max")
    parser.add_argument("--retry_count",
                        default="1")
    # These are the ASes that we are using as vantage points.
    parser.add_argument("--fix_initial_vantage_point",
                        default="false")
    # These are the ASNs that we are calculating the resilience for.
    parser.add_argument("--max_iterations",
                        default="20")
    parser.add_argument("--vantage_point_set_size",
                        default="5")
    return parser.parse_args()


# A resilience set is a dictionary of domain ASes and their resiliences for a given vantage point.
# vatnagePointInfo[1] is the resilience set. vatnagePointInfo[0] is the vantage point ASN.


args = parse_args()


vantagePointsData = json.load(open('cg_resilience.json'))
vantagePointsDataList = vantagePointsData.items()
asWeightData = json.load(open('as-weights.json'))
totalASWeights = 0
for asWeightPair in asWeightData.items():
	totalASWeights += asWeightPair[1]

utils = Utils(asWeightData, totalASWeights)



potentialVantagePoints = []

emptyResilienceSet = {}

vantagePointSetSize = int(args.vantage_point_set_size)
selectedVantagePoints = [None] * vantagePointSetSize

# Make selected vantage point sets to be an empty dictionary.
selectedVantagePointSets = {}


maxIterations = int(args.max_iterations)

for domainAS, _ in vantagePointsDataList[0][1].items():
	emptyResilienceSet[domainAS] = 0


potentialVantagePoints = vantagePointsData.keys()


#for vantagePointInfo in vantagePointsDataList:
#	potentialVantagePoints.append(vantagePointInfo[0])


def metric(resilienceSet):
	global utils
	return utils.getAverageResilienceFromSet(resilienceSet)

def getResilienceSetForVantagePoint(vantagePointASN):
	if vantagePointASN == None:
		return emptyResilienceSet.copy()
	else:
		return vantagePointsData[vantagePointASN]


def getVantagePointArrayFromVantagePointIdentifier(vantagePointIdentifier):
	return vantagePointIdentifier.split()


currentVantagePointIndex = 0

if args.initial_vantage_point.lower() != "max":
	if not args.initial_vantage_point in potentialVantagePoints:
		print "Initial vantage point not found in list of potential vantage points."
		exit()
	selectedVantagePoints[0] = args.initial_vantage_point
	currentVantagePointIndex += 1
	currentVantagePointIndex = currentVantagePointIndex % vantagePointSetSize 

for randomStartingPointNumber in xrange(int(args.retry_count)):
	
	
	passesCount = 0
	
	vantagePointsInEqualibrium = 0
	
	while True: # loop over passes
		print "Pass number: {0} Current recommended vantage point set: ".format(passesCount)
		print selectedVantagePoints
		print "\n"
		while True: # loop over each vantage point in the potential vantage point set.
			print "Currently on vantage point index: {0}".format(currentVantagePointIndex)
			if args.fix_initial_vantage_point.lower() == "true" and currentVantagePointIndex == 0:
				vantagePointsInEqualibrium += 1
				currentVantagePointIndex += 1
				if currentVantagePointIndex == vantagePointSetSize:
					currentVantagePointIndex = 0
					break
				continue
			# Get the resilience sets of all the vantage points excluding the one we are working on.
			relavantResilienceSets = []
			
			# Debugging print. Not needed if current vantage points are printed on each pass.
			#print selectedVantagePoints
	
			for i in xrange(len(selectedVantagePoints)):
				if i == currentVantagePointIndex:
					continue
				relavantResilienceSets.append(getResilienceSetForVantagePoint(selectedVantagePoints[i]))
	
			# Get the max of the resilience sets of all the other vantage poitns.
	
			currentMaxResilienceSet = utils.getMaxResilienceSet(*relavantResilienceSets)
	
			# Get the average resilience of the above computed set.
			currentAverageResilience = metric(currentMaxResilienceSet)
	
	
			# Get the vantage point we were previously considering for this location.		
			previouslyConsideredVantagePoint = selectedVantagePoints[currentVantagePointIndex]
	
			vantagePointWithMaximumResilienceIncrease = 0
			maximumResilienceIncrease = 0
	
			for consideredVantagePoint in potentialVantagePoints: # loop over all of our considered vantage points that we might put into this spot.
				newMaxResilienceSetGivenVantagePoint = utils.getMaxResilienceSet(currentMaxResilienceSet, vantagePointsData[consideredVantagePoint])
				averageNewResilience = metric(newMaxResilienceSetGivenVantagePoint)
				resilienceIncrease = averageNewResilience - currentAverageResilience
				if resilienceIncrease > maximumResilienceIncrease:
					# This vantage point has currently been the best one of the potential vantage points we have found.
					vantagePointWithMaximumResilienceIncrease = consideredVantagePoint
					maximumResilienceIncrease = resilienceIncrease
	
			if vantagePointWithMaximumResilienceIncrease == 0:
				print "Warning: In current set, vantage point: {0} does not increase resilience.".format(previouslyConsideredVantagePoint)
	
			if vantagePointWithMaximumResilienceIncrease == previouslyConsideredVantagePoint or vantagePointWithMaximumResilienceIncrease == 0:
				vantagePointsInEqualibrium += 1
			else:
				selectedVantagePoints[currentVantagePointIndex] = vantagePointWithMaximumResilienceIncrease
	
			currentVantagePointIndex += 1
			if currentVantagePointIndex == vantagePointSetSize:
				currentVantagePointIndex = 0
				break
	
		passesCount += 1
	
		if vantagePointsInEqualibrium == vantagePointSetSize:
			break
	
		vantagePointsInEqualibrium = 0
	
		if passesCount == maxIterations:
			break

	vantagePointSetIdentifier = " ".join(sorted(selectedVantagePoints))
	equilibrium = vantagePointsInEqualibrium == vantagePointSetSize
	vantagePointIdentifierAlreadyInDictionary = vantagePointSetIdentifier in selectedVantagePointSets

	if vantagePointIdentifierAlreadyInDictionary and equilibrium:
		selectedVantagePointSets[vantagePointSetIdentifier]["count"] += 1
	elif not vantagePointIdentifierAlreadyInDictionary:
		# The key is not in the dictionary so we must initialize.
		selectedVantagePointSets[vantagePointSetIdentifier] = {}

		# Compute the max resilience set.
		resilienceSets = []
		for i in xrange(len(selectedVantagePoints)):
			resilienceSets.append(getResilienceSetForVantagePoint(selectedVantagePoints[i]))

		maxResilienceSet = utils.getMaxResilienceSet(*resilienceSets)

		# Imput the max resilience set into the dictionary.
		selectedVantagePointSets[vantagePointSetIdentifier]["resilienceSet"] = maxResilienceSet

		selectedVantagePointSets[vantagePointSetIdentifier]["count"] = 1 if equilibrium else 0
		selectedVantagePointSets[vantagePointSetIdentifier]["metricResilience"] = metric(maxResilienceSet)
	
	if int(args.retry_count) == 1:
		break

	selectedVantagePoints = [None] * vantagePointSetSize

	selectedVantagePoints = [random.choice(potentialVantagePoints) for i in xrange(vantagePointSetSize)]

	currentVantagePointIndex += 1
	currentVantagePointIndex = currentVantagePointIndex % vantagePointSetSize 
print "\n"



if int(args.retry_count) == 1:
	if vantagePointsInEqualibrium == vantagePointSetSize:
		print "An equilibrium was found."
	else:
		print "Script exited after {0} passes. No equilibrium found.".format(passesCount)
	
	print "The set of maximum vantage points is: "
	print selectedVantagePoints
else:
	# Output for random initial state runs.

	# Remember, if the metric is changed away from average or median we might want to still sort in terms of average because average is likely the final metric we will use.
	sortedSelectedVantagePointSets = sorted(selectedVantagePointSets.items(), key=lambda kvp: kvp[1]["metricResilience"], reverse=True)
	print "All selected vantage in preference order points are: {0}".format([(kvp[0], kvp[1]["count"], kvp[1]["metricResilience"]) for kvp in sortedSelectedVantagePointSets])
	print "The set of vantage points found with the highest resilience is: {0}.".format(sortedSelectedVantagePointSets[0][0])

	popularitySortedSelectedVantagePointSets = sorted(selectedVantagePointSets.items(), key=lambda kvp: kvp[1]["count"], reverse=True)

	print "All selected vantage in popularity order points are: {0}".format([kvp[0] for kvp in popularitySortedSelectedVantagePointSets])
	popularityRanking = len(popularitySortedSelectedVantagePointSets)
	for i in xrange(len(popularitySortedSelectedVantagePointSets)):

		# If the current vantage point weare on corrosponds to the the best vantage point.
		if popularitySortedSelectedVantagePointSets[i][0] == sortedSelectedVantagePointSets[0][0]:
			popularityRanking = i + 1

	print "This set is number {0} in terms of popularity.".format(popularityRanking)



	# Set selected vatage points so the analysis below is correct.
	selectedVantagePoints = getVantagePointArrayFromVantagePointIdentifier(sortedSelectedVantagePointSets[0][0])





resilienceSets = []
for i in xrange(len(selectedVantagePoints)):
	resilienceSets.append(getResilienceSetForVantagePoint(selectedVantagePoints[i]))

maxResilienceSet = utils.getMaxResilienceSet(*resilienceSets)


print "The average resilience given these selected vantage points is: {0}".format(utils.getAverageResilienceFromSet(maxResilienceSet))


print "The median resilience given these selected vantage poitns is: {0}".format(utils.getMedianResilienceFromSet(maxResilienceSet))

with open("gen-histogram.sql", "w") as histogram_file:
    histogram_file.write(getHistogramSQL(maxResilienceSet, "/tmp/resiliences.csv"))

# Consider outputing histogram code.
exit()