#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 02:21:26 2020

@author: tomachache
"""

import numpy as np

# Adaptation of Needleman-Wunsch algorithm, which computes global alignment 
# between sequences, with custom gaps length and associated costs. 
# Each gap length has costs corresponding to opening and extending the gap.
# E.g. : {1  : (4,2), 3 : (5,3)} means we can have gaps of length 1, for which the costs
# for opening and extending such a gap are 4 and 2 respectively. We can also have gaps 
# of length 3, for which the costs for opening and extending are 5 and 3 respectively.

def cost(x, y, gaps, match_cost = -1, mismatch_cost = 1):
    # Compute the minimimum cost of aligning x and y, 
    # and return a dict containing the path leading to the alignment
    # gaps : dict/list/array containing gaps and costs
    n = len(x)
    m = len(y)
    S = np.zeros((n+1, m+1))
    D = np.zeros((n+1, m+1), dtype = bool) # Deletions (D[i][j] = True <=> currently in a deletion gap)
    I = np.zeros((n+1, m+1), dtype = bool) # Insertions
    bp = {} # dictionnary of backpointers (in order to retrieve the path)
    # bp[(i,j)] = (p,q) means the path goes from cell (p,q) to cell (i,j)
    
    if type(gaps) == dict: # convert the dict into an array
        array_cost = np.array([(k,) + gaps[k] for k in gaps.keys()])
    else:
        array_cost = np.array(gaps)
    
    nb_gap = array_cost.shape[0]
    max_gap_length = np.max(array_cost[:,0])
    
    ### INITIALISATION ###
    
    for i in range(1, n+1): # initialize first column
        if i <= max_gap_length:
            costs_del = D[np.maximum(i - array_cost[:,0], 0), 0] * array_cost[:,2] \
                      + (1 - D[np.maximum(i - array_cost[:,0], 0), 0]) * array_cost[:,1]
            # if D is true, we are extending a gap, otherwise we are opening it
            # the max is here to prevent having to separately handle the cases 
            # where i is smaller than the gap we considered, as such a gap would be ill-defined
        
            L = S[np.maximum(i - array_cost[:,0], 0), 0] + costs_del \
                - np.minimum(i - array_cost[:,0], 0) * (2 * costs_del + 1)
            # the "2 * current_cost + 1" ensures that the min won't be the ill-defined gaps
        
            S[i,0] = np.min(L)
            D[i,0] = True
            bp[i,0] = (i - array_cost[np.argmin(L), 0], 0)
    
        else: # in this case we are always extending, so no need for current_cost or the max
            L = S[i - array_cost[:,0], 0] + array_cost[:,2]
        
            S[i,0] = np.min(L)
            D[i,0] = True
            bp[i,0] = (i - array_cost[np.argmin(L), 0], 0)

    for j in range(1, m+1): # initialize first row
        if j <= max_gap_length:
            costs_ins = I[0, np.maximum(j - array_cost[:,0], 0)] * array_cost[:,2] \
                      + (1 - I[0, np.maximum(j - array_cost[:,0], 0)]) * array_cost[:,1]
        
            L = S[0, np.maximum(j - array_cost[:,0], 0)] + costs_ins \
                - np.minimum(j - array_cost[:,0], 0) * (2 * costs_ins + 1)
        
            S[0,j] = np.min(L)
            I[0,j] = True
            bp[0,j] = (0, j - array_cost[np.argmin(L), 0])
    
        else:
            L = S[0, j - array_cost[:,0]] + array_cost[:,2]
        
            S[0,j] = np.min(L)
            I[0,j] = True
            bp[0,j] = (0, j - array_cost[np.argmin(L), 0])

    ### CORE OF THE ALGORITHM ###
            
    for i in range(1, n+1):
        for j in range(1, m+1):
            delta = match_cost * (x[i-1] == y[j-1]) + mismatch_cost * (x[i-1] != y[j-1])
            # delta is match or mismatch cost
       
            costs_del = D[np.maximum(i - array_cost[:,0], 0), j] * array_cost[:,2] \
                      + (1 - D[np.maximum(i - array_cost[:,0], 0), j]) * array_cost[:,1]
            L_del = S[np.maximum(i - array_cost[:,0], 0), j] + costs_del \
                    - np.minimum(i - array_cost[:,0], 0) * (2 * costs_del + 1)
            
            costs_ins = I[i, np.maximum(j - array_cost[:,0], 0)] * array_cost[:,2] \
                      + (1 - I[i, np.maximum(j - array_cost[:,0], 0)]) * array_cost[:,1]
            L_ins = S[i, np.maximum(j - array_cost[:,0], 0)] + costs_ins \
                    - np.minimum(j - array_cost[:,0], 0) * (2 * costs_ins + 1)
            
            L = np.concatenate(([S[i-1][j-1] + delta], L_del, L_ins))
            
            S[i][j] = np.min(L) # compute new value
            index = np.argmin(L) # save index
            
            if index == 0: # means the best alignment at position (i,j) is match/mismatch
                bp[i,j] = (i-1, j-1)
            elif index > 0 and index <= nb_gap : # means best alignment is a deletion
                D[i,j] = True
                bp[i,j] = (i - array_cost[index - 1, 0], j)
            else: # means best alignment is an insertion
                I[i,j] = True
                bp[i,j] = (i, j - array_cost[index - nb_gap - 1, 0])

    return S[n][m], bp # return cost and dict of backpointers

def backtracking_seq(bp, n, m): 
    # Unwind the path from the backpointers dict
    i = n
    j = m
    
    seq = []
    while (i,j) != (0,0):
        (i_new, j_new) = bp[i,j] # unroll the backpointers dictionnary
        if i_new == i-1:
            if j_new == j-1:
                seq += ['M'] # we did a match/mismatch
            else: # then j_new = j
                seq += ['D'] # we did a deletion
        elif i_new == i:
            if j_new == j-1:
                seq += ['I'] # we did an insertion
            else: # then j_new = j-3
                seq += ['I', 'I', 'I'] # we did 3 insertions
        else: # only 1 case left (i_new = i - 3 and j_new = j)
            seq += ['D', 'D', 'D'] # we did 3 deletions
        i = i_new
        j = j_new
        
    seq.reverse() # reverse the list to have the path from (0,0) --> (n,m)
    
    return seq

def print_alignment(x, y, gaps): 
    # Print alignment and cost
    c, bp = cost(x, y, gaps)
    n = len(x)
    m = len(y)
    s = backtracking_seq(bp, n, m)
    
    x_new = ''
    y_new = ''
    trans = '' # will be used for a nice rendering (show '|' when nucleotides match)
    
    q = len(s)
    ind_x = 0 # counter
    ind_y = 0 # counter
    
    for k in range(q):
        if s[k] == 'I': # i.e. we did an insertion in x
            x_new += '-'
            y_new += y[ind_y]
            trans += ' '
            ind_y += 1
        elif s[k] == 'D': # i.e. we did an insertion in y (i.e. a deletion in x)
            x_new += x[ind_x]
            y_new += '-'
            trans += ' '
            ind_x += 1
        else: # i.e. we did a match/mismatch
            x_new += x[ind_x]
            y_new += y[ind_y]
            if x[ind_x] == y[ind_y]: # i.e. we have a match
                trans += '|'
            else : 
                trans += ' '
            ind_x += 1
            ind_y += 1
    
    # Now we can print the sequences (in a nice way)
            
    z = q//50
    r = q % 50
    
    for k in range(z):
        print("Seq 1 (part {}): ".format(k+1) + x_new[50*k : 50*(k+1)])
        print("                " + trans[50*k : 50*(k+1)])
        print("Seq 2 (part {}): ".format(k+1) + y_new[50*k : 50*(k+1)])
        print("\n")
    if r > 0:
        print("Seq 1 (part {}): ".format(z+1) + x_new[50*z:])
        print("                " + trans[50*z:])
        print("Seq 2 (part {}): ".format(z+1) + y_new[50*z:])
        print("\n")  
    print("Score : {}.".format(int(c)))
    
    return

def generate_random_seq(n, A = ['A', 'C', 'G', 'T']):
    # Generate random sequence of length n for alphabet A
    return ''.join(np.random.choice(A, n))


# Some examples
    
if __name__ == "__main__":
    gaps = {1  : (4,2), 3 : (5,3)}

    # compare coding sequences of Covid-19 and a previous Coronavirus
    s = 'ATGTTGCTTTTCAAACTGTCAAACCCGGTAATTTTAACAAAGACTTCTATGACTTTGCTGTGTCTAAGGG'\
        'TTTCTTTAAGGAAGGAAGTTCTGTTGAATTAA'
    s_old = 'ATGTTGCTTTTCAAACTGTCAAACCCGGTAATTTTAATAAAGACTTTTATGACTTTGCTGTGTCTAA'\
        'AGGTTTCTTTAAGGAAGGAAGTTCTGTTGAACTAA'
        
    print_alignment(s, s_old, gaps)
    
    # compare alignment of random sequences
    print_alignment(generate_random_seq(50), generate_random_seq(40), gaps)