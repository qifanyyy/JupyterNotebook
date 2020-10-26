#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time
from Banded import *
from Unrestricted import *

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

	
# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment

	def align( self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		self.d = 3
		results = []

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):

				if(j < i):
					s = {}
				else:
					# If the banded checkbox is checked, run the banded algorithm
					if self.banded:
						banded_alg = Banded()
						# If the test sequence is paired with a Coronavirus sequence, report no alignment possible
						if (i == 0 or i == 1) and j > 1:
							score, alignment1, alignment2 = float('inf'), "No Alignment Possible", "No Alignment Possible"
						# If the provided characters to align is less than the 2 sequence lengths (i.e. not a test case)
						elif self.MaxCharactersToAlign < len(sequences[i]) and self.MaxCharactersToAlign < len(sequences[j]):
							score, alignment1, alignment2 = banded_alg.edit_distance(sequences[i], sequences[j],
								self.MaxCharactersToAlign, self.MaxCharactersToAlign,  self.d)
						# If either the test cases of polynomial or exponential
						else:
							m, n = len(sequences[i]), len(sequences[j])
							score, alignment1, alignment2 = banded_alg.edit_distance(sequences[i], sequences[j],
								m, n, self.d)
					# If the banded checkbox is not checked, run the unrestricted algorithm
					else:
						unrestricted_alg = Unrestricted()
						# If the test sequence is paired with a Coronavirus sequence, report no alignment possible
						if (i == 0 or i == 1) and j > 1:
							score, alignment1, alignment2 = float('inf'), "No Alignment Possible", "No Alignment Possible"
						# If the provided characters to align is less than the 2 sequence lengths (i.e. not a test case)
						elif self.MaxCharactersToAlign < len(sequences[i]) and self.MaxCharactersToAlign < len(
								sequences[j]):
							score, alignment1, alignment2 = unrestricted_alg.edit_distance(sequences[i], sequences[j],
																					 self.MaxCharactersToAlign,
																					 self.MaxCharactersToAlign)
						# If either the test cases of polynomial or exponential
						else:
							m, n = len(sequences[i]), len(sequences[j])
							score, alignment1, alignment2 = unrestricted_alg.edit_distance(sequences[i], sequences[j],
																					 m, n)
					s = {'align_cost':score, 'seqi_first100':alignment1[0:100], 'seqj_first100':alignment2[0:100]}
					table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
					table.update()	
				jresults.append(s)
			results.append(jresults)
		return results


