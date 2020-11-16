import matplotlib.pyplot as plt


class KNearestNeighbours:

    def __init__(self, trainingData, k, testData, method = 'euclidean'):
        self.k = k
        self.trainingData = trainingData
        self.testData = testData
        self.method = method

    def classify_test_data(self):
        """
        Returns: the classified datapoints
        -------
        """
        classifications = []
        for dataPoint in testData:
            #we want to classify every data point

            #get the k closest points
            closestPoints = self.get_closest_k_points(dataPoint)
            classification = self.classify_point(closestPoints)
            classifications.append(classification)

        return classifications


    def classify_point(self, closestPoints):
        """

        Parameters
        ----------
        closestPoints

        Returns
        -------

        """
        label_counts = []
        for closestPoint in closestPoints:
            # the last column of the dataPoint is the label
            label = closestPoint[-1]
            label_counts.append(label)

        # get the label which occurs the most - thats the classification
        classification = self.most_frequent(label_counts)
        return classification


    def most_frequent(self, list):
        """

        Parameters
        ----------
        list

        Returns
        -------

        """
        return max(set(list), key=list.count)

    def get_closest_k_points(self, dataPoint):
        """
        Parameters
        ----------
        dataPoint: the coordinate of the datapoint to be classified

        Returns
        -------

        """
        distances = []
        for training_point in self.trainingData:
            distance = self.get_distance(training_point, dataPoint)
            distances.append([distance, training_point])




    def plot_data(self):
        """

        Returns
        -------

        """

        plt.scatter(self.trainingData[:,0], self.trainingData[:,1])
        plt.scatter(self.testData[:,0], self.testData[:,1])




    def get_distance(self, point1, point2):
        """

        Parameters
        ----------
        point1
        point2

        Returns
        -------

        """




