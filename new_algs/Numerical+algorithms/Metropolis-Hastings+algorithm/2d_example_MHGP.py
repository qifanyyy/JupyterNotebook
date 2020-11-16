import numpy as np
from MHGP import MHGP
from vanillaMH import vanillaMH
import matplotlib.pyplot as plt
%matplotlib inline

def logbananaPosterior(z):
    x = z[0]
    y = z[1]
    A=0.5
    B=0
    C1=3
    C2=3
    return -0.5*(A*(x**2)*(y**2)+(x**2)+(y**2)-2*B*x*y-2*C1*x-2*C2*y)

def bananaPosterior(z):
    return np.exp(logbananaPosterior(z))


bounds = [(-4,9), (-4,9)]
sampler = MHGP(logbananaPosterior, bounds, None, 0.01, 0.1, 0.005, 250, 2000, 20000, 0.001)
samplesTaken, numOfCallsMHGP, covProposal, max_pt_bo, chain, transchain = sampler.RunMHGP()

samplesMH = vanillaMH(bananaPosterior, [-0.5, -0.5], 10000, 2500, [0.01, 0.01])

#get actual values from the banana distribution
actualVals = [] 
data_len = 100
x1 = np.linspace(-0.5,6.0,data_len) 
x2 = np.linspace(-0.75,5.5,data_len) 
X_actual, Y_actual = np.meshgrid(x1,x2)
for i in range(len(X_actual)):
    actualVals.append(bananaPosterior([X_actual[i],Y_actual[i]]))
    
    
MHGP_samples = np.random.permutation(samplesTaken)
MH_samples = np.random.permutation(samplesMH)
MHGP_samples = MHGP_samples[0:1000,:]
MH_samples = MH_samples[0:1000,:]

print('Number of Total Calls to target distribution: ' + str(numOfCallsMHGP))
#plotting the results:
fig = plt.figure()
ax1 = plt.subplot(131)
ax1.set_title('Accepted samples from MHGP')
ax1.set_xlim([-15,15])
ax1.set_ylim([-15,15])
ax1.scatter(MHGP_samples[1:,0],MHGP_samples[1:,1], s=1)
ax2 = plt.subplot(132)
ax2.set_title('Actual Banana Distribution')
ax2.set_xlim([-15,15])
ax2.set_ylim([-15,15])
ax2.contour(X_actual,Y_actual,actualVals,zdir='z')
ax3 = plt.subplot(133)
ax3.set_title('Accepted samples from MH')
ax3.set_xlim([-15,15])
ax3.set_ylim([-15,15])
ax3.scatter(MH_samples[1:,0],MH_samples[1:,1], s=1)


plt.rcParams['figure.figsize'] = 7, 1
plt.rcParams.update({'font.size': 6})
plt.tight_layout()
plt.savefig('banana_plots.png', figsize=(7,1),dpi=150)
plt.show()
plt.close()