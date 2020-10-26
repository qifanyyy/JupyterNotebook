import math
import random
import numpy as np
import matplotlib.pyplot as plt
##克隆选择算法
# Input：种群规模N,最大迭代次数GenMax,克隆选择率alpha,突变率Pm,募集率mu,罚因子k
class CSA():
    def __init__(self,price,weight,b,N,GenMax,alpha,Pm,mu,k):
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
        self.OptimalValue = 0
        self.fbest = []
        self.Pbest = []
        self.fitness = []
    # 求和函数，计算解的背包重量 or 背包中物品总价格
    def sum_weight(self,solution,Dn):
        count = 0
        for i in range(0,len(solution)):
            if solution[i] == 1:
                count += Dn[i]
        return count
    # 适应度函数，计算每个解的适应度，罚函数法
    def FitnessFun(self,solution):
        self.fitness = []
        for i in range(0,len(solution)):
            x = solution[i]
            fx = self.sum_weight(x,self.price)
            '''
            Fx = 0
            for item in range(0,len(self.b)):
                gx = self.sum_weight(x,self.weight[item]) - self.b[item]
                Fx = Fx + fx-self.parameter['k']*max(gx,0)
            '''
            gx = self.sum_weight(x,self.weight) - self.b
            Fx = fx - self.parameter['k'] * max(gx,0)
            self.fitness.append(Fx)
        #return Fx
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
    # 亲和突变
    def mutation(self,solution):
        n = len(solution[0])
        m = random.randint(1,11)
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
            self.Pbest.append(self.sum_weight(max_solution,self.price))
            if self.Pbest[t] >= self.OptimalValue:
                self.OptimalValue = self.Pbest[t]
                self.fbest = max_solution
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
##改进克隆选择算法
#Input：种群规模N,最大迭代次数GenMax,基因段长度sigma,克隆选择率alpha,编辑率Tr
class ImCSA():
    def __init__(self,price,weight,b,N,GenMax,sigma,alpha,Tr):
        self.price = price
        self.weight = weight
        self.N = N
        self.GenMax = GenMax
        self.b = b
        self.parameter = {'sigma': sigma,
                          'alpha': alpha,
                          'Tr': Tr}
        self.Ge = []
        self.OptimalValue = 0
        self.fbest = []
        self.Pbest = []
        self.aff = []
        self.Inf = 999999999999999
    # 求和函数，计算解的背包重量 or 背包中物品总价格
    def sum_weight(self,solution,Dn):
        count = 0
        for i in range(0,len(solution)):
            if solution[i] == 1:
                count += Dn[i]
        return count
    # 适应度函数，计算每个解的适应度
    def affinity(self,solution):
        self.aff = []
        for i in range(0,len(solution)):
            x = solution[i]
            Fx = sum(x*self.price)
            Gx = sum(x*self.weight) - self.b
            if Gx <= 0:
                aff = Fx
            else:
                aff = 1/(Gx + 1)
            self.aff.append(aff)
    # 生成基因库
    def GenePool(self,n):
        if n % self.parameter['sigma'] == 0:
            m = int(n/self.parameter['sigma'])
            l1 = l2 =self.parameter['sigma']
        else:
            m = math.floor(n/self.parameter['sigma']) + 1
            l1 = self.parameter['sigma']
            l2 = n - (m - 1) * self.parameter['sigma']
        self.Ge = []
        for i in range(0,m):
            if i < m:
                self.Ge.append(np.random.randint(0,2,l1))
            else:
                self.Ge.append(np.random.randint(0,2,1,l2))                   
    # 受体编辑
    #对于待编辑抗体，若rand <= Tr，随机产生一个编辑起点q，否则对下一个抗体进行操作
    def ReceptorEditing(self,solution):
        n = len(solution[0])
        new_solution = solution
        for i in range(0,len(solution)):
            rand_num = random.random()
            if rand_num <= self.parameter['Tr']:
                q = random.randint(0,len(solution[i]))
            else:
                continue
            self.GenePool(n)
            rand = random.randint(0,len(self.Ge)-1)
            Ge = self.Ge[rand]
            if q + len(Ge) <= n:
                new_solution[i][q:q+len(Ge)] = Ge
            else:
                new_solution[i][q:n] = Ge[0:n-q]
                new_solution[i][0:len(Ge)-(n-q)] = Ge[n-q:len(Ge)]
        return new_solution
    # 解的修复/改进，依照价值密度
    def RepairSolution(self,Gn):
        rho = [self.price[i]/self.weight[i] for i in range(0,len(self.price))]
        sigma = [self.price[i]/self.weight[i] for i in range(0,len(self.price))]
        if self.sum_weight(Gn,self.weight) > self.b:
            for i in range(0,len(rho)):
                if Gn[i] == 0:
                    rho[i] = self.Inf
            while True:
                location = rho.index(min(rho))
                rho[location] = self.Inf
                if self.sum_weight(Gn,self.weight) > self.b:
                    Gn[location] = 0
                else:
                    break
        if self.sum_weight(Gn,self.weight) < self.b:
            for i in range(0,len(rho)):
                if Gn[i] == 1:
                    sigma[i] = -1
            while True:
                location = sigma.index(max(sigma))
                sigma[location] = -1;
                if self.sum_weight(Gn,self.weight) + self.weight[location] <= self.b:
                    Gn[location] = 1
                else:
                    break
        return Gn
    def ImCSA(self):
        n = len(self.price)
        solution = np.random.randint(0,2,(self.N,n)) #随机产生规模为N的初始种群，置t = 0
        t = 0
        self.fbest = [] #全局最优解
        self.OptimalValue = 0 #全局最优值
        #停止准则：t < GenMax?
        while t < self.GenMax:
            #抗体评价：计算solution中各抗体亲和度
            self.affinity(solution)
            aff_B = []
            B = []
            #免疫克隆：1）、选择solution中亲和力较大的|alpha*N|个抗体构成种群B
            for i in range(0,math.ceil(self.parameter['alpha']*self.N)):
                location = self.aff.index(max(self.aff))
                aff_B.append(self.aff[location])
                self.aff[location] = -1
                B.append([item for item in solution[location]])
            B = np.array(B,int)
            self.aff = aff_B
            C = []
            #免疫克隆：2）、对B中抗体按照亲和力比例克隆，获得克隆群C
            for i in range(0,len(B)):
                Nc = math.ceil(self.N*(self.aff[i]/sum(self.aff)))
                for k in range(0,Nc):
                    C.append([item for item in B[i]])
            C = np.array(C,int)
            #受体编辑：对群C中每个抗体执行RE操作，获得群体D
            D = self.ReceptorEditing(C)
            #约束处理：对群D中每个抗体经解的修复/改进，获得群体E
            E = [self.RepairSolution(item) for item in D]
            self.affinity(E)
            aff_solution = []
            #免疫选择：取群体E中亲和力较大的N个抗体构成群体P.置solution <- P
            for i in range(0,self.N):
                location = self.aff.index(max(self.aff))
                aff_solution.append(self.aff[location])
                self.aff[location] = -1
                solution[i] = E[location]
            #判断当前最优解是否大于当前全局最优解
            location = aff_solution.index(max(aff_solution))
            max_solution = solution[location]
            self.Pbest.append(self.sum_weight(max_solution,self.price))
            if self.Pbest[t] >= self.OptimalValue:
                self.OptimalValue = self.Pbest[t]
                self.fbest = max_solution
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

