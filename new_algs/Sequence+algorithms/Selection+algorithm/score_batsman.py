import pandas as pd 
import numpy as np 
import pickle as pb 

# Random Forest Models for both batsman and bowler
with open('./models/random_forest_regressor_batsman.pb', 'rb') as f:
    rfr_batsman = pb.load(f)

batsman_cols = ['Matches_Played', 'Not_Out', 'Hundreds', 'Fifties', 'Sixes', 'Fours', 'Highest_Score', 'Total_Runs', 'Avg', 'Balls_Faced', 'Strike_Rate']

# bowlers_cols = ['MP', 'BB', 'R', 'W', '5WI', '10WM', 'Avg', 'SR', 'Econ']

df = pd.read_excel('./dataset/Batsmen_Data.xlsx')

def get_score(df):
    attributes = df[batsman_cols].values
    pred = rfr_batsman.predict(attributes)
    return pred

df['score'] = get_score(df)
df.to_csv('output.csv', index=False)

def get_batsman(df):
    columns = ['Player_Name', 'Matches_Played', 'Not_Out', 'Hundreds', 'Fifties', 'Sixes', 
           'Fours', 'Highest_Score', 'Total_Runs', 'Avg', 'Balls_Faced', 'Strike_Rate', 'score']
    top_class = df.where(df['score'] > df['score'].mean() + 160).dropna()
    middle_class = df.where(df['score'] >= df['score'].mean() + 70).where(df['score'] <= df['score'].mean() + 160).dropna()
    low_class = df.where(df['score'] < df['score'].mean() + 70).dropna()
    
    top_class['Difference_avg_score'] = top_class['score'] - top_class['Avg']
    middle_class['Difference_avg_score'] = middle_class['score'] - middle_class['Avg']
    low_class['Difference_avg_score'] = low_class['score'] - low_class['Avg']
    
    x = top_class.where(top_class['Difference_avg_score'] > 100).where(top_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(2)
    y = middle_class.where(middle_class['Difference_avg_score'] > 200).where(middle_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(3)
    z = low_class.where(low_class['Difference_avg_score'] > 100).where(low_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(1)
    
    return pd.concat([x, y, z]).to_csv('batsman_result2.csv', index=False, columns=columns)
get_batsman(df)