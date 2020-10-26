import sys
import numpy as np
import math
import random
import itertools
import datetime
import time as cronometro
import os
from random import shuffle
from multiprocessing import Pool
import multiprocessing
import logging
from operator import itemgetter

# FILE_TO_BEST_SOLUTION ='results/la_cu_caratia.txt'
ITERACTIONS = 10000000
# NUM_VIZINHOS = 8
# SOLUCOES_GULOSAS = 100
# ALPHA = 0.1
# LOCAL_SEARCH_CRITERIA = 20


FILE_TO_BEST_SOLUTION = sys.argv[1]
MINUTES = int(sys.argv[2])
NUM_VIZINHOS = 8
SOLUCOES_GULOSAS = 100
ALPHA = float(sys.argv[3])
LOCAL_SEARCH_CRITERIA = 10
NUM_CORES = 1


#           0               1                   2       3
#python3 ngrasp.py <FILE_TO_BEST_SOLUTION> <MINUTES> <ALPHA>



# -------- ----------GRASP --------- ---------------
def grasp(d, l, inst):

    M,L = d.shape

    start = cronometro.time()

    min_dist_m = calculate_min_distances(d)
    min_dists_sorted = sorted(min_dist_m, key=itemgetter(1), reverse=True)[:]
   
    f = 0
    S = []
    it = 0
    while (cronometro.time()-start)/60 < MINUTES:
        s = greedy_randomized(d, l, min_dists_sorted)
        s = local_search(s, l, d, min_dist_m)
        f_ = evaluate(s, d)
        if f_ > f:
            f = f_
            S[:] = s[:]
        print("it. {}: bv: {} - seconds execution: {}...".format(it, f, int(cronometro.time()-start)))
        it += 1
    logging.info("TOTAL TIME: {} ".format(int(cronometro.time()-start)))

    return S, f


# --------------------------------------------------
# ----------- Início guloso Randomizado ------------

def greedy_randomized(d, l, min_dist_m):
    """Gera solução inicial """
    M,L = d.shape
    S = set()
    cut = int(abs((len(min_dist_m)*ALPHA)))
  
    if l > cut:
        print("Infactível, impossível criar conjunto de soluções.")
        pass 
    indexes = random.sample(range(1, cut), l)
    for e in indexes:
        S.add(min_dist_m[e][0])

    return list(S)

# ------------------------------------------------
# ----------- Busca local  ------------

def local_search(S, l, d, min_dists):
    """ Aplica uma busca local com NUM_VIZINHOS vizinhos """

    _, L = d.shape

    best_sol = []
    best_sol_value = 0

    S_  = S[:]
    f = evaluate(S_,d)

    # GERA OS VIZINHOS E SEUS VALORES (S,VAL) 
    N = generate_neighbors(S_, L, d, min_dists)
    best_index = np.argmax([x[1] for x in N])
    best_neighbor = N[best_index][0]
    bn_value = N[best_index][1]

    while bn_value > f:

        f = bn_value
        S_[:] = best_neighbor[0][:]

        N = generate_neighbors(S_, L, d, min_dists)
        best_index = np.argmax([x[1] for x in N])
        best_neighbor = N[best_index][0]
        bn_value = N[best_index][1]

    return N[best_index][0]


# ----------- Geração dos vizinhos   -------------

def generate_neighbors(S,L,d,min_dists):

    s_value = evaluate(S,d)

    l = len(S)
    possible = set(range(L)) - set(S)
    possibles = list(possible)
    
    N = []
    count = 0
    for i in range(l):
        for new_element in possibles:            
            S_ = S[:]
            S_[i] = new_element
   
            n_value = min(s_value, get_element_min_dist(new_element, min_dists))
            N.append(tuple([S_, n_value]))
            if count == 0:
                print(n_value, s_value)
            count += 1
            
    
    return N 


# ------------------------------------------------
# ---------- Função objetivo ---------------------

def evaluate(S, d):
    """Função objetivo"""
    M, L = d.shape
    result = 0
    for m in range(M):
        dm = math.inf
        for e in S:
            dm = min(dm, d[m,e])
        result += dm
    return result

# -----------------------------------------------
def calculate_min_distances(d):
    """ Calcula as distâncias mínimas e retorna uma lista com (l,dist) ordanada """
    M, L = d.shape
    min_dists_vs_l = []
    for l in range(L):
        min_dist = np.inf
        for m in range(M):
            min_dist = min(min_dist, d[m,l])
        min_dists_vs_l.append(tuple([l, min_dist]))     
    return min_dists_vs_l
# -----------------------------------------------

# def update_sol(S,d, min_dists, sol_value):
#     """ Função para facilitar a função objetivo """
#     M, L = d.shape
#     best_m = []
#     result = 0
#     for m in range(M):
#         dm = math.inf
#         for e in S:
#             dm = min(dm, d[m,e])
#         result += dm
#         best_m.append(dm)
#     return best_m

        

# -------------------------------------------------

def get_element_min_dist(e, min_dists):
    return min_dists[e][1]

# ------------------------------------------------
# ----------- Parser para a entrada  ------------

def parse_instance(inst):

    file = open(inst,'r')
    instance = [abs(float(x)) for x in file.read().split()]
    file.close()
 
    M = int(instance[0]) 
    L = int(instance[1]) 
    l = int(instance[2])

    print("|M|: {}, |L|: {}, l: {}".format(M,L,l))

    D = np.zeros((M,L), int)

    i = 0
    for k in range(3,(M*L)+3):
        j = (k-3)%L

        D[(i,j)] = instance[k]
        if j == L-1:
            i+=1 

    return M, L, l, D

            
def main():
    
    #instancia = input()
    instancia = '/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.A.ins'
    M, L, l, d = parse_instance(instancia)

    if (ALPHA*L) < l:
        print("impossível prosseguir para esse valor de alpha")
    else:
        S, value = grasp(d,l,instancia)
  
    f=open(FILE_TO_BEST_SOLUTION, 'w')
    f.write("Best value: \n")
    f.write(str(value))
    f.close

if __name__ == "__main__":
    main()