import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
SEED = 999

#==============================================================================
# Data Processing
#==============================================================================
df = pd.read_csv('data.csv')
X, y = df.drop(['diagnosis','id','Unnamed: 32'], axis=1), df['diagnosis']      
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

#==============================================================================
# Create interactions and standarize
#==============================================================================
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

# Interaction terms
poly = PolynomialFeatures(degree=2)
X_train = pd.DataFrame(poly.fit_transform(X_train), columns=poly.get_feature_names(X.columns))
X_test = pd.DataFrame(poly.transform(X_test), columns=poly.get_feature_names(X.columns))
# Standardize data
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_train.columns)

#==============================================================================
# All features
#==============================================================================
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression

# Fit Logistic Features to all features
est = LogisticRegression()
est.fit(X_train, y_train)

# Test accuracy
acc = accuracy_score(y_test, est.predict(X_test))
print('Test Accuracy {}'.format(acc))

# Plot confusion matrix
cm = confusion_matrix(y_test, est.predict(X_test))
sns.heatmap(cm, fmt='d', cmap='GnBu', cbar=False, annot=True)
         
#==============================================================================
# Recursive Feature Selection
#==============================================================================
from sklearn.feature_selection import RFECV

# RFE
rfe = RFECV(estimator=LogisticRegression(), cv=4, scoring='accuracy')
rfe = rfe.fit(X_train, y_train)

# Select variables and calulate test accuracy
cols = X_train.columns[rfe.support_]
acc = accuracy_score(y_test, rfe.estimator_.predict(X_test[cols]))
print('Number of features selected: {}'.format(rfe.n_features_))
print('Test Accuracy {}'.format(acc))

# Plot number of features vs CV scores
plt.figure()
plt.xlabel('k')
plt.ylabel('CV accuracy')
plt.plot(np.arange(1, rfe.grid_scores_.size+1), rfe.grid_scores_)
plt.show()

#==============================================================================
# Feature importances
#==============================================================================
from sklearn.ensemble import RandomForestClassifier

# Feature importance values from Random Forests
rf = RandomForestClassifier(n_jobs=-1, random_state=SEED)
rf.fit(X_train, y_train)
feat_imp = rf.feature_importances_

# Select features and fit Logistic Regression
cols = X_train.columns[feat_imp >= 0.01]
est_imp = LogisticRegression()
est_imp.fit(X_train[cols], y_train)

# Test accuracy
acc = accuracy_score(y_test, est_imp.predict(X_test[cols]))
print('Number of features selected: {}'.format(len(cols)))
print('Test Accuracy {}'.format(acc))

#==============================================================================
# Boruta
#==============================================================================
from boruta import BorutaPy

# Random Forests for Boruta 
rf_boruta = RandomForestClassifier(n_jobs=-1, random_state=SEED)
# Perform Boruta
boruta = BorutaPy(rf_boruta, n_estimators='auto', verbose=2)
boruta.fit(X_train.values, y_train.values.ravel())

# Select features and fit Logistic Regression
cols = X_train.columns[boruta.support_]
est_boruta = LogisticRegression()
est_boruta.fit(X_train[cols], y_train)

# Test accuracy
acc = accuracy_score(y_test, est_boruta.predict(X_test[cols]))
print('Number of features selected: {}'.format(len(cols)))
print('Test Accuracy {}'.format(acc))