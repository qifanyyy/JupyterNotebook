import pandas as pd 
import numpy as np 

nec_columns = ['Player', 'MP', 'BB', 'R', 'W', '5WI', '10WM', 'Avg', 'SR', 'Econ', 'score']

def get_df_with_score(file_path):
    if 'xlsx' in file_path:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    def score_function(df):
        score = df['W']*10 + df['5WI']*10 + df['10WM']*20 + ((1/df['Avg'] + 1/df['SR'] + 1/df['Econ']) * 100)
        return score.round(2)

    df['score'] = score_function(df)

    return df

df = get_df_with_score(file_path='./dataset/BowlersData2.xlsx')

top_class = df.where(df['score'] > df['score'].mean() + 50).dropna()
middle_order = df.where(df['score'] > df['score'].mean()).where(df['score'] <= df['score'].mean() + 50).dropna()
low_class = df.where(df['score'] <= df['score'].mean()).dropna()

# top_class.shape, middle_order.shape, low_class.shape

# Players Selection
a = top_class.sample(2)
b = middle_order.sample(2)
c = low_class.sample(1)

pd.concat([a,b,c]).to_csv('bowlers_result.csv', index=False, columns=nec_columns)