# Name: Qi Hong Chen
# Shallow learner - svm 

# Import statement

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.model_selection import GridSearchCV

dataframe = open("result.txt")
# Split into a Training and Test Data
x = dataframe["Implementation"]
y = dataframe["Label"]
x_train, y_train = x[0: 8860], y[0: 8860]
x_test, y_test = x[8860: ], y[8860:]
# Extract feature
cv = CountVectorizer()
features = cv.fit_transform(x_train)
# Build a model
model = svm.SVC(C=1, gamma= 0.0001, kernel = 'rbf')
model.fit(features, y_train)

features_test = cv.transform(x_test)

print("Accuracy of the model is: ", model.score(features_test, y_test))
