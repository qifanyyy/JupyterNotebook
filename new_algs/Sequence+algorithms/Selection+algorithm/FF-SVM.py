import random
import math
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import cross_val_score
from sklearn import svm
import numpy as np


class FireflyAlgorithm():

    def __init__(self, function):
        self.D = 121  # dimension of the problem (Gene number)
        self.NP = 100  # population size (Firefly number)
        self.nFES = 1  # number of function evaluations (repeate number)
        self.alpha = 1  # alpha parameter,(randomization parameter)
        self.betamin = 0.5  # beta parameter
        self.gamma = 1  # gamma parameter (light intensity coefficency)
        # sort of fireflies according to fitness value
        self.Index = [0] * self.NP
        self.Fireflies = [[np.random.rand() for i in range(self.D)] for j in range(self.NP)]  # firefly agents,
        self.Fireflies_tmp = [[np.random.rand() for i in range(self.D)] for j in range(
            self.NP)]  # intermediate pop
        self.Fitness = [0.0] * self.NP  # fitness values (Accuracy)
        self.I = [0.0] * self.NP  # light intensity
        self.nbest = [0.0] * self.NP  # the best solution found so far
        self.LB = 0  # lower bound
        self.UB = 1  # upper bound
        self.fbest = None  # the best
        self.evaluations = 0
        self.Fun = function

    def alpha_new(self, a):
        delta = 1.0 - math.pow((math.pow(10.0, -4.0) / 0.9), 1.0 / float(a))
        return (1 - delta) * self.alpha

    def sort_ffa(self):  # implementation of bubble sort

        for i in range(self.NP):
            self.Index[i] = i

        for i in range(0, (self.NP - 1)):
            j = i + 1
            for j in range(j, self.NP):
                if (self.I[i] > self.I[j]):
                    z = self.I[i]  # exchange attractiveness
                    self.I[i] = self.I[j]
                    self.I[j] = z
                    z = self.Fitness[i]  # exchange fitness
                    self.Fitness[i] = self.Fitness[j]
                    self.Fitness[j] = z
                    z = self.Index[i]  # exchange indexes
                    self.Index[i] = self.Index[j]
                    self.Index[j] = z


    def replace_ffa(self):  # replace the old population according to the new Index values
        # copy original population to a temporary area
        for i in range(self.NP):
            for j in range(self.D):
                self.Fireflies_tmp[i][j] = self.Fireflies[i][j]

        # generational selection in the sense of an EA
        for i in range(self.NP):
            for j in range(self.D):
                self.Fireflies[i][j] = self.Fireflies_tmp[self.Index[i]][j]

    def FindLimits(self, k):
        for i in range(self.D):
            if self.Fireflies[k][i] < self.LB:
                self.Fireflies[k][i] = self.LB
            if self.Fireflies[k][i] > self.UB:
                self.Fireflies[k][i] = self.UB

    def move_ffa(self):
        for i in range(self.NP):
            scale = abs(self.UB - self.LB)
            for j in range(self.NP):
                r = 0.0
                for k in range(self.D):
                    r += (self.Fireflies[i][k] - self.Fireflies[j][k]) * \
                        (self.Fireflies[i][k] - self.Fireflies[j][k])
                r = math.sqrt(r)
                if self.I[i] > self.I[j]:  # brighter and more attractive
                    beta0 = 1.0
                    beta = (beta0 - self.betamin) * math.exp(-self.gamma * math.pow(r, 2.0)) + self.betamin
                    for k in range(self.D):
                        r = random.uniform(0, 1)
                        tmpf = self.alpha * (r - 0.5) * scale
                        self.Fireflies[i][k] = self.Fireflies[i][
                            k] * (1.0 - beta) + self.Fireflies_tmp[j][k] * beta + tmpf
            self.FindLimits(i)

    def Run(self):
        while self.evaluations < self.nFES:

            # optional reducing of alpha
            #self.alpha = self.alpha_new(self.nFES/self.NP)
            self.evaluations = self.evaluations + 1
            # evaluate new solutions
            for i in range(self.NP):
                self.Fitness[i] = self.Fun(self.Fireflies[i])

                self.I[i] = self.Fitness[i]


            # ranking fireflies by their light intensit
            self.sort_ffa()
            # replace old population
            self.replace_ffa()
            # move all fireflies to the better locations
            self.move_ffa()

        bestFirefly = self.Fireflies[self.NP - 1]

        return bestFirefly

#File which applied
file_ = "File Name: "

df = pd.read_excel(file_)

y = df['Label'].values
X = df.drop('Label', axis=1).values


def evaluation(feature_possibilities):
        feature_possibilities = np.round(feature_possibilities)

        feature_possibilities = feature_possibilities > np.float32(0.5)

        selectedX = X[:, feature_possibilities]

        s = svm.SVC(kernel="poly", C=1)

        loocv = LeaveOneOut()
        evaluation = cross_val_score(s, selectedX, y,  cv=loocv)

        return evaluation.mean()

Algorithm = FireflyAlgorithm(evaluation)
Best = Algorithm.Run()


a = np.round(Best)

feature_take_or_not = a > np.float32(0.7)

print(feature_take_or_not)

print(Best)

true_number = np.array(np.unique(feature_take_or_not, return_counts=True)).T


bestX = X[:, gene_take_or_not]

print(true_number)

s = svm.SVC(kernel="linear")
loocv = LeaveOneOut()
evaluation = cross_val_score(s, bestX, y,  cv=loocv)
print("Final Accuracy: %.6f%% (%.6f%%)" % (evaluation.mean(), evaluation.std()))

total = ((df.drop("Label", axis=1).columns.values, gene_take_or_not, Best))

df2 = pd.DataFrame(total, ["Features", "Selection", "Importance"])
df2.to_excel(f"FF-SVM-Feature-Selection-{file_}", index=False)
