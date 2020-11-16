#!/usr/bin/python
__author__ = "Jeff Mandell"
__email__ = "jeff.mandell@yale.edu"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "1.0.0"

import argparse, re, sys

### We need to read input file and score file.
parser = argparse.ArgumentParser(description='Smith-Waterman Algorithm')
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument('-s', '--score', help='score file', required=True)
parser.add_argument('-o', '--opengap', help='open gap', required=False, default=-2)
parser.add_argument('-e', '--extgap', help='extension gap', required=False, default=-1)
args = parser.parse_args()

### Implement your Smith-Waterman Algorithm

# A class to store information related to each entry in the scoring matrix
# Each entry has score and a source (which is another scoring matrix entry).
# Also keeping track of whether each entry constitutes an alignment
# for tracking gap length and printing the final alignment.
class Score_matrix_entry():
	def __init__(self, source, score, index):
		self.source = source
		self.score = score
		self.index = index

### Implementation of Smith-Waterman algorithm
def runSW(inputFile, scoreFile, openGap, extGap):

	# read in input sequences
	with open (inputFile, 'r') as f:
		seq1_string = (f.readline().strip())
		seq2_string = (f.readline().strip())
	seq1 = list(seq1_string)
	seq2 = list (seq2_string)

	# read in substitution matrix
	sub_scores = parse_substitution_matrix(scoreFile)

	# 2D list of score entries: each element corresponds with one row of visualization
	score_matrix = []

	# keep track of highest scores for the traceback (starting with a placeholder entry)
	highest_scoring = [Score_matrix_entry(source = None, score = 0, index=(-1, -1))]

	# In visualization, sequences 1 and 2 will be column and row sequences, respectively.
	# Starting at the top, the algorithm will go through all residues in sequence 2, 
	# comparing each to all residues in sequence 1.

	# Note: The Smith-Waterman paper calls for all zeros in the first row and the first
	# column. Those empty cells are not included in the data structure, but they are
	# printed in the output.

	for i in range(0, len(seq2)):
		score_matrix.append(list())
		for j in range(0, len(seq1)):

			# Keep track of which choice (continuing alignment or introducing gaps) maximizes score
			acids = (seq2[i], seq1[j])
			current_best = 0
			current_best_source = None

			# first try extending an alignment (or starting one)
			if j - 1 >= 0 and i - 1 >=0:
				top_left_neighbor_entry = score_matrix[i - 1][j - 1]
				candidate_score = sub_scores[acids] + top_left_neighbor_entry.score
				if candidate_score > current_best:
					current_best = candidate_score
					current_best_source = top_left_neighbor_entry
			else:
				candidate_score = sub_scores[acids]
				if candidate_score > current_best:
					current_best = candidate_score

			# assess scores from introducing a gap in sequence 1
			gap_length = 1
			while j - gap_length >= 0:
				gap_penalty = openGap + extGap * (gap_length - 1)
				leftward_neighbor_entry = score_matrix[i][j - gap_length]
				candidate_score = leftward_neighbor_entry.score + gap_penalty
				if candidate_score > current_best and candidate_score > 0:
					current_best = candidate_score
					current_best_source = leftward_neighbor_entry
				gap_length += 1

			# assess scores from introducing a gap in sequence 2
			gap_length = 1 # reset gap length
			while i - gap_length >= 0:
				gap_penalty = openGap + extGap * (gap_length - 1)
				upward_neighbor_entry = score_matrix[i - gap_length][j]
				candidate_score = upward_neighbor_entry.score + gap_penalty
				if candidate_score > current_best and candidate_score > 0:
					current_best = candidate_score
					current_best_source = upward_neighbor_entry
				gap_length += 1
			new_entry = Score_matrix_entry(source = current_best_source, score = current_best, index = (i, j))
			score_matrix[i].append(new_entry)

			# if current entry has highest score of all entries so far, make a note of it
			if current_best > highest_scoring[0].score:
				highest_scoring = [new_entry,]
			elif current_best == highest_scoring[0].score:
				highest_scoring.append(new_entry) # keeeping track of ties, too

	### Now that the scoring matrix is completed, calculate and print results

	# Print input sequences
	print_heading("Sequences")
	print("Sequence 1:\t%s" % seq1_string)
	print("Sequence 2:\t%s" % seq2_string)
	print_heading("Scoring Matrix")

	# Print scoring matrix, including leading zeroes for column 1 and row 1
	print("\t\t" + "\t".join(seq1))
	empty_row = ['0'] * (len(seq1) + 1)
	print("\t" + "\t".join(empty_row))
	for i in range(0, len(seq2)):
		row = seq2[i] + "\t0\t" + "\t".join([str(x.score) for x in score_matrix[i]])
		print(row)

	# Run traceback and print best alignments
	heading = "Best alignment"
	multiple_alignments = False
	if len(highest_scoring) > 1:
		heading += 's'
		multiple_alignments = True
	print_heading(heading)

	highest_score = highest_scoring[0].score

	# Prevent unalignable queries from returning a long list of 0-scoring "best alignments"
	if highest_score == 0:
		print("No alignments found!")
		sys.exit()
	print("Alignment Score:\t%s" % highest_scoring[0].score)

	# take the highest-scoring entry (or multiple entries if there's a tie) and print the alignments
	for i in range(0, len(highest_scoring)):
		indexes = []
		if multiple_alignments:
			print("Alignment %d:" % (i + 1))
		entry = highest_scoring[i]

		# traceback
		while entry.source != None:
			indexes.append(entry.index)
			entry = entry.source
		indexes.append(entry.index) # get the first entry in the alignment (it has no source)
		indexes.reverse() # since we traced back, reverse the list to get it in forward order

		# construct the output such that the aligned portions of sequence 1 and 2 line up
		start_of_alignment = indexes[0]
		s1_display = seq1_string[0:start_of_alignment[1]] + '('
		s2_display = seq2_string[0:start_of_alignment[0]] + '('

		# will need to pad the shorter sequence with whitespace to keep things lined up
		if len(s1_display) > len(s2_display):
			s2_display = ' ' * (len(s1_display) - len(s2_display)) + s2_display
		else:
			s1_display = ' ' * (len(s2_display) - len(s1_display)) + s1_display
		identity_display = ' ' * len(s1_display)

		# traverse entries and assemble the printable alignment
		previous_s1_index = -1 # placeholder values
		previous_s2_index = -1
		for seq2_index, seq1_index in indexes:
			# when (seq2_index, seq1_index) each increase by 1, that's a continued alignment
			# when one increases and the other stays the same, that means there's a gap
			if seq2_index == previous_s2_index:
				gap = seq1_index - previous_s1_index
				next_seq2_char = '-' * gap
				next_seq1_char = seq1_string[(previous_s1_index + 1):(seq1_index + 1)]
			elif seq1_index == previous_s1_index:
				gap = seq2_index - previous_s2_index
				next_seq1_char = '-' * gap
				next_seq2_char = seq2_string[(previous_s2_index + 1):(seq2_index + 1)]
			else:
				next_seq2_char = seq2_string[seq2_index]
				next_seq1_char = seq1_string[seq1_index]

			s1_display += next_seq1_char
			s2_display += next_seq2_char
			previous_s1_index = seq1_index
			previous_s2_index = seq2_index

			# when seq1 and seq2 characters match, indicate the identity
			if next_seq1_char == next_seq2_char:
				identity_display += '|'
			else:
				identity_display += ' ' * len(next_seq1_char)
		s1_display += ')' + seq1_string[seq1_index + 1:]
		s2_display += ')' + seq2_string[seq2_index + 1:]

		print(s1_display)
		print(identity_display)
		print(s2_display + "\n")



### Read the substitution matrix file into a dictionary. This file
### should be tab- or space-delimited. It's assumed that the file is
### formatted correctly (no missing values, illegal characters, etc.).
### Example dictionary entry: scores[('A', 'W')] = -3

def parse_substitution_matrix(score_file):
	scores = {} 
	with open (score_file, 'r') as f:
		# read in amino acid column headers in first line
		y_names = re.split('[ \t]+', f.readline().strip())
		for line in f:
			fields = re.split('[ \t]+', line.strip())
			# skip empty lines in matrix file
			if len(fields) == 0:
				continue
			# read in the amino acid for the current row
			x_name = fields[0]

			# store every score given in the current row
			for i in range(1,len(fields)):
				scores[(x_name, y_names[i - 1])] = int(fields[i])
	return scores

### Helper function to print output section headers
def print_heading(heading):
	print("\n " + "-" * 50)
	filler_1 = (50 - len(heading)) / 2
	filler_2 = filler_1
	if len(heading) % 2 == 1:
		filler_2 += 1
	print("|%s%s%s|" % (" " * filler_1, heading, " " * filler_2))
	print(" " + "-" * 50 + "\n")

### Run the Smith-Waterman algorithm
runSW(args.input, args.score, float(args.opengap), float(args.extgap))

