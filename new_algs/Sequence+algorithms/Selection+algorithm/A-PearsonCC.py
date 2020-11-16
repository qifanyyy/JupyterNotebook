#https://towardsdatascience.com/feature-selection-with-pandas-e3690ad8504b

#importing libraries
from sklearn.datasets import load_boston
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso


#Loading the dataset
x = load_boston()
df = pd.DataFrame(x.data, columns = x.feature_names)
df["MEDV"] = x.target
X = df.drop("MEDV",1)   #Feature Matrix
y = df["MEDV"]          #Target Variable
print(df.head())

#Using Pearson Correlation
plt.figure (figsize = (12,10)) 
cor = df.corr () 
sns.heatmap (cor, annot = True, cmap = plt.cm.Reds) 
#plt.show ()

#Correlation with output variable
cor_target = abs(cor["MEDV"])
#Selecting highly correlated features
relevant_features = cor_target[cor_target>0.5]
print("\n")
print(relevant_features)

#Mantener las variables relacionadas
print("\n")
print(df[["LSTAT","PTRATIO"]].corr())
print(df[["RM","LSTAT"]].corr())