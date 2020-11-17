# Name: Qi Hong Chen
# Shallow learner - svm 

# Import statement

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.model_selection import GridSearchCV

# Load data using Panda
dataframe = open("result.txt")
# print("training instances = ", dataframe.describe())
# Split into a Training and Test Data
x = dataframe["Implementation"]
y = dataframe["Label"]
x_train, y_train = x[0: 8860], y[0: 8860]
x_test, y_test = x[8860: ], y[8860:]
# Extract feature
cv = CountVectorizer()
features = cv.fit_transform(x_train)
# Build a model
# tuned_parameters = {'kernel':['linear','rbf'], 'gamma':[1e-3, 1e-4], 'C':[1,10,100,1000]}
# tuned_parameters = {'C': 1, 'gamma': 0.0001, 'kernel': ['rbf']}
# model = GridSearchCV(svm.SVC(), tuned_parameters)
model = svm.SVC(C=1, gamma= 0.0001, kernel = 'rbf')
model.fit(features, y_train)
#print("best parameters = ", model.best_params_)
# Test accuracy
features_test = cv.transform(x_test)

print("Accuracy of the model is: ", model.score(features_test, y_test))
