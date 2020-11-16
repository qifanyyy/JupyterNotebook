# Using StandardScaling
import pandas as pd
import numpy as np
from sklearn import preprocessing
import joblib as joblib

pd.set_option('display.expand_frame_repr', False)
file = ""
data = pd.read_excel(file)
NormList = data["Normal/Attack"]

data = data.drop([" Timestamp" , "Normal/Attack"], axis = 1) # This is to remove the non numerical data
standardscaler = preprocessing.StandardScaler()
data_minmax = standardscaler.fit(data)
data_minmax = standardscaler.transform(data)

df = pd.DataFrame(data_minmax, columns = data.columns.values, index= None)
scalerfile = 'scaler.pkl'
joblib.dump(standardscaler, scalerfile)

data2 = pd.read_excel("")
NormAttList = data2["Normal/Attack"]
data2 = data2.drop([" Timestamp" , "Normal/Attack"], axis = 1)
test_scaled_set = standardscaler.transform(data2)

df2 = pd.DataFrame(test_scaled_set, columns = data2.columns.values, index= None)
df["Normal/Attack"] = NormList
df2["Normal/Attack"] = NormAttList

df2.to_csv("normalized_test_testing.csv", header= True, sep= ',', index= False)
df.to_csv("normalized_data_training.csv", header= True, sep= ',', index= False)



