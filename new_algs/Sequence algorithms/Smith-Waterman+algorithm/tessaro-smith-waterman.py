'''
Author: Filippo Tessaro
Mail: filippo.tessaro@studenti.unitn.it
Delivery Date: 3 June 2019
'''
from __future__ import division, print_function
import numpy as np

#Dictionary for the match, mismatch and gap scores
scores ={'match': 3, 'mismatch': -1, 'gap': -2}

def spaceitout(source):
    '''
    This function add a space to every character into a string
    '''
    pile = ""
    for letter in source:
        pile = pile + letter + " "
    pile = pile[:-1] #Strip last extraneous space.
    return pile

def printResult(align2, align1):
    '''
    print the 2 aligned strings with a better visualization
    '''
    c = ''
    for (a, b) in zip(align2,align1):
         if a==b:
             c += "|"
         else:
             c += '*'
    print(spaceitout(align2))
    print(spaceitout(c))
    print(spaceitout(align1))


def Similarity_Score(a, b):
    '''
    check whether two character there is a gap-mismatch-match
    '''
    if a == b:
        return scores['match']
    elif a == '-' or b == '-':
        return scores['gap']
    else:
        return scores['mismatch']

# function to return the first element of the
# 2 elements passed as the paramater
def sortFirst(val):
    return len(val[0])

def smithWaterman(s1, s2):
    '''
    compute the smith smithWaterman algorithm
    between 2 strings
    '''
    m, n = len(s1), len(s2)

    Score_Matrix = np.zeros((m+1, n+1), np.int)    #SCORE MATRIX
    Pointer_Matrix = np.zeros((m+1, n+1), np.int)    #POINTER MATRIX (useful for the traceback)
    max_score = 0

    # Score, Pointer Matrix genetation
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sc_diag = Score_Matrix[i-1][j-1] + Similarity_Score(s1[i-1], s2[j-1])    #diagonal value
            sc_up = Score_Matrix[i][j-1] + scores['gap']   #upper value
            sc_left = Score_Matrix[i-1][j] + scores['gap'] #left value

            #Find the maximum score beteen the three variables
            #and set it to the score MATRIX
            Score_Matrix[i][j] = max(0,sc_left, sc_up, sc_diag)
            if Score_Matrix[i][j] == 0: Pointer_Matrix[i][j] = 0
            if Score_Matrix[i][j] == sc_left: Pointer_Matrix[i][j] = 1
            if Score_Matrix[i][j] == sc_up: Pointer_Matrix[i][j] = 2
            if Score_Matrix[i][j] == sc_diag: Pointer_Matrix[i][j] = 3
            if Score_Matrix[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = Score_Matrix[i][j]

    #Log the SCORE MATRIX
    print('SCORE MATRIX:\n',Score_Matrix,'\n')

    #Initialization for the traceback
    align1, align2 = '', '' #the 2 alignemnt strings
    i,j = max_i,max_j       #index of the max score of the matrix

    #Traceback
    while Pointer_Matrix[i][j] != 0:
        if Pointer_Matrix[i][j] == 3:
            a1 = s1[i-1]
            a2 = s2[j-1]
            i -= 1
            j -= 1
        elif Pointer_Matrix[i][j] == 2:
            a1 = '-'
            a2 = s2[j-1]
            j -= 1
        elif Pointer_Matrix[i][j] == 1:
            a1 = s1[i-1]
            a2 = '-'
            i -= 1
        align1 += a1
        align2 += a2

    align1 = align1[::-1]
    align2 = align2[::-1]

    print('Max Score =', max_score,'\n')

    print('Result:')
    printResult(align2,align1)

def smithWatermanModified(s1, s2, min_score, min_lenght):
    '''
    return all the possible alignemnt, ordered by decreasing alignment lenght,
    with lenght > min_lenght and score > min_score
    '''
    m, n = len(s1), len(s2)

    Score_Matrix = np.zeros((m+1, n+1), np.int)    #SCORE MATRIX
    Pointer_Matrix = np.zeros((m+1, n+1), np.int)    #POINTER MATRIX (useful for the traceback)

    #declaire a list of coordinates and score where the score is > 3
    scores_list = []

    # Score, Pointer Matrix genetation
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sc_diag = Score_Matrix[i-1][j-1] + Similarity_Score(s1[i-1], s2[j-1])    #diagonal value
            sc_up = Score_Matrix[i][j-1] + scores['gap']   #upper value
            sc_left = Score_Matrix[i-1][j] + scores['gap'] #left value

            #Find the maximum score beteen the three variables
            #and set it to the score MATRIX
            Score_Matrix[i][j] = max(0,sc_left, sc_up, sc_diag)
            if Score_Matrix[i][j] == 0: Pointer_Matrix[i][j] = 0
            if Score_Matrix[i][j] == sc_left: Pointer_Matrix[i][j] = 1
            if Score_Matrix[i][j] == sc_up: Pointer_Matrix[i][j] = 2
            if Score_Matrix[i][j] == sc_diag: Pointer_Matrix[i][j] = 3
            if Score_Matrix[i][j] > min_score:
                scores_list.append ([Score_Matrix[i][j], i, j])

    #possible reorder of the scores list
    #scores_list.sort(key = sortFirst, reverse = True)
    print("Lenght of scores list with score major than {}: {}".format(min_score, len(scores_list)))

    print('SCORE MATRIX:\n',Score_Matrix,'\n')

    #list of possible alignment strings with score
    #major than a certain value (min_score)
    sequences_list = []

    for elem in scores_list:
        #Initialization for the traceback
        align1, align2 = '', '' #the 2 alignemnt strings
        i,j = elem[1],elem[2]       #index of the max score of the matrix
        #Traceback
        while Pointer_Matrix[i][j] != 0:
            if Pointer_Matrix[i][j] == 3:
                a1 = s1[i-1]
                a2 = s2[j-1]
                i -= 1
                j -= 1
            elif Pointer_Matrix[i][j] == 2:
                a1 = '-'
                a2 = s2[j-1]
                j -= 1
            elif Pointer_Matrix[i][j] == 1:
                a1 = s1[i-1]
                a2 = '-'
                i -= 1
            align1 += a1
            align2 += a2
        #check if the minimum lenght is satisfied
        if(len(align1) > min_lenght):
            #Reverse the two aligned strings
            align1 = align1[::-1]
            align2 = align2[::-1]
            #store it in the list
            sequences_list.append([align1,align2, elem[0]])

    #Sort by Alignment Lenght in a decreasing way
    sequences_list.sort(key = sortFirst, reverse = True)

    #Loop for print the results
    for idx, align in enumerate(sequences_list):
        print('Alignment number ', idx, ' with score ', align[2])
        printResult(align[0],align[1])
        print('\n')


if __name__ == '__main__':
    #smithWaterman('GGTTGACTA','TGDTACG')
    #Run the modified version of the Smith Waterman Algorithm
    smithWatermanModified('GGTTGACTA','TGDTACG',3 , 5)
