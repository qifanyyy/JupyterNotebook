import pandas as pd 
import numpy as np 
from data_clean import get_cleaned_batsman_data

df = get_cleaned_batsman_data()

def get_batsman(df):
    columns = ['Player_Name', 'Matches_Played', 'Not_Out', 'Hundreds', 'Fifties', 'Sixes', 
           'Fours', 'Highest_Score', 'Total_Runs', 'Avg', 'Balls_Faced', 'Strike_Rate', 'Player_Score']
    top_class = df.where(df['Player_Score'] > df['Player_Score'].mean() + 160).dropna()
    middle_class = df.where(df['Player_Score'] >= df['Player_Score'].mean() + 70).where(df['Player_Score'] <= df['Player_Score'].mean() + 160).dropna()
    low_class = df.where(df['Player_Score'] < df['Player_Score'].mean() + 70).dropna()
    
    top_class['Difference_avg_score'] = top_class['Player_Score'] - top_class['Avg']
    middle_class['Difference_avg_score'] = middle_class['Player_Score'] - middle_class['Avg']
    low_class['Difference_avg_score'] = low_class['Player_Score'] - low_class['Avg']
    
    batsman_6 = top_class.where(top_class['Difference_avg_score'] > 100).where(top_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(2)
    x = middle_class.where(middle_class['Difference_avg_score'] > 200).where(middle_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(3)
    y = low_class.where(low_class['Difference_avg_score'] > 100).where(low_class['Difference_avg_score'] < 300).dropna().sort_values(by='Avg', ascending=False).sample(1)
    
    return pd.concat([batsman_6, x, y]).to_csv('batsman_result.csv', index=False, columns=columns)
get_batsman(df)