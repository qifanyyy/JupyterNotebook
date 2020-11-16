
# coding: utf-8

# # Feature Selection for Categorical Variables

# ## Calculation of IV and WOE for Categorical Variables

import pandas as pd
import numpy as np

import math
df4 = pd.read_csv('test.csv')
df4
m = pd.melt(df4, id_vars=['weights','ABOVE50K'], var_name='variables')
aggt1 = m.groupby(['variables','value','ABOVE50K'])['weights'].sum().reset_index()
aggt1

# Create a list of all the variables in the data
list = aggt1['variables'].unique()

# Converting the list into a dataframe
df1 = pd.DataFrame({'variables': list})
df2 = df1['variables'].tolist()

z={}
iv={}
k={}
for i in range(0,df1.shape[0]):
    x=df1.loc[i]['variables']
    temp3 = aggt1[(aggt1['variables']== x)]
    temp3 = temp3.drop(['variables'],axis =1)
    z[i] = pd.DataFrame(pd.pivot_table(temp3, 
                        values=['weights'],
                        index=['value'],
                        columns=['ABOVE50K'],
                        aggfunc=np.sum,
                        fill_value=0))
    z[i].index.name = None
    z[i].columns =[s1 + str(s2) for (s1,s2) in z[i].columns.tolist()]
    z[i].loc['col_totals']= z[i].sum()
    z[i]['total'] = z[i]['weights0'] + z[i]['weights1']
    # hard coded to be changed
    z[i]['pct_non_events'] = z[i]['weights0']/z[i].loc['col_totals'][0]
    z[i]['pct_events'] = z[i]['weights1']/z[i].loc['col_totals'][1]


    z[i]['woe'] = np.log(z[i]['pct_events']/z[i]['pct_non_events'])
    z[i]['iv'] = (z[i]['pct_events']-z[i]['pct_non_events'])*z[i]['woe']
    k[i] = z[i].sum()
    iv[i] = k[i]['iv']

s = pd.Series(iv, name='iv')
s1 = pd.DataFrame({'variables':df2,'iv':s.values})

s1

