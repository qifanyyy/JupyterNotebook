import numpy as np
from BinaryDiffEvolution import MBDE
import time
import scipy.io as scio
#数据导入
f = open('E:/Graduationthesis/data_MKP/mknapcb1.txt')
K = int(f.readline().split()[0])
KS = [24381,24274,23551,23534,23991,24613,25591,23410,24216,24411,
      42757,42545,41968,45090,42218,42927,42009,45020,43441,44554,
      59822,62081,59802,60479,61091,58959,61538,61520,59453,59965]
for ii in range(K):
    item = f.readline().split()
    n,m,optimal = int(item[0]),int(item[1]),int(item[2])
    price = []
    for i in range(0,15):
        item = [int(i) for i in f.readline().split()]
        for dat in item:
            price.append(dat)
    price = np.array(price,'double')
    weight = []
    for i in range(0,m):
        data = []
        for j in range(0,15):
            item = [int(i) for i in f.readline().split()]
            for dat in item:
                data.append(dat)
        weight.append(data)
    weight = np.array(weight,'double')
    c = np.array([int(i) for i in f.readline().split()],'double')
    #dataNew = 'E:/Graduationthesis/data_MKP/mknapcb'+str(ii+1)+'.mat'
    #scio.savemat(dataNew,{'price':price,
    #                      'weight':weight,
    #                      'b':b.reshape(-1,1)},'double')
    

    #计算价值密度并由大到小排序 vsort
    start = time.clock()
    temp = [0 for i in range(len(price))]
    for i in range(len(price)):
        for j in range(len(c)):
            temp[i] += weight[j][i]/c[j]
    d = [price[i]/temp[i] for i in range(0,len(price))]
    vsort = [0 for i in range(len(price))]
    for i in range(len(d)):
        location = d.index(max(d))
        vsort[i] = location
        d[location] = -1
    N = 30
    F = 1.0
    Cr = 0.8
    GenMax = 1000
    KnSolution = KS[ii]
    mbde = MBDE(price,weight,c,N,GenMax,F,Cr,vsort,KnSolution)
    mbde.MBDE()
    end = time.clock()
    print('5.100.',ii,' ',mbde.OptimalValue,' ','用时：',end - start)







'''
import math
import random
import numpy as np
def GenePool(n):
    parameter = 4
    if n % parameter == 0:
        m = int(n/parameter)
        l1 = l2 =parameter
    else:
        m = math.floor(n/parameter) + 1
        l1 = parameter
        l2 = n - (m - 1) * parameter
    Ge = []
    for i in range(0,m):
        if i < m - 1:
            G = [np.random.randint(0,2,l1) for i in range(10)]
            Ge.append(G)
        else:
            G = [np.random.randint(0,2,l2) for i in range(10)]
            Ge.append(G)
    return Ge

#数据导入
f = open('E:/Graduationthesis/data_MKP/mknapcb1.txt')
K = int(f.readline().split()[0])
item = f.readline().split()
n,m,optimal = int(item[0]),int(item[1]),int(item[2])
price = []
for i in range(0,15):
    item = [int(i) for i in f.readline().split()]
    for dat in item:
        price.append(dat)
price = np.array(price)
weight = []
for i in range(0,m):
    data = []
    for j in range(0,15):
        item = [int(i) for i in f.readline().split()]
        for dat in item:
            data.append(dat)
    weight.append(data)
weight = np.array(weight)
c = np.array([int(i) for i in f.readline().split()])
#计算价值密度并由大到小排序 vsort
temp = [0 for i in range(len(price))]
for i in range(len(price)):
    for j in range(len(c)):
        temp[i] += weight[j][i]/c[j]
d = [price[i]/temp[i] for i in range(0,len(price))]
vsort = [0 for i in range(len(price))]
for i in range(len(d)):
    location = d.index(max(d))
    vsort[i] = location
    d[location] = -1
def is_FeaSol(weight,c,solution):
    for i in range(len(c)):
        if sum(solution*weight[i]) <= c[i]:
            continue
        if sum(solution*weight[i]) > c[i]:
            return False
    return True
def GLM(x):
    n = len(price)
    m = len(c)
    b = [0 for i in range(n)]
    s = [0 for i in range(m)]
    value = 0
    for i in range(n):
        flag = 0
        if x[vsort[i]] == 1:
            for j in range(m):
                if s[j] + weight[j][vsort[i]] > c[j]:
                    flag = 1
                    break
            if flag == 0:
                b[vsort[i]] = 1
                value += price[vsort[i]]
                for j in range(m):
                    s[j] += weight[j][vsort[i]]
    for i in range(n):
        flag = 0
        if x[vsort[i]] == 0:
            for j in range(m):
                if s[j] + weight[j][vsort[i]] > c[j]:
                    flag = 1
                    break
            if flag == 0:
                b[vsort[i]] = 1
                value += price[vsort[i]]
                for j in range(m):
                    s[j] += weight[j][vsort[i]]
    return b,value

t = 0
sum_num = 0
while(t < 20000):
    x = np.random.randint(0,2,100)
    b,value = GLM(x)
    if not is_FeaSol(weight,c,b):
        sum_num += 1
    t += 1
'''
