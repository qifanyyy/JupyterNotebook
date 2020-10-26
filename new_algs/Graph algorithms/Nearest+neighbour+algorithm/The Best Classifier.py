#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from sklearn import preprocessing
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df=pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_train.csv')
df.head()


# In[3]:


df.shape


# In[4]:


df['due_date'] = pd.to_datetime(df['due_date'])
df['effective_date'] = pd.to_datetime(df['effective_date'])
df.head()


# In[5]:


df['loan_status'].value_counts()


# In[6]:


import seaborn as sns

bins = np.linspace(df.Principal.min(), df.Principal.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'Principal', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()


# In[7]:


bins = np.linspace(df.age.min(), df.age.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'age', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()


# In[8]:


df['dayofweek'] = df['effective_date'].dt.dayofweek
bins = np.linspace(df.dayofweek.min(), df.dayofweek.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'dayofweek', bins=bins, ec="k")
g.axes[-1].legend()
plt.show()


# In[9]:


df['weekend'] = df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)
df.head()


# In[10]:


df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)


# In[11]:


df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)
df.head()


# In[12]:


df.groupby(['education'])['loan_status'].value_counts(normalize=True)


# In[13]:


df[['Principal','terms','age','Gender','education']].head()


# In[14]:


Feature = df[['Principal','terms','age','Gender','weekend']]
Feature = pd.concat([Feature,pd.get_dummies(df['education'])], axis=1)
Feature.drop(['Master or Above'], axis = 1,inplace=True)
Feature.head()


# In[15]:


X = Feature
X[0:5]


# In[16]:


y = df['loan_status'].values
y[0:5]


# In[17]:


X= preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]


# In[18]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=4)
print('Train Set:',x_train.shape,y_train.shape)
print('Test Set:',x_test.shape,y_test.shape)


# In[19]:


# KNN

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
ks=20
mean_acc=np.zeros((ks-1))
std_acc=np.zeros((ks-1))
for n in range(1,ks):
    neigh=KNeighborsClassifier(n_neighbors=n).fit(x_train,y_train)
    yhat=neigh.predict(x_test)
    mean_acc[n-1]=accuracy_score(y_test,yhat)
    std_acc[n-1]=np.std(yhat==y_test)/np.sqrt(yhat.shape[0])

print( "The best accuracy was with", mean_acc.max(), "with k=", mean_acc.argmax()+1)

k=mean_acc.argmax()+1

k_neigh=KNeighborsClassifier(n_neighbors=k).fit(X,y)


# In[20]:


plt.plot(range(1,ks),mean_acc,'g')

plt.fill_between(range(1,ks),mean_acc - 1 * std_acc,mean_acc + 1 * std_acc, alpha=0.10)

plt.legend(('Accuracy ', '+/- 3xstd'))

plt.ylabel('Accuracy ')

plt.xlabel('Number of Nabors (K)')

plt.tight_layout()

plt.show()


# In[21]:


#Decision Tree

from sklearn.tree import DecisionTreeClassifier
LoanTree=DecisionTreeClassifier(criterion='entropy',max_depth=4)
LoanTree.fit(X,y)


# In[22]:


from sklearn.externals.six import StringIO
import pydotplus
import matplotlib.image as mpimg
from sklearn import tree
dot_data=StringIO()
filename='Loan.png'
featureNames=X[0:8]
targetNames=df['loan_status'].unique().tolist()
out=tree.export_graphviz(LoanTree,feature_names=featureNames,out_file=dot_data,class_names=np.unique(y_train),filled=True,special_characters=True,rotate=False)
graph=pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png(filename)
img=mpimg.imread(filename)
plt.figure(figsize=(100,200))
plt.imshow (img,interpolation='nearest')


# In[23]:


#SVM

from sklearn import svm
lm=svm.SVC(kernel='rbf')
lm.fit(X,y)


# In[24]:


# Logistic Regression

from sklearn.linear_model import LogisticRegression
LR=LogisticRegression(C=0.01,solver='liblinear').fit(X,y)


# In[25]:


test_df=pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_test.csv')
test_df.head()


# In[26]:


test_df['due_date'] = pd.to_datetime(test_df['due_date'])
test_df['effective_date'] = pd.to_datetime(test_df['effective_date'])
test_df.head()


# In[27]:


test_df['dayofweek'] = test_df['effective_date'].dt.dayofweek
test_df['weekend'] = test_df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)
test_df.head()


# In[28]:


test_df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)


# In[29]:


test_df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)
test_df.head()


# In[30]:


test_df.groupby(['education'])['loan_status'].value_counts(normalize=True)


# In[31]:


test_df[['Principal','terms','age','Gender','education']].head()


# In[32]:


feature = test_df[['Principal','terms','age','Gender','weekend']]
feature = pd.concat([feature,pd.get_dummies(test_df['education'])], axis=1)
feature.drop(['Master or Above'], axis = 1,inplace=True)
feature.head()


# In[33]:


X = feature
X[0:5]


# In[36]:


y = test_df['loan_status'].values
y[0:5]


# In[37]:


X= preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]


# In[38]:


from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss


# In[39]:


#KNN

y_hat=k_neigh.predict(X)

K_J=jaccard_similarity_score(y,y_hat)

y_hat_l=preprocessing.LabelEncoder()
y_hat_l.fit(['PAIDOFF','COLLECTION'])
y_hat_l=y_hat_l.transform(y_hat)

y_l=preprocessing.LabelEncoder()
y_l.fit(['PAIDOFF','COLLECTION'])
y_l=y_l.transform(y)

K_F=f1_score(y_l,y_hat_l)


# In[40]:


#Decision Tree

y_hat=LoanTree.predict(X)

T_J=jaccard_similarity_score(y,y_hat)

y_hat_l=preprocessing.LabelEncoder()
y_hat_l.fit(['PAIDOFF','COLLECTION'])
y_hat_l=y_hat_l.transform(y_hat)

T_F=f1_score(y_l,y_hat_l)


# In[41]:


#SVM

y_hat=lm.predict(X)

S_J=jaccard_similarity_score(y,y_hat)

y_hat_l=preprocessing.LabelEncoder()
y_hat_l.fit(['PAIDOFF','COLLECTION'])
y_hat_l=y_hat_l.transform(y_hat)

T_F=f1_score(y_l,y_hat_l)


# In[42]:


#LR

y_hat=LR.predict(X)

L_J=jaccard_similarity_score(y,y_hat)

y_hat_l=preprocessing.LabelEncoder()
y_hat_l.fit(['PAIDOFF','COLLECTION'])
y_hat_l=y_hat_l.transform(y_hat)

L_F=f1_score(y_l,y_hat_l)

L_L=log_loss(y_l,y_hat_l)


# In[43]:


print('Algorithm:\t\t jaccard \t\t F1 score \t\t Log Loss')
print(f'KNN\t\t     {K_J}\t\t{K_F}\t    NA')
print(f'Decision Tree\t     {T_J}\t\t{T_F}\t    NA')
print(f'SVM\t\t     {S_J}\t\t{T_F}\t    NA')
print(f'Logistic Expression  {L_J}\t        {L_F}\t {L_L}')


# In[ ]:





# In[ ]:




