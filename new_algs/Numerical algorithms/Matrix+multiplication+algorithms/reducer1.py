#!/usr/bin/python

import sys

#initialize previous key, index, and value:
previous_key = None
prev_ind = None
prev_v = None

#initialize list:
calc_list = []

for line in sys.stdin:
    #strip and get the values in each line (i.e. the key, the index and the value)
    line = line.strip()
    ind, key, v = line.split("\t")
    #error-prone type conversion to integer:
    try:
        ind = int(ind)
        v = int(v)
    except ValueError:
        continue
    #if the key changes and we are not at the start of the algorithm, calculate result fr specific key
    if (key != previous_key) & (previous_key!=None):
        i=0
        output = 0
        while i<len(calc_list)-1:
            output = output + calc_list[i]*calc_list[i+1]
            i=i+2
        #check if result is 0 (not output 0, as we want sparse result)
        if (output != 0):
            print "%s\t%s"%(previous_key,output)
        #empty list, as key is over now:
        calc_list = []
    
    #check if 2 consequtive index's and keys are equal -> append those 2 values
    if (previous_key == key) & (prev_ind == ind):
        calc_list.append(prev_v)
        calc_list.append(v)
    #update previous key, value and previous index
    previous_key = key
    prev_v = v
    prev_ind = ind

#the last list needs to be treated as well:   
i=0
output = 0
while i<len(calc_list)-1:
    output = output + calc_list[i]*calc_list[i+1]
    i=i+2
if (output != 0):
    print "%s\t%s"%(previous_key,output)

##!/usr/bin/python
#
#import sys
#
##initialize previous key, index, and value:
#previous_key = None
#prev_ind = None
#prev_v = None
#
##initialize list:
#calc_list = []
#
#for line in sys.stdin:
#    #strip and get the values in each line (i.e. the key, the index and the value)
#    line = line.strip()
#    key, ind, v = line.split("\t")
#    #error-prone type conversion to integer:
#    try:
#        ind = int(ind)
#        v = int(v)
#    except ValueError:
#        continue
#    #if the key changes and we are not at the start of the algorithm, calculate result fr specific key
#    if (key != previous_key) & (previous_key!=None):
#        i=0
#        output = 0
#        while i<len(calc_list)-1:
#            output = output + calc_list[i]*calc_list[i+1]
#            i=i+2
#        #check if result is 0 (not output 0, as we want sparse result)
#        if (output != 0):
#            print "%s\t%s"%(previous_key,output)
#        #empty list, as key is over now:
#        calc_list = []
#    
#    #check if 2 consequtive index's and keys are equal -> append those 2 values
#    if (previous_key == key) & (prev_ind == ind):
#        calc_list.append(prev_v)
#        calc_list.append(v)
#    #update previous key, value and previous index
#    previous_key = key
#    prev_v = v
#    prev_ind = ind
#
##the last list needs to be treated as well:
#i=0
#output = 0
#while i<len(calc_list)-1:
#    output = output + calc_list[i]*calc_list[i+1]
#    i=i+2
#if (output != 0):
#    print "%s\t%s"%(previous_key,output)
#
#
#
