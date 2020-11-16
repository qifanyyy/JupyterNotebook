import sympy
import math
from CF import better_a
import simulation as sim
from myAlgo import shorNormal
import matplotlib.pyplot as plt
prime_lis=list(sympy.primerange(0, 100))
n_lis = []
for i in range(len(prime_lis)):
    for j in range(i,len(prime_lis)):
        if prime_lis[i]!=prime_lis[j] and prime_lis[i]!=2 and prime_lis[j]!=2:
            to_put=prime_lis[j]*prime_lis[i]
            if to_put<128:
                n_lis.append(to_put)

n_lis = sorted(n_lis)
print(n_lis)
a_lis=[]
for i in n_lis:
    a_lis.append(better_a(i))
print(a_lis)

nor_lis=[]
seq_lis=[]
for i in n_lis:
    n = math.ceil(math.log(i,2))
    nor_lis.append(4*n+2)
    #seq_lis.append(2*n+3)
print(nor_lis)
#print(seq_lis)
t_lis=[]
x_lis=[]
labels=[]
j=0
'''
for i in range(0,len(nor_lis)):
    if nor_lis[i]!=0:
        j+=1
        N = n_lis[i]
        labels.append(str(N))
        x_lis.append(j)
        a = a_lis[i]
        print(N,a)
        t_lis.append(sim.gpuSim(shorNormal(N,a)))

fig, ax = plt.subplots()
bar_plot=plt.bar(x_lis,t_lis,tick_label=labels)
def autolabel(rects):
    for idx,rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                t_lis[idx],
                ha='center', va='bottom', rotation=0)

autolabel(bar_plot)
plt.savefig('qbit.png')
'''

    
