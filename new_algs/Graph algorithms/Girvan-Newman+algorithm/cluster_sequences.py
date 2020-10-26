#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 11:52:20 2018

@author: Landen Gozashti under the guidance of Russel Corbett-Detig
"""


"""

This script identifies introner elements in genomes and only requires an annotation file and assembly fasta file.

This program is written in an object oriented fashion.

"""
from pathlib import Path
from shutil import which
import matplotlib
matplotlib.use('Agg')
from sequenceAnalyzer import FastAreader
import os
from Bio.Seq import Seq
#from IEExtraction import DataDic
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import community
import sys
import argparse 


class Graph():
    """
    Employs a graph theory algorithm to cluster sequences. 
    Returns communities formed from sequence clusters.
    
    """
    def __init__(self, minimapOut, algorithm, minAln, lengthDic, minFam):
        self.minimapOut = minimapOut
        self.minAln = float(minAln)
        self.lengthDic = lengthDic
        self.algorithm = algorithm
        self.minFam = int(minFam)

    def graph(self):
        IEfamilies = []
        IEs = []
        strandDic = {}
        backupStrandDic = {}
        try:
            try:
                os.system('rm -r final_allvall.tsv')
                with open (self.minimapOut,'r') as file1:
                    if self.algorithm == 'BLAST':
                        for line in file1:

                            line = line.rstrip()
                            sp = line.split('\t')
                            length = self.lengthDic[sp[0]]
                            #print(sp[0],length)
                            if length > 0:
                                if float(int(sp[3])/length) > float(self.minAln):
                                    strandDic[sp[0]] = sp[-1]
                                    backupStrandDic[sp[1]] = sp[-1] 
                                    with open('final_allvall.tsv', 'a') as file2:
                                        file2.write('{0}\n'.format(line))

                    elif self.algorithm == 'minimap2':
                        for line in file1:

                            line = line.rstrip()
                            sp = line.split('\t')
                            length = self.lengthDic[sp[0]]
                            if length > 0:
                                if float(int(sp[11])/length) > float(self.minAln):
                                    strandDic[sp[0]] = sp[6]
       	       	       	       	    backupStrandDic[sp[7]] = sp[-1]
 
                                    with open('final_allvall.tsv', 'a') as file2:
                                        file2.write('{0}\n'.format(line))
                
                data = pd.read_csv('final_allvall.tsv', sep='\t', header=None)
                df = nx.from_pandas_edgelist(data, source=0, target=1, edge_attr=True)
                
                
                communities_generator = community.girvan_newman(df)
                top_level_communities = next(communities_generator)
                IEfam = sorted(map(sorted, top_level_communities))
                for fam in IEfam:
                    if len(fam) > self.minFam:
                        IEfamilies.append(fam)
                    else:
                        IEs = IEs + fam
                for fam in IEs:
                    df.remove_node(fam)
            except EmptyDataError:
                print('EmptyDataError')
                pass
        except FileNotFoundError:
       	    print('NameError')

            IEfamilies = 'None'

        return IEfamilies,strandDic,backupStrandDic


                
            
                

def main():
    parser = argparse.ArgumentParser(description='Employs a Girvin-Newman algorithm to cluster DNA sequences into families based on similarity') 
    parser.add_argument('-fasta', nargs='?', required=True,
                        help='Path to fasta file containing sequences') 
    parser.add_argument('-algorithm', nargs='?', required=True,
                         help='Options are BLAST and minimap2')
    parser.add_argument('-min_aln_proportion', nargs='?', required=False, default=.8,
                    help='Minimum alignment length relative to query length  (Default = .8)')
    parser.add_argument('-min_cluster_size', nargs='?', required=False, default=2,
                    help='Minimum number of sequences required in a particular cluster  (Default = 2)')
    parser.add_argument('-min_percentID', nargs='?', required=False, default=80,
                    help='Minimum percent identity for all v all BLAST   (Default = 80)') 
    args = vars(parser.parse_args())

    print('Reading sequences')
    lengthDic = {}
    seqDic = {}
    myReaderReads = FastAreader(args['fasta'])
    for header, seq in myReaderReads.readFasta():
        seqDic[header] = seq
        lengthDic[header] = len(seq)
     
    if args['algorithm'] == 'minimap2':
        if which('minimap2') is not None:
                  
            print('Performing all vs all alignment with minimap2')
            os.system("minimap2 -X -N 1000 {0} {0} > overlaps.paf".format(args['fasta'])) #| awk '$10>50'
            os.system("awk '$1 != $6' overlaps.paf > all-vs-all_deduped.tsv")

        else:
            print("minimap2 doesn't seem to be in your PATH")
            sys.exit()


    elif args['algorithm'] == 'BLAST':
        if which('blastn') is not None:

            
            print("Performing all-v-all BLAST")
            min = args['min_percentID']       
            os.system("makeblastdb -dbtype nucl -in {0} -title cluster_input -out seqDB".format(args['fasta']))
            os.system('blastn -db seqDB -query {0} -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sstrand" -perc_identity {1} -out all-vs-all.tsv'.format(args['fasta'],int(min)))
            os.system("awk '$1 != $2' all-vs-all.tsv > all-vs-all_deduped.tsv")
        else:
            print("BLAST doesn't seem to be in your PATH")
            sys.exit()



    print('Clustering sequences...')
    Data = Graph('all-vs-all_deduped.tsv',args['algorithm'],args['min_aln_proportion'],lengthDic,args['min_cluster_size'])
         
    IEfamilies,strandDic,backup = Data.graph()
    count = 1

    with open('clusters.fa', 'w') as file:
            
        for family in IEfamilies:
            if len(family) > int(args['min_cluster_size']):
                for header in family:
                    try:
                        #print(header,strandDic[header])
                        if strandDic[header] == '-' or strandDic[header] == 'minus': #If aln was found on the noncoding strand
                            sequence = Seq(seqDic[header])
                            revcomp = sequence.reverse_complement() #Return reverse complement so that all introns are in the same orientation
        
                            file.write('>{1}_{0}\n'.format(header, count))
                            file.write('{0}\n'.format(revcomp))
                        else:                                
                            file.write('>{1}_{0}\n'.format(header, count))
                            file.write('{0}\n'.format(seqDic[header]))
                    except KeyError:
                        if backup[header] == '-' or backup[header] == 'minus': #If aln was found on the noncoding strand
                            sequence = Seq(seqDic[header])
                            revcomp = sequence.reverse_complement() #Return reverse complement so that all introns are in the same orientation

                            file.write('>{1}_{0}\n'.format(header, count))
                            file.write('{0}\n'.format(revcomp))
                        else:
                            file.write('>{1}_{0}\n'.format(header, count))
                            file.write('{0}\n'.format(seqDic[header]))
                count += 1
                        
    
    
if __name__ == "__main__":
    main() 
    
    
    
    
