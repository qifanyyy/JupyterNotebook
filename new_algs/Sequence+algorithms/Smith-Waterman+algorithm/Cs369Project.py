#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lawrence
"""

# for arrays
import numpy as np
# for data frames (i.e tabular data that have row names and column names)
# unlike numpy arrays data frames support different data types for each column 
import pandas 
# for random sequences
import random
# for measuring execution time
import timeit
# for plotting
import matplotlib 


"""
This part implements both Needleman-Wunsch and Smith-Waterman algorithms 
for DNA sequence alignment.
"""


def get_F_matrix(A, B, match=1.0, mismatch=-1.0, gap=-2.0):
    """
    Returns a global alignment between sequences A and B,
    gap is the linear gap penalty.
    F is the F matrix, where A is in row, B is in column.
    Strings AlignmentA and AlignmentB make up the alignment. 
    """
    
    # The dimension of the matrix
    rown = len(A) + 1
    coln = len(B) + 1

    # init 2D F matrix, shape=(len(A)+1, len(B)+1)
    F = np.zeros(shape=(rown, coln))
    
    #Filling the F-Matrix
    for i in range (1,len(A)+1):
        #initialises left-most column
        F[i,0]=F[i-1,0]+gap
        for j in range(1,len(B)+1):
            #initialises top row
            F[0,j]=F[0,j-1]+gap
            if A[i-1] == B[j-1]:
                S = match
            else: S = mismatch
            F[i,j]= (max(F[i-1,j-1]+S,F[i,j-1]+gap,F[i-1,j]+gap))
    
    return F

def trace_back(F, A, B, match=1.0, mismatch=-1.0, gap=-2.0):
    """
    Returns a global alignment between two sequences A and B.
    gap is the linear gap penalty
    F is the F matrix, where A is in row, B is in column.
    Strings AlignmentA and AlignmentB make up the alignment. 
    """
    # i indexing row, j indexing col in F
    i, j = len(A), len(B)
    if i == 0 or j == 0 or i >= np.shape(F)[0] or j >= np.shape(F)[1]:
        raise ValueError('Invalid position [%s, %s] !' % (i, j))

    # aligned sequence A
    AlignmentA = ""
    # aligned sequence B
    AlignmentB = ""
    
    #Function to check if Sequence A and B have the same characters at a specific alignment
    def match_nomatch(q,w):
        if A[q] == B[w]:
            S = match
        else:
            S = mismatch
        return S
    
    
    while i > 0 and j > 0:
        cur = F[i,j]
        diag = F[i-1,j-1]
        hor = F[i,j-1]
        vert = F[i-1,j]
        
        #Check where current score came from, then update i and j accordingly
        if cur == vert + gap:
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = '-' + AlignmentB
            i-=1
        elif cur == diag + match_nomatch(i-1,j-1):
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            i-=1
            j-=1
        elif cur == hor + gap:
            AlignmentA = '-' + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            j-=1
    
    # returns two strings
    return AlignmentA, AlignmentB

def get_optimal_score(A, B, match=1.0, mismatch=-1.0, gap=-2.0):
    """
    Calculates and returns the score of the optimal global alignment of sequences A and B.
    gap is the linear gap penalty.
    """
    
    # YOUR CODE HERE
    
    
    """
    MEMORY COMMENT:
    This function creates the entire F matrix, so takes up a quadratic amount (len(A)+1)*(len(B)+1) (O(n^2)) of memory.
    """
    
    
    #Simple wrapping Function for get_F_matrix
    opt_F = get_F_matrix(A,B,match,mismatch,gap)
    score = opt_F[len(A),len(B)]
    # YOUR CODE FINISHED ABOVE
    
    return score

def get_optimal_score2(A, B, match=1.0, mismatch=-1.0, gap=-2.0):
    """
    Calculates and returns the score of the optimal global alignment of sequences A and B.
    Uses memory efficient score calculation. 
    gap is the linear gap penalty.
    """
    
    """
    MEMORY COMMENT:
    This variation only requires a 2*(len(B)+1) F matrix, so takes up a linear amount 2*(len(B)+1) (O(n)) of memory.
    """
    
    
    #Aligns row and column length of matrix with sequence length
    rn="-"+A
    cn="-"+B
    
    #Function to check if Sequence A and B have the same characters at a specific alignment
    def find_score(a,b): 
        if a==0 and b==0:
            return 0
        elif rn[a]==cn[b]:
            return match
        else:
            return mismatch
        
    #create 2,len(B) matrix of zeroes
    F = np.zeros(shape=(2, len(cn)))

    for j in range(1,len(B)+1):
    #initialises top row
        F[0,j]=F[0,j-1]+gap

    #Filling the bottom row first, than copying bottom to top and repeat
    for i in range(1,len(A)+1):
        #Score bottom row
        for j in range(1,len(B)+1):
            F[1,0]=F[0,0]+gap
            F[1,j]=max(F[1,j-1]+gap,F[0,j-1]+find_score(i,j),F[0,j]+gap)
        #Copy bottom row onto top row until the last row is reached
        F[0,:]=F[1,:]
    #Score is the rightmost value of the bottom row
    score = F[1,len(B)]
                
    return score

import matplotlib.pyplot as plt

def random_sequence(alphabet='CGTA', N=5):
    """
    Generates a random sequence of length N using letters from alphabet, the set of possible letters.  
    Each letter has equal probability to be chosen at any position of the sequences
    """

    # YOUR CODE HERE
    sequence =''
    for i in range(0,N):
        sequence = sequence + random.choice(alphabet)
    # YOUR CODE FINISHED ABOVE
    
    # returns the random sequence as a string
    return sequence

def time_and_plot(alphabet='CGTA', pairs_N =5, min_N = 5, max_N = 21, step_N = 5,
                  match=1.0, mismatch=-1.0, gap=-2.0):
    """
    Empirical analysis of time performance of get_optimal_score()
    Calculates and save the times in a pandas.DataFrame
    Calls functions random_sequences() and get_optimal_score()
    """
    
    # We set the seed of the random number generator for output reproducibility.
    random.seed(12345)
    
    # YOUR CODE HERE
    global timethis
    d=[]
    for j in range(min_N,max_N,step_N):
        sc=0
        for i in range(0,pairs_N):
            seq1 = random_sequence(alphabet,j)
            seq2 = random_sequence(alphabet,j)
            
            #Wrapping function for get_optimal_score for each pair of sequences as timethis 
            #does not allow any values to be passed in
            def timethis():
                score = get_optimal_score(seq1,seq2,match,mismatch,gap)
                return score
            
            #Use timeit with 100 iterations to record execution time
            tm = timeit.timeit('timethis()', number = 100 , globals=globals())
            #Adds together the execution time for the five sequence combinations of a specific N
            sc = sc + (tm/100)
        #Finds average time for each N   
        avg_time = sc/pairs_N
        d.append([j,avg_time])
    #use scatter plot, repeat 100 times for each time sequence, only 1 reading for every N
    time_df = pandas.DataFrame(data=d,columns=['N','Time'])
    plt.scatter(time_df['N'],time_df['Time'])
    plt.xlabel('sequences of length N characters')
    plt.ylabel('average Time(s)')
    plt.title('Average Time vs Sequence length')
    plt.show()
    # YOUR CODE FINISHED ABOVE
    
    # data frame with two columns N, Time
    # Time is the average execution time for the optimal score of pair_N pairs of sequences of length N
    return time_df

# define score matrix S1 and S2

nuc = ['A', 'G', 'C', 'T'] # Purines, Pyramidines
# match=1, mismatch=-1
match_mismatch = np.reshape((1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1), (4, 4))
# score matrix:
S1 = pandas.DataFrame(match_mismatch, index=nuc, columns=nuc)
print("S1 = \n", S1)
# 2 if a = b, 1 if a b is purine or a b is pyrimidine,
# -2 if a is a purine and b is a pyrimidine or vice versa.
pur_pyr = np.reshape((2, 1, -2, -2, 1, 2, -2, -2, -2, -2, 2, 1, -2, -2, 1, 2), (4, 4))
S2 = pandas.DataFrame(pur_pyr, index=nuc, columns=nuc)
print("\nS2 = \n", S2)

def local_alignment(A, B, S, d=-2.0):    
    """
    Returns a local alignment between sequences A and B,
    S is the score matrix as pandas.DataFrame, and d is the penalty.
    F is the F matrix, where A is in row, B is in column.
    max_pos is the coordinate of the highest score max_score in F matrix.
    Strings AlignmentA and AlignmentB make up the alignment. 
    """
    
    # The dimension of the matrix
    rown = len(A) + 1
    coln = len(B) + 1

    # init 2D F matrix, shape=(len(A)+1, len(B)+1)
    F = np.zeros(shape=(rown, coln))
    
    # holds the highest score in F matrix
    # initialize to 0 
    max_score = 0
    # coordinates of the highest score in F matrix as a tuple, 
    # i.e. (row index, col index)
    max_pos = None  

    AlignmentA = ""
    AlignmentB = ""
    
    #Align sequences with Matrix length
    rn = '-'+A
    cn = '-'+B
    
    #Check match-score for specific position
    def score(q,w):
        if q == 0 and w == 0:
            return 0
        else:
            return S.loc[rn[q],cn[w]]
        
    #Create F matrix     
    for i in range(1,rown):
        for j in range(1,coln):
            F[i,0]=F[i-1,0]+d; F[0,j]=F[0,j-1]+d
            #Take maximum of previous diagonal score + match score, vertical or horizontal + gap or 0
            F[i,j]=max(F[i-1,j-1]+score(i,j),F[i-1,j]+d,F[i,j-1]+d,0)
            if F[i,j] >= max_score:
                max_score = F[i,j]
                max_pos = (i,j)
                
    #Trace-back:
    i,j = max_pos
    
    while i > 1 or j > 1:
        cur = F[i,j]
        diag = F[i-1,j-1]
        hor = F[i,j-1]
        vert = F[i-1,j]
        if cur == vert + d:
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = '-' + AlignmentB
            i -=1
        elif cur == diag + score(i,j):
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            i -=1
            j -=1       
        elif cur == hor + d:
            AlignmentA = '-' + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            j -=1
        else:
            print('ERROR!')
            break
                                       
    return AlignmentA, AlignmentB, max_score, max_pos, F

def readBLOSUM62():
    """
    Returns the BLOSUM62 scoring matrix in BLOSUM_df, a pandas.DataFrame 
    The scoring matrix is stored in a text file, provided to you as "blosum62.txt". 
    Comments in the file are marked with # sign, and these should be excluded.
    """
    # The fourth line in the file has 23 elements represnting 20 canonical and 3 ambiguous amino acids
    # So the scoring matrix is 23 x 23 
    amino_acids = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V","B","Z","X"]
    col_names = amino_acids
    row_names = amino_acids
    # it is available with the Jupyter notebook  
    length = len(amino_acids)
    text_file = open("blosum62.txt", "r")
    
    matrix_array=[]
    while True:
        #reads in scoring matrix line by line
        line = text_file.readline()
        #checks if it has arrived at the end of the matrix
        if len(line) == 0:
            break
        #skips comments
        elif line[0] == '#':
            continue
        #checks for every character in the line if it is alphabetical, if not add to line array.
        #Credit for idea: https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
        else:
            line_array =   [int(s) for s in line.split() if not s.isalpha()]
        #if line array is greater than 0, add to matrix
        if len(line_array) > 0:
            matrix_array.append(line_array) 
    #combines matrix into pandas dataframe
    BLOSUM_df = pandas.DataFrame(data=matrix_array,index=row_names,columns=col_names)

    return BLOSUM_df

def overlap(A,B,S,d=-2.0):
    
    """
    Returns an overlap alignment between sequences A and B,
    S is the score matrix, and d is the penalty.
    F is the F matrix, where A is in row, B is in column.
    String AlignmentA and AlignmentB are the alignment. 
    score is the optimal alignment score
    """
    # init 2D F matrix, shape=(len(A)+1, len(B)+1)
    F = np.zeros((len(A)+1,len(B)+1))
    
    AlignmentA = ""
    AlignmentB = ""
    
    #Align sequences with Matrix length
    rn ='-'+A
    cn ='-'+B

    #determine the score in the scoring matrix by going through the position in the sequences
    def find_score(q,w):
        if q == 0 or w == 0:
            return 0
        else:
            return S.loc[rn[q],cn[w]]

    #create f-matrix similar to needleman-wunsch, but with the first column and row being zeros
    for i in range(1,len(A)+1):
        for j in range(1,len(B)+1):
            #Take maximum of previous diagonal score + match score, vertical or horizontal + gap
            F[i,j]=max(F[i-1,j-1]+find_score(i,j),F[i-1,j]+d,F[i,j-1]+d)

    #Find maximum scoring position in the right-most column and bottom row
    #right-most column:
    rc=F[:,len(B)]

    #lowest row:
    lr=F[len(A),:]

    
    #find max. element, lowest, then rightmost position if same score multiple times
    #If max. element occurs only once, use 
    
    #Builds list with indices of the maximum element in right-most column
    max_col_ind = [i for i in range(len(rc)) if rc[i]== max(rc)]
    #Takes the final(lowest) element of list with indices of max. values
    max_col_ind = max_col_ind[-1]

    #Builds list with indices of the maximum element in lowest row
    max_row_ind = [i for i in range(len(lr)) if lr[i]== max(lr)]
    #Takes the final(right-most) element of list with indices of max. values
    max_row_ind = max_row_ind[-1]

    
    
    #Take maximum score, if both are the same take lowest first, then right most score
    #If max. value is in the bottom row
    if lr[max_row_ind] >= rc[max_col_ind]: i,j,score = len(A),max_row_ind,F[len(A),max_row_ind]
    #If max. value is in the right most column
    else: i,j,score = max_col_ind,len(B),F[max_col_ind,len(B)]

    #Traceback:

    #First, reallign both sequences ends
    if i < len(A):
        gap=len(A)-i
        for k in range(0,gap):
            AlignmentB="-"+AlignmentB
            AlignmentA=rn[len(A)-k]+AlignmentA
    elif j < len(B):
        gap=len(B)-j
        for k in range(0,gap):
            AlignmentA="-"+AlignmentA
            AlignmentB=cn[len(B)-k]+AlignmentB


    #Once both are aligned, continue as in Needleman-Wunsch until either the top row (i=0)
    #or leftmost column (j=0) are reached
    while i > 0 and j > 0:
        cur = F[i,j]
        diag = F[i-1,j-1]
        hor = F[i,j-1]
        vert = F[i-1,j]
        if cur == vert+d:
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = '-' + AlignmentB
            i -=1
        elif cur == diag + find_score(i,j):
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            i -=1
            j -=1
        elif cur == hor + d:
            AlignmentA = '-' + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            j -=1
        else: 
            print('ERROR!')
            break

    if i > 0:
        for k in range(0,i):
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = '-' + AlignmentB
            i-=1
    elif j > 0:
        for k in range(0,j):
            AlignmentA = '-' + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            j-=1

    return AlignmentA, AlignmentB, score, F








"""
This part implements a hidden markov model to model infectious diseases.
"""

import random
import numpy as np
import pandas as pd
random.seed(3)

class ShotgunSequencing:
    def __init__(self):
        #initiates sequence as an empty string
        self.sequence =""
    
    def readSequence(self,filename,i=1):
        #Finds number of sequences in fasta file
        my_file = open(filename)
        num_seqs = my_file.read().count('>')
        my_file.close()
        #if i is non-positive or larger than the number of sequences in the file
        if i < 1 or i > num_seqs:
            return
        #Makes sure i=1 gives the first sequence which is i=0 in python
        else: i -= 1
        
        my_file = open(filename)
        seqs=[]
        first=True
        for j in range(0,num_seqs):
            sequence = ""
            while True:
                #reads in sequence line by line
                line = my_file.readline()
                #checks if it has arrived at the end of the file
                if len(line) == 0:
                    break
                #skips comments
                elif line[0] == ';':
                    continue
                #Ensures only one sequence is read at a time
                elif line[0] == '>' and first==True:
                    first = False
                    continue
                elif line[0] == '>' and first==False:
                    break
                #Adds new line to sequence
                else:
                    sequence = sequence + line
            #Appends sequence to sequences list   
            seq1 = sequence.replace('\n','')
            seqs.append(seq1)
        if len(seqs[i]) > 0:
            #Adds the current sequence to the array of sequences
            self.sequence = seqs[i]
            
    def shotgun(self,l_min,l_max):
        fragmented_seq=[]
        seq = self.sequence
        
        while len(seq) > 0:
            #Generate random sequence length
            frag = random.randint(l_min,l_max)
            #Take a slice from 0 to the random sequence length
            fragmented_seq.append(seq[0:frag])
            #Remove the part that was already fragmented from sequence
            seq=seq[frag:]
        return fragmented_seq   
        
    def cloning(self,l_min,l_max,n):
        sorted_seq=[]
        #Run shotgun n times, store results in sorted_seq array
        for i in range(0,n):
            sorted = self.shotgun(l_min,l_max)
            sorted_seq+=sorted
        sorted_seq.sort(key=len)
        return sorted_seq
class SequenceAssembler:
    def __init__(self):
        self.graph={}
              
    def calculateOverlap(self,fragmentA,fragmentB):
        while True:
            #Checks if fragB from position 0 to len(fragA) is the same as fragB
            if fragmentA==fragmentB[0:len(fragmentA)]:
                return len(fragmentA)
            #returns zero if length of fragA goes to zero
            elif len(fragmentA)==0:
                return 0
            else: fragmentA=fragmentA[1:] #cut of the first char of fragA and try again
    
    def createOverlapGraph(self,fragments):

        #First step: Eliminate duplicates and add all nodes to the graph
        self.graph=dict.fromkeys(fragments)
        
        #Removes nodes that are substrings of other nodes
        no_dups=list(self.graph)
        for i in no_dups:
            for j in no_dups:
                #If it finds itself don't remove
                if i==j:continue
                #If element finds its a substring of something else remove element
                if i in j: 
                    self.graph.pop(i)
                    break

        #Creates a dictionary for all nodes of the nodes it goes to, and the scores
        for i in self.graph:
            self.graph[i]=dict()
        
        #Second step: Add destination nodes and scores
        for node in self.graph:
            for dest_node in self.graph:
                #No edge going back to the same node
                if node==dest_node:
                    continue
                #Check for overlap with other nodes, if there is add to nodes dictionary with overlap score
                else: 
                    score = self.calculateOverlap(node,dest_node)
                    if score > 0:
                        self.graph[node][dest_node]=score 
        
    def getMaxEdge(self):
        
        max_start_node=""
        max_dest_node=""
        max_score=0
        #Iterates through every node in the graph
        for node in self.graph:
            #Iterates through every nodes edges 
            #and takes the first score it finds as the highest score
            for inner_node in self.graph[node]:
                #Than checks if any of the next nodes have a higher score, 
                #otherwise it sticks with the first highest scoring node
                if self.graph[node][inner_node]>max_score: 
                    max_score=self.graph[node][inner_node]
                    max_start_node=node
                    max_dest_node=inner_node
        return max_start_node,max_dest_node,max_score
    
    def assembling(self):
        while True:
        
            #Find highest scoring edge
            max_start_node,max_dest_node,max_score = self.getMaxEdge()

            #Combines the two nodes that are connecting by the highest scoring edge
            combined_node=max_start_node+max_dest_node[max_score:]
            
            #The combined node will point to the same nodes as the dest_node did 
            #This is because dest_node is the end of the new node, which determines the
            #overlap score with any of the other nodes
            
            #If max_dest_node was also pointing back at max_start_node this edge
            #shouldn't be copied because otherwise the combined_node will have an edge with itself
            if max_start_node in self.graph[max_dest_node]:
                del(self.graph[max_dest_node][max_start_node])
            self.graph[combined_node]=self.graph[max_dest_node]
            
            #Deletes the two old nodes
            del(self.graph[max_start_node])
            del(self.graph[max_dest_node])
            
            #Iterates through all the other nodes in the graph and checks if they are 
            #pointing to any of the two old nodes
            for nodes in self.graph:
                #If they point to max_dest_node these edges can be deleted as the front of
                #max_dest_node has already been merged
                if max_dest_node in self.graph[nodes]: del(self.graph[nodes][max_dest_node])
                #If they point to max_start_node that means they should now point to the new combined node
                if max_start_node in self.graph[nodes]: 
                    #Adds a new edge to the combined node where edge to max_start_node was
                    self.graph[nodes][combined_node]= self.graph[nodes][max_start_node]
                    #Then deletes edge to max start node
                    del(self.graph[nodes][max_start_node])
            _,_,max_score = self.getMaxEdge()
            if max_score==0: break
        superstring=""
        for keys in self.graph: superstring +=keys
        return superstring
    
    

    
#Tests
def similarity(x,y):
    """
    Very crude testing function that goes element by element to check if the two strings match
    """
    score=0
    for i in range(0,min(len(x),len(y))):
        if x[i]==y[i]: score+=1
        else: score-=1
    return score


test_statistic = {'Sequence': [], 'l_min': [], 'l_max': [], 'n': [], 'Similarity_score': [], 'Original sequence length/ Superstring length': []}



#Test sequence
t_list=[3,5,10]
t_min_max=[(5,10),(10,20),(20,30)]

p1 = ShotgunSequencing()
p1.readSequence('A3_DNAs.fasta',1)
seq=p1.sequence

for n in t_list:
    for m in t_min_max:
        fragment=p1.cloning(m[0],m[1],n)
        a1 = SequenceAssembler()
        a1.createOverlapGraph(fragment)
        superstring=a1.assembling()
        score=similarity(seq,superstring)
        test_statistic['Sequence'].append('Test')
        test_statistic['l_min'].append(m[0])
        test_statistic['l_max'].append(m[1])
        test_statistic['n'].append(n)
        test_statistic['Similarity_score'].append(similarity(seq,superstring))
        test_statistic['Original sequence length/ Superstring length'].append((len(seq),len(superstring)))
        
#Real_mRNA
r_list=[5,10,15]
r_min_max=[(50,100),(100,200),(200,500)]       

p2 = ShotgunSequencing()
p2.readSequence('A3_DNAs.fasta',2)
whole_seq=p2.sequence


for n in r_list:
    for m in r_min_max:
        fragment=p2.cloning(m[0],m[1],n)
        a2 = SequenceAssembler()
        a2.createOverlapGraph(fragment)
        superstring=a2.assembling()
        score=similarity(whole_seq,superstring)
        test_statistic['Sequence'].append('Real mRNA')
        test_statistic['l_min'].append(m[0])
        test_statistic['l_max'].append(m[1])
        test_statistic['n'].append(n)
        test_statistic['Similarity_score'].append(similarity(whole_seq,superstring))
        test_statistic['Original sequence length/ Superstring length'].append((len(whole_seq),len(superstring)))


test_stat_df = pd.DataFrame(data=test_statistic)
print(test_stat_df)

import random
import math
import matplotlib.pyplot as plt
import numpy as np
random.seed(3)
np.random.seed(3)

"Q3b"
def rand_exp(lam):
    if lam==0: return None
    u = random.uniform(0,1)
    x = (-math.log(1-u)/lam)
    return x

"Q3c"
def sim_SIR(N,I_0,beta,gamma):
    S=N-I_0;I=I_0;R=0;t=0
    event_log={t:[S,I,R]}
    while I>0:
        #Times between all events are exponentially distributed with the below rates
        tran_rate = (beta*S*I)/N
        rec_rate = gamma*I
        
        #By the merging&splitting property, we can combine the two random processes into one process
        comb_rate=tran_rate+rec_rate
        
        #first_event is the time until either one of the two events happens
        first_event = rand_exp(comb_rate)
        
        #We then need to determine if the first event that happened was a new infection or a recovery
        #The probability that it was either of the two events is the rate of the event/combined rate:s 
        
        prob_infection = tran_rate/comb_rate
        prob_recovery = rec_rate/comb_rate
        
        #We then need to randomly determine for every first event, given above the probabilities, if it
        #was a new infection or a recovery:
        event = np.random.choice(['New infection','Recovery'],p=[prob_infection,prob_recovery])
        
        if event=='New infection':S -=1; I +=1
        elif event=='Recovery':I -=1; R+=1

        t+=first_event
        event_log[t]=[S,I,R]
        
    return event_log



"Q3d"
sim=sim_SIR(1000,10,2.2,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='Infections over time, beta=2.2, gamma=2',)
plt.xlabel('Time')
plt.ylabel('Number of people')
plt.show()


"Q3e"
"""
Defining a large outbreak as one that lasts for at least 15 people, the probability of a large outbreak lies at about 18%.
If there is no outbreak, the simulation just runs for a few time periods and then dies down.
"""
simulations=[]
runs=10000
threshold=15

#Running the simulation 10000 times and storing each trajectory in the simulations list
for i in range(0,runs):
    sim=sim_SIR(1000,1,2.2,2)
    simulations.append(sim)

outbreak_count=0
max_infected=0
for i in simulations: 
    df=pd.DataFrame.from_dict(i, orient='index')
    #Defining an outbreak as more than 15 people being infected with the disease over the entire course of the infection
    if df.iloc[-1,2]>threshold: outbreak_count+=1
    if df.iloc[-1,2]>max_infected: max_infected=df.iloc[-1,2]
outbreak_probability=outbreak_count/runs
print("Probability that a large outbreak occurs =",outbreak_probability)
print("Highest number of infections over course of the outbreak:",max_infected)


"Q3f"
"For R0 = 1, i.e beta=gamma:"
sim=sim_SIR(1000,10,2,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='For R0 = 1, i.e beta=gamma:',)
plt.xlabel('Time periods')
plt.ylabel('Number of people')
plt.show()

"For R0 = 0.75, i.e beta=1.5, gamma=2"
sim=sim_SIR(1000,10,1.5,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='For R0 = 0.75, i.e beta=1.5, gamma=2',)
plt.xlabel('Time periods')
plt.ylabel('Number of people')
plt.show()


"For R0 = 1.25, i.e beta=2.5, gamma=2:"
sim=sim_SIR(1000,10,2.5,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='For R0 = 1.25, i.e beta=2.5, gamma=2:',)
plt.xlabel('Time periods')
plt.ylabel('Number of people')
plt.show()

"For R0 = 1.5, i.e beta=3, gamma=2:"
sim=sim_SIR(1000,10,3,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='For R0 = 1.5, i.e beta=3, gamma=2:',)
plt.xlabel('Time periods')
plt.ylabel('Number of people')
plt.show()

"For R0 = 2, i.e beta=4, gamma=2:"
sim=sim_SIR(1000,10,4,2)
df=pd.DataFrame.from_dict(sim, orient='index')
df.columns=['Susceptible','Infectious','Recovered']
df.plot(title='For R0 = 2, i.e beta=4, gamma=2:',)
plt.xlabel('Time periods')
plt.ylabel('Number of people')
plt.show()







"""
This part implements a hidden markov model to simulate the evolution process.
"""
emission_probabilities ={'H':{'B':0.3,'I':0.6,'N':0.1},
                        'S':{'B':0.55,'I':0.15,'N':0.3},
                        'T':{'B':0.1,'I':0.2,'N':0.7}}
print(pd.DataFrame.from_dict(emission_probabilities))

import numpy as np

def stateSim(length):
    states=['H','S','T']
    state=np.random.choice(states) #At the start of a sequence, any structure is equally likely.
    symb_seq=[]
    state_seq=[]
    
    #Function that randomly decides on the next emission, given the current state
    def new_em(state):
        emission=['B','I','N']
        emit=""
        if state=='H':
            emit=np.random.choice(emission, p=[0.3, 0.6, 0.1])   
        elif state=='S':
            emit=np.random.choice(emission, p=[0.55,0.15,0.3])
        elif state=='T':
            emit=np.random.choice(emission, p=[0.1,0.2,0.7])
        return emit
    
    #Function that randomly decides on the next state, given the current state
    def next_state(state):
        nextS=""
        if state=='H':
            nextS=np.random.choice(states, p=[14/15, 0.3/15, 0.7/15])   
        elif state=='S':
            nextS=np.random.choice(states, p=[0.4/8,7/8,0.6/8])
        elif state=='T':
            nextS=np.random.choice(states, p=[0.5/6,0.5/6,5/6])
        return nextS
    
    #While the generated sequence hasn't reached the desired length yet, keep going
    while len(symb_seq) < length:
        symb_seq.append(new_em(state))
        state_seq.append(state)
        state=next_state(state)
        
    
    return symb_seq,state_seq

symbols,states=stateSim(length = 150)
symbols300,states300=stateSim(length = 300)
symbols500,states500=stateSim(length = 500)
    
print('Symbols: ',''.join(symbols))
print('States: ',''.join(states))

np.random.seed(90)
class HMM:
    def __init__(self):
        #Possible states
        self.states=['H','S','T']
        #Any of the three secondary structures is equally likely to be the first in a sequence, hence p_pi0|start=1/3
        self.p_pi0 = 1/len(self.states)
        #Possible emissions
        self.emissions=['B','I','N']
        
        #Dictionary of the conditional probabilities of the emission of particular types of residues given the current secondary structure
        self.emission_probs ={'H':{'B':0.3,'I':0.6,'N':0.1},
                              'S':{'B':0.55,'I':0.15,'N':0.3},
                              'T':{'B':0.1,'I':0.2,'N':0.7}}
        
        #Dictionary of the conditional probabilities on the next state, given the current state
        self.state_probs = {'H':{'H':14/15,'S':0.3/15,'T':0.7/15},
                            'S':{'H':0.4/8,'S':7/8,'T':0.6/8},
                            'T':{'H':0.5/6,'S':0.5/6,'T':5/6}}
    

    def joint_probability(self,pi,x):
        
        #Initialise the first step
        joint_prob=self.p_pi0*self.emission_probs[pi[0]][x[0]]
        
        #Multiplies the remaining joint probabilities
        for i in range(1,len(x)):
            emission=x[i]
            current_state=pi[i]
            previous_state=pi[i-1]

            #Conditional probability of the current emission given the current state
            cond_prob=self.emission_probs[current_state][emission]
            #Conditional probability of going into the current state given the previous state
            state_pr=self.state_probs[previous_state][current_state]

            joint_prob *= (cond_prob*state_pr)

        return np.log(joint_prob)
    
    def forward(self,x):
        
        #The initial likelihoods of being in any of the three states and that this state
        #would have produced the observed symbol
        a={'T': [self.p_pi0*self.emission_probs['T'][x[0]]],
           'S': [self.p_pi0*self.emission_probs['S'][x[0]]],
           'H': [self.p_pi0*self.emission_probs['H'][x[0]]]}
        
        #Iterates through all the emitted symbols
        for i in range(1,len(x)):
            #Current likelihood depends on the product of all the prior likelihoods of all the states * the probability of
            #having come to the current state from these past states
            for curr_state in self.states:
                next_a=0
                for prev_state in self.states:
                    next_a+=a[prev_state][i-1]*self.state_probs[prev_state][curr_state]*self.emission_probs[curr_state][x[i]]
                
                a[curr_state].append(next_a)
                
        #Returns the sum of all three strands
        return np.log(a['T'][-1]+a['S'][-1]+a['H'][-1])   
        
    
h1 = HMM()


#Testing various simulated sequences with different lengths to find if relationship between joint probability and forward probability holds in general
print("Joint log probabilites P(pi,x):")
print("Joint prob test: ",h1.joint_probability(['S','S','H','H','H','T','T','S','S','S','H','H','H','H','H','H','S','S','S','S','S','S'],['B','I','N','B','N','I','N','B','N','I','N','B','I','N','B','I','I','N','B','B','N','B']))
print("Joint prob q1b seqs (L=150): ",h1.joint_probability(states,symbols))
print("Joint prob L = 300: ",h1.joint_probability(states300,symbols300))
print("Joint prob L = 500: ",h1.joint_probability(states500,symbols500))

print('\n')

print("Forward log probabilites P(x):")
print("forward test seq: ",h1.forward(['B','I','N','B','N','I','N','B','N','I','N','B','I','N','B','I','I','N','B','B','N','B']))
print("forward q1b seq (L=150): ",h1.forward(symbols))
print("Joint prob L = 300: ",h1.forward(symbols300))
print("Joint prob L = 500: ",h1.forward(symbols500))
    
"""
tree69.py
A tree utility library for COMPSCI 369.
"""

# The MIT License (MIT)
#
# Copyright (c) 2016 Arman Bilge and Stuart Bradley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def compute_upgma_tree(matrix):

    import itertools as it

    n = len(matrix)
    nodes = [Node(str(i + 1)) for i in range(n)]
    for node in nodes:
        node.set_height(0)
    matrix = {nodes[i]: {nodes[j]: matrix[i][j] for j in range(n)} for i in range(n)}
    while len(matrix) > 1:
        a, b = min(it.combinations(matrix.keys(), 2), key=lambda xy: matrix[xy[0]][xy[1]])
        u = Node()
        u.add_child(a)
        u.add_child(b)
        u.set_height(matrix[a][b] / 2)
        uc = {c: (a.get_leaf_count() * matrix[a][c] + b.get_leaf_count() * matrix[b][c]) / (a.get_leaf_count() + b.get_leaf_count()) for c in matrix.keys() - set((a, b))}
        del matrix[a]
        del matrix[b]
        for k, v in matrix.items():
            del v[a]
            del v[b]
            v[u] = uc[k]
        matrix[u] = uc
    return Tree(u)

def plot_tree(tree):

    import itertools as it
    import numpy as np
    from matplotlib import pyplot as plt

    def compute_node_xy(node, counter=it.count()):
        node.x = node.get_height()
        if node.is_leaf():
            node.y = next(counter)
        else:
            children = node.get_children()
            for child in children:
                compute_node_xy(child, counter)
            node.y = np.mean([c.y for c in children])

    def plot_node(node):
        if node.is_leaf():
            plt.text(node.x, node.y, ' ' + node.get_label(), {'ha':'left', 'va':'center'})
        else:
            children = node.get_children()
            plt.plot([node.x] * 2, [min(c.y for c in children), max(c.y for c in children)], 'k')
            for child in children:
                plt.plot([node.x, child.x], [child.y] * 2, 'k')
                plot_node(child)

    root = tree.get_root()
    compute_node_xy(root)
    plt.plot([root.x, root.x + root.x/16], [root.y] * 2, 'k')
    plot_node(root)
    lc = tree.get_leaf_count()
    plt.ylim(- lc / 16, 17/16 * lc - 1)
    axes = plt.gca()
    axes.invert_xaxis()
    axes.yaxis.set_visible(False)
    axes.set_frame_on(False)
    axes.grid()

"""
Python Tree Class
Stuart Bradley - 5931269
23-05-2014
"""
class Tree:

    def __init__(self, root=None):
        self.root = root

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def get_leaves(self):
        return self.root.get_leaves()

    def get_leaf_count(self):
        return self.root.get_leaf_count()

    def get_newick(self):
        return self.root.get_newick() + ";"

    def __str__(self):
        return self.get_newick()

"""
Python Node Class
Stuart Bradley - 5931269
23-05-2014
"""
class Node:
    def __init__(self, label=None):
        self.parent = None
        self.children = []
        self.height = -1.0
        self.label = label
        self.sequence = None

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)
        child.set_parent(self)

    def remove_child(self, child):
        self.children.remove(child)

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return not self.children

    def get_sequence(self):
        return self.sequence

    def set_sequence(self, sequence):
        self.sequence = sequence

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def get_leaves(self):
        leaf_list = []

        if (self.is_leaf()):
            leaf_list.append(self)
        else:
            for child in self.children:
                leaf_list.extend(child.get_leaves())

        return leaf_list

    def get_leaf_count(self):
        if self.is_leaf():
            return 1
        else:
            return sum(map(Node.get_leaf_count, self.children))

    def get_newick(self):
        sb = ""

        if (not self.is_leaf()):
            sb += "("
            for i in range(0, len(self.children)):
                if (i>0):
                    sb += ","
                sb += self.children[i].get_newick()
            sb += ")"

        if (self.label != None):
            sb += self.label

        branch_length = -1.0
        if (not self.is_root()):
            branch_length = self.parent.height - self.height
        else:
            branch_length = 0.0

        sb += ":" + str(branch_length)

        return sb

import matplotlib.pyplot as plt
np.random.seed(90)

def treeSim(leaf_number,branching_parameter):
    k=leaf_number;t=0
    unassigned_nodes=[]
    tr1=Tree()
    
    #Initiates nodes
    for i in range(leaf_number):
        node=Node()
        node.set_height(t)
        node.set_label(str(i+1))
        unassigned_nodes.append(node)
    
    while k>1:
        #increment time
        scale=1/(k*branching_parameter)
        time_step = np.random.exponential(scale)
        t += time_step
        
        #Create new node
        new_node=Node()
        new_node.set_height(t)
        
        #Remove 1st node
        child_nd = np.random.choice(unassigned_nodes)
        child_nd.set_parent(new_node)
        new_node.add_child(child_nd)
        unassigned_nodes.remove(child_nd)
    
        
        #Remove 2nd node
        child_nd = np.random.choice(unassigned_nodes)
        child_nd.set_parent(new_node)
        new_node.add_child(child_nd)
        unassigned_nodes.remove(child_nd)
            
        unassigned_nodes.append(new_node)
        k-=1
    
    tr1.set_root(unassigned_nodes[0])
    return tr1

simulations=[]
for i in range(1000):
      simulations.append(treeSim(10,0.5).get_root().get_height())
print("Mean tree height: ",np.mean(simulations))

def jukes_kantor_model(tree,sequence_length,mutation_rate):
    
    bases=['A','C','G','T'] 
    seq_matrix=dict()
    
    def alphabet_mutate(X,t,mu):
        """
        Same as the original mutate function but mutates directly to alphabetical base character instead of int
        """
        L= len(X)
        mutatedSeq = X.copy()

        numMutation = np.random.poisson(L*mu*t)
        for i in range(numMutation):
            site = np.random.randint(0,L)
            mutatedSeq[site] =  np.random.choice(bases)

        return mutatedSeq
    
    
    def set_mutated_sequence(node):
        """
        A function that takes in a node, takes its sequence, mutates it twice and 
        then sets these two mutated sequences to its children nodes
        """
    
        if node.is_leaf(): return   #if node is a leaf it doesn't have any children
        
        children=node.get_children()
        seq=node.get_sequence()
        
        #Mutates sequence for the first child
        current_branch_length = abs(node.get_height() - children[0].get_height())
        
        first_mut=alphabet_mutate(np.array(seq),current_branch_length,mutation_rate)
        children[0].set_sequence(first_mut)
        #If child a leaf node, add to seq matrix
        if children[0].get_label(): seq_matrix[children[0].get_label()]=first_mut
        
        #Mutates sequence for the second child
        current_branch_length = abs(node.get_height() - children[1].get_height()) 
        second_mut=alphabet_mutate(np.array(seq),current_branch_length,mutation_rate)
        children[1].set_sequence(second_mut)
        #If child a leaf node, add to seq matrix
        if children[1].get_label():seq_matrix[children[1].get_label()]=second_mut
        
        return children
    
       
    #Generates random sequence of length L
    seq = np.random.choice(bases,sequence_length)   
    node=tree.get_root()
    
    #Sets this sequence at the root of the passed in tree
    node.set_sequence(seq)
    seq_matrix['.Root']=seq
    
   
    #left_overs stores nodes that still need to have sequences added to them
    left_overs=[node]                       
    
    while left_overs:
        #Takes the first node out of left_overs list
        node=left_overs.pop(0)
        children=set_mutated_sequence(node)
        
        #Checks if the node has children, if so adds them to left_overs list
        #Maintains the tree structure as children always get added to the end of the list
        if children: left_overs.extend(children)
    

    return tree,seq_matrix


    
t1=treeSim(10,0.5)
plot_tree(t1)
jktree,seq_matrix=jukes_kantor_model(tree=t1,sequence_length=20,mutation_rate=0.5)

for key in sorted(seq_matrix):
    print('Node: ',key,''.join(seq_matrix[key]))
    
import numpy as np

def distance_matrix(set):
    
    def distance(x,y):
        #Find Dxy = the number of differing sites between x and y    
        differing_sites_xy=0
        for i in range(0,len(x)): 
            if x[i]!=y[i]: differing_sites_xy+=1

        f_xy=min(differing_sites_xy/len(x),0.75-1/len(x))

        d_xy=-(3/4)*np.log(1-(4/3)*f_xy)
        return d_xy
    
    
    dist_matrix=np.zeros((len(set),len(set)))
    for i in range(len(set)):
        for j in range(len(set)):
            dist_matrix[i,j] = np.round(abs(distance(set[i],set[j])),2)
    return dist_matrix


jktree,seq_matrix=jukes_kantor_model(tree=treeSim(10,0.5),sequence_length=20,mutation_rate=0.5)

leaves= jktree.get_leaves()

#Sort leaves by node label
s_leaves = sorted(leaves,key=lambda node: int(node.get_label())) 



tree_leaf_seqs=[]
for i in s_leaves:
    tree_leaf_seqs.append(i.get_sequence())
    print('Node ',i.get_label(),' ',''.join(i.get_sequence()))
matrix = distance_matrix(tree_leaf_seqs)
print('\n')
print(matrix)

t_org2=treeSim(10,0.5)

t2,dic1=jukes_kantor_model(tree = t_org2,sequence_length = 20,mutation_rate = 0.1)
leaves2 = t2.get_leaves()

#Sort leaves by key value
s_leaves = sorted(leaves2,key=lambda node: int(node.label) )

tree_leaf_seqs=[]
print('Generated sequences with length L = 20')
for i in s_leaves:
    tree_leaf_seqs.append(i.sequence)
    print('Node ',i.label,' ',''.join(i.sequence))
    
matrix2 = distance_matrix(tree_leaf_seqs)
print("\nDistance matrix with sequence length=",len(tree_leaf_seqs[0]),": \n",matrix2)
print('\n')

t2,dic1=jukes_kantor_model(tree = t_org2, sequence_length = 50, mutation_rate = 0.1)
leaves2 = t2.get_leaves()

#Sort leaves by key value
s_leaves = sorted(leaves2,key=lambda node: int(node.label))

tree_leaf_seqs=[]
print('Generated sequences with length L = 50')
for i in s_leaves:
    tree_leaf_seqs.append(i.sequence)
    print('Node ',i.label,' ',''.join(i.sequence))
    
matrix3 = distance_matrix(tree_leaf_seqs)
print("\nDistance matrix with sequence length=",len(tree_leaf_seqs[0]),": \n",matrix3)
print('\n')

t2,dic1=jukes_kantor_model(tree = t_org2, sequence_length = 200, mutation_rate = 0.1)
leaves2 = t2.get_leaves()

#Sort leaves by key value
s_leaves = sorted(leaves2, key = lambda node: int(node.label) )

tree_leaf_seqs=[]
print('Generated sequences with length L = 200')
for i in s_leaves:
    tree_leaf_seqs.append(i.sequence)
    print('\n''Node ',i.label,' ',''.join(i.sequence) )
    
matrix4 = distance_matrix(tree_leaf_seqs)
print("\nDistance matrix with sequence length=",len(tree_leaf_seqs[0]),": \n",matrix4)


#Compute upgma trees
tree20= compute_upgma_tree(matrix2)
tree50= compute_upgma_tree(matrix3)
tree200= compute_upgma_tree(matrix4)

print('First tree with sequence length L=20')
plot_tree(tree20)
print("\n")

print('Second tree with sequence length L=50')
plot_tree(tree50)
print("\n")

print('Third tree with sequence length L=200')
plot_tree(tree200)
print("\n")
