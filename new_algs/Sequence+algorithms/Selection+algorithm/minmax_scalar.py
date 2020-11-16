import numpy as np
from sklearn import preprocessing

X_train = np.array([[ 1., -1.,  2.],
                    [ 2.,  0.,  0.],
                    [ 0.,  1., -1.]])

X_test = np.array([[2,3,3],
					[3,3,3]]
	)

X_test2 = np.array([[2,3,3],
					
					]
	)
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)
X_test_minmax = min_max_scaler.transform(X_test)
X_test_minmax2 = min_max_scaler.transform(X_test2)
X_train_minmax["testingcolumn"] = [1,2,3]
print(X_train_minmax)
print(X_test_minmax)
print(X_test_minmax2)