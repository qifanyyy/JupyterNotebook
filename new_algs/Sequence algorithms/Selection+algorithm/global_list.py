import pandas as pd
import  numpy as np
import  ann
global dataMat
global labelMat

#建立全局变量，提取全部特征值

###read the data###
pandas_data = pd.read_csv('sql_eigen.csv')
data = pandas_data.fillna(np.mean(pandas_data))

data['age'][data['age'] > 200] = 91
data2 = data.drop(['hr_cov', 'bpsys_cov', 'bpdia_cov', 'bpmean_cov', 'pulse_cov', 'resp_cov', 'spo2_cov','height'], axis=1)
dataSet=np.array(data2)
dataSet[:,0:78]=ann.preprocess(dataSet[:,0:78])
dataSet[:,0:78]=ann.preprocess1(dataSet[:,0:78])
# dataSet=np.array(dataSet)
# print("test")
 ###read the data