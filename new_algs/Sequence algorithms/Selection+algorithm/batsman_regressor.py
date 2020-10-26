from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
import pickle as pb 

df = pd.read_csv('./created/New_batsman_data_with_Score.csv') #5th is proper
# df.columns

necessary_cols = ['Matches_Played', 'Not_Out', 'Hundreds',
       'Fifties', 'Sixes', 'Fours', 'Highest_Score', 'Total_Runs', 'Avg',
       'Balls_Faced', 'Strike_Rate']
label_column = ['Player_Score']

x = df[necessary_cols]
y = df[label_column]

x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, test_size=0.1, random_state=542)
# x_train.shape, y_train.shape

lr = LinearRegression()
lr.fit(x_train, y_train)
conf_lr = lr.score(x_test, y_test)
# conf_lr

rfr = RandomForestRegressor(n_estimators=200)
rfr.fit(x_train, y_train)
score = rfr.score(x_test, y_test)
# score

with open('./models/linear_regressor_batsman.pb', 'wb') as f:
    pb.dump(lr, f)

with open('./models/random_forest_regressor_batsman.pb', 'wb') as f:
    pb.dump(rfr, f)

print('Done')