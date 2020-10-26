#import argparse
import time
from myAlgo import *
import simulation as sim
alis = []
N = 15

a = 4
n = math.ceil(math.log(N, 2))
ctrl = True
counts = 0
tStart = time.time()
#qc = shorNormal(N,a)
qc = shorSequential(N, a)
# print(qc)
while ctrl:
    res = sim.single_mySim(qc)
    lis = sim.sort_by_prob(res)
    res = lis[0][0]
    from factorize import cf_ind
    ctrl = not cf_ind(res, 2*n, N, a)
    counts += 1
tEnd = time.time()
print('+'*35)
print("Factorization finish...")
print(f"Number of execution: {counts} ")
t = tEnd-tStart
print(f"Elapsed time: {t:.2f} sec")
