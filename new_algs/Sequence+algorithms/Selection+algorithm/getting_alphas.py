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
# ALPHA = float(sys.argv[3])
LOCAL_SEARCH_CRITERIA = 10
NUM_CORES = 1


#           0               1                   2       3
#python3 ngrasp.py <FILE_TO_BEST_SOLUTION> <MINUTES> <ALPHA>



# -------- ----------GRASP --------- ---------------
def grasp(d, l, inst, alpha):

    start = cronometro.time()

    #-------------------------------LOGS-----------------------------------------------------
    logging.basicConfig(filename='results/'+str(datetime.datetime.now()),level=logging.DEBUG)
    logging.info("Instância: {} ".format(inst))
    #logging.info("GRASP ITERATIONS: {} ".format(interactions))
    logging.info("SOLUCOES_GULOSAS: {} ".format(SOLUCOES_GULOSAS))
    logging.info("ALPHA: {} ".format(alpha))
    logging.info("LOCAL_SEARCH_CRITERIA: {} ".format(LOCAL_SEARCH_CRITERIA))
    logging.info("NUM_VIZINHOS: {} ".format(NUM_VIZINHOS))
    #-----------------------------------------------------------------------------------------

   
    f = 0
    S = []
    it = 0
    while (cronometro.time()-start)/60 < MINUTES:
        s = greedy_randomized(d, l, alpha)
        s = local_search(s, l, d)
        f_ = evaluate(s, d)
        if f_ > f:
            f = f_
            S[:] = s[:]
            logging.info('{} - {} - {} - {}'.format(alpha, it, f, int(cronometro.time()-start)))
        print("alpha: {} it. {}: bv: {} - seconds execution: {}...".format(alpha, it, f, int(cronometro.time()-start)))
        it += 1
    logging.info("TOTAL TIME: {} ".format(int(cronometro.time()-start)))

    return S, f


# --------------------------------------------------
# ----------- Início guloso Randomizado ------------

def greedy_randomized(d, l, alpha):
    """Gera solução inicial """

    M,L = d.shape
   
    list_of_solutions = []

    l_elements = [x for x in range(L)]
    for it in range(SOLUCOES_GULOSAS):
        shuffle(l_elements)
        s = l_elements[:l] 
        f = evaluate(s, d)       
        list_of_solutions.append([f, s])
            
    index_max = int(math.floor(len(list_of_solutions)*alpha))
   
    rlc = sorted(list_of_solutions, key=itemgetter(0), reverse=True)[:index_max]
   
    index_solution = random.randint(0, len(rlc)-1) 
    best_sol = rlc[index_solution][1]

    return best_sol

# ------------------------------------------------
# ----------- Busca local  ------------

def local_search(S, l, d):
    """ Aplica uma busca local com NUM_VIZINHOS vizinhos """

    _, L = d.shape

    best_sol = []
    best_sol_value = 0

    for it in range(LOCAL_SEARCH_CRITERIA):
        S_ = []
        S_ [:] = S[:]
        f = evaluate(S_,d)

        N = generate_neighbors(S_, L)
        best_neighbor = N[np.argmax([evaluate(x, d) for x in N])]
        bn_value = evaluate(best_neighbor, d)

        while bn_value > f:
    
            f = bn_value
            S_[:] = best_neighbor[:]

            N[:] = generate_neighbors(S_, L)
            best_neighbor[:] = N[np.argmax([evaluate(x, d) for x in N])].copy()
            
            bn_value = evaluate(best_neighbor, d)
        if f > best_sol_value:
            best_sol[:] = S_[:]
            best_sol_value = f

    return best_sol






# ----------- Geração dos vizinhos   -------------

def generate_neighbors(S,L):

    S_ = S[:]
    
    N = []
    while len(N) < NUM_VIZINHOS:
        index = random.randint(0,len(S_)-1)
        n = random.randint(0,L-1)
        while n in S_:
            n = random.randint(0,L-1)
        if (n >= 450):
            break
        S_[index] = n
        N.append(S_)
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
    

    # D é a matriz de adjacência com os valores dos pesos
    
    #instancia = input()
    
    #M, L, l, d = parse_instance(instancia)

    # it_process = int(abs(math.ceil(ITERACTIONS/NUM_CORES)))

    # iteractions_list = [[d,l,instancia,it_process] for _ in range(NUM_CORES)]

    # sol_list = []
    # with Pool(NUM_CORES) as p:
    #     sol_list = p.starmap(grasp, iteractions_list)
    
    # index = np.argmax([x[1] for x in sol_list])
    # best_sol, best_value = sol_list[index]

    # best_sol, best_value = grasp(d,l,instancia)
    #print("Best solution quality: {} \n Agent: \n {}".format(best_value, best_sol))
    #logging.info("Best solution quality: {} \n Agent: \n {}".format(best_value, best_sol))
    

    # posso rodar os testes aqui
    mdmt39_112_A = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.A.ins"
    mdmt39_112_B = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.B.ins"
    mdmt39_225_A = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.225.A.ins"
    mdmt39_225_B = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.225.B.ins"
    mdmt40_56_A = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.56.A.ins"
    mdmt40_56_B = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.56.B.ins"
    mdmt40_112_A = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.112.A.ins"
    mdmt40_112_B = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.112.B.ins"
    mdmt40_225_A = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.225.A.ins"
    mdmt40_225_B = "/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt40.225.B.ins"

    mdmt39_112_A_inst = parse_instance(mdmt39_112_A)
    mdmt39_112_B_inst = parse_instance(mdmt39_112_B)
    mdmt39_225_A_inst = parse_instance(mdmt39_225_A)
    mdmt39_225_B_inst = parse_instance(mdmt39_225_B)
    mdmt40_56_A_inst = parse_instance(mdmt40_56_A)
    mdmt40_56_B_inst = parse_instance(mdmt40_56_B)
    mdmt40_112_A_inst = parse_instance(mdmt40_112_A)
    mdmt40_112_B_inst = parse_instance(mdmt40_112_B)
    mdmt40_225_A_inst = parse_instance(mdmt40_225_A)
    mdmt40_225_B_inst = parse_instance(mdmt40_225_B)

    # 0  1  2  3
    # M, L, l, d = parse_instance(instancia) and  grasp(d,l,instancia)




    # descobrir o melhor alpha para a primeira instancia
    # rodar o algoritmo pelo menos três vezes para cada alpha na primeira instancia, pegar a média dos resultados de cada alpha e comparar

    cores = multiprocessing.cpu_count()


    
    inst_with_alpha10 = (mdmt39_112_A_inst[3], mdmt39_112_A_inst[2], mdmt39_112_A, 0.1)
    inst_with_alpha20 = (mdmt39_112_A_inst[3], mdmt39_112_A_inst[2], mdmt39_112_A, 0.2)
    inst_with_alpha30 = (mdmt39_112_A_inst[3], mdmt39_112_A_inst[2], mdmt39_112_A, 0.3)
  
    bests = []


    # ------------------ testa alpha = 10 3 vezes:
    sol_list = []
    with Pool(cores) as p:
        sol_list = p.starmap(grasp, [inst_with_alpha10, inst_with_alpha10, inst_with_alpha10])
    
    index = np.argmax([x[1] for x in sol_list])
    best_sol, best_value = sol_list[index]
    bests.append(best_value)
    f=open("results/alpha_10_results.txt", 'w')
    f.write("Best solutions: (alpha = 10)\n")
    f.write(str([x[1] for x in sol_list]) + '\n')
    f.close

    # --------------------------------------------
    # ------------------ testa alpha = 20 3 vezes:

    sol_list = []
    with Pool(cores) as p:
        sol_list = p.starmap(grasp, [inst_with_alpha20, inst_with_alpha20, inst_with_alpha20])
    
    index = np.argmax([x[1] for x in sol_list])
    best_sol, best_value = sol_list[index]
    bests.append(best_value)
    f=open("results/alpha_20_results.txt", 'w')
    f.write("Best solution: (alpha = 20)\n")
    f.write(str([x[1] for x in sol_list]) + '\n')
    f.close

    # --------------------------------------------
    # ------------------ testa alpha = 30 3 vezes:

    sol_list = []
    with Pool(cores) as p:
        sol_list = p.starmap(grasp, [inst_with_alpha20, inst_with_alpha20, inst_with_alpha20])
    
    index = np.argmax([x[1] for x in sol_list])
    best_sol, best_value = sol_list[index]
    bests.append(best_value)
    f=open("results/alpha_30_results.txt", 'w')
    f.write("Best solution: (alpha = 30)\n")
    f.write(str([x[1] for x in sol_list]) + '\n')
    f.close

    # --------------GRAVA O MELHOR ALPHA----------

    index = np.argmax(bests)

    best = ""
    if index == 0:
        best = "alpha=10%"
    if index == 1:
        best = "alpha=20%"
    if index == 2:
        best = "alpha=30%"
    

    f=open("results/the_best_alpha_is.txt", 'w')
    f.write("Where goes the best alpha found!!! \n")
    f.write(best)
    f.close



if __name__ == "__main__":
    main()
