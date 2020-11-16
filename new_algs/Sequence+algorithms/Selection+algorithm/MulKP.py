import numpy as np
from ClonalSelection import ImCSA
from ClonalSelection import CSA
from BinaryDiffEvolution import MBDE
import cython
import time
#
times = []
solution = []
KnSolution = [24381,24274,23551,23534,23991,24613,25591,23410,24216,24411,
      42757,42545,41968,45090,42218,42927,42009,45020,43441,44554,
      59822,62081,59802,60479,61091,58959,61538,61520,59453,59965]
f = open('E:/Graduationthesis/data_MKP/mknapcb1.txt')
K = int(f.readline().split()[0])
for ii in range(K):
    print('5.100.',ii,end = ' ')
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
    b = np.array([int(i) for i in f.readline().split()])
    #
    temp = [0 for i in range(len(price))]
    for i in range(len(price)):
        for j in range(len(b)):
            temp[i] += weight[j][i]/b[j]
    d = [price[i]/temp[i] for i in range(0,len(price))]
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
        flscsa = ImCSA(price,weight,b,N,GenMax,sigma,alpha,Tr,KnSolution[ii],vsort)
        flscsa.ImCSA()
        end = time.clock()
        if f_max < flscsa.OptimalValue:
            f_max = flscsa.OptimalValue
            #Pbest = csa.Pbest
        if f_min > flscsa.OptimalValue:
            f_min = flscsa.OptimalValue
        f_mean += flscsa.OptimalValue
        times += end - start

    #print(flscsa.OptimalValue,end = ' ')
    print('FLSCSA',' ','最大值:',f_max,'平均值:',f_mean/10,'最小值:',f_min,'平均用时:',round(times/10,2),end = ' ')
    '''
    N = 30  
    alpha = 0.4  
    Pm = 0.8
    mu = 0.2
    k = 1000
    GenMax = 1500 
    f_max = 0
    f_mean = 0
    f_min = 99999999999999999
    times = 0
    for cs in range(10):
        start = time.clock()
        csa = CSA(price,weight,b,N,GenMax,alpha,Pm,mu,k,KnSolution[ii])
        csa.CSA()
        end = time.clock()
        if f_max < csa.OptimalValue:
            f_max = csa.OptimalValue
            #Pbest = csa.Pbest
        if f_min > csa.OptimalValue:
            f_min = csa.OptimalValue
        f_mean += csa.OptimalValue
        times += end - start
    print('CSA',' ','最大值:',f_max,'平均值:',f_mean/10,'最小值:',f_min,'平均用时:',round(times/10,2),end = ' ')
    #start = time.clock()
    #csa = ImCSA(price,weight,b,N,GenMax,sigma,alpha,Tr,KnSolution[ii],vsort)
    #csa.ImCSA()
    #end = time.clock()
    #print('CSA','  ',csa.OptimalValue,' ','用时：',end - start,'s',end = ' ')
    #csa.printResult()
    #solution.append(csa.fbest)
    #csa.printResult()
    #
    ########################-#-#-
    #start = time.clock()
    N = 30
    F = 1.0
    Cr = 0.8
    GenMax = 1000
    f_max = 0
    f_mean = 0
    f_min = 99999999999999999
    times = 0
    for cs in range(10):
        start = time.clock()
        mbde = MBDE(price,weight,b,N,GenMax,F,Cr,vsort,KnSolution[ii])
        mbde.MBDE()
        end = time.clock()
        if f_max < mbde.OptimalValue:
            f_max = mbde.OptimalValue
            #Pbest = mbde.Pbest
        if f_min > mbde.OptimalValue:
            f_min = mbde.OptimalValue
        f_mean += mbde.OptimalValue
        times += end - start
    print('MDBE',' ','最大值:',f_max,'平均值:',f_mean/10,'最小值:',f_min,'平均用时:',round(times/10,2),end = ' ')
    #mbde = MBDE(price,weight,b,N,GenMax,F,Cr,vsort,KnSolution[ii])
    #mbde.MBDE()
    #end = time.clock()
    #print('MDBE：',' ',mbde.OptimalValue,' ','用时：',end - start,'s',end = ' ')
    '''
    print('已知最优',KnSolution[ii])
    

    
    '''
    k = [b[i]/sum(b) for i in range(len(b))]
    v = [0 for i in range(len(price))]
    for i in range(len(price)):
        for j in range(len(b)):
            v[i] += weight[j][i]/k[j]
    rho = [price[i]/v[i] for i in range(0,len(price))]
    vsort = [0 for i in range(len(price))]
    for i in range(len(rho)):
        location = rho.index(max(rho))
        vsort[i] = location
        rho[location] = -1
    '''
