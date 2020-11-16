import random

#constraint check
def ContraintCheck(x1,x2,x3,x4):
	if(0.5*int(x1)+1.0*int(x2)+1.5*int(x3)+0.1*int(x4)<=3.1):
		if(0.3*int(x1)+0.8*int(x2)+1.5*int(x3)+0.4*int(x4)<=2.5):
			if(0.2*int(x1)+0.3*int(x2)+0.3*int(x3)+0.1*int(x4)<=0.4):
				return 1
	else:
		return 0




# wheel algo
def SelectionOfParent(Generation):
	count=0
	print()
	print("Population fitness:")
	for x in Generation:
		print(x,end='')
		print("->",end='')
		characterList=list(x)
		x1=characterList[0]
		x2=characterList[1]
		x3=characterList[2]
		x4=characterList[3]
		if(ContraintCheck(x1,x2,x3,x4)==1):
			fitness=0.2*int(x1)+0.3*int(x2)+0.5*int(x3)+0.1*int(x4)
		else:
			fitness=0
		count=count+fitness
		print(fitness)
	randomVariableForSelection=random.uniform(0,count)
	#print(randomVariableForSelection)
	variableToMatchVariableForSelection=0
	for x in Generation:
		characterList=list(x)
		x1=characterList[0]
		x2=characterList[1]
		x3=characterList[2]
		x4=characterList[3]
		if(ContraintCheck(x1,x2,x3,x4)==1):
			fitness=0.2*int(x1)+0.3*int(x2)+0.5*int(x3)+0.1*int(x4)
		else:
			fitness=0
		variableToMatchVariableForSelection=variableToMatchVariableForSelection+fitness
		if(variableToMatchVariableForSelection>=randomVariableForSelection):
			return x
	return -1

#Function for mutation
def Mutation(OffSpring):
	charList=list(OffSpring)
	for i in range(0,3):
		number=random.uniform(0,1)
		if(number<0.01):
			if(int(charList[i])==1):
					charList[i]='0'
			else:
				charList[i]='1'
	OffSpring=''.join(charList)
	return OffSpring

	






def CrossOverOfParents(selection,selection2):
	generateNumberForProbablityOfCrossover=random.randint(0,100)
	print("Parent1 Selected:",selection," Parent2 Selected:",selection2)
	if(generateNumberForProbablityOfCrossover<=75):
		indexForCrossover=random.randint(1,len(selection)-2)
		#print(indexForCrossover)
		stringFirst1half=selection[0:indexForCrossover]
		stringFirst2half=selection[indexForCrossover:len(selection)]
		stringSecond1half=selection2[0:indexForCrossover]
		stringSecond2half=selection2[indexForCrossover:len(selection2)]
		newOffSpring1=stringSecond1half+stringFirst2half
		newOffSpring2=stringFirst1half+stringSecond2half
		listMember=[]
		element1=Mutation(newOffSpring1)
		element2=Mutation(newOffSpring2)
		print("Offspring1:",element1," OffSpring2:",element2)
		listMember.append(element1)
		listMember.append(element2)
		return listMember
	else:
		listMember=[]
		listMember.append(Mutation(selection))
		listMember.append(Mutation(selection2))
		print("Offspring1:",listMember[0]," OffSpring2:",listMember[1])
		
		return listMember

#best fitness in generation
def BestFitness(Generation,flag1):
	count=0
	#print()
	allFitnessInGeneration=[]
	#print("Best Fitness:")
	listOfFitnessInGeneration=[]
	for x in Generation:
		#print(x,end='')
		#print("->",end='')
		characterList=list(x)
		x1=characterList[0]
		x2=characterList[1]
		x3=characterList[2]
		x4=characterList[3]
		if(ContraintCheck(x1,x2,x3,x4)==1):
			fitness=0.2*int(x1)+0.3*int(x2)+0.5*int(x3)+0.1*int(x4)
			listOfFitnessInGeneration.append(fitness)
			#print(fitness)
		else:
			fitness=0
			listOfFitnessInGeneration.append(fitness)
			#print(fitness)
		count=count+fitness

		allFitnessInGeneration.append(fitness)
		highest=0
	temp=0;
	indexget=0;
	for i in allFitnessInGeneration:
		if(i>highest):
			highest=i
			indexget=temp
			temp=temp+1
		else:
			temp=temp+1
	
	#print(highest)
	if(flag1==1):
		return count
	elif(flag1==2):
		return Generation[indexget]
	elif(flag1==3):
		listIn=[]
		listIn.append(Generation[indexget])
		listIn.append(highest)
		return listIn
	else:
		return listOfFitnessInGeneration


#function to check Convergence

def checkConvergence(Generation):
	lastIndex=len(Generation)-1
	listOfFitnessInGeneration=BestFitness(Generation,4)
	count=0
	for i in range(0,lastIndex):
		for y in range(0,lastIndex):
			print("count:",count)
			if(listOfFitnessInGeneration[i]==listOfFitnessInGeneration[y]):
				count=count+1
				if(count>16):
					return 1
		count=0
	return 0

	


def GenericAlgorithmForProjects():
	#set to store 
	firstGeneration=[]
	levelOfGeneration=0
	#setOfFirstGeneration=set([])
	#loop for generating first generation
	for i in range(0, 21):
		a=random.randint(0, 15)
		firstGeneration.append(bin(a)[2:].zfill(4))
	fitnessList=[]	
	dicForAnswer={}
	print("Starting Population:",end='')
	print(" ",end='')
	for x in firstGeneration:
		print(x, end='')
		print(" ",end='')
	#selection of Parents for crossover
	fitnessList.append(BestFitness(firstGeneration,1))
	nextGeneration=[]
	countSameFitness=0
	while(countSameFitness<=100):
		while(len(nextGeneration)<20):
			#print(firstGeneration)
			selection=SelectionOfParent(firstGeneration)
			selection2=SelectionOfParent(firstGeneration)
			listOfNewMember=CrossOverOfParents(selection,selection2)
			for i in range(0,1):
				if(len(nextGeneration)<20):
					nextGeneration.append(str(listOfNewMember[i]))
				
		saveList=BestFitness(nextGeneration,3)
		#dicForAnswer[countSameFitness]=saveList
		
		firstGeneration.clear()
		firstGeneration.extend(nextGeneration)
		fitnessList.append(BestFitness(nextGeneration,1))
		levelOfGeneration=levelOfGeneration+1
		if(checkConvergence(nextGeneration)==1):
			#print(fitnessList)
			print(BestFitness(nextGeneration,4))
			answer=BestFitness(nextGeneration,2)
			print(answer)
			print("levelOfGeneration:",levelOfGeneration)
			break
        	




		print(len(nextGeneration))
		nextGeneration.clear()
		
		countSameFitness=countSameFitness+1
	#print("Dic:")
	#for i in dicForAnswer:
		#print(dicForAnswer[i])
GenericAlgorithmForProjects()