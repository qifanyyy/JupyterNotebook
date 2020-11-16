#https://towardsdatascience.com/feature-selection-using-wrapper-methods-in-python-f0d352b346f

from sklearn.datasets import load_boston
import pandas as pd
import statsmodels.api as sm

boston = load_boston()

'''
print(boston.data.shape)         # for dataset dimension
print(boston.feature_names)      # for feature names
print(boston.target)             # for target variable
print(boston.DESCR)              # for data description
'''

bos = pd.DataFrame(boston.data, columns = boston.feature_names)
bos['Price'] = boston.target
X = bos.drop("Price", 1)       # feature matrix 
y = bos['Price']               # target feature

print(bos.head())

print("------------forward_selection-----------")
def forward_selection(data, target, significance_level=0.05):
    initial_features = data.columns.tolist()
    best_features = []
    while (len(initial_features)>0):
        remaining_features = list(set(initial_features)-set(best_features))
        new_pval = pd.Series(index=remaining_features)
        for new_column in remaining_features:
            model = sm.OLS(target, sm.add_constant(data[best_features+[new_column]])).fit()
            new_pval[new_column] = model.pvalues[new_column]
        min_p_value = new_pval.min()
        if(min_p_value<significance_level):
            best_features.append(new_pval.idxmin())
        else:
            break
    return best_features


print(forward_selection(X,y))


print("------------Implementing Forward selection using built-in-----------")
#Implementing Forward selection using built-in functions in Python:
#http://rasbt.github.io/mlxtend/installation/
#importing the necessary libraries
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LinearRegression

# Sequential Forward Selection(sfs)
sfs = SFS(LinearRegression(),
           k_features=11,
           forward=True,
           floating=False,
           scoring = 'r2',
           cv = 0)

sfs.fit(X, y)
print(sfs.k_feature_names_)     # to get the final set of features

print("-----------backward_elimination-----------")
#Backward elimination
def backward_elimination(data, target,significance_level = 0.05):
    features = data.columns.tolist()
    while(len(features)>0):
        features_with_constant = sm.add_constant(data[features])
        p_values = sm.OLS(target, features_with_constant).fit().pvalues[1:]
        max_p_value = p_values.max()
        if(max_p_value >= significance_level):
            excluded_feature = p_values.idxmax()
            features.remove(excluded_feature)
        else:
            break 
    return features
print(backward_elimination(X,y))

print("-----------backward_elimination using built-in functions-----------")
#Implementing Backward elimination using built-in functions in Python:
#Sequential backward selection(sbs)
sbs = SFS(LinearRegression(), 
          k_features=11, 
          forward=False, 
          floating=False,
          cv=0)
sbs.fit(X, y)
print(sbs.k_feature_names_)

#Bi-directional elimination(Stepwise Selection)
print("-----------Bi-directional elimination(Stepwise Selection)-----------")
def stepwise_selection(data, target,SL_in=0.05,SL_out = 0.05):
    initial_features = data.columns.tolist()
    best_features = []
    while (len(initial_features)>0):
        remaining_features = list(set(initial_features)-set(best_features))
        new_pval = pd.Series(index=remaining_features)
        for new_column in remaining_features:
            model = sm.OLS(target, sm.add_constant(data[best_features+[new_column]])).fit()
            new_pval[new_column] = model.pvalues[new_column]
        min_p_value = new_pval.min()
        if(min_p_value<SL_in):
            best_features.append(new_pval.idxmin())
            while(len(best_features)>0):
                best_features_with_constant = sm.add_constant(data[best_features])
                p_values = sm.OLS(target, best_features_with_constant).fit().pvalues[1:]
                max_p_value = p_values.max()
                if(max_p_value >= SL_out):
                    excluded_feature = p_values.idxmax()
                    best_features.remove(excluded_feature)
                else:
                    break 
        else:
            break
    return best_features

print(stepwise_selection(X,y))
#Implementing bi-directional elimination using built-in functions in Python:
# Sequential Forward Floating Selection(sffs)
sffs = SFS(LinearRegression(), 
          k_features=(3,11), 
          forward=True, 
          floating=True,
          cv=0)
sffs.fit(X, y)
print(sffs.k_feature_names_)