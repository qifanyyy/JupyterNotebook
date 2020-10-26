#!/usr/bin/env python3

'''
Eric Vogel
Principle of Bioinformatics
Module 2 Assignment

This program is a implementation of the Smith-Waterman algorithm 
to find best local alignment between two sequences
'''

match = 5
mismatch = -4
gap      = -4
seq_1 = "GCTGGAAGGCAT"
seq_2 = "GCAGAGCACG"
 
def main():
    
    # Scoring grid contains sequences and has a 0th row and column
    rows = len(seq_1) + 1
    cols = len(seq_2) + 1

    #Create scoring grid and locate sink vertex and its score
    score_grid, sink_vertex, max_vertex_score = create_score_grid(rows, cols)

    # Find best local alignments by traceing back through the scoring grid
    alignment_1, alignment_2 = alignment(score_grid, sink_vertex)

    print("\nScore = %d" % (max_vertex_score))
    print("Best Local Alignment:")
    print("Q: %s" % (alignment_1))
    print("P: %s" % (alignment_2))
    print("")

# Check if the two vertices are a match or mismatch
def check_match(vertex_1, vertex_2):
    if vertex_1 == vertex_2:
        return match
    else:
        return mismatch
    
# Create, populate, and find sink vertex of scoring grid
def create_score_grid(rows, cols):

    # Initalize all grid position with zeros
    score_grid = [[0 for col in range(cols)] for row in range(rows)]

    # Track max vertex and its score
    max_vertex = (0, 0)
    max_vertex_score = 0

    # Populate scoring grid with values
    for i in range(1, rows):
        for j in range(1, cols):

            # Calculate values based on diagonal, vertical, and horizontal vertices
            diagonal = score_grid[i - 1][j - 1] + check_match(seq_1[i - 1], seq_2[j - 1])
            vertical   = score_grid[i - 1][j] + gap
            horizontal = score_grid[i][j - 1] + gap

            # Vertex score equals the max of these values
            vertex_score = max(0, diagonal, vertical, horizontal)

            # Track max vertex and its score
            if vertex_score > max_vertex_score:
                max_vertex_score = vertex_score
                max_vertex = (i, j)

            # Insert value in scoring grid
            score_grid[i][j] = vertex_score

    return score_grid, max_vertex, max_vertex_score

# Trace back through scoring grid from sink vertex to find best local alignment
def alignment(score_grid, sink_vertex):

    # Track alignments
    alignment_1 = ''
    alignment_2 = ''

    # Start at sink vertex
    i,j = sink_vertex

    # Trace back through scoring grid
    while i > 0 and j > 0:

        # Find score of vertex and its diagonal, vertical, and horizontal positions
        vertex = score_grid[i][j]
        diagonal = score_grid[i - 1][j - 1]
        vertical = score_grid[i][j - 1]
        horizontal = score_grid[i - 1][j]

        # Create best local alignment
        if vertex == diagonal + check_match(seq_1[i - 1], seq_2[j - 1]):
            alignment_1 += seq_1[i - 1]
            alignment_2 += seq_2[j - 1]
            i -= 1
            j -= 1
        elif vertex == vertical + gap:
            alignment_1 += '-'
            alignment_2 += seq_2[j - 1]
            j -= 1
        elif vertex == horizontal + gap:
            alignment_1 += seq_1[i - 1]
            alignment_2 += '-'
            i -= 1
        
    return alignment_1[::-1], alignment_2[::-1]

if __name__ == '__main__':
    main()