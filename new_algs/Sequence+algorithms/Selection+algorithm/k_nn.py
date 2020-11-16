import numpy as np
import pandas as pd
from operator import itemgetter
from collections import Counter
import matplotlib.pyplot as plt
from sklearn import neighbors
import arff
import sys

# returns the majority class of k-nearest neighbors of a given point
# given a dataset and their classes
# accepts the dataset (with classes as the last column), point to which class is to be assigned and the value of k
# all vectors/matrices are numpy arrays
def k_nearest_neighbors(data, point, k):
    features = data.shape[1] - 1
    # stores the squared euclidean distance and the class of a point in the dataset
    point_map = []
    for index,row in data.iterrows():
        dist = get_distance(point, row[0:features])
        point_map.append([dist, row[features]])

    # sort the data points by distance
    point_map = sorted(point_map, key=itemgetter(0))
    # select the closest k neighbors
    point_map = point_map[0:k]
    classes = map(itemgetter(1), point_map)
    return most_common(classes)


# returns the squared euclidean distance between given points
def get_distance(point1, point2):
    diff = point1-point2
    return np.dot(diff, diff)

def most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

# predicts the test data using k-nearest neighbors algorithm
# returns a dictionary of correctly and incorrectly identified class counts
def get_accuracy(train_data, test_data, k):
    target_attribute = train_data.columns[-1]
    #prediction = []
    #for index,row in test_data.iterrows():
    #    prediction.append(k_nearest_neighbors(train_data, row[0:len(row)-1], k))
    clf = neighbors.KNeighborsClassifier(k)
    features = train_data.columns[0:len(train_data.columns)-1]
    clf.fit(train_data[features], train_data[target_attribute])
    prediction = clf.predict(test_data[features])

    correct_count = {}
    incorrect_count = {}
    for val in test_data[target_attribute].unique():
        correct_count[val] = 0
        incorrect_count[val] = 0

    for index,row in test_data.iterrows():
        if prediction[index] == row[target_attribute]:
            correct_count[row[target_attribute]] += 1
        else:
            incorrect_count[row[target_attribute]] += 1

    return correct_count, incorrect_count


def main():
    if len(sys.argv) != 4:
        print ("Invalid number of arguments!\nUsage: \npython ", sys.argv[0], " <TRAINING_DATA> <TEST_DATA> <k>\n")
        quit()

    train_data = pd.read_csv(sys.argv[1])
    test_data = pd.read_csv(sys.argv[2])

    k = int(sys.argv[3])
    features = 200
    vec = range(features)
    vec.append(-1)
    train_data = train_data[vec]
    test_data = test_data[vec]

    correct_count, incorrect_count = get_accuracy(train_data, test_data, k)

    p1 = plt.bar(range(len(correct_count)), correct_count.values(), align='center', color='g')
    p2 = plt.bar(range(len(incorrect_count)), incorrect_count.values(), align='center', color='r', bottom=correct_count.values())
    plt.xticks(range(len(correct_count)), correct_count.keys())
    plt.legend((p1[0], p2[0]), ('Correct', 'Incorrect'))
    plt.ylabel('Number of data points')
    plt.show(block=False)

    correct_count_total = sum(correct_count.values())
    incorrect_count_total = sum(incorrect_count.values())
    print ("Total correct predictions: ", correct_count_total)
    print ("Total incorrect predictions: ", incorrect_count_total)
    print ("Prediction accuracy: ", float(correct_count_total)/len(test_data))

    plt.show()

if __name__ == "__main__":
    main()