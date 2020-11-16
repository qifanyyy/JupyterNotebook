def exonChain(geneFile, genomeFile):
	from Bio import SeqIO
	import numpy as np
	import pandas as pd
	from exonChainFunctions import align_local
	from exonChainFunctions import Stack
	from exonChainFunctions import calLength, getRank
	########## Read fasta files ##########
	print('Exon chaining method started, reading sequence files...')
	for record in SeqIO.parse(geneFile,"fasta"):
		gene = record.seq
		geneLen = len(gene)
		geneSeq = str(gene)
	for record in SeqIO.parse(genomeFile,"fasta"):
		genome = record.seq
		genomeSeq = str(genome)
  
	########## Find a portion of genome for generating putative exons ##########
	# find the best local alignment between gene sequence and entire genome sequence
	i = 0 # i indicate the alignment should begin at the first nucleotide of the genome sequence
	# set the score for match, mismatch and gap
	match = 2
	misMatch = -3
	gap = -2
	print('Local alignment between gene and the genome... (this dynamic programming step may take a while ~ 8 min during test)')
	alignment = align_local(geneSeq, genomeSeq, [match, misMatch, gap],i)
	print('first alignment:')
	print(alignment)
	# select -250 and +250 extend region from the first alignment
	selectStartLoc = alignment['genome_start']-250
	selectEndLoc = alignment['genome_end']+250
	selectGenoSeq = genomeSeq[selectStartLoc:selectEndLoc]
	seletLen = len(selectGenoSeq)

	######### Calculating putative exons ##########
	# perform local alignment with sliding window, step = 10 bp, window size = input gene length
	hsp = [] # create a list called hsp to store all the local alignments
	print('Calculating putative exons from genome region '+ str(selectStartLoc)+ ' to ' + str(selectEndLoc) + ' (dynamic programmming...)')
	for i in np.arange(0,seletLen,10):
		genomeSeg = selectGenoSeq[i:i+geneLen]
		summary = align_local(geneSeq, genomeSeg, [match, misMatch, gap],i)
		hsp.append(summary)
  
	putativeExons = pd.DataFrame(data=hsp)
	putativeExons= putativeExons[['score','genome_start','genome_end']]
	putativeExons.drop_duplicates(['genome_start','genome_end'],keep='first', inplace = True)
	putativeExons['length'] = putativeExons.apply (lambda row: calLength(row),axis=1)
	putativeExons.sort_values('genome_end', ascending =True, inplace = True)
	# print putative exons
	print(putativeExons)
  
	######## Exon chaining algorithm #########
	# give rank to the start location and end location for all the intervals
	inputs = putativeExons.to_dict('list')
	ranks = getRank(inputs)
	# create a dataframe with all the score, location and rank data
	exons = pd.DataFrame()
	exons['genome_end'] = inputs['genome_end']
	exons['genome_start'] = inputs['genome_start']
	exons['weight'] = inputs['length']
	exons['start_rank'] = list(ranks.loc[ranks['label'] =='start_rank']['loc_Rank'])
	exons['end_rank'] = list(ranks.loc[ranks['label'] =='end_rank']['loc_Rank'])
	exons.sort_values(['genome_end','end_rank'],ascending=False, inplace = True)
	# the algorithm
	numOfExons = exons.shape[0]
	sumScore = [0]*(numOfExons*2)
	endLoc=Stack()
	startLoc=Stack()
	weight = Stack()
	usedEndLoc = Stack()
	usedStartLoc = Stack()
	lastExon =[]
	for idx, row in exons.iterrows():
		endLoc.push(int(row['end_rank']))
		startLoc.push(int(row['start_rank']))
		weight.push(row['weight'])
	for i in range(0,numOfExons*2):
		if endLoc.isEmpty() == False:
			rightEnd = endLoc.peek()-1
			if i == rightEnd:
				leftEnd = startLoc.peek()-1
				thisScore = weight.peek()
				addOption = sumScore[leftEnd] + thisScore
				if addOption > sumScore[i-1]:
					sumScore[i] = addOption
					lastExon = [startLoc.peek(),endLoc.peek()]
					usedEndLoc.push(endLoc.peek())
					usedStartLoc.push(startLoc.peek())
				else:
          				sumScore[i] = sumScore[i-1]
				endLoc.pop()
				startLoc.pop()
				weight.pop()
			else:
				sumScore[i] = sumScore[i-1]
 
	######## Print out exon chaining results #########
	selectedExons =[]
	selectedExons.append(lastExon)
	validExon = lastExon
	endLoc=Stack()
	startLoc=Stack() 
	while usedEndLoc.isEmpty() == False:
		flag = validExon[0]
		currentExonEnd = usedEndLoc.pop()
		if currentExonEnd<=flag:
			validExon = [usedStartLoc.pop(),currentExonEnd]
			selectedExons.insert(0,validExon)
		else:
			usedStartLoc.pop()
	print('The final selected exon are:')
	generatedGeneSeq = ''
	for eachExon in selectedExons:
		start_rank = eachExon[0]
		genome_start = exons.loc[exons['start_rank'] == start_rank]['genome_start'] + selectStartLoc
		genome_end = exons.loc[exons['start_rank'] == start_rank]['genome_end'] + selectStartLoc
		exonSequence = genomeSeq[int(genome_start):int(genome_end)]
		print(str(int(genome_start)) +'-'+str(int(genome_end)))
		print(exonSequence)
		generatedGeneSeq = generatedGeneSeq+'-'+exonSequence
	print('Concatenated gene sequence:')
	print(generatedGeneSeq)
	return(generatedGeneSeq)
