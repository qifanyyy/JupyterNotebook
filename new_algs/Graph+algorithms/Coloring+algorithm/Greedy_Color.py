#!/usr/bin/python
import csv, os
import string
import random
string.ascii_lowercase

#point to a relative path
#os.chdir(os.path.relpath('Stims', start='.')+'//')

def searchList( object, myList ):
    for index in range(len(myList)):
        if object == myList[index]['STIMULUS NAME']:
            return index;

    return -1;

'''might need to put a full path before file name'''
files=csv.DictReader(open(os.getcwd()+'/Stims_Similarities.csv','r+'))
files=list(files)

for i in files:
    i['SIMILAR IN COLOR'] = i['SIMILAR IN COLOR'].replace(" ", "")
    i['SIMILAR IN COLOR'] = i['SIMILAR IN COLOR'].split(',')
    i['SIMILAR IN SHAPE'] = i['SIMILAR IN SHAPE'].replace(" ", "")
    i['SIMILAR IN SHAPE'] = i['SIMILAR IN SHAPE'].split(',')
    i['STIMULUS NAME'] = i['STIMULUS NAME'].replace(" ", "")
    i['SIMILAR IN COLOR'] = set(i['SIMILAR IN COLOR'])
    i['SIMILAR IN SHAPE'] = set(i['SIMILAR IN SHAPE'])
    
stims = [file['STIMULUS NAME'] for file in files] # format dictionary => all stim names in one list called [stims], shuffle
finalStims = [] # initialize list for finalStims

#keep adding items until you get a list of 4, if you have deleted all items from stim, reset
while(len(finalStims) != 4):
    #shuffle files and add item from the first index
    random.shuffle(stims)
    finalStims.append(stims[0])
    tempIndex = searchList(stims[0],files);

    if tempIndex == -1:
        finalStims = []
        stims = [file['STIMULUS NAME'] for file in files]
        continue

    #removes simlarities between the two and the item
    stims = set(stims) - files[tempIndex]['SIMILAR IN COLOR']
    stims = stims - files[tempIndex]['SIMILAR IN SHAPE']

    #print set(stims).symmetric_difference(files[tempIndex]['SIMILAR IN COLOR'])
    #print stims.symmetric_difference(files[tempIndex]['SIMILAR IN SHAPE'])

    if files[tempIndex]['STIMULUS NAME'] in stims:
        stims.remove(files[tempIndex]['STIMULUS NAME'])
    stims = list(stims) # turn it back into a list

    if len(stims) == 0:
        finalStims = []
        stims = [file['STIMULUS NAME'] for file in files]
        continue

print (finalStims)