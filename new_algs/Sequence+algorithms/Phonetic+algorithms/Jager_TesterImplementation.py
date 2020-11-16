# -*- coding: utf-8 -*-

'''
Created on 22-nov-2018

Kilani Marwan

Python 3.7
'''

from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import ast

import io

f =  open("Jager-PMI.txt", "r")
str = f.read()

matrix = ast.literal_eval(str)

#read file

#set location of the file to analyse (the files are provided in the folder: TestsArticle/Datasets/Inputs )

locationDataset = 'path/to/data/dataset/1_corpus_jager_input_no_alignments.txt'

#set location of output file (the files are provided in the folder: TestsArticle/Datasets/Results )
locationResults = 'path/to/data/dataset/1_jager_results.txt'

#name = '/Users/iome/Desktop/Articoli : ricerche varie 30-1-2014-/nuovo algoritmo comparazione linguistica/risposta reviewers/databases/1_corpus_jager_test_tot.txt'

lines = tuple(io.open(locationDataset, 'r', encoding='utf-8'))



# open/create, write, and close the file with the results
output = open(locationResults, 'w', encoding='utf-8')

for i in range(1, len(lines), 3):
    word1 = lines[i]
    word2 = lines[i+1]
    
    word1.replace('\n', "")
    word2.replace('\n', "")

    
    word1 = word1.strip()
    word2 = word2.strip()


    alignments = pairwise2.align.globalds(word1, word2,  matrix, -2.4930, -1.7057)

    print(lines[i-1])
    print(format_alignment(*alignments[0]))


    output.write(lines[i-1] + '\n')
    output.write(format_alignment(*alignments[0]) + '\n')



output.close()