#!/usr/bin/python

import sys

# We assume we know the dimensions of the final matrix output (m row, n columns)
# Here we will set m and n for our matrix example where A is (2 x 3) and B is (3 x 2) so C is (2 x 2)
# Since python indexing starts at 0 it has column indexes 0 and 1 (same for rows)

# IMPORTANT : - If you are using our matrix generator please input the same m and n you used in that script!
#             - If you aren't don't mind that, just change the split to "," instead of "\t"!

m = 2
n = 2

for line in sys.stdin:
    
    # remove leading and trailing whitespace
    line = line.strip()
    
    # split the line corresponding to one element of either matrix
    element = line.split("\t")
    
    # Retrieve the 4 attributes of each line respectively
    provenance = element[0]
    row = int(element[1])
    col = int(element[2])
    value = float(element[3])
    
    
    # Matrix A
    ## If line corresponds to an element of matrix A, we will need to replicate each element of this matrix n times
    
    if provenance == "A":
        
        for k in range(0, n + 1): # We add 1 so Python will replicate n times
            
            print ('%s\t%s' % ((row, k),(provenance, col, value)))

# Matrix B
# If line corresponds to an element of matrix B, we will need to replicate each element of this matrix m times

    else:
    
        for i in range(0, m + 1): # We add 1 so Python will replicate m times
        
            print ('%s\t%s' % ((i, col),(provenance, row, value)))

# Printing last object!

#print '%s\t%s' % ((i, col),(provenance, row, value))

# Each element then goes through a sort&shuffle phase where key-value pairs are grouped by composite key (k1, k2)

#### NOTES : We could try two implementations :
####    - this one
####    - using a dictionnary where we append every element which should have the same composite key
####
#### Main difference is that dictionnaries may be faster but are memory bound, which implies it may crash if the
#### matrix is too big


