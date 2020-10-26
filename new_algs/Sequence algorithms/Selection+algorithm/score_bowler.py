import pandas as pd 
import numpy as np 
import pickle as pb 

# Random Forest Models for both batsman and bowler
with open('./models/random_forest_regressor_bowlers.pb', 'rb') as f:
    rfr_bowler = pb.load(f)

bowlers_cols = ['MP', 'BB', 'R', 'W', '5WI', '10WM', 'Avg', 'SR', 'Econ']

df = pd.read_excel('./dataset/BowlersData2.xlsx')

def get_score(df):
    attributes = df[bowlers_cols].values
    pred = rfr_bowler.predict(attributes)
    return pred

df['score'] = get_score(df)

top_class = df.where(df['score'] > df['score'].mean() + 50).dropna()
middle_class = df.where(df['score'] > df['score'].mean()).where(df['score'] <= df['score'].mean() + 50).dropna()
low_class = df.where(df['score'] <= df['score'].mean()).dropna()

# Players Selection
a = top_class.sample(2)
b = middle_class.sample(2)
c = low_class.sample(1)

pd.concat([a,b,c]).to_csv('bowlers_result2.csv', index=False)