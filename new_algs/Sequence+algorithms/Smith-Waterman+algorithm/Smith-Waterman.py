#Smith Waterman algorithm : Algorithm for BioInformatics - UniTN 2019
#Sébastien Cararo


# This algorithm compute the best local alignement given two sequences of ADN, plus it displays the scoring matrix, the path, and a few gifures about the alignement (%matches, %mismatches, %gaps) 
# During the construction of the scoring matrix we also construct a "path_matrix" which records the way we obtained the score in the score_matrix and gives instruction about the traceback : each cell is of the form [distance, 'DIRECTION'] when DIRECTION can be either DIAG, UP, LEFT or NULL (presence of a 0). 

#Input = sequence A, sequence B, scoring system (match, mismatch, gap)
#Output Best solution for the local alignment (2 strings), score assigned for this solution. 
# example of output : recall of the input, score of the best local alignment, best local alignment in the form of two sequences (eventually with gaps) 

#Libraries
import numpy 
import argparse
import os
import re
import sys
import unittest
import time
from pandas import *


#Initialization
seqA = 'TTAGCTGATCTTAC'
seqB = 'TTAGGCTATCGA'

match = 3
mismatch = -1
#gap = '' -> we define a gap penalty function at the end of the code 
#(so the program is suitable for affine penalties too) 

alphabet = 'ACGT'


def main():  
    
    
    #First we display the Substitution matrix, the scoring matrix
    print('The substitution matrix for the alphabet {0} is:'.format(alphabet))
    Substi = create_Substi(alphabet, match, mismatch)
    print(DataFrame(Substi))
    
    rows = len(seqA) + 1
    cols = len(seqB) + 1

    
    score_matrix, start_pos, max_score, path_matrix = create_score_matrix(rows, cols)  
                                                                
    print('Scoring Matrix : \n')
    print_matrix(score_matrix)         
    print('Highest score = ', max_score)
    print('start_pos=',start_pos)
    print('The path to 0 is:')
    time.sleep(0.5)
    
    # Traceback : it also displays the path  
    seqA_aligned, seqB_aligned = traceback(path_matrix, start_pos, score_matrix)
    assert len(seqA_aligned) == len(seqB_aligned), 'aligned strings are not the same size'
    
    
    
    
    # Printing the alignements and a few figures 
    Graphical_display(seqA_aligned, seqB_aligned)
    print('Score of the alignment = ')
    print(max_score)
    return(0)
    
    
    
    

def traceback(path_matrix, start_pos, score_matrix):
    '''The function does the traceback based on the starting position
    and on the instructions contained in the path_matrix, 
    it also displays the move done at each step '''
    
    x,y = start_pos
    aligned_seqA = []
    aligned_seqB = []
    
    
    while path_matrix[x][y] != [0, 'NULL'] :
        d, direction = path_matrix[x][y][0], path_matrix[x][y][1]
        if direction == 'DIAG' :
            assert d ==1, 'path_matrix wrongly constructed !'
            aligned_seqA.append(seqA[x - 1])     
            aligned_seqB.append(seqB[y - 1])
            x -= 1
            y -= 1
            print('DIAG',score_matrix[x][y])
        elif direction == 'UP' : 
            for c in range(d):
                aligned_seqA.append(seqA[x - 1])
                aligned_seqB.append('-')             
                x -= 1
                print('UP',score_matrix[x][y])
        elif direction == 'LEFT' :
            for c in range(d):
                aligned_seqA.append('-')            
                aligned_seqB.append(seqB[y - 1])
                y -= 1
                print('LEFT',score_matrix[x][y])
    print('Traceback reached a 0 at :',(x,y))
    
    return ''.join(reversed(aligned_seqA)), ''.join(reversed(aligned_seqB))
    
    
    
    
    
    
    
    
    
    
    


def create_score_matrix(rows, cols):
    '''The function creates the score_matrix and the path_matrix'''
    score_matrix = [[0 for col in range(cols)] for row in range(rows)]
    path_matrix = [[[0 , 'NULL'] for col in range(cols)] for row in range(rows)]  
    
    max_score = 0
    max_pos   = None    
    for i in range(1, rows): 
        for j in range(1, cols):
            score, antecedent = calc_score(score_matrix, i, j)
            if score > max_score:                  
                max_score = score
                max_pos   = (i, j)

            score_matrix[i][j],path_matrix[i][j] = score, antecedent           

    assert max_pos is not None, 'No maximum found'

    return score_matrix, max_pos, max_score, path_matrix   


def calc_score(score_matrix, x, y): 
    '''this function is used during the score_matrix construction, 
    it is suitable for affine gap penalties and works with a substitution matrix'''
    similarity = Substitution_score(Substi, x, y)

    
    same_row = [(score_matrix[x][y-l]-gap_penalty(l)) for l in range(1,x+1)]
    same_col = [(score_matrix[x-k][y]-gap_penalty(k)) for k in range(1,x+1)]
    
    up_score = max(same_col)
    left_score = max(same_row)
    
    
    diag_score = score_matrix[x - 1][y - 1] + similarity
    pos_max_up = first_pos_max(same_col)    
    pos_max_left = first_pos_max(same_row)
                  

    score =  max(0, diag_score, up_score, left_score)  
    
    if score == diag_score :
        antecedent = [1, 'DIAG']
        return score, antecedent
    elif score == up_score :
        antecedent = [pos_max_up + 1, 'UP']
        return score, antecedent
    elif score == left_score : 
        antecedent = [pos_max_left + 1, 'LEFT']
        return score, antecedent 
    else :
        return score, [0, 'NULL']


        




def alignment_string(aligned_seqA, aligned_seqB): 

    idents, gaps, mismatches = 0, 0, 0
    alignment_string = []                           
    for base1, base2 in zip(aligned_seqA, aligned_seqB): #loop that runs over both sequences simultaneously 
        if base1 == base2:
            alignment_string.append('|')
            idents += 1
        elif '-' in (base1, base2):
            alignment_string.append(' ')
            gaps += 1
        else:
            alignment_string.append(':')
            mismatches += 1

    return ''.join(alignment_string), idents, gaps, mismatches


def create_Substi(alphabet, match, mismatch):
    '''Creates a substitution matrix, given the alphabet and the match/mismatch scores'''
    global Substi 
    Substi = [['NULL' for col in range(len(alphabet))] for row in range(len(alphabet))] 

    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            if alphabet[i] == alphabet[j] :
                Substi[i][j] = match
            elif alphabet[i] != alphabet[j]:
                Substi[i][j] = mismatch
                
    
    return Substi
    
def Substitution_score(Substi, x, y):
    '''we seek the score between seqA[x-1] and seqB[y-1]'''
    a_i = alphabet.index(seqA[x-1])
    b_j = alphabet.index(seqB[y-1])
    
    return Substi[a_i][b_j]
    

def Graphical_display(seqA_aligned, seqB_aligned):
    alignment_str, idents, gaps, mismatches = alignment_string(seqA_aligned, seqB_aligned)
    alength = len(seqA_aligned)
    time.sleep(0.2)    
    print()
    print(' Identities = {0}/{1} ({2:.1%}), Gaps = {3}/{4} ({5:.1%}), Mismatches = {6}/{7} ({8:.1%})'.format(idents,
          alength, idents / alength, gaps, alength, gaps / alength, mismatches, alength, mismatches/alength))
    print()
    for i in range(0, alength, 60):
        seqA_slice = seqA_aligned[i:i+60]
        print('Query  {0:<4}  {1}  {2:<4}'.format(i + 1, seqA_slice, i + len(seqA_slice)))
        print('             {0}'.format(alignment_str[i:i+60]))
        seqB_slice = seqB_aligned[i:i+60]
        print('Sbjct  {0:<4}  {1}  {2:<4}'.format(i + 1, seqB_slice, i + len(seqB_slice)))
        print()





def print_matrix(matrix): # graphical display of matrix 
    print('\n'.join([''.join(['     {:4}'.format(item) for item in row])for row in matrix]))
          
 
def first_pos_max(list):
    maxi = max(list)
    return [i for i, j in enumerate(list) if j == maxi][0]
      
def gap_penalty(k) : 
    return 3*k



if __name__ == '__main__':
    sys.exit(main())