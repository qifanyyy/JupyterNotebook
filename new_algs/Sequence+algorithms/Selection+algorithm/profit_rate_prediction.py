# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 15:42:10 2017

@author: limen
"""
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import metrics
import re


#build MAPE function
def mean_absolute_percentage_error(y,p):
   
    return np.mean(np.abs((y-p)/y))


#import jd attributes table
attrs =  pd.read_table('sku_attrs_jd.csv',sep = '\t', encoding = 'utf-8') 
sku_attrs = attrs[['sku_id','attr_name','attr_value']]


#transform original table to pivot_table 
a = pd.pivot_table(sku_attrs, index=['sku_id'], columns=['attr_name'],
                    values=['attr_value'],fill_value = np.nan, aggfunc='max')
a.columns = a.columns.droplevel(level=0)
a = a.reset_index(drop=False)
#print(a[u'分类'].value_counts())
a = a.apply(lambda x: x.fillna(x.value_counts().index[0]))

#replace wrong information with correct data while transforming
a.replace(42741,'1-6',inplace=True)
a.replace(42928,'7-12',inplace=True)
a.replace(u'其他',u'其它',inplace=True)

a.drop([u'适用场景', u'茶饮料系列',u'碳酸饮料分类',u'是否含糖',u'功能饮料'],axis = 1, inplace = True) 



#use regular expression method to filter complex string data           
a[u'产品产地'] = a[u'产品产地'].apply(lambda x: re.sub('.*#\$','',x))
a[u'包装'] = a[u'包装'].apply(lambda x: re.sub('.*#\$','',x))
a[u'分类'] = a[u'分类'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'功能饮料'] = a[u'功能饮料'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'碳酸饮料分类'] = a[u'碳酸饮料分类'].apply(lambda x: re.sub('.*#\$','',x))
a[u'口味'] = a[u'口味'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'是否含糖'] = a[u'是否含糖'].apply(lambda x: re.sub('.*#\$','',x))

#filter normal string data
a[u'分类'] = a[u'分类'].apply(lambda x: x.split('/')[0])
a[u'口味'] = a[u'口味'].apply(lambda x: x.split('/')[0])
#a[u'碳酸饮料分类 '] = a[u'碳酸饮料分类'].apply(lambda x: x.split('/')[0])

def juice_percentage(x):
    if (x[u'分类'] == u'果蔬汁') & (x[u'果汁成分含量'] == 'None'):
        return 1 
    elif (x[u'分类'] == u'果汁') & (x[u'果汁成分含量'] == 'None'):
        return u'100%以下'
    elif (x[u'分类'] == u'果汁') & (x[u'果汁成分含量'] == u'其它'):
        return u'100%以下'
    elif (x[u'分类'] == u'果味饮料') & (x[u'果汁成分含量'] == 'None'):
        return u'100%以下'
    elif (x[u'分类'] == u'果味饮料') & (x[u'果汁成分含量'] == u'其它'):
        return u'100%以下'
    else:
        return x[u'果汁成分含量']
    
a[u'果汁成分含量'] = a.apply(lambda x: juice_percentage(x), axis = 1)
a[u'果汁成分含量'].replace(u'浓缩100%以下',u'100%以下', inplace = True)



a[u'包装'].replace(u'瓶装',u'其它',inplace = True)
a[u'包装'].replace(u'利乐装',u'其它',inplace = True)
a[u'包装'].replace(u'不限',u'其它',inplace = True)
a[u'分类'].replace(u'果汁',u'果蔬汁',inplace = True)
#a[u'功能饮料'].replace(u'运动饮料',u'能量饮料',inplace = True)
#a[u'碳酸饮料分类'].replace(u'雪碧/七喜',u'可乐',inplace = True)
#a[u'碳酸饮料分类'].replace(u'盐汽水',u'苏打水',inplace = True)
a[u'口味'].replace(u'混合果味',u'混合饮料',inplace = True)
a[u'口味'].replace(u'不限',u'其它',inplace = True)
#a[u'是否含糖'].replace(u'含木糖醇',u'含糖',inplace = True)
a[u'单件容量'].replace(u'其它',u'250mL及以下',inplace = True)
a[u'单件容量'].replace(u'250ml及以下',u'250mL及以下',inplace = True)
a[u'进口/国产'].replace(u'其它',u'国产',inplace = True)
a[u'产品产地'].replace(u'马来西亚',u'泰国',inplace = True)
a[u'产品产地'].replace(u'韩国',u'日本',inplace = True)
a[u'产品产地'].replace(u'港澳台',u'其它',inplace = True)
a[u'产品产地'].replace(u'澳大利亚',u'其它',inplace = True)

origin = a[u'产品产地'].value_counts()


#import profit table
sku_profit = pd.read_table('app_cfo_profit_loss_b2c_det.csv')
sku_profit['sku_id'] = sku_profit['item_sku_id']
sku_profit.drop(['dt','item_third_cate_name','item_sku_id','cost_tax',
'income','grossfit','gross_sales','rebate_amunt_notax',
'adv_amount','store_fee','deliver_fee'], axis = 1, inplace = True)

    
#put the last column to the very front
cols = sku_profit.columns.tolist()
cols = cols[-1:]+cols[:-1]
sku_profit = sku_profit[cols]


#filter sku_profit table
sku_profit_1 = sku_profit[sku_profit['gmv'] >= 0.5 ]
sku_profit_2 = sku_profit[sku_profit['gmv'] <= -0.5 ]
sku_profit = pd.concat([sku_profit_1,sku_profit_2])
sku_profit = sku_profit[sku_profit['net_profit'] < sku_profit['gmv']]
#sns.distplot(final_npp['net_profit'] ) 观察net_profit分布情况


#make the profit_rate column
sku_profit['profit_rate'] = (sku_profit['net_profit']/sku_profit['gmv'])*100
#sku_profit[~np.isfinite(sku_profit)] = np.nan
sku_profit.drop(['net_profit','gmv'], axis =1, inplace = True)

sku_profit = sku_profit[sku_profit['profit_rate'] > -70]
sku_profit = sku_profit[sku_profit['profit_rate'] < 100]


#extract the mean sku_id profit table
average_profit = sku_profit.groupby('sku_id').mean()
average_profit.reset_index(inplace=True)


#merge attributes table and mean profit table based on sku_id
final_npp = pd.merge(a,average_profit, how = 'inner', on = 'sku_id')
final_npp['profit_rate'] = final_npp['profit_rate'].astype(int)
#final_npp.to_csv('final_npp.csv', encoding = 'utf-8') to show final_npp content
final_npp = final_npp[final_npp['profit_rate'] != 0]


#import sku_price table
sku_price = pd.read_csv('drinks.csv')
sku_price.drop(u'Unnamed: 0', axis = 1, inplace = True)
sku_price['sku_id'] = sku_price['item_sku_id']
sku_price.drop(['item_first_cate_cd','item_second_cate_cd',
                'item_third_cate_cd','item_sku_id'], axis = 1, inplace = True)

   
#merge final_npp table with sku_price table based on sku_id 
net_profit_percent = pd.merge(final_npp,sku_price, how = 'inner', on = 'sku_id')
net_profit_percent.drop('sku_id', axis = 1, inplace=True)



#replace numbers with characters and set price feature to be integer
net_profit_percent[u'果汁成分含量'].replace(1,'100%', inplace = True)
net_profit_percent['price'] = net_profit_percent['price'].apply(lambda x: int(x))
net_profit_percent[u'sku价格'] = net_profit_percent['price']
net_profit_percent.drop('price', axis = 1, inplace = True)

#put the last column to the very front
cols = net_profit_percent.columns.tolist()
cols = cols[-1:]+cols[:-1]
net_profit_percent = net_profit_percent[cols]


#net_profit_percent = encode_onehot(net_profit_percent, [u'产品产地'])


#label encoder method to handle discrete/categorical features except continuous features
for attribute in net_profit_percent.columns.difference(['profit_rate','sku价格']):
    le = preprocessing.LabelEncoder()
    net_profit_percent[attribute] = le.fit_transform(net_profit_percent[attribute])

'''
net_profit_percent = pd.get_dummies(net_profit_percent, columns=[u'产品产地',
                                                                 u'分类', 
                                                                 u'包装',
                                                                 u'包装件数',
                                                                 u'单件容量',
                                                                 u'口味',
                                                                 u'果汁成分含量',
                                                                 u'品牌',
                                                                 u'进口/国产'],
                                                                 #u'碳酸饮料分类'],
    prefix=['origin', 'classifi','package','pakunit','unitvol','taste'
            ,'juiceper','brand','import'])
'''

#normalize continuous features('price')
net_profit_percent[u'sku价格'] = net_profit_percent[u'sku价格'].apply(lambda x: 
    (x-net_profit_percent[u'sku价格'].mean())/(net_profit_percent[u'sku价格'].std()))

#handle high cardinality of brand feature using kmeans clustering
from sklearn.cluster import KMeans
X = net_profit_percent[[u'sku价格',u'产品产地',u'品牌']]
kmeans = KMeans(n_clusters = 20, random_state = 0).fit(X)
net_profit_percent[u'品牌'] = kmeans.labels_
      
'''
net_profit_percent['profit_rate'] = net_profit_percent['profit_rate'].apply(lambda x: 
    (x-net_profit_percent['profit_rate'].mean())/(net_profit_percent['profit_rate'].std()))
'''   
    

if __name__ == '__main__':    
    
    #net_profit_percent.drop(net_profit_percent.index[[227,476,383,293,392,360]], inplace = True)
    net_profit_percent.drop(net_profit_percent.index[[392,360]], inplace = True)
    #train_test_split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(net_profit_percent.drop('profit_rate',
                                                                                axis=1), 
                                                        net_profit_percent['profit_rate'], 
                                                        test_size=0.30,
                                                        random_state = 101)

    #y_test[y_test == 0] = 1
    
    #optimize algotirhm and tune parameter with GridSearchCV
    '''
    from sklearn.grid_search import GridSearchCV
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(  n_estimators = 500, 
                                  max_features = 'auto',
                                  max_depth=8,
                                  min_samples_leaf=4,
                                  min_samples_split=8,
                                  oob_score=True,
                                  #random_state = 42,
                                  n_jobs=-1,
                                  criterion = 'mae',
                                  bootstrap = True)
    param_grid = { 
    'max_depth':[5,8],
    'min_samples_leaf':[2,4,6],
    'min_samples_split':[4,8,10]
    }


    CV_rfr= GridSearchCV(estimator=rfr, param_grid=param_grid, cv=5)

    CV_rfr.fit(X_train, y_train) 
    print (CV_rfr.best_params_)
    '''
    
    
    #implement RandomForestregressor to solve regression problem    
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(  n_estimators = 500, 
                                  max_features = 'auto',
                                  max_depth=8,
                                  min_samples_leaf=4,
                                  min_samples_split=8,
                                  oob_score=True,
                                  #random_state = 42,
                                  criterion = 'mae',
                                  n_jobs=-1,
                                  bootstrap = True)
                                  #warm_start=False,
                                  #max_leaf_nodes = 30)
    rfr.fit(X_train, y_train)
    predictions = rfr.predict(X_test)
    
      
 
    #plt.scatter(y_test,predictions)
    print('MAE:', metrics.mean_absolute_error(y_test, predictions))
    print('MSE:', metrics.mean_squared_error(y_test, predictions))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    print('MAPE:', mean_absolute_percentage_error(y_test,predictions))
    
    #columns = net_profit_percent.columns
    #print (sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), columns),reverse=True)) 
    
       
    #subplots method of matplotlib 
    fig, axes = plt.subplots(nrows = 2, ncols = 1)
    axes[0].scatter(y_test, predictions)
    plt.sca(axes[1]) #Use the pyplot interface to change just one subplot
    plt.xticks(range(X_train.shape[1]),X_train.columns, color='r')
    axes[1].bar(range(X_train.shape[1]),rfr.feature_importances_, color= 'b',align = 'center')
    
    
        
