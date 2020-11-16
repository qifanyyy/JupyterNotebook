import numpy as np
import os
from smith_waterman import algs, algs2, read_PAM, __main__, ROC
import sys
import re
import tqdm as tq

#from .algs import sw


BLOSUM50 = read_PAM.read_matrix("./BLOSUM50")
#print(BLOSUM50)
BLOSUM62 = read_PAM.read_matrix("./BLOSUM62")
MATIO = read_PAM.read_matrix("./MATIO")
PAM100 = read_PAM.read_matrix("./PAM100")
PAM250 = read_PAM.read_matrix("./PAM250")

def test_smithwaterman(): #test that two identical sequences return a perfect match
	#file prot-0004.fa
	seq1 = "SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPEMAAQAQSFKGLVSNWVDNLDNAGALEGQCKTFAANHKARGISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDM"
	seq2 = "SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPEMAAQAQSFKGLVSNWVDNLDNAGALEGQCKTFAANHKARGISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDM     "

    # update this assertion
	assert algs.sw(seq1, seq2) == (142, 1.0, 284) 
	#142 out of 142 matched, 1.0 perfect match, the score returned is 284 
"""
output looks like this 
 Identities = 142/142 (100.0%), Gaps = 0/142 (0.0%)
Seq A  1     SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPE  60  
             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Seq B  1     SLEAAQKSNVTSSWAKASAAWGTAGPEFFMALFDAHDDVFAKFSGLFSGAAKGTVKNTPE  60  

Seq A  101   ISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDM  142 
             ||||||||||||||||||||||||||||||||||||||||||
Seq B  101   ISAGQLEAAFKVLSGFMKSYGGDEGAWTAVAGALMGEIEPDM  142
"""

def testROC():

	if __name__ == "__main__":
		pos_matches = []
		all_files = []
		for file in pairs("./Pospairs.txt"): #probably redundant but keeping everything to be safe
			pos_matches.append(file) #you always said never delete code haha
			all_files.append(file[0])
			all_files.append(file[1])
		neg_matches = []
		for file in pairs("./Negpairs.txt"):
			neg_matches.append(file)
			all_files.append(file[0])
			all_files.append(file[1])

		all_files = set(all_files)

		sequences = {file:parseFasta("./"+file) for file in all_files}

		BLOSUM50 = read_matrix("./BLOSUM50")

		#below we will make the actual ROC
		matrices = ["BLOSUM50","BLOSUM62","PAM100","PAM250"] #we will test with each different scoring method 
		thresholds = [0,10,15,30,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,230,250,500]
		gap_p = -20
		gap_e = -4
		r = roc() 

		for matrix in matrices:
			matrix_dict = read_matrix("./" + matrix) #this will run for every matrix
			print("Testing ",matrix)
			for threshold in tq.tqdm(thresholds):#loop over 8 different thresholds
				
				tp,fp = calculate_tp_fp(pos_matches,neg_matches,sequences,
					threshold,gap_p,gap_e,matrix_dict, normalize = False) #one for normalize true and one for false
				
				r.add_rates(tp,fp) #put the rates on the graph
				truePositives.append(tp)
				falsePositives.append(fp)
				print(truePositives)
			return truePositives, falsePositives


		assert truePositives[:10] == [1.0, 1.0, 1.0, 0.96, 0.34, 0.18, 0.12, 0.1, 0.08, 0.04, 0.04] #basically rerunning all of this to check that the true and false positives are working 
		assert truePositives[:10] == [1.0, 1.0, 1.0, 0.72, 0.08, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0] #and then these will be plotted. these are just got BLOSUM50

	#r.save_plot("final_normalized_ROC") #save the final graph


"""
def testOptimization():
	pop, scores, library, objectiveMeans = optimization(scoreMatrix, chance, mutation, pressure, N, stepCutoff, noImprovementSteps, librarySize, gap, gap_e, truePositives, trueNegatives)
	originalScores = algs.sw(seq1, seq2)[0]
	assert scores >= originalScores
"""



def read_matrix(filename):

	scoring_dict = {}
	flag = False
	with open(filename) as fh:
		count = 0
		for line in fh:
			line = line.strip()
			if line.startswith("#"): continue
			elif line.startswith("A"):
				amino_acids = line.split("  ")
				flag = True
				continue

			if flag:
				values = []
				m = re.split(' ',line) #could not figure out regex for 1 and 2 spaces
				for x in m:
					try: values.append(int(x))
					except: pass

				for index,value in enumerate(values):
					scoring_dict[(amino_acids[count],amino_acids[index])] = int(value)
				count += 1

	return scoring_dict	

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

def run_local_alignment(seq1, seq2, gap_penalty, gap_extension,matrix):
	A = algs2.sw(seq1.upper(), seq2.upper(),gap_penalty,gap_extension,matrix) #pass dictionary
	return A[2]

def calculate_tp_fp(pos_matches,neg_matches,sequences,threshold,gap_p,gap_e,matrix,normalize=True):
	"""
	true and false positives are necessary for making an roc
	"""
	true_pos = 0 #initializations
	false_neg = 0 
	true_neg = 0
	false_pos = 0 

	for pos in pos_matches: #run this to scrape all of the + matches
		score = run_local_alignment(sequences[pos[1]], sequences[pos[0]],gap_p,gap_e,matrix)
		if normalize: #the normalized score is tajing into account the length of the sequence
			score = score/len(sequences[pos[1]])
		if score >= threshold: #we want 70% true positives ideally
			true_pos += 1
		else:
			false_neg += 1	
			
	for neg in neg_matches: #do the same with the negative matches
		score = run_local_alignment(sequences[neg[1]], sequences[neg[0]],gap_p,gap_e,matrix)
		if normalize:
			score = score/len(sequences[neg[1]])
		if score < threshold:
			true_neg += 1
		else:
			false_pos += 1	
	tp = true_pos/(true_pos+false_neg) #calculate the % and return the rates
	fp = false_pos/(true_neg+false_pos)	

	return tp,fp

threshold = [0,10,15,30,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,230,250,500]
gap_p = -20
gap_e = -4
matrix = "BLOSUM50"




	#r.save_plot("final_normalized_ROC") #save the final graph



