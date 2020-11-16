# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from pandas import read_excel
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder

# 读取表格数据
df = read_excel(r'C:\Users\withs\Desktop\By_activity.xlsx',Sheetname='Sheet1',header=0 )
len1 = df['Weekday'].__len__()
# step0: Weekday 7
# step1: Register Request_event1	Check Date_event2	Audit Mode_event3 3+2+2
# step2: Manual Review_event4	Review the Reason_event4	Duration_event4 Resource_event4	Cost_event4	4+3+1+2+1=11
# step3: Check Ticket_event5	Examine_event5	Duration_event5	Resource_event5  Cost_event5 3+5+1+3+1 = 13
# step4: Check Ticket_event6 Examine_event6	Duration_event6	Resource_event6	Cost_event6 3+5+1+3+1 =13
# step5: Decide_event7	Duration_event7	Resource_event7	Cost_event7 4+2+1+1 = 8
X = df.ix[:,[ 'Weekday',  #7
             'Register Request_endA',   #a 3                        10
             'Check Date_endB',         #b 2                        12
             'Audit Mode_endC',         #c 2                        14
             'Manual Review_endD', 'Resource4_endD',  #d 4 2 13      15+7
            'Review the Reason_endE', 'Resource5_endE',  #e 3 2 18    22+7
            'Examine Casually_endF', 'Resource7_endF',  #f 3 2 23    29+7
             'Check Ticket_endF',  'Resource6_endF',    #f 3 2 28    36+7
             'Examine Thoroughly_endG', 'Resource8_endG',#g 3 2 33   43+7
            'Check Ticket_endG',  'Resource6_endG',      #g 3 2 38   50+7
            'Check Ticket_endH',  'Resource6_endH',      #h 3 2 43   57+7
            'Examine Casually_endH', 'Resource7_endH',    #h 3 2 48   64+7
             'Examine Thoroughly_endH', 'Resource8_endH',#h 3 2 53   71+7
             'Decide_endI', 'Resource9_endI',  #i 4 2 59   79+7
            'Accept_endJ', 'Resource10_endJ',  #j 2 2 63   85+7
            'Reject_endK', 'Resource11_endK',  #k 2 2 67   91+7
            'Reapply_endL', 'Resource12_endL']].values  #i 2 2 71   97+7
#a,b,c (0:7)  d(7:15) e(15:22) f(22:36) g(36:50) h(50:71) i(71:79) j(79:85) k(85:91) l(91:97)
X2 = df.ix[:,['Duration4_endD','Cost4_endD', 'Duration5_endE','Cost5_endE','Duration7_endF', 'Cost7_endF', 'Duration6_endF','Cost6_endF', 'Duration8_endG','Cost8_endG',
              'Duration6_endG','Cost6_endG', 'Duration6_endH', 'Cost6_endH', 'Duration7_endH', 'Cost7_endH', 'Duration8_endH', 'Cost8_endH',
              'Duration9_endI', 'Cost9_endI', 'Duration10_endJ', 'Cost10_endJ', 'Duration11_endK', 'Cost11_endK', 'Duration12_endL', 'Cost12_endL']].values
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
arr1 = [20, 25, 30, 35, 40, 45, 50, 55, 60, 66, 70, 74, 78]
res = XX[:, :20]
for i in range(1, len(arr1)):
    res = np.hstack((res, X2[:, 2*(i - 1): 2*i], XX[:, arr1[i-1]:arr1[i]]))
res = np.hstack((res, X2[:, 24:26]))

#[ 0  7 10 12 14 18 20 23 25 28 30 33 35 38 40 44 46]

# 1.a,b,c;
standardLst = [14]
print("1.RandomForest + onehot +cost:")
for i in range(len(standardLst)):
    XXXX = res[:, :standardLst[i]]
    X_train, X_test, y_train, y_test = train_test_split( XXXX , y, random_state=0, test_size=.2 )
    print("X_train.shape: {}".format(X_train.shape))
    #decisionTree
    tree = RandomForestClassifier(random_state=0)
    tree.fit(X_train, y_train)
    print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
    print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))

    # fip = tree.feature_importances_
    # fips = [sum(fip[:3])]
    # for tmp in range(1, i+1):
    #     fips.append(sum(fip[:standardLst[tmp]]) - sum(fips))
    # result = [format(x, '.2%') for x in fips]
    # print("Feature importances:\n{}".format(result))

# # 2.a,b,c,d
XXXX_d = []
yy = []
for x in range(len(res)):
    if res[x][19] == 1:
        XXXX_d.append(res[x][:22])
        yy.append(y[x])
yy = np.array(yy)
XXXX_d = np.array(XXXX_d)
X_train, X_test, y_train, y_test = train_test_split( XXXX_d , yy, random_state=0, test_size=.2 )
print("X_train.shape: {}".format(XXXX_d.shape))
tree = RandomForestClassifier(random_state=0)
tree.fit(X_train, y_train)
print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))

#3.a,b,c,e
X_e = []
y_e = []
for x in range(len(res)):
    if res[x][26] == 1:
        X_e.append(np.hstack((res[x][:14], res[x][22:29])))
        y_e.append(y[x])
X_e = np.array(X_e)
y_e = np.array(y_e)
X_train, X_test, y_train, y_test = train_test_split( X_e , y_e, random_state=0, test_size=.2 )
print("X_train.shape: {}".format(X_e.shape))
tree = RandomForestClassifier(random_state=0)
tree.fit(X_train, y_train)
print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))

#4.a,b,c,e,*,*,i
X_i = []
y_i = []
for x in range(len(res)):
    if res[x][83] == 1:
        X_i.append(np.hstack((res[x][:14], res[x][22:29], res[x][29:36], res[x][43:50], res[x][57:64], res[x][78:86])))
        y_i.append(y[x])
X_i = np.array(X_i)
y_i = np.array(y_i)
X_train, X_test, y_train, y_test = train_test_split( X_i , y_i, random_state=0, test_size=.2 )
print("X_train.shape: {}".format(X_i.shape))
tree = RandomForestClassifier(random_state=0)
# tree = DecisionTreeClassifier(random_state=0)
tree.fit(X_train, y_train)
print("Accuracy on train set: {:.4f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.4f}".format(tree.score(X_test, y_test)))





