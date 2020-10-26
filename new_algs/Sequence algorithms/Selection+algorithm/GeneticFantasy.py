import random
import csv
import copy
import time

class Player(object):
	def __init__(self, row):
		self.name=row[0]
		self.team=row[1]
		self.cost=float(row[2])
		self.totalScore=int(row[3])
		self.roundScore=int(row[4])
		self.ppg=float(row[5])
		self.minutes=int(row[6])
		self.ppm=float(row[7])
		self.gw2Score=int(row[8])
		self.selected=False
	
	def __str__(self):
		return "[%s,%s,%0.1f,%d,%d,%0.1f,%d,%0.4f,%d, %d]"%(self.name,
			self.team, self.cost, self.totalScore, self.roundScore,
			self.ppg, self.minutes, self.ppm, self.gw2Score, self.selected)

			
def readData(data):
	readGoalkeeperData(data)
	readDefenderData(data)
	readMidfielderData(data)
	readForwardData(data)
	
def readGoalkeeperData(data):
	data.gkList=[]
	with open("Goalkeepers.csv") as goalkeepers:
		file=csv.reader(goalkeepers, delimiter=',')
		for row in file:
			goalkeeper=Player(row)
			data.gkList.append(goalkeeper)		
			
def readDefenderData(data):
	data.defList=[]
	with open("Defenders.csv") as defenders:
		file=csv.reader(defenders, delimiter=',')
		for row in file:
			defender=Player(row)
			data.defList.append(defender)		
	
def readMidfielderData(data):
	data.midList=[]
	with open("Midfielders.csv") as midfielders:
		file=csv.reader(midfielders, delimiter=',')
		for row in file:
			midfielder=Player(row)
			data.midList.append(midfielder)		
	
def readForwardData(data):
	data.fwdList=[]
	with open("Forwards.csv") as forwards:
		file=csv.reader(forwards, delimiter=',')
		for row in file:
			forward=Player(row)
			data.fwdList.append(forward)
	
def printPopulation(data):
	for individual in data.population:
		printIndividual(data, individual)
		
def printIndividual(data, individual):
	print "Fitness:", calcFitness(data, individual)
	print "Cost:", calcCost(data, individual)
	# for key in individual:
		# for player in individual[key]:
			# if player.selected==True:
				# print key, player
	
def calcCost(data, individual):
	totalCost=0
	for key in individual:
		for player in individual[key]:
			if player.selected==True:
				totalCost+=player.cost
				
	return totalCost

def calcFitness(data, individual):
	d=data
	totalFitness=0	
	for key in individual:
		for player in individual[key]:
			if player.selected==True:
				normTotalScore=player.totalScore/d.cumulativeTotalScore
				normRoundScore=player.roundScore/d.cumulativeRoundScore
				normMinutes=player.minutes/d.cumulativeMinutes
				normPPM=player.ppm/d.cumulativePPM
				normPPG=player.ppm/d.cumulativePPG
				playerFitness=(d.tsW*normTotalScore+d.rsW*normRoundScore+
					d.minW*normMinutes+d.ppmW*normPPM+d.ppgW*normPPG)
				totalFitness+=playerFitness
					
	return totalFitness

def findMaxFitness(data):
	maxFitness=calcFitness(data, data.population[0])
	for individual in data.population:
		fitness=calcFitness(data, individual)
		if fitness>maxFitness:
			maxFitness=fitness
	return maxFitness

def calcGWScore(data, individual):
	score=0
	for key in individual:
		for player in individual[key]:
			if player.selected==True:
				score+=player.gw2Score
	return score
	
def calcTotalScore(data, individual):
	totalScore=0
	for key in individual:
		for player in individual[key]:
			if player.selected==True:
				totalScore+=player.totalScore
	return totalScore

def writeData(data):
	for individual in data.population:
		fitness=calcFitness(data, individual)
		score=calcGWScore(data, individual)
		cost=calcCost(data, individual)
		totalScore=calcTotalScore(data, individual)
		with open('fitnessvsscore.csv', 'a') as csvfile:
			writer = csv.writer(csvfile,delimiter='\t',quoting=csv.QUOTE_MINIMAL)
			writer.writerow([str(fitness),str(score)])	
		with open('costvsfitness.csv', 'a') as csvfile:
			writer = csv.writer(csvfile,delimiter='\t',quoting=csv.QUOTE_MINIMAL)
			writer.writerow([str(cost),str(fitness)])
		with open('costvstotalScore.csv', 'a') as csvfile:
			writer = csv.writer(csvfile,delimiter='\t',quoting=csv.QUOTE_MINIMAL)
			writer.writerow([str(cost),str(totalScore)])			

def writeFitnessData(data, i):
	maxFitness=findMaxFitness(data)
	print maxFitness, i
	with open('fitnessvsiterations.csv', 'a') as csvfile:
		writer = csv.writer(csvfile,delimiter='\t',quoting=csv.QUOTE_MINIMAL)
		writer.writerow([str(maxFitness),str(i)])	

def satisfyConstraints(data, individual):
	individualCost=0
	teamList=[]
	for key in individual:
		for player in individual[key]:
			if player.selected==True:
				individualCost+=player.cost
				teamList.append(player.team)
				if individualCost>data.maxCost:					
					return False
				if teamList.count(player.team)>data.maxTeam:
					return False
	if individualCost<data.minCost:
		return False
						
	return True
	
def selectPlayers(data, key, individual):
	selectionList=[]
	for player in individual[key]:
		if player.totalScore!=0 and (player.cost>4.0 or player.minutes>100):
			selectionList.append(player)	
	selections=random.sample(xrange(len(selectionList)),
		data.limits[key])
	for selection in selections:	
		individual[key][selection].selected=True

def calcAverageFitness(data, population):
	totalFitness=0
	for individual in population:
		totalFitness+=calcFitness(data, individual)
		
	averageFitness=totalFitness/len(population)
	return averageFitness

def selectElite(data):
	oldPop=copy.deepcopy(data.population)
	data.population=[]
	averageFitness=calcAverageFitness(data, oldPop)
	for individual in oldPop:
		if (calcFitness(data, individual)>averageFitness or 
			almostEqual(calcFitness(data, individual), averageFitness)):
			data.population.append(individual)
	assert(len(data.population)!=0)
	
def roulletteWheelSelect(data):
	oldPop=copy.deepcopy(data.population)
	data.population=[]
	cumulProbList=[]
	cumulativeProb=0
	totalFitness=calcAverageFitness(data, oldPop)*len(oldPop)
	for individual in oldPop:
		fitness=calcFitness(data, individual)
		cumulativeProb+=fitness/totalFitness
		cumulProbList.append(cumulativeProb)
	assert almostEqual(cumulativeProb,1.0)
	while (len(data.population)!=data.popSize):
		prob=random.random()
		for i in xrange(len(cumulProbList)):
			if cumulProbList[i-1]<prob<=cumulProbList[i]:
				data.population.append(copy.deepcopy(oldPop[i]))
				assert(satisfyConstraints(data,oldPop[i])==True)
	assert(len(data.population)==data.popSize)
	
def almostEqual(d1, d2):
	epsilon = 0.000001
	return (abs(d2 - d1) < epsilon)
	
def geneticSelection(data):
	selectElite(data)
	roulletteWheelSelect(data)
	
def mutateIndividual(data, i):
	oldPop=data.population
	data.population=[]
	individual=oldPop[i]
	selectedPlayerIndex=[]
	unselectedPlayerIndex=[]
	mutKey=random.sample(data.keyList, 1)[0]
	for playerIndex in xrange(len(individual[mutKey])):
		player=individual[mutKey][playerIndex]
		if player.selected==True:
			selectedPlayerIndex.append(playerIndex)
		else:
			if player.totalScore!=0 and (player.cost>4.0 or player.minutes>100):
				unselectedPlayerIndex.append(playerIndex)	
	mutationDone=False
	mutPlayerIndex=random.sample(selectedPlayerIndex,1)[0]
	while (mutationDone==False):
		newPlayerIndex=random.sample(unselectedPlayerIndex,1)[0]
		individual[mutKey][mutPlayerIndex].selected=False
		individual[mutKey][newPlayerIndex].selected=True
		if (satisfyConstraints(data, individual)):
			mutationDone=True
		else:
			individual[mutKey][mutPlayerIndex].selected=True
			individual[mutKey][newPlayerIndex].selected=False
	
	data.population=oldPop[0:i]+[individual]+oldPop[i+1:]
	

def geneticMutation(data):
	doMutation=False
	assert(len(data.population)==data.popSize)
	i=0
	mut=random.random()
	while(i!=len(data.population)):
		mut=random.random()
		if (mut<=data.mutProb):
			mutateIndividual(data, i)
		else:
			i+=1
		
	assert(len(data.population)==data.popSize)


def checkMaxIndex(data, maxIndex, minIndex):
	if maxIndex<indexLimits["GK"]:

	elif indexLimits["GK"]<=maxIndex<indexLimits["DEF"]:
	
	elif indexLimits["DEF"]<=maxIndex<indexLimits["MID"]:
	
	elif indexLimits["MID"]<=maxIndex<indexLimits["FWD"]:
	

def crossover(data, ind1, ind2):
	indexLimits=dict()
	indexLimits["GK"]=data.limits["GK"]
	indexLimits["DEF"]=indexLimits["GK"]+data.limits["DEF"]
	indexLimits["MID"]=indexLimits["DEF"]+data.limits["MID"]
	indexLimits["FWD"]=indexLimits["MID"]+data.limits["FWD"]
	sliceIndex1=random.randint(0,indexLimits["FWD"]-1)
	sliceIndex2=random.randint(0,indexLimits["FWD"]-1)
	while sliceIndex2==sliceIndex1:
		sliceIndex2=random.randint(0,indexLimits["FWD"]-1)
	minIndex=min(sliceIndex1, sliceIndex2)
	maxIndex=max(sliceIndex1, sliceIndex2)
	for i in xrange(minIndex,maxIndex+1):
		key=random.sample(["GK", "DEF", "MID", "FWD"], 1)
		
	
def geneticCrossover(data):
	for i in xrange(data.popSize):
		for j in xrange(i+1, data.popSize):
			ind1=data.population[i]
			ind2=data.population[j]
			crossProb=random.random()
			if crossProb<data.crossoverProbability:
				crossover(data, ind1, ind2)
	

def initPopulation(data):
	data.population=[]	
	while (len(data.population)!=data.popSize):
		individual=dict()
		individual["GK"]=copy.deepcopy(data.gkList)
		individual["DEF"]=copy.deepcopy(data.defList)
		individual["MID"]=copy.deepcopy(data.midList)
		individual["FWD"]=copy.deepcopy(data.fwdList)
		for key in individual:
			selectPlayers(data, key, individual)
		if satisfyConstraints(data, individual):
			print "Yes"
			data.population.append(individual)
		
def geneticAlgorithm(data):	
	startTime=time.time()
	initPopulation(data)
	for i in xrange(data.maxGenerations):
		geneticSelection(data)
		geneticCrossover(data)
		# writeData(data)
		geneticMutation(data)
		# writeData(data)
		# writeFitnessData(data, i)
	
	totalTime=time.time()-startTime
	print "Total Time:", totalTime
	
def initCumulativeScores(data):
	data.cumulativeTotalScore=0.0
	data.cumulativeRoundScore=0.0
	data.cumulativeMinutes=0.0
	data.cumulativePPM=0.0
	data.cumulativePPG=0.0
	for list in [data.gkList, data.defList, data.midList, data.fwdList]:
		for player in list:
			data.cumulativeTotalScore+=player.totalScore
			data.cumulativeRoundScore+=player.roundScore
			data.cumulativeMinutes+=player.minutes
			data.cumulativePPM+=player.ppm
			data.cumulativePPG+=player.ppg

def initRestrictions(data):
	data.limits=dict()
	data.limits["GK"]=2
	data.limits["DEF"]=5
	data.limits["MID"]=5
	data.limits["FWD"]=3
	data.totalPlayers=(data.limits["GK"]+data.limits["DEF"]+data.limits["MID"]
		+data.limits["FWD"])
	data.maxCost=100.0
	data.minCost=85.0
	data.maxTeam=3

def initWeights(data):
	data.tsW=30
	data.rsW=15
	data.minW=10
	data.ppmW=15
	data.ppgW=30

def main():
	class Struct: pass
	data=Struct()
	data.popSize=10
	data.maxGenerations=10
	data.keyList=["GK","DEF","MID","FWD"]
	readData(data)
	initCumulativeScores(data)
	initWeights(data)
	initRestrictions(data)
	data.mutProb=0.2
	geneticAlgorithm(data)

main()