import pandas
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sensitivity_specificity import true_false


class rf_algorithm:
	def __init__(self):
		print("the rf.py is called");

	def rf_code(self):
		heart = pandas.read_csv("pc.csv")
		#print(heart.describe())
		heart.loc[heart["heartpred"] == 2, "heartpred"] = 1
		heart.loc[heart["heartpred"] == 3, "heartpred"] = 1
		heart.loc[heart["heartpred"] == 4, "heartpred"] = 1
		heart["slope"] = heart["slope"].fillna(heart["slope"].median())
		heart["thal"] = heart["thal"].fillna(heart["thal"].median())
		heart["ca"] = heart["ca"].fillna(heart["ca"].median())
		#print(heart.describe())
		predictors=["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]
		alg=RandomForestClassifier(n_estimators=75,min_samples_split=20,min_samples_leaf=1)
		kf=KFold(heart.shape[0],n_folds=10, random_state=1)
		predictions = []
		for train, test in kf:
		    # The predictors we're using the train the algorithm.  Note how we only take the rows in the train folds.
		    train_predictors = (heart[predictors].iloc[train,:])
		    #print(train_predictors)
		    # The target we're using to train the algorithm.
		    train_target = heart["heartpred"].iloc[train]
		    #print(train_target)
		    # Training the algorithm using the predictors and target.
		    alg.fit(train_predictors, train_target)
		    # We can now make predictions on the test fold
		    test_predictions = alg.predict(heart[predictors].iloc[test,:])
		    predictions.append(test_predictions)
		# The predictions are in three separate numpy arrays.  Concatenate them into one.  
		# We concatenate them on axis 0, as they only have one axis.
		predictions = np.concatenate(predictions, axis=0)

		# Map predictions to outcomes (only possible outcomes are 1 and 0)
		predictions[predictions > .5] = 1
		predictions[predictions <=.5] = 0

		plot_predicted=[]
		plot_original=[]
		i=0
		count=0

		for each in heart["heartpred"]:
			plot_original.append(float(each))
			plot_predicted.append(float(predictions[i]))
			if each==predictions[i]:
				count+=1
			i+=1

		accuracy = count/i

		print("Confusion matrix is: ")
		cm = confusion_matrix(plot_original, plot_predicted)
		print(cm)

		true_false(cm)

		return accuracy, plot_original, plot_predicted