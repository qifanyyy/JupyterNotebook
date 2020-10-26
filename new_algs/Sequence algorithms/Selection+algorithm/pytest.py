import math
import random
import numpy as np
import time
import matplotlib.pyplot as plt

Inf = 999999999999999

# 求和函数，计算解的背包重量 or 背包中物品总价格
def sum_weight(solution,Dn):
    count = 0
    for i in range(0,len(solution)):
        if solution[i] == 1:
            count += Dn[i]
    return count
##克隆选择算法
# 适应度函数，计算每个解的适应度，罚函数法
def FitnessFun(Pn,Wn,x,C,k):
    fx = sum(x*Pn)
    gx = sum(x*Wn) - C
    Fx = fx-k*max(gx,0)
    return Fx
# 亲和突变
def mutation(solution,Pm):
    n = len(solution[0])
    m = random.randint(1,11)
    new_solution = solution
    for i in range(0,len(solution)):
        ismutation = random.random()
        if ismutation >= Pm:
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
# Input：种群规模N,最大迭代次数GenMax,克隆选择率alpha,突变率Pm,募集率mu,罚因子k
def CSA(Cn,Wn,W,N,GenMax,alpha,Pm,mu,k):
    n = len(Cn)
    solution = np.random.randint(0,2,(N,n)) #初始种群，设置初始代数t=0
    t = 0
    Gbest = [solution[0][i] for i in range(0,n)]
    Pbest = [] 
    OptimalValue = sum_weight(Gbest,Cn)
    #停止准则：t<GenMax?
    while t < GenMax:
        aff = [FitnessFun(Cn,Wn,item,W,k) for item in solution]
        B = []
        aff_B = []
        #依据抗体-抗原亲和度，选择亲和度较大的|alpha*N|个抗体，构成种群B
        for i in range(0,math.ceil(alpha*N)):
            location = aff.index(max(aff))
            aff_B.append(aff[location])
            aff[location] = -1
            B.append([item for item in solution[location]])
        B = np.array(B,int)
        C = []
        #对种群B执行克隆操作，得到临时种群C，克隆规模与抗体-抗原亲和度成正比
        for i in range(0,len(B)):
            Nc = math.ceil(N*(aff_B[i]/sum(aff_B)))
            for j in range(0,Nc):
                C.append([item for item in B[i]])
        C = np.array(C,int)
        #对克隆临时种群C进行高频超变异，得到种群D
        D = mutation(C,Pm)
        aff_D = [FitnessFun(Cn,Wn,item,W,k) for item in D]
        E = []
        aff_E = []
        #从D中选择亲和力较大的N个抗体，得到种群E
        for i in range(0,N):
            location = aff_D.index(max(aff_D))
            aff_E.append(aff_D[location])
            aff_D[location] = -1
            E.append([item for item in D[location]])
        E = np.array(E,int)
        #随机产生|mu*N|个抗体代替E中亲和力较低的抗体
        for i in range(0,math.floor(mu*N)):
            location = aff_E.index(min(aff_E))
            aff_E[location] = Inf
            E[location] = np.random.randint(0,2,n)
        #置solution <-- E,t <-- t+1
        solution = E
        aff_solution = [FitnessFun(Cn,Wn,item,W,k) for item in solution]
        location = aff_solution.index(max(aff_solution))
        max_solution = solution[location]
        Pbest.append(sum_weight(max_solution,Cn))
        if Pbest[t] >= OptimalValue:
            OptimalValue = Pbest[t]
            Gbest = max_solution
        t += 1
    return OptimalValue,Gbest,Pbest
##改进克隆选择算法
# 适应度函数，计算每个解的适应度
def affinity(Pn,Wn,x,C):
    Fx = sum(x*Pn)
    Gx = sum(x*Wn) - C
    if Gx <= 0:
        aff = Fx
    else:
        aff = 1/(Gx + 1)
    return aff
# 生成基因库
def GenePool(n,sigma):
    if n % sigma == 0:
        m = int(n/sigma)
        l1 = l2 =sigma
    else:
        m = math.floor(n/sigma) + 1
        l1 = sigma
        l2 = n - (m - 1) * sigma
    Ge = []
    for i in range(0,m):
        if i < m:
            Ge.append(np.random.randint(0,2,l1))
        else:
            Ge.append(np.random.randint(0,2,1,l2))                   
    return Ge
# 受体编辑
#对于待编辑抗体，若rand <= Tr，随机产生一个编辑起点q，否则对下一个抗体进行操作
def ReceptorEditing(solution,Tr,sigma):
    n = len(solution[0])
    new_solution = solution
    for i in range(0,len(solution)):
        rand_num = random.random()
        if rand_num <= Tr:
            q = random.randint(0,len(solution[i]))
        else:
            continue
        Ge= GenePool(n,sigma)
        rand = random.randint(0,len(Ge)-1)
        Ge = Ge[rand]
        if q + len(Ge) <= n:
            new_solution[i][q:q+len(Ge)] = Ge
        else:
            new_solution[i][q:n] = Ge[0:n-q]
            new_solution[i][0:len(Ge)-(n-q)] = Ge[n-q:len(Ge)]
    return new_solution
# 解的修复/改进，依照价值密度
def RepairSolution(Cn,Wn,Gn,W):
    rho = [Cn[i]/Wn[i] for i in range(0,len(Cn))]
    sigma = [Cn[i]/Wn[i] for i in range(0,len(Cn))]
    if sum_weight(Gn,Wn) > W:
        for i in range(0,len(rho)):
            if Gn[i] == 0:
                rho[i] = Inf
        while True:
            location = rho.index(min(rho))
            rho[location] = Inf
            if sum_weight(Gn,Wn) > W:
                Gn[location] = 0
            else:
                break
    if sum_weight(Gn,Wn) < W:
        for i in range(0,len(rho)):
            if Gn[i] == 1:
                sigma[i] = -1
        while True:
            location = sigma.index(max(sigma))
            sigma[location] = -1;
            if sum_weight(Gn,Wn) + Wn[location] <= W:
                Gn[location] = 1
            else:
                break
    return Gn
#Input：种群规模N,最大迭代次数GenMax,基因段长度sigma,克隆选择率alpha,编辑率Tr
def ImCSA(Cn,Wn,W,N,GenMax,sigma,alpha,Tr):
    n = len(Cn)
    solution = np.random.randint(0,2,(N,n)) #随机产生规模为N的初始种群，置t = 0
    t = 0
    Gbest = [solution[0][i] for i in range(0,n)] #全局最优解
    Pbest = []  #局部最优值
    OptimalValue = sum_weight(Gbest,Cn) #全局最优值
    #停止准则：t < GenMax?
    while t < GenMax:
        #抗体评价：计算solution中各抗体亲和度
        aff = [affinity(Cn,Wn,item,W) for item in solution]
        aff_B = []
        B = []
        #免疫克隆：1）、选择solution中亲和力较大的|alpha*N|个抗体构成种群B
        for i in range(0,math.ceil(alpha*N)):
            location = aff.index(max(aff))
            aff_B.append(aff[location])
            aff[location] = -1
            B.append([item for item in solution[location]])
        B = np.array(B,int)
        C = []
        #免疫克隆：2）、对B中抗体按照亲和力比例克隆，获得克隆群C
        for i in range(0,len(B)):
            Nc = math.ceil(N*(aff_B[i]/sum(aff_B)))
            for k in range(0,Nc):
                C.append([item for item in B[i]])
        C = np.array(C,int)
        #受体编辑：对群C中每个抗体执行RE操作，获得群体D
        D = ReceptorEditing(C,Tr,sigma)
        #约束处理：对群D中每个抗体经解的修复/改进，获得群体E
        E = [RepairSolution(Cn,Wn,item,W) for item in D]
        aff_E = [affinity(Cn,Wn,item,W) for item in E]
        aff_solution = []
        #免疫选择：取群体E中亲和力较大的N个抗体构成群体P.置solution <- P
        for i in range(0,N):
            location = aff_E.index(max(aff_E))
            aff_solution.append(aff_E[location])
            aff_E[location] = -1
            solution[i] = E[location]
        #判断当前最优解是否大于当前全局最优解
        location = aff_solution.index(max(aff_solution))
        max_solution = solution[location]
        Pbest.append(sum_weight(max_solution,Cn))
        if Pbest[t] >= OptimalValue:
            OptimalValue = Pbest[t]
            Gbest = max_solution
        t += 1
    return OptimalValue,Gbest,Pbest
#
Cn = [220,208,198,192,180,180,165 ,162,160,
    158,155,130,125,122,120,118,115,110,105,101,
    100,100,98,96,95,90,88,82,80,77,75,73,72,70,
    69,66,65,63,60,58,56,50,30,20,15,10,8,5,3,1]  #物品价格
Wn = [80,82,85,70,72,70,66,50,55,25,50,
    55,40,48,50,32,22,60,30,32,40,38,35,32,25,28,
    30,22,50,30,45,30,60,50,20,65,20,25,30,10,20,
    25,15,10,10,10,4,4,2,1]  #物品重量
W = 1000  #背包最大承重量
N = 100  #种群规模
alpha = 0.4  #克隆选择率
Tr = 0.9   #编辑率
sigma = 4  #基因段长度
GenMax = 1000  #最大迭代代数
Pm = 1/len(Cn) #突变率
mu = 0.1 #募集率
k = 10 * sum(Cn)/sum(Wn) #罚因子
start = time.clock()
OptimalValue,Gbest,Pbest = CSA(Cn,Wn,W,N,GenMax,alpha,Pm,mu,k)
end = time.clock()
print('用时：',end - start)
print('最优值为：',OptimalValue)
print('最优解为：',Gbest)
x = np.arange(0,GenMax,1)
Pbest = np.array(Pbest)
plt.figure(num = 1)
plt.plot(x,Pbest,'r-.',linewidth = 1)
plt.xlabel('Generation',fontsize = 'medium')
plt.ylabel('Single generation optimal solution',fontsize = 'medium')
plt.title('Clonal Selection Algorithm')
#
start = time.clock()
OptimalValue,Gbest,Pbest = ImCSA(Cn,Wn,W,N,GenMax,sigma,alpha,Tr)
end = time.clock()
print('用时：',end - start,'s')
print('最优值为：',OptimalValue)
print('最优解为：',Gbest)
x = np.arange(0,GenMax,1)
Pbest = np.array(Pbest)
plt.figure(num = 2)
plt.plot(x,Pbest,'r-.',linewidth = 1)
plt.xlabel('Generation',fontsize = 'medium')
plt.ylabel('Single generation optimal solution',fontsize = 'medium')
plt.title('Improved Clonal Selection Algorithm')
plt.show()
