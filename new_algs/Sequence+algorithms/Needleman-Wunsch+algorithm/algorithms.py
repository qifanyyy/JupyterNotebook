#!/usr/bin/env python

import logging.config
import os
import time

import numpy as np
import pandas as pd
from NeedlemanWunschPy.substitutionmatrix import Blosum50, Blosum62, PAM250

# About
__author__ = "Antonio Benitez Hidalgo"
__email__ = "antonio.b@uma.es"
__version__ = "1.4-SNAPSHOT"

# Load logger config from file
logging.config.fileConfig("logconfig.ini")
logger = logging.getLogger(__name__)


"""
 Global NeedlemanWunschPy with simple gap costs using the Needleman-Wunsch algorithm.

 Note: The pseudo-code implemented in this example can be found here:
            http://www.inf.fu-berlin.de/lehre/WS05/aldabi/downloads/pairAlign_part1.pdf
 More info: https://ab.inf.uni-tuebingen.de/teaching/ws06/albi1/script/pairalign_script.pdf,
            http://www.itu.dk/people/sestoft/bsa/graphalign.html
"""


def get_time_of_execution(f):
    """ Decorator to get time of execution """

    def wrapped(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        logger.info("Time elapsed to " + f.__name__ + " (s): " + str(time.time() - start_time))
        return res

    return wrapped


class NeedlemanWunschLinear():
    def __init__(self, seqA, seqB, gap_penalty=-8, substitution_matrix=Blosum50(-8)):
        self.seq_h = seqA  # seq A (horizontal, rows)
        self.seq_v = seqB  # seq B (vertical, columns)
        self.gap_penalty = gap_penalty  # gap penalty both for opening and extension (linear gap penalty)
        self.substitution_matrix = substitution_matrix

        self.num_rows = len(seqA) + 1  # number of rows plus one (the first one)
        self.num_cols = len(seqB) + 1  # number of columns plus one (the first one)

        # Initialization of scoring matrix
        self.M = np.zeros(shape=(self.num_cols, self.num_rows),
                          dtype=np.int)  # matrix of zeros of integers (score matrix)

    def _get_score(self, i, j):
        """ Get score from two chars.

        :return: Score of the pair of chars.
        """

        char1, char2 = self.seq_h[j-1], self.seq_v[i-1]
        return self.substitution_matrix.get_score(char1, char2)

    @get_time_of_execution
    def _compute_score_matrix(self):
        """ Needleman Wunsch algorithm. Formula:
                M(0,0) = 0
                M(i,0) = M(i-1,0) - gap_penalty
                M(0,j) = M(0,j-1) - gap_penalty
                M(i,j) = max{ M(i-1,j-1) + score , M(i-1,j) + gap_penalty, M(i,j-1) + gap_penalty }

            M will be our scoring matrix.
        """

        # First column and row
        self.M[0, 0] = 0
        for j in range(self.num_cols):  # First row
            self.M[j, 0] = j * self.gap_penalty
        for i in range(self.num_rows):  # First column
            self.M[0, i] = i * self.gap_penalty

        # Rest of the matrix (recursive)
        for i in range(1, self.num_cols):
            for j in range(1, self.num_rows):
                self.M[i, j] = max(self.M[i-1, j-1] + self._get_score(i, j),  # score_diagonal
                                   self.M[i-1, j] + self.gap_penalty,  # score_up
                                   self.M[i, j-1] + self.gap_penalty)  # score_left

    @get_time_of_execution
    def _compute_traceback(self):
        """ Traceback algorithm. We can make the traceback looking to the traceback matrix (T):
            ...up arrow: we consume a character from the vertical sequence and add a gap to the horizontal one
            ...left arrow: we consume a character from the horizontal sequence and add a gap to the vertical one
            ...diagonal arrow: we consume a character from both sequences.
        """

        seqAaln, seqBaln, path = [], [], []
        i, j = self.num_cols - 1, self.num_rows - 1

        while i > 0 and j > 0:
            if self.M[i,j] == self.M[i-1, j-1] + self._get_score(i, j):  # score_diagonal
                logger.debug(" > going diagonal, i={0}, j={1}".format(i, j))
                seqAaln.append(self.seq_h[j-1])
                seqBaln.append(self.seq_v[i-1])
                path.append(self.M[i, j])
                i, j = i-1, j-1
            elif self.M[i,j] == self.M[i-1, j] + self.gap_penalty:  # score_up
                logger.debug(" > going up, i={0}, j={1}".format(i, j))
                seqAaln.append('-')
                seqBaln.append(self.seq_v[i-1])
                path.append(self.M[i, j])
                i -= 1
            else:  # score_left
                logger.debug(" > going left, i={0}, j={1}".format(i, j))
                seqAaln.append(self.seq_h[j-1])
                seqBaln.append('-')
                path.append(self.M[i, j])
                j -= 1

        # Finish tracing up to the top left cell
        while i > 0:
            logger.debug(" > going left, i={0}, j={1}".format(i, j))
            seqAaln.append('-')
            seqBaln.append(self.seq_v[i-1])
            path.append(self.M[i, j])
            i -= 1
        while j > 0:
            logger.debug(" > going up, i={0}, j={1}".format(i, j))
            seqAaln.append(self.seq_h[j-1])
            seqBaln.append('-')
            path.append(self.M[i, j])
            j -= 1

        # Return both reversed sequences
        seqAaln, seqBaln = "".join(seqAaln)[::-1], "".join(seqBaln)[::-1]
        logger.debug('Pathway chosen in the traceback matrix: {0}'.format(path))

        return seqAaln, seqBaln

    @get_time_of_execution
    def _save_matrix_to_file(self, matrix, filename, output_dir):
        """ Save matrix dataframe into a .csv file separated by commas. """

        data = pd.DataFrame(matrix, index=list(' ' + self.seq_v), columns=list(' ' + self.seq_h))
        data.to_csv(output_dir+filename+'.csv', sep=',', encoding='utf8')

    @get_time_of_execution
    def get_alignment(self, save_score_matrix_to_file=False, filename='score_matrix', output_dir='output/'):
        # Compute matrix
        self._compute_score_matrix()

        # Create output directory
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)

        if save_score_matrix_to_file:
            # Save to file
            self._save_matrix_to_file(self.M, filename, output_dir)

        return self._compute_traceback()
