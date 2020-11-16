
# coding: utf-8

# ## Calculating Chi Square for the existing data

# #### Importing the libraries

import pandas as pd
import numpy as np
import scipy.stats as stats

# Importing the data for Chi Square test
test_data = pd.read_csv('Data for Chi Square test-1.csv')
test_data.head()

# Aggregating the numbers for each segment and Geico Buyers numbers
aggt1 = test_data.groupby(['type_segment','segment','geico_buyers'])['nbi_person_id'].count().reset_index()
# # Renaming the column
# aggt = aggt.rename(columns={'nbi_person_id': 'count_pids'})
list = aggt1['type_segment'].unique()

df1 = pd.DataFrame({'type_segment': list})
#df2 = df1['type_segment'].tolist()
df1

## Calculation of Chi-Square for the given product
no_cols = {}
no_rows = {}
z = {}
observed ={}
expected = {}
total_obs = {}
net = {}
degrees_of_freedom = {}
chi_square = {}
p_value = {}

for i in range(0,df1.shape[0]):
    x=df1.loc[i]['type_segment']
    temp3 = aggt1[(aggt1['type_segment']== x)]
    temp3 = temp3.drop(['type_segment'],axis =1)
    renamed_aggt = temp3.rename(columns = {'nbi_person_id' : 'count_pids'})
    z[i] = pd.DataFrame(pd.pivot_table(renamed_aggt, 
                        values=['count_pids'],
                        index=['segment'],
                        columns=['geico_buyers'],
                        aggfunc=np.sum,
                        fill_value=0))
    no_cols[i] = z[i].shape[1]
    no_rows[i] = z[i].shape[0]
    
    ## Degrees of freedom
    degrees_of_freedom[i] = (no_cols[i]-1)*(no_rows[i]-1)
    z[i].columns =[s1 + str(s2) for (s1,s2) in z[i].columns.tolist()]
    z[i].index.name = None
    z[i].loc['col_totals']= z[i].sum()
    z[i]['row_totals'] = z[i]['count_pids0'] + z[i]['count_pids1']
    total_obs[i] = z[i].iloc[no_rows[i]][no_cols[i]]
    observed[i] = z[i].iloc[0:no_rows[i],0:no_cols[i]]
    
    # Expected Matrix Calculation                    
    expected[i] =  np.outer(z[i]["row_totals"][0:no_rows[i]],
                     z[i].loc["col_totals"][0:no_cols[i]]) / total_obs[i]
    expected[i] = pd.DataFrame(expected[i])
    expected[i].columns = ["count_pids0","count_pids1"]
    expected[0].index = observed[0].index
    
    # Chi Square calculation
    net[i] = pd.DataFrame((observed[i].values-expected[i].values)**2/expected[i].values, columns=observed[i].columns, index=observed[i].index)
    chi_square[i] = net[i].sum().sum()
    
    ## p-value
    p_value[i]=stats.distributions.chi2.sf(chi_square[i], degrees_of_freedom[i])

p_value

s = pd.Series(p_value, name='p_value')
s1 = pd.DataFrame({'type_segment':df2,'p_value':s.values})
s1.sort_values(by=['p_value'],ascending =False)

import math
df4 = pd.read_csv('test.csv')
m = pd.melt(df4, id_vars=['weights','ABOVE50K'], var_name='Name')
aggt1 = m.groupby(['Name','value','ABOVE50K'])['weights'].sum().reset_index()
# aggt1

# Create a list of all the variables in the data
list = aggt1['Name'].unique()

# Converting the list into a dataframe
df1 = pd.DataFrame({'variables': list})
df1

#
z = pd.DataFrame(pd.pivot_table(aggt1, 
                    values=['weights'],
                    index=['value'],
                    columns=['ABOVE50K'],
                    aggfunc=np.sum,
                    fill_value=0))
z.index.name = None
z.columns =[s1 + str(s2) for (s1,s2) in z.columns.tolist()]
z.loc['col_totals']= z.sum()
z['total'] = z['weights0'] + z['weights1']
# hard coded to be changed
z['pct_non_events'] = z['weights0']/24720
z['pct_events'] = z['weights1']/7481


z['woe'] = np.log(z['pct_events']/z['pct_non_events'])
z['iv'] = (z['pct_events']-z['pct_non_events'])*z['woe']
z
