import numpy as np
from collections import Counter
from data_loader import DataLoader
import matplotlib.pyplot as plt
import pandas as pd


class KNearestNeighbours:
    """
     model class for K Nearest Neighbours Classification
    """

    def __init__(self):
        self.max_k = 30
        self.best_k = None  # Learned by the system or passed as input by the user
        self.best_acc = None

        # For plotting
        self.k_values = []
        self.accuracy_values = []

        # For optimizing the distance calculation and finding K Nearest neighbors
        self.distance_cache = {}
        self.k_neighbours = {}


    def get_euclidean_distance(self, x1, x2):
        """
            Calculates the Euclidean distance between 2 vectors and caches the distance
        """

        if np.array_equal(x1, x2):
            return 0.0
        else:
            key = (tuple(x1), tuple(x2))
            if key not in self.distance_cache:
                self.distance_cache[key] = np.linalg.norm(x1 - x2)
            return self.distance_cache[key]

    def learn(self, full_dataset, k=None, verbose=False):

        # If k is not provided then k is learned by the model
        if k is None:
            self.best_k, self.best_acc = self.learn_best_k(full_dataset, verbose=verbose)

    def k_nearest_neighbours(self, train_set, predict):
        """
        :param train_set: A list of training data subsets
            each subset is 2-tuple of attributes and corresponding labels
        :param predict: a single data-point whose k nearest neighbors must be determined
        :param k: number of neighbors

        This method is only called if K is not passed by the user and has to learned by the model
        """
        row_key = tuple(predict)
        if row_key not in self.k_neighbours:
            neighbours = []
            for train_attrs, train_labels in train_set:
                for index, row in train_attrs.iterrows():
                    euclidean_distance = self.get_euclidean_distance(row.values, predict)
                    neighbours.append((euclidean_distance, train_labels.iat[index, 0]))

            neighbours = sorted(neighbours, key=lambda x: x[0])[:self.max_k]
            self.k_neighbours[row_key] = neighbours
        return self.k_neighbours[row_key]

    def knn_classify_point(self, train_set, predict, k=3):
        """
        :param train_set: A list of training data subsets
            each subset is 2-tuple of attributes and corresponding labels
        :param predict: a single data-point whose class must be determined
        :param k: number of neighbors
        :return: the predicted label of the single target data-point
        """
        neighbours = self.k_nearest_neighbours(train_set, predict)
        neighbour_classes = [i[1] for i in neighbours][:k]
        selected_class = Counter(neighbour_classes).most_common(1)[0][0]
        return selected_class

    def classify(self, train_set, test_attrs, true_values=None, k=None):
        """
        :param train_set: A list of training data subsets
            each subset is 2-tuple of attributes and corresponding labels
        :param test_attrs: test data for classification
        :param true_values: true_labels of the test set
        :param k: number of neighbors
        :return: the predicted labels of all the data-points in the test set and the accuracy
        """

        if true_values is not None:
            if len(test_attrs) != len(true_values):
                raise ValueError('count mismatch in attributes and labels')

        if k is None:
            k = self.best_k

        predicted_labels = []
        correct = 0
        incorrect = 0
        for index, row in test_attrs.iterrows():
            predicted_label = self.knn_classify_point(train_set, row.values, k=k)
            predicted_labels.append(predicted_label)
            if true_values is not None:
                true_label = true_values.iat[index, 0]
                if predicted_label == true_label:
                    correct += 1
                else:
                    incorrect += 1

        accuracy = None
        if true_values is not None:
            accuracy = correct / (correct + incorrect) * 100

        predicted_labels = pd.DataFrame(np.array(predicted_labels))
        return predicted_labels, accuracy

    def t_fold_cross_validation(self, full_dataset, t=10, k=3):
        avg_accuracy = 0
        for i in range(t):
            test_attrs, test_labels = full_dataset.pop(0)
            accuracy = self.classify(full_dataset, test_attrs, true_values=test_labels, k=k)[1]
            full_dataset.append((test_attrs, test_labels))
            avg_accuracy += accuracy
        return avg_accuracy / 10

    def learn_best_k(self, full_dataset, verbose=False):

        self.k_values = []
        self.accuracy_values = []


        print('Learning in progress...')

        for k in range(1, self.max_k + 1):
            accuracy = self.t_fold_cross_validation(full_dataset, t=10, k=k)
            if verbose:
                print('At k = %d Accuracy = %.3f' % (k, accuracy))
            self.k_values.append(k)
            self.accuracy_values.append(accuracy)

        self.best_acc = max(self.accuracy_values)
        self.best_k = self.k_values[self.accuracy_values.index(self.best_acc)]

        if verbose:
            print('Learned value of k =', self.best_k)

        return self.best_k, self.best_acc

    def plot_accuracy(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.k_values, self.accuracy_values, '.-')

        ymax = self.best_acc
        xmax = self.best_k

        ax.annotate('max at k = %d, acc = %.3f %%' % (xmax, ymax), xy=(xmax, ymax), xytext=(xmax + 3, ymax + 1),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    )
        ax.scatter([xmax], [ymax], c='r')
        plt.xlabel('k')
        plt.ylabel('Accuracy(%)')
        plt.title('Accuracy vs k')
        plt.show()


if __name__ == '__main__':
    dataset = DataLoader.load_full_dataset('./knn-dataset')
    model = KNearestNeighbours()
    print(model.learn_best_k(dataset, verbose=True))
    model.plot_accuracy()
