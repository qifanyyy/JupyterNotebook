import matplotlib.pyplot as plt
import numpy as np
import re
from tqdm import tqdm
from operator import itemgetter
import seaborn as sns
import portfolio

algorithms = portfolio.getAlgorithms()
timePoints = portfolio.getTimePoints()
n = timePoints.size
names = portfolio.getNames()

def generatePortfolio(portfolioName):
    class Data:
        x = []
        y = []
        col = []
    data = Data()
    lastUsage = dict()
    for t in tqdm(range(n)):
        name = "portfolios/" + portfolioName + "/" + str(t) + ".cost"
        with open(name) as f:
            f.readline()
            a = 0
            while True:
                l = f.readline()
                if l == "":
                    break
                l = re.findall(r'\d', l)
                for d in l:
                    if d == "1":
                        data.x.append(np.log(timePoints[t])/np.log(10))
                        data.y.append(algorithms[a])
                        lastUsage[algorithms[a]] = t
                    a+=1

    
    lastUsage = list(lastUsage.items())
    lastUsage.sort(key=itemgetter(1, 0))
    algorithmsOrd = [u[0] for u in lastUsage]

    
    plt.figure(figsize=(10,6))
    ax = sns.stripplot(x = data.x, y = data.y, jitter=False, order=algorithmsOrd)
    box = ax.get_position()
    ax.set_position([box.x0+box.width*0.2, box.y0, box.width*0.8, box.height])

    plt.savefig("portfolios/plots/" + portfolioName + ".pdf", bbox_inches='tight')

for name in names:
    generatePortfolio(name)