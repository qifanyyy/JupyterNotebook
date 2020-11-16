import numpy as np
import time
import editdistance
import pandas as pd
from math import isnan




def match_score_df(alpha, beta, company_df, index_df, gap_penalty):
    c_a = company_df.loc[alpha, "sequence_text"]
    c_b = index_df.loc[beta, "sequence_text"]

    if c_a == '------' or c_b == '------':
        return gap_penalty
    else:
        # If GCV skips a row it returns nan in pandas which this catches
        # TODO: improve logic so that actual floats in company names (unlikely)
        # are handled
        if  isinstance(c_a, float):
            if isnan(c_a):
                return -1
        if isinstance(c_b, float):
            if isnan(c_b):
                return -1
        # Normalise distance so lies in [0, 1]
        distance = editdistance.eval(c_a, c_b) / max(len(c_a), len(c_b))
        # Distance is a cost so times -1
        return -1 * distance





def needleman_wunsch_df(seq1, seq2, company_df, index_df,  gap_penalty):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = np.zeros((m+1, n+1))
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score_df(seq1[j-1], seq2[i-1], company_df, index_df, gap_penalty)
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = []
    align2 = []
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score_df(seq1[j-1], seq2[i-1], company_df, index_df, gap_penalty):
            align1 += [seq1[j-1]]
            align2 += [seq2[i-1]]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += [seq1[j-1]]
            align2 += ['------']
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += ['------']
            align2 += [seq2[i-1]]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += [seq1[j-1]]
        align2 += ['------']
        j -= 1
    while i > 0:
        align1 += ['------']
        align2 += [seq2[i-1]]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    print("Scoring Matrix:")
    print(pd.DataFrame(score))

    align_df = pd.DataFrame()
    align_df["sequence_1"] = align1
    align_df["sequence_2"] = align2
    return(align_df)



def create_nw_df(df1, df2, col1, col2, gap_penalty = -1):
    # Creating indices in original DFs
    df1["sequence_1"] = np.arange(len(df1))
    df2["sequence_2"] = np.arange(len(df2))
    # Renaming columns for NW()
    df1 = df1.rename(columns = {col1 : "sequence_text"}, errors = "raise").reset_index(drop = True)
    df2 = df2.rename(columns = {col2 : "sequence_text"}, errors = "raise").reset_index(drop = True)
    # Running algorithm
    nw_output = needleman_wunsch_df(df1["sequence_1"], df2["sequence_2"], df1, df2, gap_penalty = gap_penalty)

    # Combining output
    joint_df = nw_output.merge(
        df1.drop(columns=['data_source_type'],
                 errors='ignore'), # since data source present in both dfs occasionally
        on = "sequence_1",
        how = "left"
    )
    joint_df = joint_df.merge(
        df2,
        on = "sequence_2",
        how = "left"
    )
    return joint_df

if __name__ == "__main__":
    pd.options.display.max_rows = 200

    wide_df = pd.read_csv("tmo.csv")
    index_df = pd.read_csv("company-index-names-initial-experiment-ed.csv")
    
    start = time.time()
    all_joint_df = create_nw_df(wide_df, index_df, "company name", "text")
    print(all_joint_df)

    end = time.time()
    print("Time Taken:", end - start)


    
    