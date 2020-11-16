
# coding: utf-8

# In[1]:


# Loading the required libraries:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import cross_val_score
from collections import Counter
from sklearn import cross_validation


# In[2]:


from time import time

# Some helper functions:
def get_shape(seq):
    if type(seq) == type([]):
        print("The shape of data is:", len(seq),",",len(seq[0]))
    else:
        print("The shape of data is:", seq.shape)
    return

def time_taken(start):
    print("\nRuntime:", round(time()-start, 2), "seconds")
    return


# # 4. Machine Learning Models
# We will apply two ML Algorithms and generate 2 models:
# 1. Random Modelling Algorithm on a Sample of Quora Question Pairs Data.
# 2. K-Nearest Neighbour Algorithm on a Sample of Quora Question Pairs Data.
# 
# ## 4.1 Loading Data

# In[3]:


st = time()
# Load only a sample of the final features data:
quora_df = pd.read_csv('./final_features_100k.csv', nrows=25000)

# Data Info:
print(type(quora_df))
get_shape(quora_df)
time_taken(st)
quora_df.head()


# In[4]:


quora_df.tail()


# In[5]:


# We will drop some useless features:
y_class = quora_df['is_duplicate']
quora_df.drop(['id', 'is_duplicate', 'Unnamed: 0'], axis=1, inplace=True)
quora_df.head()


# In[6]:


# We have our class variable as:
y_class.head()


# In[8]:


type(y_class)


# ## 4.2 Converting strings to numerics

# In[7]:


st = time()

cols = list(quora_df.columns)
for i in cols:
    quora_df[i] = quora_df[i].apply(pd.to_numeric)
    print(i, end=", ")


# In[8]:


time_taken(st)


# ## 4.3 Random Train-Test Split (70:30)

# In[9]:


# Our class variable is y_class:
X_train, X_test, y_train, y_test = train_test_split(
    quora_df, y_class, stratify=y_class, test_size=0.3
)

print('Number of data points in train data:', X_train.shape)
print('Number of data points in test data :', X_test.shape)


# In[10]:


print(type(X_train))
X_train.tail()


# In[11]:


X_test.tail()


# In[12]:


get_shape(y_train)
y_train.tail()


# In[13]:


get_shape(y_test)
y_test.tail()


# In[14]:


# Now we will see the distribution of points classwise:
print("-"*10, "Distribution of O/P Variable in train data", "-"*10)
tr_disb = Counter(y_train)
print("Number of data points that correspond to 'is_duplicate = 0' are:", tr_disb[0])
print("Number of data points that correspond to 'is_duplicate = 1' are:", tr_disb[1])
tr_len = len(y_train)
print("Total Number of points in train:", tr_len, "\n")
print("O/P (or) class-label: 'is_duplicate'")
print("is_duplicate = 0:", float(tr_disb[0]/tr_len),
     "\nis_duplicate = 1:", float(tr_disb[1]/tr_len))


# ## 4.3 Building a Random Model
# We will find the worst case accuracy score using a random model.

# In[15]:


# We will create a list which has exactly same size as our test data
# and generate a non-uniform random model:
random_y = np.random.choice(2, size=len(y_test), 
                            p = [0.1, 0.9]
                           )
random_y


# In[16]:


# Now we check the accuracy score:
rand_acc = accuracy_score(random_y, y_test, normalize=True) * float(100)
print("Accuracy Score for Random Model is {}%".format(rand_acc))


# With a Random Model, we are getting ~40% Accuracy, i.e., Our Random Model is able to predict whether 2 questions are similar or not, correctly, only 50% of the time. Therefore, this is the worst case Accuracy Score.
# 
# We want our k-NN to get an Accuracy Score > 40%.

# ## 4.4 Building k-Nearest Neighbours Model using Simple Cross Validation

# In[17]:


# Split the train data into cross validation train and cross validation test
X_tr, X_cv, y_tr, y_cv = train_test_split(
    X_train, y_train, stratify=y_train, test_size=0.3
)

# train and cv data info:
print('Number of data points in train data:', X_tr.shape)
print('Number of data points in cross validation data :', X_cv.shape)


# In[18]:


# Now we will see the distribution of points classwise:
print("-"*15, "Distribution of O/P Variable in train data", "-"*15)
train_tr_disb = Counter(y_tr)
print("Number of data points that correspond to 'is_duplicate = 0' are:", 
      train_tr_disb[0])
print("Number of data points that correspond to 'is_duplicate = 1' are:", 
      train_tr_disb[1])
train_tr_len = len(y_tr)
print("Total Number of points in train:", train_tr_len, "\n")
print("O/P (or) class-label: 'is_duplicate'")
print("is_duplicate = 0:", float(train_tr_disb[0]/train_tr_len),
     "\nis_duplicate = 1:", float(train_tr_disb[1]/train_tr_len))


# __Hyper Parameter Selection (or) Selection of Optimal K__

# In[20]:


# Finding the right k and applying k-NN using simple cross-validation:
# Hyper parameter selection:

# Creating odd list of K for K-NN:
my_list = list(range(0,100))
neighbours = list(filter(lambda x: x%2 != 0, my_list))
print("We will test K-NN Algorithm for these values of K:\n")
for i in neighbours:
    print(i, end=' ')


# In[21]:


# Now we have all the odd numbers, we can now apply the sklearn
# implementation of KNN to know the similarity/polarity between two questions:

st = time()

# Code for hyper parameter selection:
for k in neighbours:
    
    # Configured parameters are:-
    #
    # 1. algorithm = 'auto':
    #    automatically choose the algorithm (KDTree, BallTree or Brute Force)
    #
    # 2. metric = 'minkowski', p = 2:
    #    Use L2 Minkowski Distance which is nothing but Euclidean Distance.
    #
    # 3. n_jobs = -1: 
    #    Use all the CPU cores to apply KNN Classfication.
    
    # Instantiate the learning model:
    knn = KNeighborsClassifier(
        n_neighbors = k,
        algorithm = 'auto',
        metric = 'minkowski',
        p = 2,
        n_jobs = -1
    )
    
    # Fitting the model on train:
    knn.fit(X_tr, y_tr)
    
    # Predict the response on cross validation:
    predict_y_cv = knn.predict(X_cv)
    
    # Evaluate the cross validation accuracy:
    acc = accuracy_score(predict_y_cv, y_cv, normalize=True) * float(100)
    print('\nCross Validation Accuracy for k={} is {}%'
         .format(k, acc))
    
time_taken(st)


# Cross Validation Accuracy for k=29 is 65.18095238095239%. This is highest accuracy score out of all the accuracy scores.
# 
# Therefore, we got our k=29, i.e., we will consider the majority vote of the classes of 29 nearest neighbours in the vicinity of a query point -> xq.

# ### Applying the K Value from Simple Cross Validation on Test Data 

# In[23]:


# Configured parameters are:-
#
# 1. algorithm = 'auto':
#    automatically choose the algorithm (KDTree, BallTree or Brute Force)
#
# 2. metric = 'minkowski', p = 2:
#    Use L2 Minkowski Distance which is nothing but Euclidean Distance.
#
# 3. n_jobs = -1: 
#    Use all the CPU cores to apply KNN Classfication.

# Instantiate the learning model with k=29:
k_simple = 29
knn_simple_cv = KNeighborsClassifier(
    n_neighbors = k_simple,
    algorithm = 'auto',
    metric = 'minkowski',
    p = 2,
    n_jobs = -1
)

# Fitting the model on train data:
knn_simple_cv.fit(X_tr, y_tr)

# Predict the response on test data:
predict_y_test_simple_cv = knn_simple_cv.predict(X_test)

# Evaluate the test accuracy:
acc_test_simple = accuracy_score(predict_y_test_simple_cv, y_test, normalize=True) * float(100)
print('\n****** Test Accuracy for k={} is {}% *******'
     .format(k_simple, acc_test_simple))


# We will now apply K-NN using K-fold Cross Validation to get the best K, so that we can classify whether question1 is similar to question2 or not.

# ## 4.5 Building k-Nearest Neighbours Model using K-fold Cross Validation
# 
# Here, the k used for k-NN is a Hyper Parameter which tells us the number of neighbours that the algorithm is considering before making a decision about the class of a query point.
# 
# But, K used in K-fold Cross Validation is the number of folds/divisions we are making in our data, to consider the data as train and cross validation data with different division each time. After we get scores for each division, we take the mean of all of the scores, and that's our accuracy score of the k-fold cross validation.

# #### K = 10: 10 fold Cross Validation

# In[24]:


# Empty list to store the cross validation scores:
cv_scores = []

st = time()
# Perform 10-fold cross validation:
for k in neighbours:
        # Configured parameters are:-
    #
    # 1. algorithm = 'auto':
    #    automatically choose the algorithm (KDTree, BallTree or Brute Force)
    #
    # 2. metric = 'minkowski', p = 2:
    #    Use L2 Minkowski Distance which is nothing but Euclidean Distance.
    #
    # 3. n_jobs = -1: 
    #    Use all the CPU cores to apply KNN Classfication.
    
    # Instantiate the learning model:
    knn = KNeighborsClassifier(
        n_neighbors = k,
        algorithm = 'auto',
        metric = 'minkowski',
        p = 2,
        n_jobs = 3
    )
    
    # cv = 10: meaning 10 folds in the given data to get combinations
    # of train and cross validation data
    scores = cross_val_score(
        knn, X_train, y_train, cv=10, scoring='accuracy'
    )
    
    # record all the scores until now:
    cv_scores.append(scores.mean())


# In[25]:


time_taken(st)


# In[32]:


for i in cv_scores:
    print(i, end=', ')


# In[33]:


# Changing to Misclassification error:
MSE = [1-x for x in cv_scores]

for i in MSE:
    print(i, end=', ')


# In[34]:


# Now, we will determine the best k:
optimal_k = neighbours[MSE.index(min(MSE))]
print("The optimal number of neighbours is:", optimal_k)


# In[37]:


# Plot the Misclassification Error v/s k:
plt.figure(figsize=(10,7))
plt.plot(neighbours, MSE)

#for xy in zip(neighbours, np.round(MSE, 2)):
    #plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')

plt.xlabel('Number of Neighbours K')
plt.ylabel('Misclassification Error')
plt.show()

print("The Miscalssification Error for each k value is:\n", np.round(MSE, 3))


# From the plot above, we can see that the lowest value of Misclassification error is generated in between k=[20, 21, ..., 40].
# That's the reason, we got our optimal_k to be 27.
# 
# Let us see the accuracy score after querying the k-NN model with the test data.

# In[40]:


# KNN with k = optimal_k
st = time()
# Configured parameters are:-
#
# 1. algorithm = 'auto':
#    automatically choose the algorithm (KDTree, BallTree or Brute Force)
#
# 2. metric = 'minkowski', p = 2:
#    Use L2 Minkowski Distance which is nothing but Euclidean Distance.
#
# 3. n_jobs = -1: 
#    Use all the CPU cores to apply KNN Classfication.

# Instantiate the learning model:
knn_optimal = KNeighborsClassifier(
    n_neighbors = optimal_k,
    algorithm = 'auto',
    metric = 'minkowski',
    p = 2,
    n_jobs = 3
)

# Fitting the model on train:
knn_optimal.fit(X_train, y_train)

# Predict the response on test:
predict_y_test = knn_optimal.predict(X_test)

# Evaluate the test accuracy:
acc_test = accuracy_score(predict_y_test, y_test, normalize=True) * float(100)
print('''\nThe Accuracy of k-NN classifier on Quora Question Pairs Dataset 
for predicting whether two given questions have the same intent or not with 
k={} is {}%'''.format(optimal_k, acc_test))

time_taken(st)

