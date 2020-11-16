import math
import random
import numpy as np
import matplotlib.pyplot as plt
from numba import jit
'''
binary differential evolution

'''
class MBDE():
    @jit
    def __init__(self,price,weight,c,N,GenMax,F,Cr,vsort,KnSolution):
        self.price = price
        self.weight = weight
        self.c = c
        self.N = N
        self.GenMax = GenMax
        self.F = F
        self.Cr = Cr
        self.vsort = vsort
        self.KnSolution = KnSolution
        self.fbest = []
        self.pbest = []
        self.OptimalValue = 0
    #可行解的生成和优化
    def GLM(self,x):
        n = len(self.price)
        m = len(self.c)
        b = [0 for i in range(n)]
        s = [0 for i in range(m)]
        value = 0
        for i in range(n):
            flag = 0
            if x[self.vsort[i]] == 1:
                for j in range(m):
                    if s[j] + self.weight[j][self.vsort[i]] > self.c[j]:
                        flag = 1
                        break
                if flag == 0:
                    b[self.vsort[i]] = 1
                    value += self.price[self.vsort[i]]
                    for j in range(m):
                        s[j] += self.weight[j][self.vsort[i]]
        for i in range(n):
            flag = 0
            if x[self.vsort[i]] == 0:
                for j in range(m):
                    if s[j] + self.weight[j][self.vsort[i]] > self.c[j]:
                        flag = 1
                        break
                if flag == 0:
                    b[self.vsort[i]] = 1
                    value += self.price[self.vsort[i]]
                    for j in range(m):
                        s[j] += self.weight[j][self.vsort[i]]
        return b,value
    #解的适应度
    def affinity(self,x):
        fvalue = sum(x*self.price)
        return fvalue
    #精英局部搜索          
    def LocalSearch(self,Gn,k):
        n = len(Gn[0])
        aff = [self.affinity(Gn[i]) for i in range(len(Gn))]
        location = aff.index(max(aff))
        aff[location] = -1
        max_solution = [Gn[location][i] for i in range(len(Gn[location]))]
        temp_solution = [Gn[location][i] for i in range(len(Gn[location]))]
        rand_num = random.random()
        evl_rand = np.random.randint(0,49,k)
        for temp in evl_rand:
            temp_solution[temp] = 1 - temp_solution[temp]
        solution,value = self.GLM(temp_solution)
        if sum(solution*self.price) >= sum(max_solution*self.price):
            Gn[location] = solution
        else:
            Gn[location] = max_solution
        return Gn
      
    def MBDE(self):
        n = len(self.price)
        solution = np.zeros([self.N,n])
        f_x = []
        P = np.zeros([self.N,n])
        for i in range(self.N):
            P[i] = np.random.random(n)
        Pt = np.zeros([self.N,n])
        P2 = np.zeros([self.N,n])
        #初始化
        t = 0
        for i in range(self.N):
            x = np.array([0 for i in range(n)],int)
            for j in range(n):
                if P[i][j] >= 0.5:
                    x[j] = 1
                else:
                    x[j] = 0
            x,value = self.GLM(x)
            x = np.array(x)
            solution[i] = x
            f_x.append(value)
        while(t < self.GenMax):
            #解的变异和交叉
            T = []
            for i in range(self.N):
                x = np.array([0 for i in range(n)],int)
                location = [i for i in range(self.N)]
                location.remove(i)
                k = np.random.choice(location,3)
                Pt[i] = P[k[0]] + self.F * (P[k[1]] - P[k[2]])
                for j in range(n):
                    if Pt[i][j] >= 0.5:
                        x[j] = 1
                    else:
                        x[j] = 0
                T.append(x)
                for j in range(n):
                    rnd = random.random()
                    if rnd < self.Cr: 
                        T[i][j] = solution[i][j]
                        Pt[i][j] = P[i][j]
            f_T = []
            for i in range(self.N):
                T[i],value = self.GLM(T[i])
                f_T.append(value)
            for i in range(self.N):
                if f_T[i] > f_x[i]:
                    solution[i] = T[i]
                    P[i] = Pt[i]
                    f_x[i] = f_T[i]
            #反向测试搜索
            for i in range(self.N):
                #1)、反向个体
                x = np.array([0 for i in range(n)],int)
                for j in range(n):
                    theta = random.random()
                    P2[i][j] = 1 - P[i][j] * theta
                    if P2[i][j] >=0.5:
                        x[j] = 1
                    else:
                        x[j] = 0
                #2)、GLM
                x,value = self.GLM(x)
                x = np.array(x,int)
                #3)、判断
                if value > f_x[i]:
                    solution[i] = x
                    P[i] = P2[i]
                    f_x[i] = value
                 
            #精英局部搜索
            solution = np.array(self.LocalSearch(solution,3),int)
            f_x = [sum(solution[i] * self.price) for i in range(len(solution))]
            self.pbest.append(max(f_x))
            max_solution = solution[f_x.index(max(f_x))]
            if self.pbest[t] >= self.OptimalValue:
                self.OptimalValue = self.pbest[t]
                self.fbest = max_solution
            else:
                f_x[f_x.index(self.pbest[t])] = self.OptimalValue
                self.pbest[t] = self.OptimalValue
                solution[f_x.index(max(f_x))] = self.fbest
            if self.OptimalValue == self.KnSolution:
                break
            t = t + 1
