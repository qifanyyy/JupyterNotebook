__author__ = 'Nerya Yekutiel'

import numpy as np


class topsis:
    a = None  # Matrix
    w = None  # Weight matrix
    r = None  # Normalisation matrix
    alternatives = None  # Number of alternatives
    criteria = None  # Number of criteria
    rw = None  # Normalisation * Weight matrix
    aNegative = None  # worst alternative
    aPositive = None  # best alternative
    distNeg = None
    distPos = None
    sNegative = None
    sPositive = None
    cPositive = None

    # Return a numpy array with float items
    def floater(self, a):
        ax = []
        for i in a:
            try:
                ix = []
                for j in i:
                    ix.append(float(j))
            except:
                ix = float(i)
                pass
            ax.append(ix)
        return np.array(ax)

    def __init__(self, a, w, j):
        self.a = self.floater(a)
        self.alternatives = len(a)
        self.criteria = len(a[0])
        self.w = self.floater(w)
        print
        self.a
        # self.w = self.w / sum(self.w)
        self.j = self.floater(j)

    # print self.a
    # print self.w
    # print self.j

    # Step 1
    def step1(self):
        self.r = self.a.copy()
        for j in range(self.criteria):
            nm = sum(self.a[:, j] ** 2) ** 0.5
            for i in range(self.alternatives):
                self.r[i, j] = self.a[i, j] / nm

    # Step 2
    def step2(self):
        self.rw = self.r.copy()
        for i in range(self.alternatives):
            self.rw[i] = self.r[i] * self.w

    # Step 3
    def step3(self):
        self.aNegative = []
        self.aPositive = []
        for i in range(self.criteria):
            if self.j[0][i] == 1:
                self.aNegative.append(min(self.rw[:, i]))
                self.aPositive.append(max(self.rw[:, i]))
            else:
                self.aNegative.append(max(self.rw[:, i]))
                self.aPositive.append(min(self.rw[:, i]))

    # Step 4
    def step4(self):
        self.distNeg = self.rw.copy()
        self.distPos = self.rw.copy()
        for j in range(self.criteria):
            for i in range(self.alternatives):
                self.distPos[i][j] = (self.distPos[i][j] - self.aPositive[j]) ** 2
                self.distNeg[i][j] = (self.distNeg[i][j] - self.aNegative[j]) ** 2

        self.sPositive = np.ndarray((self.alternatives, 1))
        self.sNegative = np.ndarray((self.alternatives, 1))

        for i in range(self.alternatives):
            summ = sum(self.distPos[i, :])
            self.sPositive[i] = sum(self.distPos[i, :]) ** 0.5
            self.sNegative[i] = sum(self.distNeg[i, :]) ** 0.5

    # print self.db

    # Step 5
    def step5(self):
        self.cPositive = self.sNegative / (self.sNegative + self.sPositive)
        # print self.siw
        maxPos = -1
        minPos = -1
        max = 0.
        min = 1.
        for i in range(len(self.cPositive)):
            if self.cPositive[i] > max:
                max = self.cPositive[i]
                maxPos = i
            if self.cPositive[i] < min:
                min = self.cPositive[i]
                minPos = i;
        return maxPos, minPos

    def calc(self):
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        return self.step5()
