#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 17:57:03 2019

@author: alvi
"""

import pandas as pd
from PSO import error, PSO_update, PSO
from Text_Processing import data_preparation,split_text_num,text_tokenize,to_numeric
data_path='Reviews.csv'
data=data_preparation(data_path,memory=100)
data,text=split_text_num(data)
text_df=text_tokenize(text)
dataset=pd.concat([data,text_df], axis=1)
#Splitting X and Y
Y=dataset['Score']
dataset=dataset.drop(columns=['Score'])
dataset=to_numeric(dataset)

particle,error=PSO(X=dataset,Y=Y,generations=2,swarm=2,w=0.5,c1=1,c2=1)
print('Error\t',error,'\n Features\t',particle)
#testy=le.inverse_transform(predictions)
