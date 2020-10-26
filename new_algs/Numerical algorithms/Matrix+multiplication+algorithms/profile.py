import numpy as np
from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
from read_likwid import LikwidReader

plt.clf()# clear , only need if you have plotted earlier in the code
fig, ax = plt.subplots()

#data = LikwidReader('basic/outsmall/')
#readings = data.make()
#
#x_var, y_var = 'n', 'Runtime [s]'
#xss, yss, l = data.select(readings, x_var, y_var)
#all_ = [(xss[i],yss[i],l[i]) for i in range(len(l))]
#all_.sort(key=lambda x:x[2])
#all_ = all_[8:]+all_[:8]
#xss, yss, l = [ a[0] for a in all_ ], [ a[1] for a in all_ ], [ a[2] for a in all_ ]
#
#pf = np.polyfit([x[0] for x in xss], [y[0] for y in yss], 3)
#xp = np.linspace(min([x[0] for x in xss]),max([x[0] for x in xss]), 50)
#out = np.poly1d(pf)
#
#
#cmap = plt.cm.viridis # - quite like this one too: viridis
#rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, len(xss))))
#for i in range(len(xss)):
#    ax.plot(xss[i], yss[i], color=cmap(0.8*i*(1/len(xss))), marker='.', markersize = 12)
##ax.set_xscale("log")
#ax.plot(xp, out(xp), 'r--', label='poly reg. with: '+str(pf[:2]))

#############################################

data = LikwidReader('DATA/prof_lg_sum/')
readings = data.make()

x_var, y_var = 'n', 'Runtime [s]'
xss, yss, l = data.select(readings, x_var, y_var)
all_ = [(xss[i],yss[i],l[i]) for i in range(len(l))]
all_.sort(key=lambda x:x[2])
#all_ = all_[8:]+all_[:8]
xss, yss, l = [ a[0] for a in all_ ], [ a[1] for a in all_ ], [ a[2] for a in all_ ]

pf = np.polyfit([x[0] for x in xss], [y[0] for y in yss], 2)
xp = np.linspace(min([x[0] for x in xss]),max([x[0] for x in xss]), 50)
out = np.poly1d(pf)

#plt.clf()# clear , only need if you have plotted earlier in the code
#fig, ax = plt.subplots()

cmap = plt.cm.viridis # - quite like this one too: viridis
rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, len(xss))))
for i in range(len(xss)):
    ax.plot(xss[i], yss[i], color=cmap(i*(1/len(xss))), marker='.', label=l[i], markersize = 12)
#ax.set_xscale("log")
#num1 = str(pf[0])
#num1 = round(float(num1[:num1.index('e')]),1)*10**int(num1[num1.index('e')+1:])
#num2 = str(pf[1])
#num2 = round(float(num2[:num2.index('e')]),1)*10**int(num2[num2.index('e')+1:])
ax.plot(xp, out(xp), 'r--')#, label='poly reg. with: '+str(num1)+'$x^{2}$ '+str(num2)+'x')

#############################################


box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#ax.legend(loc='right upper', fancybox=True, shadow=True)
plt.xlabel(x_var)
plt.ylabel(y_var)
plt.title('Optimised Sum Algorithm, n vs Runtime (large matrices)')
plt.plot()
#plt.savefig('filename.png',dpi=500, bbox_inches = 'tight')# dpi is quality dots per inch