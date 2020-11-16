import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np
from math import *
"""
Comparaison du temps des algos selon la taille du "k" 
"""
"""
v=np.arange(1,17,1)
tab = []
for j in v:
    T=[]
    for i in range (3):
        bloc = str(j)
        out = sp.check_output(['../cmake-build-release/src/Matrusse 4096 4096 '+bloc+' -m1'], shell=True).decode("utf-8")
        out = out.split(": ")
        p = out[1]
        p = int(p)
        T.append(p)
        moy = (sum(T)/len(T))
        barre = str(i+1)+"/3"
        print(barre)
    tab.append(moy)
    barre = "k : "+str(j)
    print(barre)
plt.plot(v,tab)
plt.xlabel("k")
plt.ylabel("Temps d exécution")
"""
"""
Recherche du k optimal en fonction de la taille de la matrice
"""
"""
A=[500,1000,1500,2000,2500,3000,4000,5000,6000,7000,8000,9000,10000]
v=np.arange(5,12,1)
tab = []
for l in A:
    mint = inf
    mink = inf
    taille = str(l)
    for j in v:
        T = []
        for i in range (3):
            bloc = str(j)
            out = sp.check_output(['../cmake-build-release/src/Matrusse '+taille+' '+taille+' '+bloc+' -m1'], shell=True).decode("utf-8")
            out = out.split(": ")
            p = out[1]
            p = int(p)
            T.append(p)
            barre = str(i+1)+"/3"
            print(barre)
        moy = (sum(T)/len(T))
        if moy<mint:
            mint = moy
            mink = j   
        barre = "k : "+str(j)
        print(barre)
    tab.append(mink)
    barre = "Matrice de taille "+str(l)+" terminée"
    print(barre)
plt.plot(A,tab)
plt.xlabel("taille de la matrice")
plt.ylabel("k optimal")
"""
"""
Comparaison du temps des différents algos selon la taille de la matrice
"""
"""
tfinal=np.zeros((5,4))
u=[2048,4096,8192,16384]
ite=0

for j in u:
    barre = "Matrice de taille "+str(j)
    print(barre)
    for i in range (1,6):
        barre = "Version "+str(i)
        print(barre)
        k = str(int(0.75*log2(j)))
        taille = str(j)
        version = str(i)
        out = sp.check_output(['../cmake-build-release/src/Matrusse '+taille+' '+taille+' '+k+' -m'+version+' 512'], shell=True).decode("utf-8")
        out = out.split(": ")
        p = out[1]
        p = int(p)
        tfinal[i-1,ite]=p
    ite+=1

fig, ax = plt.subplots()
ax.plot(u,tfinal[0],label='Algo Naïf')
ax.plot(u,tfinal[1],label='Algo cache')
ax.plot(u,tfinal[2],label='Algo intrins')
ax.plot(u,tfinal[3],label='Algo Speed of Light')
ax.plot(u,tfinal[4],label='Gaspard')
legend = ax.legend(loc='best')
plt.xlabel("Taille de la matrice")
plt.ylabel("Temps d'exécution")


"""
"""
Comparaison temps algo découpage en bloc selon la taille du découpage du bloc
"""

A=np.arange(10,3000,20)
T=[]
for l in A:
    O=[]
    for j in range(2):
        barre = str(j+1)+"/2"
        print(barre)
        k = str(int(0.75*log2(l)))
        bloc = str(l)
        out = sp.check_output(['../cmake-build-release/src/Matrusse 8192 8192 '+k+' -m5 '+bloc], shell=True).decode("utf-8")
        out = out.split(": ")
        p = out[1]
        p = int(p)
        O.append(p)
    moy = np.mean(O)
    T.append(moy)
    print("Terminé pour la taille de bloc "+str(l)+"")
plt.plot(A,T)
plt.xlabel("Taille de bloc")
plt.ylabel("Temps d'exécution")

"""
Comparaison temps algo découpage en bloc selon la construction de la table de Gray
"""
"""
u = [128,256,512,1024,2048,4096,8192,16384]
O = []
P = []
for j in u:
    T=[]
    S=[]
    for i in range(3):
        taille = str(j)
        out = sp.check_output(['../cmake-build-release/src/Matrusse '+taille+' '+taille+' 7 -m2 1024'], shell=True).decode("utf-8")
        out = out.split(": ")
        p = out[1]
        p = int(p)
        T.append(p)
        moy = (sum(T)/len(T))
        out = sp.check_output(['../cmake-build-release/src/Matrusse '+taille+' '+taille+' 7 -m4'], shell=True).decode("utf-8")
        out = out.split(": ")
        p = out[1]
        p = int(p)
        S.append(p)
        moy2 = (sum(S)/len(S))
        print(i)
    O.append(moy)
    P.append(moy2)
    print(j)
plt.plot(u,O)
plt.plot(u,P)
"""