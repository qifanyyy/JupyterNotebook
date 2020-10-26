#!/usr/bin/env python
# generate simulate data for experiment
# including: software, user relationship(advise), invoke collaboration, current user, weight assigned to each factor
# 
from datamodel import s
from data import UNUM
from data import SNUM

import random
import pprint

# software
S = []
for i in range(SNUM):
    publisher = random.randint(0, UNUM-1)
    paper = random.randint(0, 5)
    oneS = s(publisher, paper)
    S.append(oneS)

# user relationship(advise)
# advise: a UNUM*UNUM matrix
# advise[i][j]==0: there is no relationship between user i and j
# advise[i][j]==1: user i is mentor or advisor of user j
advise = []
for i in range(UNUM):
    row = []
    for j in range(UNUM):
        row.append(0)
    advise.append(row)

for i in range(UNUM):
    for j in range(i+1, UNUM):
        flag = random.randint(0, 2)
        if flag==0:
            advise[i][j]=0
        elif flag==1:
            advise[i][j]=1
        else:
            advise[j][i]=1

# invoke collaboration
invocateCo = []
for i in range(UNUM):
    row = []
    for j in range(UNUM):
        row.append(random.randint(0, 10))
    invocateCo.append(row)

# current user
curUser = random.randint(0, UNUM-1)

# weight assigned to each factor
w = [0.25, 0.25, 0.25, 0.25]

if __name__ == "__main__":
    for i in range(SNUM):
        print S[i].publisher
        print S[i].paper
        print ""
        
    pprint.pprint(advise)
    print ""
    
    pprint.pprint(invocateCo)
    