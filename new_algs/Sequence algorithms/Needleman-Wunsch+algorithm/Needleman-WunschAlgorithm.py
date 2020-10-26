##############################################
# Antonio Rios
# February 18, 2016
# CS599 Large Data Structures
# Homework 3: Needleman-Wunsch Algorithm
#############################################
from pygments.lexers.algebra import GAPLexer



def needleman_wunsch(gseq1, gseq2, match, mismatch, gap, similarity_score_matrix):
    """
        The needleman_wunsch( ) function takes in two DNA sequences
        as string type and a genomic similarity scoring matrix and gap penalty as an input.
        
        Parameters: 
        gseq1 - 
        gseq2
        match
        mismatch
        gap
        similarity_score_matrix
        
        Returns:
        score for best alignment
        alignment in text format 
        
        GATTA
        | x||
        G_CTA

    """    
    if(not (type(gseq1)== str and type(gseq2) == str)):
        print("DNA sequences pass to this function must be of string type")
    
    
    # set the variables that we are going to use
    score_match = match
    score_mistach = mismatch
    score_gap = gap
    sscm = similarity_score_matrix
    
    
    alignmentA = gseq1
    alignmentB = gseq2
    i = len(gseq1)
    j = len(gseq2)
    
    # declare the 2d matrix to represent the similarity matrix
    # [r],[c]
    Fmatrix = [[],[]]
    
    while(i > 0 or j > 0):
        
        if(i > 0 and j > 0 and Fmatrix[i][j] == Fmatrix[i-1][j-1] + gs
    
    
        
    match = 1
    mistmatch = -1
    gap = -1
    
    #create the 2d grid
    grid = []
    grid.append([])
    grid.append([])
    
    
    
    
    
    
if __name__ == '__main__':
    
    print("Sequences            Best Alignments")
    print("----------------------------------------------------")
    print(seq1)
    print seq2)
    