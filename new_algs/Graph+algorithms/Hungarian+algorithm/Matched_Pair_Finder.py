from __future__ import division
from munkres import Munkres, print_matrix
from time import clock


class Person:
    def __init__(self, subnum, age, score):
        self.id = subnum
        self.age = age
        self.score = score
    def __repr__(self):
        return str(', '.join(map(str, [self.id, self.age, self.score])))
one = []        
for line in open('one.csv').read().split('\n')[1:]:
    try:
        parts = line.split(',')
        fields = parts[0], float(parts[1]), float(parts[2])
        one.append(Person(*fields))
    except:
        #print 'error parsing line: ', line
        pass
    
two = []        
for line in open('two.csv').read().split('\n')[1:]:
    try:
        parts = line.split(',')
        fields = parts[0], float(parts[1]), float(parts[2])
        two.append(Person(*fields))
    except:
        #print 'error parsing line: ', line
        pass
import numpy

print (len(one), len(two))
cutoff = 280
one = one[:cutoff]
two = two[:cutoff]

ages = [p.age for p in one+two]
scores = [p.score for p in one+two]
age_range = max(ages) - min(ages)
score_range = max(scores) - min(scores)


def score_(p1, p2):
    dA = abs(p1.age - p2.age) 
    if dA > dA_cutoff:
        dA = inf
    else:
        dA /= age_range

    dS = abs(p1.score - p2.score) 
    if dS > dS_cutoff:
        dS = inf
    else:
        dS /= score_range
    
    score = (dA**2 + dS**2)**.5 / 2**.5
    if score < score_cutoff:
       score = 1
    return dA, dS, score
def score(p1, p2):
    return score_(p1, p2)[2]

n = max(len(one), len(two))

print ('Starting Hungarian Algorithm trials')
start = clock()
score_cutoff = 2



dA_cutoff = 6
dS_cutoff = 8


matrix = numpy.zeros((len(one), len(two))) 
inf = 1e9
#print matrix


    

for i, p1 in enumerate(one):
    for j, p2 in enumerate(two):        
        matrix[i, j] = score(p1, p2)
        
matrix = matrix.tolist()
#print 'Setup completed'


m = Munkres()
indexes = m.compute(matrix)
matrix = numpy.array(matrix)
total = 0
pairs = []
for i, j in indexes:
    if matrix[i,j] < score_cutoff:
        value = matrix[i, j]
        pairs.append((i,j))
        #print 'value', value
        total += value
        #print 'total', total
#    print row, column, value

elapsed = clock() - start
print (elapsed, dA_cutoff, dS_cutoff, len(pairs))
start = clock()
#print 'cost per pair', total / pairs

#print 'runtime:', elapsed, elapsed/n, elapsed/n**3


"""
da, ds, cutoff, pairs
6 8 1/2 102
3 5 1/2 92
"""
for pair in pairs:
    p1, p2 = one[pair[0]], two[pair[1]]
    dA = abs(p2.age - p1.age)
    dS = abs(p2.score - p1.score)
    print (p1.id, p2.id, p1.age, p1.score, p2.age, p2.score, dA, dS, dA<=dA_cutoff and dS<=dS_cutoff)