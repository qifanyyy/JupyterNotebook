import numpy as np

#build N choose K table

maxN = 300; # !!!!!! you might want to increase it if m > 300 !!!!

nCk = [[0]*maxN for i in range(maxN)]
nCk[0][0] = 1
for n in range(maxN):
    nCk[n][0] = 1
    for k in range(1, n+1):
        nCk[n][k] = nCk[n - 1][k] + nCk[n - 1][k - 1]

class OneUniform:
    def __init__(self, p, m):
        super().__init__()
        self.m = m
        self.p = p
        self.T = [0]*(self.m + 1)
        self.P = [ 1 - (1 - self.p)**i for i in range(self.m+1)]

    def compute(self):
        for i in range(self.m - 1, 0, -1):
            self.T[i] = self.compT(i)
    
    def getConvTime(self):
        return self.T[1]

    def compT(self, i):
        sum = 0.0
        for x in range(1, self.m - i + 1):
            sum += self.T[i + x] * nCk[self.m - i][x] * (self.P[i] ** x) * (1 - self.P[i])**(self.m - i - x)
        return (1 + sum) / (1 - (1 - self.P[i])**(self.m - i))
    
# todo make it fatser
class FourUniform:
    

    def __init__(self, p, q, group):
        super().__init__()
        self.p = p
        self.q = q #p'
        self.group = group
        self.dim = len(self.group)
        self.T = self.initT()


    def selectSum(self, g, car):
        sum = 0.0
        for m in car:
            sum += m
        return car[g], sum - car[g]

    def P(self, x, y):
        return 1 - ((1 - self.p)**x) * (1 - self.q)**y 
    
    # probability of to add one car in group G
    def PGr(self, g, car): 
        x, y = self.selectSum(g, car)
        return self.P(x, y)
    
    # goupe number, number car to add to the group
    def coefGr(self, g, car, toAdd):
        p = self.PGr(g, car)
        nonLeader = self.group[g] - car[g]
        return nCk[nonLeader][toAdd[g]] *(p ** toAdd[g]) * (1 - p) ** (nonLeader - toAdd[g])

    def coef(self, car, toAdd):
        prod = 1
        for g in range(len(car)):
            prod *= self.coefGr(g, car, toAdd)
        return prod

    def compT(self, i, j, k, l):
        sum = 0.0
        for x in range(0, self.group[0] - i + 1):
            for y in range(0, self.group[1] - j + 1):
                for z in range(0, self.group[2] - k + 1):
                    for t in range(0, self.group[3] - l + 1):
                        if x == 0 and y == 0 and z == 0 and t == 0:
                            continue
                        sum += self.coef([i,j,k,l], [x,y,z,t]) * self.T[i + x][j + y][k + z][l + t]
        return (1 + sum) / (1 - self.coef([i,j,k,l], [0,0,0,0]))

    def initT(self, numDim = 0):
        if numDim == self.dim:
            return 0
        return [ self.initT(numDim + 1) for i in range(self.group[numDim] + 1)]

    def compute(self):
        

        for i in range(self.group[0], -1, -1):
            for j in range(self.group[1], -1, -1):
                for k in range(self.group[2], -1, -1):
                    for l in range(self.group[3], -1, -1):
                        if (i == self.group[0] and j == self.group[1] and k == self.group[2] and l == self.group[3]) \
                        or (i == 0 and j == 0 and k == 0 and l == 0):
                            continue
                        self.T[i][j][k][l] = self.compT(i, j, k, l)

    def getConvTime(self):
        return self.T[1][0][0][0]


# very slow
class KUniform:

    def __init__(self, p, q, group):
        super().__init__()
        self.p = p
        self.q = q #p'
        self.group = group
        self.dim = len(self.group)
        self.T = np.zeros(np.add(group, 1))
        self.cache = {}

    def P(self, x, y):
        return 1 - (1 - self.p)**x * (1 - self.q)**y 
    
    # probability of to add one car in group G
    def PGr(self, g, car): 
        if (g, car) in self.cache:
            return self.cache[(g, car)]
        
        x = car[g]
        y = np.sum(car) - car[g]
        self.cache[(g, car)] = self.P(x, y)
        return self.cache[(g, car)]
    
    # goupe number, number car to add to the group
    def coefGr(self, g, car, toAdd):
        p = self.PGr(g, car)
        nonLeader = self.group[g] - car[g]
        return nCk[nonLeader][toAdd[g]] *(p ** toAdd[g]) * (1 - p) ** (nonLeader - toAdd[g])

    def coef(self, car, toAdd):
        prod = 1
        for g in range(len(car)):
            prod *= self.coefGr(g, car, toAdd)
        return prod

    def compT(self, pos):
        sum = 0.0
        for index in np.ndindex(tuple(np.add(np.subtract(self.group, pos), 1))):
            if not np.array_equal(index,(0,) * self.dim):
                sum += self.coef(pos, index) * self.T[tuple(np.add(index, pos))]
        return (1 + sum) / (1 - self.coef(pos, (0,) * self.dim))

    def compute(self):

        for rindex in np.ndindex(self.T.shape):
            index = tuple(np.subtract(np.subtract(self.T.shape,rindex), 1))
            if not(np.array_equal(index,self.group) or np.array_equal(index,(0,) * self.dim)):
                self.T[index] = self.compT(index)

    def getConvTime(self):
        t = (1,) + (0,) * (self.dim - 1)
        return self.T[t]

"""
kuni = FourUniform(0.5, 0.5, [5, 5, 5, 5])
kuni.compute()
print(kuni.getConvTime())

kuni = KUniform(0.5, 0.5, [5, 5, 5, 5])
kuni.compute()
print(kuni.getConvTime())


kuni = OneUniform(0.5, 5*4)
kuni.compute()
print(kuni.getConvTime())"""