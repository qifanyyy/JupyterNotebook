#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 18:11:57 2019

@author: alvi
"""
import pandas as pd
def data_preparation(data_path,memory=100):
    import pandas as pd
    data=pd.read_csv(data_path)
    data=data.iloc[:100,:]
    return data
def split_text_num(data):
    desc=data.iloc[:,9]
    data=data.drop(columns=['Text'])
    return data,desc
def text_tokenize(desc):
    description=[i.split(' ') for i in desc]
    m=0
    for i in description:
        if(len(i)>m):
            m=len(i)
    import numpy as np
    text_data=np.chararray((len(description), m),itemsize=500)
    text_data[:]=''
    count=0
    for i in range(len(description)):
      for j in range(len(description[i])):
        description[i][j]=description[i][j].replace("'","").replace("Î","I").replace("î","i").replace('®','').replace('§','').upper()
        count+=1
        text_data[i,j]=description[i][j]
    dataframe1=pd.DataFrame(text_data)
    return dataframe1#,text_data
def to_numeric(dataset):
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    X=[dataset[col][row] for col in dataset.columns for row in range(dataset.shape[0])]
    le.fit(X)
    for col in dataset.columns:
        dataset[col]=le.transform(dataset[col])
    return dataset
