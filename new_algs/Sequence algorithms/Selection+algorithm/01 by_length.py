# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from pandas import read_excel
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_curve
from sklearn.cluster import KMeans

# 读取表格数据
df = read_excel(r'C:\Users\withs\Desktop\By_length.xlsx',Sheetname='Sheet1',header=0 )
len1 = df['Weekday'].__len__()
# step0: Weekday 7
# step1: Register Request_event1	Check Date_event2	Audit Mode_event3 3+2+2
# step2: Manual Review_event4	Review the Reason_event4	Duration_event4 Resource_event4	Cost_event4	4+3+1+2+1=11
# step3: Check Ticket_event5	Examine_event5	Duration_event5	Resource_event5  Cost_event5 3+5+1+3+1 = 13
# step4: Check Ticket_event6 Examine_event6	Duration_event6	Resource_event6	Cost_event6 3+5+1+3+1 =13
# step5: Decide_event7	Duration_event7	Resource_event7	Cost_event7 4+2+1+1 = 8
X = df.ix[:,[ 'Weekday',  #7
             'Register Request_event1',   #a 3 10
             'Check Date_event2',         #b 2 12
             'Audit Mode_event3',         #c 2 14
             'Manual Review_event4', 'Review the Reason_event4', 'Resource_event4',  #d 4 3 2 23     25
             'Check Ticket_event5', 'Examine_event5', 'Resource_event5', #e 3 5 3   34   38
             'Check Ticket_event6',  'Examine_event6', 'Resource_event6',     #f 3 5 3    45   51
            'Decide_event7', 'Resource_event7']].values                 #g 4 2      51   59
X2 = df.ix[:,['Duration_event4','Cost_event4', 'Duration_event5','Cost_event5','Duration_event6', 'Cost_event6', 'Duration_event7','Cost_event7']].values
y = df['Result'].values
#one-hot编码
enc = OneHotEncoder()
enc.fit(X)
XX = enc.transform(X).toarray()
#划分数据集
# print(enc.n_values_)
# print(enc.feature_indices_)
arr1 = [23, 34, 45, 51]
res = XX[:, :23]
for i in range(1, len(arr1)):
    res = np.hstack((res, X2[:, 2*(i - 1): 2*i], XX[:, arr1[i-1]:arr1[i]]))
res = np.hstack((res, X2[:, 6:8]))

standardLst = [10, 12, 14, 25]
print("1.RandomForest + onehot +cost:")
for i in range(len(standardLst)):
    XXXX = res[:, :standardLst[i]]
    X_train, X_test, y_train, y_test = train_test_split( XXXX , y, random_state=0, test_size=.2 )
    print("data.shape: {}".format(XXXX.shape))
    #decisionTree
    tree = RandomForestClassifier(random_state=0)
    tree.fit(X_train, y_train)
    print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
    print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))

#2.divide
X_d = []
y_d = []
for x in range(len(res)):
    if res[x][22] == 1:
        X_d.append(res[x])
        y_d.append(y[x])
X_d = np.array(X_d)
y_d = np.array(y_d)

#3.1.  d
standardLst1 = [38, 51, 59]
for i in range(len(standardLst1)):
    XXXX = X_d[:, :standardLst1[i]]
    X_train, X_test, y_train, y_test = train_test_split( XXXX , y_d, random_state=0, test_size=.2 )
    print("data.shape: {}".format(XXXX.shape))
    #decisionTree
    tree = RandomForestClassifier(random_state=0)
    tree.fit(X_train, y_train)
    print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
    print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))







