import numpy as np
import random as r
from math import sqrt
from copy import deepcopy
import collections

__author__ = "Michael J. Suggs // mjs3607@uncw.edu"


class KMeansPP:
    """ Brute force representation of the K-Means++ algorithm, an algorithm that
        improves on k-means by incorporating careful seeding. That is, this
        improvement focuses solely on the initialisation of the original
        centroids, seeking to pick centroids which minimises poor clusterings
        that are sometimes found in the standard k-means algorithm.

    """

    def __init__(self, k, data):
        """ Initialises classifier by giving it an arbitrary number of
         pre-defined initial classes.

        :param k: Total number of classification clusters to create
        :param data: Array containing all points represented as lists [[x1,y1],]
        """
        self.k = k
        self.sets = [[] for i in range(k)]
        self.data = [np.asarray(pt) for pt in data]
        # print("Initial data: {}".format(self.data))
        self.centroids = self.generate_centroids(k)

    def generate_centroids(self, k):
        """ Generates centroids in accordance with the k-means++ algorithm.

        :param k: number of centres
        :return:
        """

        cents = []
        cents.append(self.data[r.randint(0, len(self.data) - 1)])

        # D**2 weighting loop
        while len(cents) < k:
            for dp in self.data:
                dist = np.array([min([distance(d, c) for c in cents]) for d in self.data])
                prob = dist / dist.sum()
                cumulative_prob = prob.cumsum()
                r_val = np.random.rand()

                for j, p in enumerate(cumulative_prob):
                    if r_val < p:
                        i = j
                        break

            cents.append(self.data[i])
        return np.asarray(cents)

    def classify(self):
        prev_centroids = np.zeros((self.centroids.shape[0], self.centroids.shape[1]))

        while prev_centroids.all() != self.centroids.all():
            prev_centroids = deepcopy(self.centroids)
            self._classify()
            self.recalc_centroids()

    def _classify(self):
        self.sets = [[] for i in range(self.k)]
        for point in self.data:
            c_dists = [[distance(point, c)] for c in self.centroids]
            min_index, min_value = min(enumerate(c_dists), key=lambda p: p[1])
            # print("min index, min val:\t\t{}, {}".format(min_index, min_value))
            # print("Sets: {}".format(self.sets))
            self.sets[int(min_index)].append(point)

    def recalc_centroids(self):
        for i in range(len(self.sets)):
            set_sum = np.zeros((1, len(self.sets[i][0])))
            for j in range(len(self.sets[i])):
                set_sum += self.sets[i][j]
            self.centroids[i] = set_sum / len(self.sets[i])

    def percent_correct(self):
        for i in range(len(self.sets)):
            count = 0
            for pt in range(len(self.sets[i])):
                if self.sets[i][pt][-1] != i + 1:
                    count += 1

            print("{} of {} points misclassified in set {}.\n".format(
                count, len(self.sets[i]), i + 1))

            print("{}% of points in set {} were classified correctly.\n"
                  "{}% of points in set {} were classified incorrectly.\n".format(
                ((len(self.sets[i]) - count) / len(self.sets[i])) * 100, i + 1,
                (count / len(self.sets[i])) * 100, i + 1))

    def write_output(self, filename):
        with open(filename, 'a') as f:
            for i in range(len(self.sets)):
                f.write("Set {}:\n".format(i + 1))
                for pt in range(len(self.sets[i])):
                    f.write(str(self.sets[i][pt]) + '\n')

                f.write("\n")
            f.write("\n*** END ***\n\n")

    def write_percents(self, filename):
        with open(filename, 'a') as f:
            for i in range(len(self.sets)):
                count = 0
                for pt in range(len(self.sets[i])):
                    if self.sets[i][pt][-1] != i + 1:
                        count += 1

                f.write("{} points misclassified in set {}.\n".format(count, i + 1))

                f.write("{}% of points in set {} were classified correctly.\n"
                      "{}% of points in set {} were classified incorrectly.\n".
                    format((count / len(self.sets[i])) * 100, i + 1,
                    ((len(self.sets[i]) - count) / len(self.sets[i])) * 100, i + 1))

                f.write("\n")
            f.write("\n*** END ***\n\n")


def distance(p1, p2):
    return np.linalg.norm(p2 - p1)

if __name__ == '__main__':
    data = []
    with open("seed_dataset.csv", "r") as f:
        for line in f:
            data.append([float(i) for i in line.split(',')])

    km = KMeansPP(3, data)
    km.classify()
    km.write_output('km_out.txt')
    km.write_percents('km_percents.txt')
    km.percent_correct()
