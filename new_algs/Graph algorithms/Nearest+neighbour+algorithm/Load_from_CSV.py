#										FLOWER PREDICTION BASED ON IRIS FLOWER DATASET
#										     (Importing from CSV file)
# Link to Reference used-->https://machinelearningmastery.com/machine-learning-in-python-step-by-step/
#This program is used to learn about Ml, python libraries and their functioning etc...
#To understand, I am doing documentation about new things i will encounter.
#I am also going to add some more modifications in this program
#Potential modifications:- 
#       1) Using timenow and timeit it calculate the execution time
#       2) Plotting more types of graphs, 3d graphs if possible   
#       3) Applying dataset to more algorithms

#Importing the modules

#Creating an alias
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt

from pd.tools.plotting import scatter_matrix
from sk import model_selection
from sk.metrics import classification_report, confusion_matrix, accuracy_score
from sk.linear_model import LogisticRegression
from sk.tree import DecisionTreeClassifier
from sk.neighbors import KNeighborsClassifier
from sk.discriminant_analysis import LinearDiscriminantAnalysis
from sk.naive_bayes import GaussianNB
from sk.svm import SVC

# Loading the dataset
#Provide a url from which to take the CSV file
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

#Store the name of the attributes in form of list
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']

#Using the read_csv function from pandas to read the CSV file  
dataset = pd.read_csv(url, names=names)

# shape, we will see (150,5), 150 is instances and 5 is attributes
print(dataset.shape)

# head-20 is 20 rows of data
print(dataset.head(20))

# descriptions-This includes the count, mean, the min and max values as well as some percentiles.
print(dataset.describe())

# class distribution-number of instances (rows) that belong to each class
print(dataset.groupby('class').size())


#DATA Visualization

#univariate plots-plots of each individual variable.
# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()#-->gives us a much clearer idea of the distribution of the input attributes
#histograms
dataset.hist()
plt.show()#-->It looks like perhaps two of the input variables have a Gaussian distribution. This is useful to note as we can use algorithms that can exploit this assumption.

#Multivariable plots--interaction between the variables
# scatter plot matrix-helpful to spot structured relationships between input variables.
scatter_matrix(dataset)
plt.show()#-->Note the diagonal grouping of some pairs of attributes. This suggests a high correlation and a predictable relationship.

#NOTED-->to see the type of relations from looking at the graphs

#EVALUATING THE ALGORITHMS

# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Test options and evaluation metric
#We will use 10-fold cross validation to estimate accuracy.
#This will split our dataset into 10 parts, train on 9 and test on 1 and repeat for all combinations of train-test splits.
seed = 7
scoring = 'accuracy'
#Accuracy is a ratio of the number of correctly predicted instances in divided by the total number of instances in the dataset multiplied by 100 to give a percentage 

# Spot Check Algorithms-as we don't know which algorithm will be better
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)
#Select the best model!--Here it is KNN

# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

# Make predictions on validation dataset
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
