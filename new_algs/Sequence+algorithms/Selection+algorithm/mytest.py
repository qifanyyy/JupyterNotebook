from ClonalSelection_unid import CSA
from ClonalSelection_unid import ImCSA
import time
price = [220,208,198,192,180,180,165 ,162,160,
        158,155,130,125,122,120,118,115,110,105,101,
        100,100,98,96,95,90,88,82,80,77,75,73,72,70,
        69,66,65,63,60,58,56,50,30,20,15,10,8,5,3,1]  #物品价格
weight = [80,82,85,70,72,70,66,50,55,25,50,
        55,40,48,50,32,22,60,30,32,40,38,35,32,25,28,
        30,22,50,30,45,30,60,50,20,65,20,25,30,10,20,
        25,15,10,10,10,4,4,2,1]  #物品重量
b = 1000  #背包最大承重量
N = 100  #种群规模
alpha = 0.4  #克隆选择率
Tr = 0.9   #编辑率
sigma = 4  #基因段长度
GenMax = 1000  #最大迭代代数
Pm = 1/len(price) #突变率
mu = 0.1 #募集率
k = 10 * sum(price)/sum(weight) #罚因子
start = time.clock()
#csa = CSA(price,weight,b,N,GenMax,alpha,Pm,mu,k)
#csa.CSA()
'''
Imcsa = ImCSA(price,weight,b,N,GenMax,sigma,alpha,Tr)
Imcsa.ImCSA()
end = time.clock()
print('改进CSA算法')
print('用时：',end - start)
print('最优值为：',Imcsa.OptimalValue)
print('最优解为：',Imcsa.fbest)
Imcsa.printResult()
'''
######
start = time.clock()
csa = CSA(price,weight,b,N,GenMax,alpha,Pm,mu,k)
csa.CSA()
end = time.clock()
print('CSA算法')
print('用时：',end - start)
print('最优值为：',csa.OptimalValue)
print('最优解为：',csa.fbest)
csa.printResult()
