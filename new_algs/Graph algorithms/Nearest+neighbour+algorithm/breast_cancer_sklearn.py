'''
Python 36
Dataset: 
https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.names
https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/
'''

import numpy as np
import pandas as pd
from sklearn import preprocessing, neighbors, cross_validation

def main():
    df = pd.read_csv('breast_cancer.txt')
    # missing attribute ? mentioned in the dataset
    df.replace('?', -99999, inplace=True)
    # taking out useless attribute as it can effect the KNN algorithm
    df.drop(['id'], 1, inplace=True)
    
    # x is the feature array so taking features only where class is not needed
    X = np.array(df.drop(['class'], 1))
    print(X)
    # y is the label
    Y = np.array(df['class'])
    print(Y)
    
    # splitting x and y into test and train dataset
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2)
    
    # defining the classifier clf
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, Y_train)
    
    # checking the accuracy of test data in the classifier
    accuracy = clf.score(X_test, Y_test)
    print(accuracy)
    
    # testing created data
    example_measures = np.array([[6,2,1,6,6,10,3,9,1], [2,2,1,6,6,3,3,9,1]])
    example_measures = example_measures.reshape(len(example_measures),-1)
    prediction = clf.predict(example_measures)
    # returns either 2 or 4 (2 for benign, 4 for malignant; mentioned in dataset link)
    print(prediction)
    
    return
#enddef

if __name__ == '__main__':
    main()
#endif 