import sys
import numpy as np
from .read_PAM import read_matrix #for blosum and those
#from .__main__ import calculate_tp_fp
import random

match = 2 #scores taken from the suggested on wikipedia
mismatch = -1 #these decide the next step in the matrix
gap = -20 #we need to penalize a gap
gap_e = -4 #this is the penalty for continuing to extend a gap
#seq1 = []#"SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPEMAAQAQSFKGLVSNWVDNLDNAGALEGQCKTFAANHKARGISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDM"
#seq2 = []#"SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPEMAAQAQSFKGLVSNWVDNLDNAGALEGQCKTFAANHKARGISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDMXXXXX"#"ANKTRELCMKSLEHAKVDTSNEARQDGIDLYKHMFENYPPLRKYFKSREEYTAEDVQNDPFFAKQGQKILLACHVLCATYDDRETFNAYTRELLDRHARDHVHMPPEVWTDFWKLFEEYLGKKTTLDEPTKQAWHEIGREFAKEINK"
#these can be global

def sw(seq1, seq2, gap, gap_e, mat):
	#seq1=seq1
	#seq2=seq2
	rows = len(seq1) + 1 #for the matrix, plus a lil extra for the gap
	cols = len(seq2) + 1
	seq1 = seq1.upper()
	seq2 = seq2.upper()

	#initialize the scoring matrix
	flag = False #this "flag" is to tell the scoring algorithm that there was previoiusly a gap and we are continuing it
	scoreMatrix, startPosition, maxScore, flag = newScoringMatrix(rows,cols,seq1,seq2,mat,flag)

	#call the function to find the path through the scoring matrix,
	#aligning the sequences
	alignedSeq1, alignedSeq2 = path(scoreMatrix, startPosition, seq1, seq2)
	assert len(alignedSeq1) == len(alignedSeq2), 'aligned strings are not the same size'
	# print the results 
	alignmentString1, idents, gaps, mismatches = alignmentString(alignedSeq1, alignedSeq2)
	length1 = len(alignedSeq1)

	"""
	#using our alignment visualization function to show what is matches/not in the sequences
	print(' Identities = {0}/{1} ({2:.1%}), Gaps = {3}/{4} ({5:.1%})'.format(idents,length1, idents / length1, gaps, length1, gaps / length1))
	#this formula above will print out the % of matches in the sequence and the % of gaps too
	for i in range(0, length1, 100): #visualize these and print the sequences that are aligned
		seq1_slice = alignedSeq1[i:i+60]
		print('Seq A  {0:<4}  {1}  {2:<4}'.format(i + 1, seq1_slice, i + len(seq1_slice)))
		print('             {0}'.format(alignmentString1[i:i+60]))
		seq2_slice = alignedSeq2[i:i+60]
		print('Seq B  {0:<4}  {1}  {2:<4}'.format(i + 1, seq2_slice, i + len(seq2_slice)))
		print()
	"""

	#print(alignedSeq1)
	#print(alignedSeq2)
	#print(len(scoreMatrix))
	#print(scoreMatrix)
	#print(startPosition) #first good match

	A_SCORE = 0 #ignore this
	for a in range(len(alignmentString1)):
		if alignmentString1[a] == 'X': #mismatch 
			A_SCORE -= 1
			if alignmentString1[a-1] == 'X': #consecutive mismatch!
				A_SCORE -= 2
		elif alignmentString1[a] == ' ': #gap
			A_SCORE -= 1
			if alignmentString1[a-1] == ' ': #consecutive gap! if this happens there is a larger penalty than opening a gap
				A_SCORE -= 2
		elif alignmentString1[a] == '|':
			A_SCORE += 1
		normalizedAScore = A_SCORE/len(alignmentString1)

	#print(A_SCORE)
	#print(normalizedAScore)
	# print(maxScore)
	return A_SCORE, normalizedAScore, maxScore

    

def newScoringMatrix(rows, cols, seq1, seq2, mat,flag):
	"""
	making a scoring matrix that will then be filled with the scores
	the best alignment is the path with the highest cumulative score
	"""
	scoreMatrix = [[0 for col in range(cols)] for row in range(rows)] #initialize
	maxScore = 0
	maxPosition = None #highest recognized score
	for i in range(rows): #begin looking through the matrix
		for j in range(cols):
			score1, flag = score(scoreMatrix, i, j,seq1,seq2,mat,flag) #calculate the score for the position
			if score1 > maxScore: #put in the score, assign to postiion
				maxScore = score1
				maxPosition = (i, j)  #the max position is where the path will start

			scoreMatrix[i][j] = score1 #append the score to the position

	return scoreMatrix, maxPosition, maxScore, flag


def score(matrix, x, y, seq1, seq2, mat,flag):
	"""
	calculate the score for every position in the scoring matrix 
	based on the position in the table's neighbors
	"""
	# similarity = match if seq1[x-1] == seq2[y-1] else mismatch #this is meta to check if the two positions in a sequence match

	similarity = mat[(seq1[x-1],seq2[y-1])]


	diagonalScore = matrix[x-1][y-1] + similarity #we did something like this in class
	if flag: #this "flag" is to tell the scoring algorithm that there was previoiusly a gap and we are continuing it
		upScore = matrix[x-1][y] + gap_e #if flag is true then we add the gap extension penalty instead of the gap penalty
		leftScore = matrix[x][y-1] + gap_e
	else:
		upScore = matrix[x-1][y] + gap #vertical score accounting for gaps
		leftScore = matrix[x][y-1] + gap #horizontal score accounting for gaps

	maximum = max(0, diagonalScore, upScore, leftScore)

	if upScore == maximum or leftScore == maximum: #this is what sets if the flag is true of false
		flag = True #true when we open a gap and extend it
	else:
		flag = False

    #return the best score of those calculated, this will be the way through the matrix and match up the seqs
	return maximum, flag

def path(scoreMatrix, startPosition, seq1, seq2): #AKA traceback
	"""
	how to decide which path to take through the scoring matrix
	taking the best path through the matrix based on the score will 
	align the sequences with the best match and gap sequence/ratio

	also, this will be the function that takes the input matrix and can release a score

	diagonal move = match or mismatch
	up move = gap in seq1
	left move = gap in seq2
	"""

	END, DIAG, UP, LEFT = range(4) #the potential moves we can make
	alignedSeq1 = [] #initializations
	alignedSeq2 = []
	x, y = startPosition
	move = moveFunction(scoreMatrix, x, y)
	while move != END: #if there is a scheduled move according to the function
		if move == DIAG: #moving diagonally will be one up to x and y
			alignedSeq1.append(seq1[x-1])
			alignedSeq2.append(seq2[y-1])
			x-=1
			y-=1
		elif move == UP: #moving up (gap) would be just change in x
			alignedSeq1.append(seq1[x-1])
			alignedSeq2.append('-')
			x-=1
		else: #move sideways would be a change in the y here
			alignedSeq1.append('-')
			alignedSeq2.append(seq2[y-1])
			y-=1
		move = moveFunction(scoreMatrix, x, y) #keep it going in the loop
		
		if x -gap < 0 or y-gap < 0:
			break
	alignedSeq1.append(seq1[x-1])
	alignedSeq2.append(seq2[y-1])

	return ''.join(reversed(alignedSeq1)), ''.join(reversed(alignedSeq2)) #return the seq

def moveFunction(scoreMatrix, x, y):
	"""
	this will be the function that allows us to move throughout the scoring matrix
	"""
	diag = scoreMatrix[x-1][y-1] #all of the possible moves based on 
	up = scoreMatrix[x-1][y] #coordinates in the scoring matrix
	left = scoreMatrix[x][y-1]

	if diag >= up and diag >= left: #in this function, a score "tie" is a diagonal move
		return 1 if diag != 0 else 0 #0 in this case is the end
	elif up > diag and up >= left: #tie here goes to the "up" move
		return 2 if up != 0 else 0
	elif left > diag and left > up:
		return 3 if left != 0 else 0 #left move or end of sequence
	else: #this is a safety measure
		raise ValueError('invalid')

def alignmentString(alignedSeq1, alignedSeq2):
	"""
	this is a visualization of how well the sequences are aligned, we'll print this
	same nucleotide is |, gaps are -, and mismatch is X
	"""
	idents, gaps, mismatches = 0,0,0 #initialization 
	alignmentString = []
	A_SCORE = 0 #this will be the full score of the alignment
	for base1, base2 in zip(alignedSeq1, alignedSeq2):
		if base1 == base2: #if the bases are the same we show the match symbol
			alignmentString.append('|')
			idents +=1
		elif '-' in (base1, base2): #if there is a gap required we put in a space
			alignmentString.append(' ')
			gaps += 1
		else:
			alignmentString.append('X') #if they do not match but no gap put an X
			mismatches += 1

	return ''.join(alignmentString), idents, gaps, mismatches

#^^^^^ smith waterman ^^^^^
##########################################################################################################
# vvvv roc vvvvv

#the code below will allow me to take the positive and negative pairs and take the sequence
def pairs(filename):
	with open(filename) as fh:
		for line in fh:
			line = line.strip().split()
			yield line[0], line[1]
def parseFasta(filename): #This is used to take just the sequence from the fasta document
	seq = ""
	with open(filename) as fh:
		for line in fh:
			if line.startswith(">"):
				continue
			seq += line.strip()
	return seq

BLOSUM50 = read_matrix("./BLOSUM50")
#print(BLOSUM50)
BLOSUM62 = read_matrix("./BLOSUM62")
MATIO = read_matrix("./MATIO")
PAM100 = read_matrix("./PAM100")
PAM250 = read_matrix("./PAM250")

posMatches = [] #initializations
allFiles = []

for file in pairs("./Pospairs.txt"): #take the file names from the pairs and get the sequence
	posMatches.append(file)
	allFiles.append(file[0])
	allFiles.append(file[1])

negMatches = []
for file in pairs("./Negpairs.txt"):
	negMatches.append(file)
	allFiles.append(file[0])
	allFiles.append(file[1])

allFiles = set(allFiles)

sequences = {file:parseFasta("./"+file) for file in allFiles}

def Average(list): #simple average
	return sum(list) / len(list)

def roc():
	"""
	the point of this function is to develop a receiver operating characteristic curve
	I will use this to show the diagnostic ability of my smith waterman algorithm
	the curve will be plotted using the true positive rate (% of positives that are above a threshold appropriately)
	againse the false positive rate (% of negative pairs that are inappropriately above the threshold for a positive hit)

	this is how i found the best gaps to use, shown in the pdf document
	"""
	posA_SCORES = []
	posNormalizedScore = []
	negA_SCORES = []
	negNormalizedScore = []
	for pos in posMatches: #this will run through all the pairs of sequences and put them in the algorithm
		#saving the scores so that i can call all of the positive and negative match scores
		x, y, z = sw(seq1 = sequences[pos[0]], seq2 = sequences[pos[1]],mat= BLOSUM50) #done with blosum50 matrix
		posA_SCORES.append(z) #scores
		posNormalizedScore.append(y)
	for neg in negMatches: #this will run through all the pairs of sequences and put them in the algorithm
		x,y,z = sw(seq1 = sequences[neg[0]], seq2 = sequences[neg[1]],mat=BLOSUM50)
		negA_SCORES.append(z)
		negNormalizedScore.append(y)

	posA_SCORES.sort()
	#print(posA_SCORES)
	posCutoff = posA_SCORES[int(len(posA_SCORES) * 0.3)] #70% of positive scores are above this threshold
	#print(posCutoff)
	print("The gap penalty is: " + str(gap))
	print("The gap extension penalty is: " + str(gap_e))
	pcount = 0
	for k in posA_SCORES:
		if k > posCutoff:
			pcount = pcount + 1
	truePositives = (pcount / (len(posA_SCORES))) * 100
	print("The proportion of true positives is " + str(truePositives) + "%.") 
	#print(Average(posA_SCORES)) #positive scores are on average higher than negative
	#print(posNormalizedScore)
	ncount = 0
	for k in negA_SCORES:
		if k > posCutoff:
			ncount = ncount + 1
	falsePositives = (ncount/(len(negA_SCORES))) * 100
	print("The proportion of false positives is " + str(falsePositives) + "%.") 
	#print(Average(negA_SCORES))
	#print(negNormalizedScore)




##########################################################################################################
#optimization

def matrixMutation(scoreMatrix, chance, mutation):
	"""
	change the matrix values, each value has a chance of mutating
	returns the changed matrix
	"""
	for i, j in scoreMatrix.items():
		if random.random() < chance: #randomly pick a number for the chance
			scoreMatrix[i] = value + random.gauss(0, mutation) #random amount as well
	return scoreMatrix #samea s the input to be used later

def select(population, weights):
	"""
	randomly generate matrices with different weights 
	"""
	return list(np.random.choice(pop, size = len(pop), p = weights))

def scaleScores(scores, pressure):
	"""
	scales the scores in accordance to the selective pressure, with a sum of 1
	"""
	formerMinimum = min(scores)
	formerMaximum = max(scores)
	newMinimum = 1
	newMaximum = 10**pressure
	newScores = [(newMaximum - newMinimum)*(s - oldMinimum)/(oldMaximum - oldMinimum) + newMinimum for s in scores]

	return [p/sum(newScores) for p in newScores]

def optimization(scoreMatrix, chance, mutation, pressure, N, stepCutoff, 
	noImprovementSteps, librarySize, gap, gap_e, truePositives, trueNegatives):
	"""
	my idea, based on what was discussed in class, was to use a genetic optimization algorithm 
	in theory the genetic optimization is a way of solving problems that mimics biological evolution
	the algorithm repeatedly modifies a population of individual solutions

	input:
	scoring matrix
	chance of mutation (probability of a mutation in the matrix)
	mutation (amlount that changes, standard deviation)
	pressure (selective pressure)
	cutoff (to stop the run)
	no improvement steps
	size of the library
	gap
	gap extension penalty
	truePositives
	trueNegatives

	output:
	the matrices that perform the best and are optimized
	"""
	population = [scoreMatrix.copy() for i in range(N)]
	library = {} #initialize

	#this loop will keep track of the changes for the objective
	objectiveMeans = []
	counter = 0 #initialize the improvement counter

	while True: #run this loop until we find improvements
		counter += 1
		population = [matrixMutation(m, chance, mutation) for m in pop] #mutate matrices for the population 
		scores = []

		objectiveMean = sum(scores)/N #see the new avg score
		objectiveMean.append(objectiveMean) #add it on

		if len(objectiveMeans) > stepCutoff or  counter > noImprovementSteps:
			break #we will stop if these conditions are met
		weights = scaleScores(scores, pressure) #reweight the scores
		pop = select(pop, weights)[:-len(library)] + [z.copy() for z in library.values()] #put the good ones into the population
	return pop, scores, library, objectiveMeans




