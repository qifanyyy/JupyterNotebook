# We will build a model to predict new cancer cells based on cancer dataset using KNN
"""
KNN ALGORITHM FOR PREDICTING CANCER CELLS
import modules
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

"""
------------INIT OBJECT OF LOAD BREAST CANCER CLASS---------------------------------------------------
                  output keys and target names
"""
# init object of breast cancer dataset
breast_cancer_dataset = load_breast_cancer()

# print the breast cancer dataset keys
print("Sample Images Keys: {}".format(breast_cancer_dataset.keys()))

# print the breast cancer dataset target names
print("Sample Images Target Names: {}".format(breast_cancer_dataset.target_names))

# print 5 sample data
print("Sample Data: \n  {}".format(breast_cancer_dataset.data))

# print feature names
print("feature names: {}".format(breast_cancer_dataset.feature_names))

# print target
print("Target: {}".format(breast_cancer_dataset.target))

# split the data to train and test dataset
X_train, X_test, y_train, y_test = train_test_split(breast_cancer_dataset.data, breast_cancer_dataset.target, stratify=breast_cancer_dataset.target, random_state=0)

# print the split
print("X_train: {}".format(X_train.shape))
print("X_test: {}".format(X_test.shape))
print("y_train: {}".format(y_train.shape))
print("y_test: {}".format(y_test.shape))

# init knn algorithm, neighbor default = 5
knn = KNeighborsClassifier(n_neighbors=7)

# train the classifier on dataset
knn.fit(X_train, y_train)

# print accuracy
print("Accuracy of Knn on Training set: {:.3f}".format(knn.score(X_train, y_train)))
print("Accuracy of Knn on Test set: {:.3f}".format(knn.score(X_test, y_test)))

"""
------------------------------TUNNING OUR PARAMETER--------------------------------------------------------------------
we will try out a number of k neighbors to see which one yields the best result
"""

# Since we have splitted our dataset already, lets go ahead and declare two empty list
training_accuracy = []
test_accuracy = []

# define a range of neighbors
neighbors_settings = range(1,11)

# loop through no of neighbors
for n_neighbors in neighbors_settings:
    # declare the KNeighborClassifier object and asigning n_neighbors as argument
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)

    # train the classifier
    clf.fit(X_train, y_train)

    # append the score of accuracy to empty list
    training_accuracy.append(clf.score(X_train, y_train))
    test_accuracy.append(clf.score(X_test, y_test))

# visualize our result using plt
plt.plot(neighbors_settings, training_accuracy, label = "Accuracy on Training")
plt.plot(neighbors_settings, test_accuracy, label = "Accuracy on Test")

# y axis
plt.ylabel("Accuracy")
plt.xlabel("Number of Neighbors")
plt.legend
plt.show()



