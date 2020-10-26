#importing the dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
#pandas for using the dataset
#sklearn i.e scikit learn is the machine learning library for using the algorithms

#creating a dataframe of the dataset to work with the dataset
dataset=pd.read_csv('500_Person_Gender_Height_Weight_Index.csv')

#creating features list
#features list is a list of tuples having height and weight of each person
features=list(zip(dataset['Height'],dataset['Weight']))

#creating an array of target values(i.e the one which we are predicting )
value=dataset['Gender']

#splitting the dataset into train and test set 
#X_train contains the features for training the model
#X_test contains the features for testing the model
#y_train contains the target values for training the model
#y_train contains the real target values 
X_train,X_test,y_train,y_test=train_test_split(features,value,test_size=0.3)

#Using Decision trees
#importing dependency
from sklearn import tree
#creating a decision tree classifier
tree_model=tree.DecisionTreeClassifier()
#training the model 
tree_model=tree_model.fit(X_train,y_train)
#predicting the target values i.e gender for the test set
tree_predicted =tree_model.predict(X_test)


#Using k-nearest neighbours
#importing dependency
from sklearn.neighbors import KNeighborsClassifier
#creating a k-nearest neighbour  classifier and setting nearest_neighbours i.e n to 3
knn_model=KNeighborsClassifier(n_neighbors=3)
#training the model 
knn_model.fit(X_train,y_train)
#predicting the target values i.e gender for the test set
knn_predicted=knn_model.predict(X_test)


#using Multinomial Naive Bayes
#importing dependency
from sklearn.naive_bayes import MultinomialNB
#training the model 
nb_model=MultinomialNB().fit(X_train,y_train)
#predicting the target values i.e gender for the test set
nb_predicted=nb_model.predict(X_test)


#finding the accuracy of each model
from sklearn import metrics
print("Accuracy of decision tree model",metrics.accuracy_score(y_test,tree_predicted))
print("Accuracy of k-nearest neighbour model",metrics.accuracy_score(y_test,knn_predicted))
print("Accuracy of multinomial naive bayes model",metrics.accuracy_score(y_test,nb_predicted))