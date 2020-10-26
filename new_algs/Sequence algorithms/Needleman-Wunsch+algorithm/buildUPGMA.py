#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:37:45 2019

@author: Ayca
"""

import getopt
import numpy as np
INF = 9999999999999999999
def fileRead(fasta):
    file = open(fasta,'r')
    sequences = []
    names = []
    for line in file:
        if line[0] =='>':
            line = line.replace(">","")
            names.append(line.replace("\n",""))
        elif line[0] != '>':
            line = line.replace("\n","")
            sequences.append(line)
    return names,sequences
#%%
def EMatrix(s1,s2,gapOpen,gapExt):
    row = len(s1)+1
    col = len(s2)+1
    e = np.zeros((row,col), dtype=int)
    e[0][0] = -10000
    for i in range(1,row):
        e[i][0] = gapOpen+i*gapExt
    return e

def FMatrix(s1,s2,gapOpen,gapExt):
    row = len(s1)+1
    col = len(s2)+1
    f = np.zeros((row,col), dtype=int)
    f[0][0] = -10000
    for j in range(1,col):
        f[0][j] = gapOpen+j*gapExt
    return f

def GMatrix(s1,s2,gapOpen,gapExt):
    row = len(s1)+1
    col = len(s2)+1
    g = np.zeros((row,col), dtype=int)
    g[0][0] = -10000
    return g

def VMatrix(s1,s2,gapOpen,gapExt):
    row = len(s1)+1
    col = len(s2)+1
    v = np.zeros((row,col), dtype=int)
    v[0][0] = 0
    for i in range(1,row):
        v[i][0] = gapOpen+i*gapExt
    for j in range(1,col):
        v[0][j] = gapOpen+j*gapExt
    return v

def Score(c1,c2,match_score,mismatch_score):
    if c1 == c2:
        return match_score
    else:
        return mismatch_score
#%%
"""
Needleman-Wunsch Algorithm with Affine Gap Scoring
"""
"""Matrices"""
""""""
def AAlign(matrix, s1,s2, gapOpen, gapExt,i,j,match,mismatch):
    align1 = ""
    align2 = ""
    isMatch = 0
    count = 0
    distance = 0
    while i >= 1 and j >= 1:
        current_score = matrix[i][j]
        if s1[i-1] == s2[j-1]:
            isMatch = match
        else:
            isMatch = mismatch
            distance +=1
        if current_score == matrix[i-1][j-1] + isMatch:
            align1 = align1+ s1[i-1]
            align2 = align2+ s2[j-1]
            i -=1
            j -=1

        elif (current_score == matrix[i][j-1] + gapExt) or (current_score == matrix[i][j-1] + gapOpen+ gapExt):
            align1 = align1 + s1[i]
            align2 = align2 + "-"
            j -=1
            distance +=1
        elif (current_score == matrix[i-1][j] + gapExt) or (current_score == matrix[i-1][j] + gapOpen+ gapExt):
            align1 = align1 + "-"
            align2 = align2 + s2[j]
            i -=1
            distance +=1
        count += 1
    align1 = align1[::-1]
    align2 = align2[::-1]
    #print("align1: {}, align2: {}".format(align1,align2))
    return align1, align2, distance
def AGlobal(s1,s2,gapOpen, gapExt,match,mismatch):
    row = len(s1)+1
    col = len(s2)+1
    e = EMatrix(s1, s2,gapOpen,gapExt)
    f = FMatrix(s1, s2,gapOpen,gapExt)
    g = GMatrix(s1, s2,gapOpen,gapExt)
    v = VMatrix(s1, s2,gapOpen,gapExt)
    for i in range(1,row):
        for j in range(1,col):
            e[i][j] = max(0,e[i][j-1]+gapExt,v[i][j-1]+gapOpen+gapExt)
            f[i][j] = max(0,f[i-1][j]+gapExt,v[i-1][j]+gapOpen+gapExt)
            g[i][j] = v[i-1][j-1]+ Score(s1[i-1],s2[j-1],match,mismatch)
            v[i][j] = max(0,g[i][j],e[i][j],f[i][j])
    #score = v[row-1,col-1]
    #print(score)
    i = row-1
    j = col-1
    align = AAlign(v, s1,s2, gapOpen, gapExt,i,j,match,mismatch)
    return align[2]
#%%
def update(scoring_matrix,x,y):
    for i in range(1,x):
        scoring_matrix[x][i] = (scoring_matrix[x][i]+scoring_matrix[y][i])/2
    for i in range(x,len(scoring_matrix[0])):
        scoring_matrix[i][x] = (scoring_matrix[i][x] +scoring_matrix[i][y])/2
    #if len(scoring_matrix[0])>1:
    scoring_matrix = np.delete(scoring_matrix, y, axis = 1)
    scoring_matrix = np.delete(scoring_matrix, x, axis = 0)
    #axis = 0 x
    #axis = 1 y
    return scoring_matrix
#%%
def UPGMA(names,scoring_matrix):
    out = []
    height_controller = []
    len_cont = len(names)
    copy_names = np.copy(names)
    while len(names) > 1:
        x = np.where(scoring_matrix == np.min(scoring_matrix))[0][0]
        y = np.where(scoring_matrix == np.min(scoring_matrix))[1][0]
        height = scoring_matrix[x][y]/2
        min_loc = min(x,y)
        max_loc = max(x,y)
        out.append( "("+names[min_loc]+": "+str(height)+" "+names[max_loc]+": "+str(height)+")")
        height_controller.append(height)
        scoring_matrix = update(scoring_matrix,min_loc,max_loc)

        new_name = names[min_loc]+""+names[max_loc]

        names[min_loc] = new_name
        #axis = 0 x
        #axis = 1 y
    
        names = np.delete(names,max_loc)
#    height_last = scoring_matrix[1][0]/2
#    out += ":"+str(height_last - height) +" "+ names[-1] + ":"+str(height_last)
#    out = "("+out+")"
    if len_cont == 3:
        res = ""
        for i in range(0,len(height_controller)):
            if i != len(height_controller)-1:
                res += str(out[i])+":"+str(height_controller[-1]-height_controller[i])+" "+copy_names[-1]+":"+str(height_controller[-1])
    else:
        res = ""
        for i in range(0,len(height_controller)):
            if i != len(height_controller)-1:
                res += str(out[i])+":"+str(height_controller[-1]-height_controller[i])+" "
    res = "("+res+")"
    print(res)
    return res
#%%
args = str(input())
args = args.split()
args = args[1:]
#optlist, args = getopt.getopt(args, 'buildUPGMA--fasta:--match:--mismatch:--gapopen:--gapext:--out:')
opts,args = getopt.getopt(args, "f:m:c:g:e:o:", ['fasta=', 'match=','mismatch=','gapopen=','gapext=','out='])
for i in opts:
    if i[0] == '--fasta':
        fasta = i[1]
    elif i[0] == '--match':
        match = int(i[1])
    elif i[0] == '--mismatch':
        mismatch = int(i[1])
    elif i[0] == '--gapopen':
        gapOp = int(i[1])
    elif i[0] == '--gapext':
        gapExt = int(i[1])
    elif i[0] == '--out':
        out_file = i[1]

names, sequences = fileRead(fasta)
scoring_matrix =  np.full((len(names),len(names)),99999999999999999,dtype=int)
no_of_elmts = 0
out = ""
for i in range(1,len(names)):
    for j in range(0,i):
        scoring_matrix[i][j]= AGlobal(sequences[i],sequences[j],gapOp, gapExt,match,mismatch)
        no_of_elmts +=1
#    return fasta, match,mismatch,gapOp,gapExt,out_file
out = UPGMA(names,scoring_matrix)
with open(out_file, 'w') as writer:
    writer.write(out)
writer.close()