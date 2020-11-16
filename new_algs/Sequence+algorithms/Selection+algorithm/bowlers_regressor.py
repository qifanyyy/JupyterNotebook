from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np 
import pandas as pd 
from best_bowlers import get_df_with_score
from sklearn.linear_model import LinearRegression
import pickle as pb

nec_columns = ['Player', 'MP', 'BB', 'R', 'W', '5WI', '10WM', 'Avg', 'SR', 'Econ', 'score']

df = get_df_with_score()

df = df[nec_columns]
# df.sample(5)
x = df[['MP', 'BB', 'R', 'W', '5WI', '10WM', 'Avg', 'SR', 'Econ']]
y = df[['score']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=True, random_state=4545)
# x_train.shape, y_train.shape
rfr = RandomForestRegressor(n_estimators=200)
rfr.fit(x_train, y_train)
score = rfr.score(x_test, y_test)
print('Random Forest Regressor Score:', score)

lr = LinearRegression()
lr.fit(x_train, y_train)
score = lr.score(x_test, y_test)
print('Linear Regressor Score:', score)

# Saving the model
with open('./models/random_forest_regressor_bowlers.pb', 'wb') as f:
    pb.dump(rfr, f)

with open('./models/linear_regressor_bowlers.pb', 'wb') as f:
    pb.dump(lr, f)

