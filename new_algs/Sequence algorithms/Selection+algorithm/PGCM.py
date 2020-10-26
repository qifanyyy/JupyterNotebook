'''
PCA and General Decision Tree algorithm
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 19.11.2014
'''
import datareader, mushrooms_bfgs, mlpy, nltk, datetime

def make_feature_set(model_X, model_y, x, y):
	'''
	Input : Model input data
	Output : New input on the basis of pair selection
	'''
	(new_mod_X, new_mod_y) = [],[]
	index = 0  
	for ind_feature in model_X : 
		new_mod_X.append((ind_feature[x],ind_feature[y]))
		new_mod_y.append(model_y[index])
		index += 1
	return (new_mod_X,new_mod_y)

def makeData(train_X, train_y, test_X, test_y, x, y):
	'''
	Input : Training and Testing Data along with which feature pair
			to choose
	Output : New Training and Testing Data
	'''
	(new_tr_X, new_tr_y, new_ts_X, new_ts_y) = [],[],[],[]
	(new_tr_X, new_tr_y) = make_feature_set(train_X, train_y, x, y)
	(new_ts_X, new_ts_y) = make_feature_set(test_X, test_y, x, y)
	return (new_tr_X, new_tr_y, new_ts_X, new_ts_y)

def makePairs(train_X, train_y, test_X, test_y):
	'''
	Input : Net Training and Testing Data
	Output : PGCM Matrix
	'''
	PGCM_0 = {}
	N = len(train_X[0]) - 1
	print "Number of Features ", N
	for i in xrange(1, N+1): 
		for j in xrange(i + 1, N+1):
			(new_tr_X, new_tr_y, new_ts_X, new_ts_y) = makeData(
			train_X, train_y, test_X, test_y, i, j)
			classifier = mushrooms_bfgs.train_decision_tree(
									new_tr_X, new_tr_y)
			PGCM_0[(i,j)] = nltk.classify.accuracy(classifier, 
							mushrooms_bfgs.test_decision_tree(
							new_ts_X, new_ts_y))*100
			print "Finding Accuracy for", i, j
	return PGCM_0

if __name__ == "__main__":
	timeStart = datetime.datetime.now()
	(train_X, train_y, test_X, test_y) = mushrooms_bfgs.initialize(float(1)/2)
	print "Number of Training Data =",len(train_y)
	print "Number of Testing Data =",len(test_y)
	PGCM_0 = makePairs(train_X, train_y, test_X, test_y)
	print "Total time taken = ", datetime.datetime.now() - timeStart
	f = open("PGCM_0", 'w')
	f.write(str(PGCM_0))
	f.close()
	print "Written to PGCM File"
	
