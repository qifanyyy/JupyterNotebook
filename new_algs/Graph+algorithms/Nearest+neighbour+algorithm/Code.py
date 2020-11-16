from sklearn import datasets
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
iris = datasets.load_iris()
x = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=21, stratify=y)
df = pd.DataFrame(x, columns=iris.feature_names)
print(df.head())
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=6, p=2, weights='uniform')
x_new = np.array([(7.7, 2.8, 6.7, 2.0), (5.2, 3.1, 1.4, 0.2)], dtype=float)
prediction = knn.predict(X_test)

print('Prediction: \n {}'.format(prediction))
accuracy = knn.score(X_test, y_test)
print(accuracy)
