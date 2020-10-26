#!/usr/bin/python

import sys

previous_key = None
calc_list = []

for line in sys.stdin:
    #strip and get the values in each line (i.e. the key, the index and the value)
    line = line.strip()
    key, v = line.split("\t")
    
    #error-prone type conversion to integer:
    try:
        v = int(v)
    except ValueError:
        continue

    #if the key changes and we are not at the start of the algorithm, calculate result fr specific key
    if (key != previous_key) & (previous_key!=None):
        i=0
        output = 0
        for i in range(len(calc_list)):
            output = output + calc_list[i]
        #check if result is 0 (not output 0, as we want sparse result)
        if (output != 0):
            print "%s\t%s"%(previous_key,str(output))
        #empty list, as key is over now:
        calc_list = []

    #update values:
    previous_key = key
    calc_list.append(v)

i=0
output = 0
for i in range(len(calc_list)):
    output = output + calc_list[i]
#check if result is 0 (not output 0, as we want sparse result)
if (output != 0):
    print "%s\t%s"%(previous_key,str(output))
