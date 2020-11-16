# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from pandas import read_excel
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

# 读取表格数据
df = read_excel(r'C:\Users\withs\Desktop\Feature Importance.xlsx',Sheetname='Sheet1',header=0 )
len1 = df['Weekday'].__len__()
# step0: Weekday 7
# step1: Register Request_event1	Check Date_event2	Audit Mode_event3 3+2+2
# step2: Manual Review_event4	Review the Reason_event4	Duration_event4 Resource_event4	Cost_event4	4+3+1+2+1=11
# step3: Check Ticket_event5	Examine_event5	Duration_event5	Resource_event5  Cost_event5 3+5+1+3+1 = 13
# step4: Check Ticket_event6 Examine_event6	Duration_event6	Resource_event6	Cost_event6 3+5+1+3+1 =13
# step5: Decide_event7	Duration_event7	Resource_event7	Cost_event7 4+2+1+1 = 8
X = df.ix[:,[ #'Weekday',  #7
             'Register Request',   #a 3 3
             'Check Date',         #b 2 5
             'Audit Mode',         #c 2 7
             'Manual Review', 'Resource4',  #d 4 2 13 15
            'Review the Reason', 'Resource5',  #e 3 2 18    22
             'Examine Casually', 'Resource7',  #g 3 2 23 29
             'Examine Thoroughly', 'Resource8', #h 3 2 28   36
            'Check Ticket', 'Resource6',  # f 3 2 33 43
             'Decide', 'Resource9']].values  #i 4 2 39     51
X2 = df.ix[:,['Duration4','Cost4', 'Duration5','Cost5', 'Duration7','Cost7', 'Duration8','Cost8','Duration6', 'Cost6', 'Duration9','Cost9']].values
y = df['Result1'].values
#one-hot编码
enc = OneHotEncoder()
enc.fit(X)
XX = enc.transform(X).toarray()
#划分数据集
# print(enc.n_values_)
# print(enc.feature_indices_)
# [3 2 2 4 2 3 2 3 2 3 2 3 2 4 2]
# [ 0  3  5  7 11 13 16 18 21 23 26 28 31 33 37 39]
arr1 = [13, 18, 23, 28, 33, 39]
res = XX[:, :13]
for i in range(1, len(arr1)):
    res = np.hstack((res, X2[:, 2*(i - 1): 2*i], XX[:, arr1[i-1]:arr1[i]]))
res = np.hstack((res, X2[:, 10:12]))

#[ 0  7 10 12 14 18 20 23 25 28 30 33 35 38 40 44 46]

# 1.RandomForest + onehot +cost
standardLst = [3, 5, 7, 15, 22, 29, 36, 43, 51]
print("1.RandomForest + onehot +cost:")
X_train, X_test, y_train, y_test = train_test_split(res, y, random_state=0, test_size=.2)
tree = RandomForestClassifier(random_state=0)
tree.fit(X_train, y_train)
fip = tree.feature_importances_
fips = [sum(fip[:3])]
for tmp in range(1, standardLst.__len__()):
    fips.append(sum(fip[:standardLst[tmp]]) - sum(fips))
result = [format(x, '.2%') for x in fips]
print("Feature importances:\n{}".format(result))
