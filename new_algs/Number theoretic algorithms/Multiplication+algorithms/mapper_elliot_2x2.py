#!/usr/bin/python

# Here we assume that we are working with 2x2 Matrices to try and work out the block multiplication intuition.

import sys
import time

start_time = time.time()

for line in sys.stdin:
    line = line.strip()
    element = line.split(",")
    
    provenance = element[0]
    i = str(element[1])
    j = str(element[2])
    value = float(element[3])
        
    if provenance == 'A':
        if i == 0:
            if j == 0:
                key = 'A00'
                print '%s\t%s' % (key, value)
            else:
                key = 'A01'
                print '%s\t%s' % (key, value)
    
        else:
            if j == 0:
                key = 'A10'
                print '%s\t%s' % (key, value)
            else:
                key = 'A11'
                print '%s\t%s' % (key, value)
    else:
        if i == 0:
            if j == 0:
                key = 'B00'
                print '%s\t%s' % (key, value)
            else:
                key = 'B01'
                print '%s\t%s' % (key, value)
        
        else:
            if j == 0:
                key = 'B10'
                print '%s\t%s' % (key, value)
            else:
                key = 'B11'
                print '%s\t%s' % (key, value)

end_time = time.time()
