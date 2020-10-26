from random import randint
import random
import time
from prettytable import PrettyTable
import sys

sys.setrecursionlimit(9000)

def quicksort(lista):
    if len(lista) <= 1: 
        return lista
    
    pivo = lista[0]
    iguais  = [x for x in lista if x == pivo]
    menores = [x for x in lista if x <  pivo]
    maiores = [x for x in lista if x >  pivo]
    return quicksort(menores) + \
           iguais + quicksort(maiores)


def selection(v):
    v2 = []
    resp = []
    for i in range(len(v)):
        x = v[i]
        v2.append(x)
    while v2:
        m = min(v2)
        resp.append(m)
        v2.remove(m)
    return resp

   
def merge(e, d):
    r = []
    i, j = 0, 0
    while i < len(e) and j < len(d):
        if e[i] <= d[j]:
            r.append(e[i])
            i += 1
        else:
            r.append(d[j])
            j += 1
    r += e[i:]
    r += d[j:]
    return r

def mergesort(v):
    if len(v) <= 1:
        return v
    else:
        m = len(v) // 2
        e = mergesort(v[:m])
        d = mergesort(v[m:])
        return merge(e, d)

list = []
v1 = []
i = 0
x = True
qtd = 0
k = 0

tabela = PrettyTable(["Elementos","Mergesort", "Quicksort", "Selection", "Native"])
tabela.align["Elementos"], = "l"
tabela.align["Mergesort"], = "l"
tabela.align["Quicksort"], = "r"
tabela.align["Selection"], = "r"
tabela.align["Native"], = "r"


while (x):
        if i < 2000:
            random.shuffle(v1)
            i += 1
            x = randint(1,10000)
            v1.append(x)
        else:
            qtd += 2000
            list.append(v1)
            ###############

            c = time.time()
            quicksort(v1)
            f = time.time()
            q = c-f
            ###############
            c = time.time()
            mergesort(v1)
            f = time.time()
            m = c-f
            ###############
            c = time.time()
            selection(v1)
            f = time.time()
            s = c-f
            ###############
            c = time.time()
            v1.sort()
            f = time.time()
            n = c-f
            ###############
                
            tabela.add_row([qtd, "%.2f" % m, "%.2f" % q, "%.2f" % s , "%.2f" % n])
            
            i = 0
            x = (True, False)[s <= -30.00]
            print(len(v1))

print(tabela)
























