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
import os

os.chdir('C:/Users/limen/Documents/profit_rate_prediction_warehouseprice_gmv_added')

#build MAPE function
def mean_absolute_percentage_error(y,p):
   
    return np.mean(np.abs((y-p)/y))


#build MSLE function
def squared_log_error(actual,predicted):
    
    return np.power(np.log(np.array(actual)+1) - np.log(np.array(predicted)+1), 2)

def mean_squared_log_error(actual,predicted):
    
    return np.mean(squared_log_error(actual,predicted))


#import jd attributes table
attrs =  pd.read_table('sku_attrs_jd.csv',sep = '\t', encoding = 'utf-8') 
sku_attrs = attrs[['sku_id','attr_name','attr_value']]


#transform original table to pivot_table 
a = pd.pivot_table(sku_attrs, index=['sku_id'], columns=['attr_name'],
                    values=['attr_value'],fill_value = np.nan, aggfunc='max')
a.columns = a.columns.droplevel(level=0)
a = a.reset_index(drop=False)
a = a.apply(lambda x: x.fillna(x.value_counts().index[0]))
        


#import pop attributes table
sku_attr_pop = pd.read_table('sku_attr_pop.csv',sep='\t', encoding='utf-8')
sku_attr_pop = sku_attr_pop[['sku_id','attr_name','attr_value']]
pop_attr = pd.pivot_table(sku_attr_pop,index=['sku_id'],columns = ['attr_name'],
values = ['attr_value'], fill_value=np.nan, aggfunc= 'max')
pop_attr.columns = pop_attr.columns.droplevel(level = 0)
pop_attr =  pop_attr.reset_index(drop=False)
pop_attr = pop_attr.apply(lambda x: x.fillna(x.value_counts().index[0]))


#combine jd and pop attributes table together
jd_pop_attrs = pd.concat([a,pop_attr],ignore_index = True)

jd_pop_attrs.drop([u'适用场景', u'茶饮料系列',u'碳酸饮料分类',u'是否含糖',u'功能饮料'],axis = 1, inplace = True) 



#use regular expression method to filter complex string data           
jd_pop_attrs[u'产品产地'] = jd_pop_attrs[u'产品产地'].apply(lambda x: re.sub('.*#\$','',x))
jd_pop_attrs[u'包装'] = jd_pop_attrs[u'包装'].apply(lambda x: re.sub('.*#\$','',x))
jd_pop_attrs[u'分类'] = jd_pop_attrs[u'分类'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'功能饮料'] = a[u'功能饮料'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'碳酸饮料分类'] = a[u'碳酸饮料分类'].apply(lambda x: re.sub('.*#\$','',x))
jd_pop_attrs[u'口味'] = jd_pop_attrs[u'口味'].apply(lambda x: re.sub('.*#\$','',x))
jd_pop_attrs[u'品牌'] = jd_pop_attrs[u'品牌'].apply(lambda x: re.sub('.*#\$','',x))
#a[u'是否含糖'] = a[u'是否含糖'].apply(lambda x: re.sub('.*#\$','',x))


#filter normal string data
jd_pop_attrs[u'分类'] = jd_pop_attrs[u'分类'].apply(lambda x: x.split('/')[0])
jd_pop_attrs[u'口味'] = jd_pop_attrs[u'口味'].apply(lambda x: x.split('/')[0])
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
    
jd_pop_attrs[u'果汁成分含量'] = jd_pop_attrs.apply(lambda x: juice_percentage(x), axis = 1)


jd_pop_attrs[u'果汁成分含量'].replace(u'浓缩100%以下',u'100%以下', inplace = True)
jd_pop_attrs[u'包装'].replace(u'瓶装',u'其它',inplace = True)
jd_pop_attrs[u'包装'].replace(u'利乐装',u'其它',inplace = True)
jd_pop_attrs[u'包装'].replace(u'不限',u'其它',inplace = True)
jd_pop_attrs[u'包装'].replace(u'其他',u'其它',inplace = True)
jd_pop_attrs[u'分类'].replace(u'果汁',u'果蔬汁',inplace = True)
#a[u'功能饮料'].replace(u'运动饮料',u'能量饮料',inplace = True)
#a[u'碳酸饮料分类'].replace(u'雪碧/七喜',u'可乐',inplace = True)
#a[u'碳酸饮料分类'].replace(u'盐汽水',u'苏打水',inplace = True)
jd_pop_attrs[u'口味'].replace(u'混合果味',u'混合饮料',inplace = True)
jd_pop_attrs[u'口味'].replace(u'不限',u'其它',inplace = True)
jd_pop_attrs[u'口味'].replace(u'其他',u'其它',inplace = True)
#a[u'是否含糖'].replace(u'含木糖醇',u'含糖',inplace = True)
jd_pop_attrs[u'单件容量'].replace(u'其它',u'250mL及以下',inplace = True)
jd_pop_attrs[u'单件容量'].replace(u'250ml及以下',u'250mL及以下',inplace = True)
jd_pop_attrs[u'进口/国产'].replace(u'其它',u'国产',inplace = True)
jd_pop_attrs[u'产品产地'].replace(u'马来西亚',u'泰国',inplace = True)
jd_pop_attrs[u'产品产地'].replace(u'韩国',u'日本',inplace = True)
jd_pop_attrs[u'产品产地'].replace(u'港澳台',u'其它',inplace = True)
jd_pop_attrs[u'产品产地'].replace(u'澳大利亚',u'其它',inplace = True)
jd_pop_attrs[u'产品产地'].replace(u'印尼',u'泰国',inplace = True)

'''
first = jd_pop_attrs.iloc[:1033,:]
second = jd_pop_attrs.iloc[1033:,:]
'''
#jd_pop_attrs[u'品牌'].value_counts()


#import sku_price table
sku_price = pd.read_table('drinks.csv', sep=',',encoding='utf-8')
sku_price.drop(u'Unnamed: 0', axis = 1, inplace = True)
sku_price['sku_id'] = sku_price['item_sku_id']
sku_price.drop(['item_first_cate_cd','item_second_cate_cd',
                'item_third_cate_cd','item_sku_id'], axis = 1, inplace = True)

  
    
    
#merge jd_pop_attrs table with sku_price table based on sku_id 
jd_pop = pd.merge(jd_pop_attrs, sku_price, how = 'inner', on = 'sku_id')


jd_pop['price'] = jd_pop['price'].apply(lambda x: int(x))
jd_pop[u'sku价格'] = jd_pop['price']
jd_pop.drop('price', axis = 1, inplace = True)

#put the last column to the very front
cols = jd_pop.columns.tolist()
cols = cols[-1:]+cols[:-1]
jd_pop = jd_pop[cols]



#import warehouse price
warehouse_price = pd.read_csv('warehouse_price.csv', sep = '\t', encoding = 'utf-8')
warehouse_price.columns = ['sku_id','warehouse_price', 'dt']
warehouse_price2 = pd.read_csv('warehouse_price2.csv', sep = '\t', encoding = 'utf-8')
warehouse_price2.columns = ['sku_id','warehouse_price', 'dt']
warehouse_price3 = pd.concat([warehouse_price,warehouse_price2],ignore_index=True)


ware_groupby = warehouse_price3.groupby(['sku_id'])['warehouse_price'].mean()
ware_groupby = ware_groupby.reset_index()





#merge jd_pop attributes price and warehouseprice together
attr_price_ware = pd.merge(jd_pop,ware_groupby, how = 'inner', on = 'sku_id')
###
###here warehouse price only contains jd self data, not pop's and tmall's
###so this merge result is gonna be only jd training dataset

#label encoder method to handle discrete/categorical features except continuous features
for attribute in attr_price_ware.columns.difference([u'sku价格','sku_id','warehouse_price']):
    le = preprocessing.LabelEncoder()
    attr_price_ware[attribute] = le.fit_transform(attr_price_ware[attribute])

#normalize continuous features('sku价格, warehouse_price')
attr_price_ware[u'sku价格'] = attr_price_ware[u'sku价格'].apply(lambda x: 
    (x-attr_price_ware[u'sku价格'].mean())/(attr_price_ware[u'sku价格'].std()))

attr_price_ware[u'warehouse_price'] = attr_price_ware[u'warehouse_price'].apply(lambda x: 
    (x-attr_price_ware[u'warehouse_price'].mean())/(attr_price_ware[u'warehouse_price'].std()))
    
    
#handle high cardinality of brand feature using kmeans clustering
from sklearn.cluster import KMeans
X = attr_price_ware[[u'sku价格',u'产品产地',u'品牌']]
kmeans = KMeans(n_clusters = 20, random_state = 0).fit(X)
attr_price_ware[u'品牌'] = kmeans.labels_

'''
#use elbow method to find the best number of clusters
c = range(10,50)
ks = [KMeans(n_clusters = i) for i in c]
score = [ks[i].fit(X).score(X) for i in range(len(ks))]
plt.scatter(c,score)
'''

#import profit loss table to merge with training data
sku_profit = pd.read_table('app_cfo_profit_loss_b2c_det.csv', sep = '\t', encoding = 'utf-8')
sku_profit['sku_id'] = sku_profit['item_sku_id']
sku_profit.drop(['dt','item_third_cate_name','item_sku_id','cost_tax',
'income','grossfit','gross_sales','rebate_amunt_notax',
'adv_amount','store_fee','deliver_fee'], axis = 1, inplace = True)



#filter sku_profit table
sku_profit_1 = sku_profit[sku_profit['gmv'] >= 0.5 ]
sku_profit_2 = sku_profit[sku_profit['gmv'] <= -0.5 ]
sku_profit = pd.concat([sku_profit_1,sku_profit_2],ignore_index = True)
sku_profit = sku_profit[sku_profit['net_profit'] < sku_profit['gmv']]
#sns.distplot(final_npp['net_profit'] ) 观察net_profit分布情况


#make the profit_rate column
sku_profit['profit_rate'] = (sku_profit['net_profit']/sku_profit['gmv'])*100
#sku_profit[~np.isfinite(sku_profit)] = np.nan


#calculate the average gmv per sku_id
average_gmv = sku_profit.groupby('sku_id').agg({'gmv':'mean'})
average_gmv.reset_index(inplace=True)


sku_profit.drop(['net_profit','gmv'], axis =1, inplace = True)
sku_profit = sku_profit[sku_profit['profit_rate'] > -70]
sku_profit = sku_profit[sku_profit['profit_rate'] < 100]


#calculate the average profit per sku_id
average_profit = sku_profit.groupby('sku_id').mean()
average_profit.reset_index(inplace=True)

#merge avergae gmv and average profit table based on sku_id
gmv_netprofit = pd.merge(average_gmv,average_profit,on='sku_id',how='inner')


#merge jd_pop attributes_price_warehouseprice table and average gmv_netprofit table based on sku_id
net_profit_percent = pd.merge(attr_price_ware,gmv_netprofit, how = 'inner', on = 'sku_id')
#net_profit_percent['profit_rate'] = net_profit_percent['profit_rate'].astype(int)
net_profit_percent = net_profit_percent[net_profit_percent['profit_rate'] != 0]

net_profit_percent.drop('sku_id',axis = 1, inplace = True)


#normalize continuous features('gmv')
net_profit_percent['gmv'] = net_profit_percent['gmv'].apply(lambda x: 
    (x-net_profit_percent['gmv'].mean())/(net_profit_percent['gmv'].std()))
'''
k = net_profit_percent['profit_rate'].max()
l = net_profit_percent['profit_rate'].min()
m = k - l
v = net_profit_percent[net_profit_percent[u'分类'] == 0]['profit_rate']
v = v.apply(lambda x: (x-l)/m)
'''   


#normalize continuous features('profit_rate')
k = net_profit_percent['profit_rate'].max()
l = net_profit_percent['profit_rate'].min()
m = k - l
net_profit_percent['profit_rate'] = net_profit_percent['profit_rate'].apply(lambda x: (x-l)/ m)



    
if __name__ == '__main__':       
    #train_test_split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(net_profit_percent.drop('profit_rate',
                                                                                axis=1), 
                                                        net_profit_percent['profit_rate'], 
                                                        test_size=0.30,
                                                        random_state = 101)
   
    
    '''
    from sklearn.grid_search import GridSearchCV
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(  n_estimators = 500, 
                                  max_features = 'auto',
                                  max_depth=8,
                                  min_samples_leaf=3,
                                  min_samples_split=2,
                                  oob_score=True,
                                  #random_state = 42,
                                  n_jobs=-1,
                                  criterion = 'mae')
    param_grid = { 
    'max_depth':[5,7,8],
    'min_samples_leaf':[2,4],
    'min_samples_split':[4,8]
    }

    CV_rfc= GridSearchCV(estimator=rfr, param_grid=param_grid, cv=5)
    CV_rfc.fit(X_train, y_train) 
    print (CV_rfc.best_params_)
    '''
    
    
    #implement RandomForestregressor to solve regression problem    
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(  n_estimators = 500, 
                                  max_features = 'auto',
                                  max_depth=11,
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
    

    '''
    #log likelihood
    def ll(y_test, predictions):
        actual = np.array(y_test)
        predicted = np.array(predictions)
        err = np.seterr(all='ignore')
        score = -(actual*np.log(predicted)+(1-actual)*np.log(1-predicted))
        np.seterr(divide=err['divide'], over=err['over'],
                  under=err['under'], invalid=err['invalid'])
        if type(score)==np.ndarray:
            score[np.isnan(score)] = 0
        else:
            if np.isnan(score):
                score = 0
        return score
    '''
    
    #plt.scatter(y_test,predictions)
    print('MAE:', metrics.mean_absolute_error(y_test, predictions))
    print('MSE:', metrics.mean_squared_error(y_test, predictions))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    print('MAPE:', mean_absolute_percentage_error(y_test,predictions))
    print('MSLE:', mean_squared_log_error(y_test,predictions))
    
    #columns = net_profit_percent.columns
    #print (sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), columns),reverse=True)) 
    
       
    #subplots method of matplotlib 
    fig, axes = plt.subplots(nrows = 2, ncols = 1)
    axes[0].scatter(y_test, predictions)
    plt.sca(axes[1]) #Use the pyplot interface to change just one subplot
    plt.xticks(range(X_train.shape[1]),X_train.columns, color='r')
    axes[1].bar(range(X_train.shape[1]),rfr.feature_importances_, color= 'b',align = 'center')
    





















