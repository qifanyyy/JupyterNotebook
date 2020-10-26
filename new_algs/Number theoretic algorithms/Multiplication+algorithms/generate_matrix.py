#!/usr/bin/python

import sys
import random

MIN=-1000000.0
MAX= 1000000.0

def print_usage():
    print "Usage: %s nb_rows nb_cols"%sys.argv[0];

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(-1)
    nb_rows = int(sys.argv[1])
    nb_cols = int(sys.argv[2])

    matrix = []
    for r in range(0, nb_rows):
        line = []
        for c in range(0, nb_cols):
            line.append(repr(random.uniform(MIN, MAX)))
        line = ",".join(line)
        matrix.append(line)
    print ";".join(matrix)
