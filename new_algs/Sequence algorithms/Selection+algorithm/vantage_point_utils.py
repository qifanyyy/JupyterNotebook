
class Utils:
  def __init__(self, asWeightsDictionary, sumOfAllASWeights):
    self.asWeightData = asWeightsDictionary
    self.totalASWeights = sumOfAllASWeights

  def getAverageResilienceVantagePoint(self, vatnagePointInfo):
    return self.getAverageResilienceFromSet(self, vatnagePointInfo[1])
  
  def getMaxResilienceSet(self, *resilienceSets):
    result = {}
    for domainAS, _ in resilienceSets[0].items():
      maxForThisDomainAS = 0
      for resilienceSet in resilienceSets:
        maxForThisDomainAS = max(maxForThisDomainAS, resilienceSet[domainAS])
      result[domainAS] = maxForThisDomainAS
    return result

  def getMinResilienceSet(self, *resilienceSets):
    result = {}
    for domainAS, _ in resilienceSets[0].items():
      minForThisDomainAS = 1
      for resilienceSet in resilienceSets:
        minForThisDomainAS = min(minForThisDomainAS, resilienceSet[domainAS])
      result[domainAS] = minForThisDomainAS
    return result

  def getAverageResilienceSet(self, *resilienceSets):
    result = {}
    for domainAS, _ in resilienceSets[0].items():
      sumForThisDomainAS = 0
      for resilienceSet in resilienceSets:
        sumForThisDomainAS += resilienceSet[domainAS]
      result[domainAS] = sumForThisDomainAS / len(resilienceSets)
    return result
  
  def getAverageResilienceFromSet(self, resilienceSet):
    resilienceSum = 0
    resilienceSetItems = resilienceSet.items()
    for domainAS, resilience in resilienceSetItems:
      try:
        resilienceSum += resilience * self.asWeightData[domainAS]
      except KeyError, e:
        print "Domain ASN: {0} not found in as weight file. Exiting.".format(domainAS)
        exit()
    return resilienceSum / self.totalASWeights
  
  
  def getMedianResilienceFromSet(self, resilienceSet):
    selectedIndexNumber = int(self.totalASWeights / 2)
    resilienceSetItems = sorted(resilienceSet.items(), key=lambda setEntry: setEntry[1])
    currentTotalASWeight = 0
    for domainAS, resilience in resilienceSetItems:
      currentTotalASWeight += self.asWeightData[domainAS]
      if currentTotalASWeight > selectedIndexNumber:
        return resilience
    print "Median resilience code never reached 50% mark. Improper exit."
    exit()