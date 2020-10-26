# 1) apply PCA
# 2) softmax transformation
# There is one nice attribute of Softmax as compared with standard normalisation.
# It react to low stimulation (think blurry image) of your neural net with rather uniform distribution and to high stimulation (ie. large numbers, think crisp image) with probabilities close to 0 and 1.
# While standard normalisation does not care as long as the proportion are the same.
# Have a look what happens when soft max has 10 times larger input, ie your neural net got a crisp image and a lot of neurones got activated
# https://stackoverflow.com/questions/17187507/why-use-softmax-as-opposed-to-standard-normalization/45186059

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

file = "normalized_data_training.csv"
data = pd.read_csv(file)
NormList = data["Normal/Attack"]
data = data.drop(["Normal/Attack"], axis= 1)

file2 = "normalized_test_testing.csv"
data2 = pd.read_csv(file2)
NormAttList = data2["Normal/Attack"]
data2 = data2.drop(["Normal/Attack"], axis= 1)

pca = PCA(n_components=2)
pca.fit(data)
train_pca = pca.transform(data)
test_pca = pca.transform(data2)

df = pd.DataFrame(train_pca,columns = None, index= None)
df2 = pd.DataFrame(test_pca, columns = None, index= None)

def softmax(x):
 	return np.exp(x) / np.sum(np.exp(x), axis=1)

df = softmax(df)
df2 = softmax(df2)

df["Normal/Attack"] = NormList
df2["Normal/Attack"] = NormAttList

df.to_csv("PCA_train.csv", header= True, sep= ',', index= False)
df2.to_csv("PCA_test.csv", header= True, sep= ',', index= False)
