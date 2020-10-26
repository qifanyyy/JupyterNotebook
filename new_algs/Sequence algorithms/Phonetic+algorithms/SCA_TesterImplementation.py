# -*- coding: utf-8 -*- 

'''
Created on 22-nov-2018

@author: Kilani Marwan

Python 3.7
'''

from __future__ import print_function
from pprint import pprint
DEFAULT_ENCODING = 'UTF-8' 

from lingpy import *

import io

import locale
language, output_encoding = locale.getdefaultlocale()

#read file

#set location of the file to analyse (the files are provided in the folder: TestsArticle/Datasets/Inputs )

locationDataset = 'path/to/data/dataset/1_corpus_sca_input_no_alignments.txt'


#set location of output file (the files are provided in the folder: TestsArticle/Datasets/Results )
locationResults = 'path/to/data/dataset/1_sca_results.txt'


#===============

#open/create, write, and close the file with the results
output = open(locationResults, 'w', encoding='utf-8')


lines = tuple(io.open(locationDataset, 'r', encoding='utf-8'))

print(lines[0])
print(lines[1])
print(lines[2])


for i in range(1, len(lines), 3):
    seqA = lines[i].encode("UTF8")
    seqB = lines[i+1].encode("UTF8")
    
    seqA = str(seqA, "utf-8")
    seqB = str(seqB, "utf-8")


    results_glob = Pairwise(str(seqA), str(seqB))
    
    print(lines[i-1])

    results_glob.align(mode="global", pprint=True)

    output.write(lines[i-1] + '\n')
    output.write(str(results_glob) + '\n')



output.close()




        
