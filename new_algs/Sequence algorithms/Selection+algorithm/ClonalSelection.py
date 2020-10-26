import math
import random
import numpy as np
import matplotlib.pyplot as plt
'''
improved clonal selection algorithm
Input：poplulation size : N
       maximum number of iteration : GenMax
       genic size : sigma
       clonal selection rate : alpha
       mutation rate : Tr
'''
class ImCSA():
    def __init__(self,price,weight,b,N,GenMax,sigma,alpha,Tr,KnSolution,vsort):
        self.price = price
        self.weight = weight
        self.N = N
        self.GenMax = GenMax
        self.b = b
        self.parameter = {'sigma': sigma,
                          'alpha': alpha,
                          'Tr': Tr}
        self.KnSolution = KnSolution
        self.vsort = vsort
        self.OptimalValue = 0
        self.fbest = []
        self.Pbest = []
    # Fitness function ,calculate the fitness of each solution
    def affinity(self,x):
        aff = sum(x*self.price)
        return aff
    # Segment variation
    def GeneMutation(self,x):
        n = len(x)
        rand_num = random.random()
        q = random.randint(1,6)
        if rand_num <= self.parameter['Tr']:
            evl_rand = np.random.randint(0,49,q)
            for temp in evl_rand:
                x[temp] = 1 - x[temp]
            x = self.RepairSolution(x)
        return x
    # Solution Repair/Improvement,according to value density
    def RepairSolution(self,x):
        n = len(self.price)
        m = len(self.b)
        Gn = [0 for i in range(n)]
        s = [0 for i in range(m)]
        value = 0
        # Repair
        for i in range(n):
            flag = 0
            if x[self.vsort[i]] == 1:
                for j in range(m):
                    if s[j] + self.weight[j][self.vsort[i]] > self.b[j]:
                        flag = 1
                        break
                if flag == 0:
                    Gn[self.vsort[i]] = 1
                    value += self.price[self.vsort[i]]
                    for j in range(m):
                        s[j] += self.weight[j][self.vsort[i]]
        #Improvement
        for i in range(n):
            flag = 0
            if Gn[self.vsort[i]] == 0:
                for j in range(m):
                    if s[j] + self.weight[j][self.vsort[i]] > self.b[j]:
                        flag = 1
                        break
                if flag == 0:
                    Gn[self.vsort[i]] = 1
                    value += self.price[self.vsort[i]]
                    for j in range(m):
                        s[j] += self.weight[j][self.vsort[i]]
        return Gn
    # Elite local search
    def LocalSearch(self,Gn):
        n = len(Gn[0])
        q = random.randint(1,5)
        aff_min = [self.affinity(temp) for temp in Gn]
        aff = [self.affinity(temp) for temp in Gn]
        for i in range(q):
            location = aff.index(max(aff))
            aff[location] = -1
            location_min = aff.index(min(aff_min))
            aff_min[location_min] = 99999999999999999999
            max_solution = [Gn[location][i] for i in range(len(Gn[location]))]
            temp_solution = [Gn[location][i] for i in range(len(Gn[location]))]
            rand_num = random.random()
            evl_rand = np.random.randint(0,49,3)
            for temp in evl_rand:
                temp_solution[temp] = 1 - temp_solution[temp]
            solution = self.RepairSolution(temp_solution)
            if sum(solution*self.price) >= sum(Gn[location_min]*self.price):
                Gn[location_min] = solution
        return Gn
    def ImCSA(self):
        n = len(self.price)
        # Randomly generate an initial population of size N, set t = 0
        solution = np.random.randint(0,2,(self.N,n))
        solution = np.array([self.RepairSolution(temp) for temp in solution])
        t = 0
        # Stopping criterion：t < GenMax?
        while t < self.GenMax:
            # Antibody evaluation: the affinity of each antibody
            # in the 'solution' was calculated
            aff_solution = [self.affinity(temp) for temp in solution]
            aff_B = []
            B = []
            # Immune clone：
            # 1）、The |alpha*N| antibodies with high affinity in 'solution'
            #      were selected to constitute population B
            for i in range(0,int(math.ceil(self.parameter['alpha']*self.N))):
                location = aff_solution.index(max(aff_solution))
                aff_B.append(aff_solution[location])
                aff_solution[location] = -1
                B.append([item for item in solution[location]])
            B = np.array(B,int)
            C = []
            # Immune clone：
            # 2）、The antibody in B was cloned according to the affinity
            #      ratio to obtain clonal group C
            k1 = int(0.5 * math.ceil(self.parameter['alpha']*self.N))
            k2 = k1 + int(0.3 * math.ceil(self.parameter['alpha']*self.N))
            for i in range(0,len(B)):
                if i <= k1:
                    clone = 5
                if i > k1 and i <=k2:
                    clone = 2
                else:
                    clone = 1
                for k in range(0,clone):
                    C.append([item for item in B[i]])
            C = np.array(C,int)
            # Gene segment variation:
            #           perform gene segment variation operation for each
            #           antibody in group C to obtain population D
            D = np.array([self.GeneMutation(item) for item in C])
            # Constraint treatment: each antibody in group D was Repaired/Improved
            #                      to obtain group E
            E = np.array([self.RepairSolution(item) for item in D])
            # The elitist local search of group E yields group F
            F = np.array(self.LocalSearch(E))
            aff_f = [self.affinity(temp) for temp in F]
            aff_solution = []
            # Immunological selection:
            #          N antibodies with high affinity in group E were used to
            #          constitute group p. set solution <- p
            for i in range(0,int(self.N*0.5)):
                location = aff_f.index(max(aff_f))
                aff_solution.append(aff_f[location])
                aff_f[location] = -1
                solution[i] = F[location]
            # Determine whether the current optimal solution is greater
            # than the current global optimal solution
            location = aff_solution.index(max(aff_solution))
            max_solution = solution[location]
            self.Pbest.append(sum(max_solution*self.price))
            if self.Pbest[t] >= self.OptimalValue:
                self.OptimalValue = self.Pbest[t]
                self.fbest = max_solution
            else:
                self.Pbest[t] = self.OptimalValue
                solution[location] = self.fbest
            if self.OptimalValue == self.KnSolution:
                break
            for i in range(int(self.N*0.5),self.N):
                solution[i] = self.RepairSolution(np.random.randint(0,2,n))       
            t += 1
    def printResult(self):
        x = np.arange(0,self.GenMax,1)
        Pbest = np.array(self.Pbest)
        plt.figure(num = 1)
        plt.plot(x,self.Pbest,'r-.',linewidth = 1)
        plt.xlabel('Generation',fontsize = 'medium')
        plt.ylabel('Single generation optimal solution',fontsize = 'medium')
        plt.title('Improved Clonal Selection Algorithm')
        plt.show()
##克隆选择算法
# Input：种群规模N,最大迭代次数GenMax,克隆选择率alpha,突变率Pm,募集率mu,罚因子k
class CSA():
    def __init__(self,price,weight,b,N,GenMax,alpha,Pm,mu,k,KnSolution):
        self.b = b
        self.price = price
        self.weight = weight
        self.N = N
        self.GenMax = GenMax
        self.parameter = {'alpha': alpha,
                          'Pm': Pm,
                          'mu': mu,
                          'k': k}
        self.Inf = 999999999999999
        self.KnSolution = KnSolution
        self.OptimalValue = 0
        self.fbest = []
        self.Pbest = []
        self.fitness = []
    
    def is_FeaSol(self,solution):
        gx = 0
        for i in range(len(self.b)):
            if sum(solution*self.weight[i]) <= self.b[i]:
                continue
            if sum(solution*self.weight[i]) > self.b[i]:
                gx += sum(solution*self.weight[i]) - self.b[i]
        return gx
    # 适应度函数，计算每个解的适应度，罚函数法
    def FitnessFun(self,solution):
        self.fitness = []
        for i in range(0,len(solution)):
            x = solution[i]
            fx = sum(x*self.price)
            Fx = 0
            gx = self.is_FeaSol(x)
            Fx = fx-self.parameter['k']*max(gx,0)
            self.fitness.append(Fx)
        #return Fx
    '''
    # 适应度函数，计算每个解的适应度
    def affinity(self,solution):
        self.fitness = []
        for i in range(0,len(solution)):
            x = solution[i]
            Fx = sum(x*self.price)
            Gx = [sum(x*self.weight[item]) - self.b[item] for item in range(0,len(self.b))]
            is_feasible = True
            for item in Gx:
                if item > 0:
                    is_feasible = False
                    break
            if is_feasible:
                aff = Fx
            else:
                aff = 1/(sum([abs(item) for item in Gx]) + 1)
            self.fitness.append(aff)
    '''
    # 亲和突变
    def mutation(self,solution):
        n = len(solution[0])
        m = random.randint(1,int(len(self.price)/5))
        new_solution = solution
        for i in range(0,len(solution)):
            ismutation = random.random()
            if ismutation >= self.parameter['Pm']:
                q = random.randint(0,len(solution[i]))
            else:
                continue
            Ge = np.random.randint(0,2,m)
            if q + m <= n:
                new_solution[i][q:q+m] = Ge
            else:
                new_solution[i][q:n] = Ge[0:n-q]
                new_solution[i][0:m-(n-q)] = Ge[n-q:m]
        return new_solution
    def CSA(self):
        n = len(self.price)
        solution = np.random.randint(0,2,(self.N,n)) #初始种群，设置初始代数t=0
        t = 0
        self.fbest = []
        self.OptimalValue = 0
        #停止准则：t<GenMax?
        while t < self.GenMax:
            self.FitnessFun(solution)
            B = []
            aff = []
            #依据抗体-抗原亲和度，选择亲和度较大的|alpha*N|个抗体，构成种群B
            for i in range(0,math.ceil(self.parameter['alpha']*self.N)):
                location = self.fitness.index(max(self.fitness))
                aff.append(self.fitness[location])
                self.fitness[location] = -1
                B.append([item for item in solution[location]])
            self.fitness = aff
            B = np.array(B,int)
            C = []
            #对种群B执行克隆操作，得到临时种群C，克隆规模与抗体-抗原亲和度成正比
            for i in range(0,len(B)):
                Nc = math.ceil(self.N*(self.fitness[i]/sum(self.fitness)))
                for j in range(0,Nc):
                    C.append([item for item in B[i]])
            C = np.array(C,int)
            #对克隆临时种群C进行高频超变异，得到种群D
            D = self.mutation(C)
            self.FitnessFun(D)
            E = []
            aff = []
            #从D中选择亲和力较大的N个抗体，得到种群E
            for i in range(0,self.N):
                location = self.fitness.index(max(self.fitness))
                aff.append(self.fitness[location])
                self.fitness[location] = -1
                E.append([item for item in D[location]])
            self.fitness = aff
            E = np.array(E,int)
            #随机产生|mu*N|个抗体代替E中亲和力较低的抗体
            for i in range(0,math.floor(self.parameter['mu']*self.N)):
                location = self.fitness.index(min(self.fitness))
                self.fitness[location] = self.Inf
                E[location] = np.random.randint(0,2,n)
            #置solution <-- E,t <-- t+1
            solution = E
            self.FitnessFun(solution)
            location = self.fitness.index(max(self.fitness))
            max_solution = solution[location]
            if self.fitness[location] < 0:
                self.Pbest.append(0)
            else:
                self.Pbest.append(sum(max_solution*self.price))
            if self.Pbest[t] >= self.OptimalValue:
                self.OptimalValue = self.Pbest[t]
                self.fbest = max_solution
            else:
                self.Pbest[t] = self.OptimalValue
                solution[location] = self.fbest
            if self.OptimalValue == self.KnSolution:
                break
            t += 1
    def printResult(self):
        x = np.arange(0,self.GenMax,1)
        Pbest = np.array(self.Pbest)
        plt.figure(num = 1)
        plt.plot(x,self.Pbest,'r-.',linewidth = 1)
        plt.xlabel('Generation',fontsize = 'medium')
        plt.ylabel('Single generation optimal solution',fontsize = 'medium')
        plt.title('Clonal Selection Algorithm')
        plt.show()
