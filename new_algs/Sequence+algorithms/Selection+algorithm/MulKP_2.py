import numpy as np
from ClonalSelection import ImCSA
from ClonalSelection import CSA
from BinaryDiffEvolution import MBDE
import cython
import time
from scipy.io import loadmat

weing = loadmat("E:\GraduationThesis\data_M-DMKP\weing2.mat")
b = weing['b'][0].tolist()
price = weing['price'][0].tolist()
weight = weing['weight'].tolist()
KnSolution = weing['fbest0'][0][0]
temp = [0 for i in range(len(price))]
for i in range(len(price)):
    for j in range(len(b)):
        temp[i] += weight[j][i]/b[j]
d = [price[i]/(temp[i]+1) for i in range(0,len(price))]
vsort = [0 for i in range(len(price))]
for i in range(len(d)):
    location = d.index(max(d))
    vsort[i] = location
    d[location] = -1
N = 30  
alpha = 0.4  
Tr = 0.1   
sigma = 4
GenMax = 1000
f_max = 0
f_mean = 0
f_min = 99999999999999999
times = 0

for cs in range(10):
    start = time.clock()
    flscsa = ImCSA(price,weight,b,N,GenMax,sigma,alpha,Tr,KnSolution,vsort)
    flscsa.ImCSA()
    end = time.clock()
    if f_max < flscsa.OptimalValue:
        f_max = flscsa.OptimalValue
        #Pbest = csa.Pbest
    if f_min > flscsa.OptimalValue:
        f_min = flscsa.OptimalValue
    f_mean += flscsa.OptimalValue
    times += end - start

print('FLSCSA',' ','最大值:',f_max,'平均值:',f_mean/10,'最小值:',f_min,'平均用时:',round(times/10,2),end = ' ')
print('已知最优',KnSolution[ii])
