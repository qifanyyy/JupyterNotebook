import sys
import json
import time
import argparse
import random
from histogram_sql import *
from vantage_point_utils import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_count",
                        default="100")
    parser.add_argument("--ca_count",
                        default="135")
    parser.add_argument("--vantage_point_set_size",
                        default="1")
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

potentialVantagePoints = [None] * len(vantagePointsDataList)

emptyResilienceSet = {}

vantagePointSetSize = int(args.vantage_point_set_size)


for domainAS, _ in vantagePointsDataList[0][1].items():
  emptyResilienceSet[domainAS] = 0


for i, vantagePointInfo in enumerate(vantagePointsDataList):
  potentialVantagePoints[i] = vantagePointInfo[0]

#potentialVantagePoints = ["19994", "6908"]

def getResilienceSetForVantagePoint(vantagePointASN):
  if vantagePointASN == None:
    return emptyResilienceSet.copy()
  else:
    return vantagePointsData[vantagePointASN]

sampleResilienceSets = [None] * int(args.sample_count)


for randomSampleNumber in xrange(int(args.sample_count)):
  print "Sample number: {0}".format(randomSampleNumber)

  caMaxResilienceSets = [None] * int(args.ca_count)

  for caNumber in xrange(int(args.ca_count)):

  
    
    selectedVantagePoints = [None] * vantagePointSetSize
    selectedResilienceSets = [None] * vantagePointSetSize
    
    # Generate a random set of vantage points without replacement.
    for i in xrange(vantagePointSetSize):
      # Get a random vantage point.
      candidateVantagePoint = random.choice(potentialVantagePoints)
  
      # Make sure it is not already in the set.
      while candidateVantagePoint in selectedVantagePoints:
        candidateVantagePoint = random.choice(potentialVantagePoints)
  
      # Insert it into the set.
      selectedVantagePoints[i] = candidateVantagePoint
  
      # Insert it into the resilience set.
      selectedResilienceSets[i] = vantagePointsData[candidateVantagePoint]
  
    # Get the max resilience set of this random set of vantage points.
    # This line should always be a max to find the maximum resilience of a domain given the vantage points.
    maxResilienceSet = utils.getMaxResilienceSet(*selectedResilienceSets)
    caMaxResilienceSets[caNumber] = maxResilienceSet


  # We have now computed a max resilience set for each CA. We want to now get a summery of the entire market either by taking an average resilience (CAA records in place) or a min resilience (adversarial ability to chose CA).
  summeryResilienceSetFromSample = utils.getMinResilienceSet(*caMaxResilienceSets)
  sampleResilienceSets[randomSampleNumber] = summeryResilienceSetFromSample


# We are now always averaging over samples so this line should always be an average to get proper randomization effect from multiple samples.
averageResilienceSet = utils.getAverageResilienceSet(*sampleResilienceSets)
averageResilience = utils.getAverageResilienceFromSet(averageResilienceSet)
medianResilience = utils.getMedianResilienceFromSet(averageResilienceSet)


print "The average resilience is: {0}".format(averageResilience)
print "The median resilience is: {0}".format(medianResilience)

with open("sqlout.sql", "w") as file:
  file.write(getHistogramSQL(averageResilienceSet, "/tmp/random.csv"))  


#
#minResilienceSet = utils.getMinResilienceSet(*maxResilienceSets)
#
#averageMinResilience = utils.getAverageResilienceFromSet(minResilienceSet)
#medianMinResilience = utils.getMedianResilienceFromSet(minResilienceSet)
#print "Average resilience given choice of CA: {0}".format(averageMinResilience)
#print "Median resilience given choice of CA: {0}".format(medianMinResilience)
#
#