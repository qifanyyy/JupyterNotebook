# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 10:48:48 2014
@author: snehasishbarman
"""

"""
@see http://scikit-learn.org/stable/modules/neighbors.html#neighbors
@see http://www.csie.ntu.edu.tw/~cjlin/papers/liblinear.pdf
@see http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC
@see http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
@see http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.score
@see http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
@see http://docs.scipy.org/doc/numpy/reference/
http://scikit-learn.org/stable/modules/grid_search.html#grid-search
http://scikit-learn.org/stable/auto_examples/plot_permutation_test_for_classification.html#example-plot-permutation-test-for-classification-py
http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
@see http://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
@see http://scikit-learn.org/stable/modules/learning_curve.html
@see http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
@see http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html - sparse matrix

Notes on shuffling: Do it only if data is IID and there is no implied ordering of time
"""

# preprocessing steps: counts, tf-idf, 
#                      tf-idf: min_df(0.2,0.033,0.04, 0.05), max_df(0.95), ngram, binary features, use_idf, smooth_idf
# Additional preprocessing: stemming, normalization - unit vector(by rows-instance, TF-IDF -> by feature), 
#                           take log, PCA, add NOT_ to indicate negation, include punctuations
# Linear SVM: C, loss=(l1, l2)
# KNN: k, weights, radius
# cv folds = 5, 10
# plot learning curves - cv generator, cross validation curve for the parameters - k, C, radius
# CV: stratified k-fold, stratified shuffle split (avoid class imbalance in validation set for accuracy measure)
# Approaches: Simple by taking one algo at a time, Grid Search
# Reporting headers: learning algorithm, knobs tweaked, preprocessing steps took, time taken(secs), 
#                    confusion matrix, accuracy, roc, explanation & findings
# What did you find in the data?
# What classifier worked better?
# Which parameters worked better?

from sklearn.feature_extraction import text
import sklearn.svm as svm
import sklearn.neighbors as nbrs
import sklearn.pipeline as pipes
import sklearn.grid_search as gs
import sklearn.datasets as skdata
import sklearn.cross_validation as cv
from sklearn import metrics
import sklearn.learning_curve as lc
import matplotlib.pyplot as plt
import numpy as np


def displayParameters(grid):
    for x in grid.grid_scores_:
        print x.parameters
        print "Mean Score = %f, CV = %s" % (x.mean_validation_score, x.cv_validation_scores)
        print
        
def displayBestParameters(model):
    print model.best_estimator_
    print "Mean accuracy on validation set = %f" % model.best_score_
    print model.best_params_
    print model.scorer_
    
def evaluateModel(model, Xtest, ytest):
    ypred = model.predict(Xtest)
    print metrics.accuracy_score(ytest, ypred)
    print
    print metrics.classification_report(ytest, ypred, target_names=dataset["target_names"])
    print
    print metrics.confusion_matrix(ypred, ytest)
    
def learnCurves(lalg, Xtrain, ytrain, folds):
    train_sizes, train_scores, test_scores = lc.learning_curve(lalg, Xtrain, ytrain, 
                                train_sizes=np.linspace(0.1, 1.0, 10), 
                                cv=cv.StratifiedKFold(ytrain, n_folds=folds), 
                                scoring=metrics.make_scorer(metrics.accuracy_score, True), verbose=2)
    train_scores = np.apply_along_axis(lambda x:1-x, 1, train_scores)
    test_scores = np.apply_along_axis(lambda x:1-x, 1, test_scores)                            
    return (train_sizes, train_scores, test_scores)
    
def plotLearningCurves(train_sizes, train_scores, test_scores):
    plt.figure()
    plt.title("Learning Curve")
    plt.xlabel("Training examples")
    plt.ylabel("Error")
    plt.ylim(-0.1, 0.6)
    plt.grid()
    train_scores_mean = np.mean(train_scores, axis=1)
    plt.plot(train_sizes, train_scores_mean, '-', color="r", label="Training error")
    test_scores_mean = np.mean(test_scores, axis=1)
    plt.plot(train_sizes, test_scores_mean, '-', color="g", label="Cross-validation error")
    plt.legend(loc="best")
    plt.show()

# load the dataset
movie_reviews_data_folder = "../review_polarity/txt_sentoken"
dataset = skdata.load_files(movie_reviews_data_folder, shuffle=False, random_state=53)
print dataset.keys()
print "n_samples: %d" % len(dataset["data"])

# split the dataset in training and test set:
X_train, X_test, y_train, y_test = cv.train_test_split(
               dataset.data, dataset.target, test_size=0.25, random_state=53)
print [(len(data), type(data)) for data in [X_train, X_test, y_train, y_test]]

#==============================================================================
# LA: Linear SVC (l2 regularized, l2-loss, dual optimization)
# Preprocessing knobs: min_df(0.02,0.033,0.04, 0.05), max_df(0.95)
#                      ngram_range: (1, 1), (1, 2)
#                      use_idf: True(tf-idf), False(tf)
#                      binary: False, True(use_idf=False, norm=None)
# LA knobs: C: {0.0001, 0.01, 0.1, 1.0, 10.0, 100.0, 500.0, 700.0, 1000.0}
#           loss: l1, l2
# CV: stratified 10-fold
#     stratified shuffle split, n_iter = 10, test_size = 0.25
#==============================================================================
tfidf = text.TfidfVectorizer()
tfidf.set_params(analyzer="word", max_df=0.95, ngram_range=(1, 1), use_idf=True)
svc = svm.LinearSVC()
svc.set_params(verbose=1, loss="l2", random_state=53)
pip_svm = pipes.Pipeline([("tfidf", tfidf), ("lalg", svc)])
parameter_grid = [ {"tfidf__min_df":[7, 0.02, 0.033, 0.04, 0.05], 
                    #"tfidf__ngram_range":[(1, 1), (1, 2)], 
                    #"tfidf__use_idf":[True, False],
                    #"tfidf__binary":[False, True], 
                    "lalg__C":[0.0001, 0.01, 0.1, 1.0, 10.0, 100.0, 500.0, 700.0, 1000.0], 
                    #"lalg__loss": ["l2", "l1"]
                    } ]
gs_svc_model = gs.GridSearchCV(pip_svm, parameter_grid, 
                               scoring=metrics.make_scorer(metrics.accuracy_score, True), 
                               n_jobs=1, verbose=1, 
                               cv=cv.StratifiedKFold(y_train, n_folds=5))            
gs_svc_model.fit(X_train, y_train)
displayParameters(gs_svc_model)    
displayBestParameters(gs_svc_model)
evaluateModel(gs_svc_model.best_estimator_, X_test, y_test)

# pre-process the data before plotting the learning curves
fitted_model_svc = pipes.Pipeline([("tfidf", text.TfidfVectorizer(analyzer="word", max_df=0.95, ngram_range=(1, 1), use_idf=True, min_df=0.02)), 
                                   ("lalg", svm.LinearSVC(verbose=1, loss="l2", C=1.0, random_state=53))])
x = learnCurves(fitted_model_svc, X_train, y_train, 5)
print x[2]
plotLearningCurves(x[0], x[1], x[2])

# Analyze the SVC model results
tfidf_anz_svc = text.TfidfVectorizer(analyzer="word", max_df=0.95, ngram_range=(1, 1), use_idf=True, 
                                     min_df=0.02)
tfidf_anz_svc.fit(X_train)
Xtrain_transformed = tfidf_anz_svc.transform(X_train)
svc_anz = svm.LinearSVC(C=1.0, loss="l2", random_state=53)
svc_anz.fit(Xtrain_transformed, y_train)
Xtest_transformed = tfidf_anz_svc.transform(X_test)
ypred = svc_anz.predict(Xtest_transformed)
evaluateModel(svc_anz, Xtest_transformed, y_test)
temp = zip(ypred, y_test)
pred_0_act_0 = [i for i in range(0, len(temp)) if temp[i][0] == 0 and temp[i][1] == 0]
pred_1_act_1 = [i for i in range(0, len(temp)) if temp[i][0] == 1 and temp[i][1] == 1]
pred_0_act_1 = [i for i in range(0, len(temp)) if temp[i][0] == 0 and temp[i][1] == 1]
pred_1_act_0 = [i for i in range(0, len(temp)) if temp[i][0] == 1 and temp[i][1] == 0]

X_test[87]
print pred_0_act_0
xx = Xtest_transformed.todense()

sentinel = {}
for idx in pred_0_act_1:
    for col in range(0, xx.shape[1]):
        if xx[idx, col] != 0:
            nm = tfidf_anz_svc.get_feature_names()[col]
            if nm not in sentinel:
                sentinel[nm] = 1
            else:
                sentinel[nm] = sentinel[nm] + 1
print sorted(sentinel.items(), key=lambda x: x[1], reverse=True)


# Observation: with C=1.0 and min_df=0.02, we get 82.2% accuracy on test set. 
# [[206  52]
# [ 37 205]]
# 0.822
# as with his other stateside releases , jackie chan's latest chopsocky vehicle , mr . nice guy , is contrived , blockheaded , and lacking in narrative logic . \nbut also like those other films , it is a highly enjoyable ride . \nonce again , chan's screenwriters ( here edward tang and fibe ma ) have taken the easy way out and named their star's character simply jackie , with no last name . \nthis jackie is a world-class chef who co-hosts a popular cooking show on australian television . \nof course , jackie also happens to be a talented martial artist , and these skills come in handy when he becomes involved in an ambitious reporter's ( gabrielle fitzpatrick ) expose of a drug dealing ring . \nother plot details , involving a videotape and a biker gang , are irrelevant ; in fact , as is the case with most chan films , the plot itself is just about irrelevant . \nthe sole purpose of mr . nice guy's existence are chan's comic fight scenes , and those here do not disappoint . \ndirector samo hung ( who has a cameo role ) , a longtime collaborator of chan's , does not waste any time putting chan in action , diving head-on into a wild chase/fight/shootout after a brief cooking show prologue . \nother impressive set pieces follow , most notably a chase in a mall , which directly leads to some frenzied , if cliched ( can you say fruit cart ? ) , business involving a runaway carriage ; and an extended late-film sequence at a construction site , in which a hilarious pursuit through a maze of blue doors culminates in some exciting fights involving boards , cement mixers , and a deadly buzzsaw . \nnone of the action sequences in mr . nice guy are as spectacular as supercop's thrilling helicopter-train finale or rumble in the bronx's daring leap between two buildings ; nor is anything as inventive as the ladder fight or air tunnel climax in first strike and operation condor , respectively . \nbut the action delivers , even if the energy peters out before the film's end ( the finale , as spectacular as it is , is a letdown for fans of chan's athletic prowess ) . \nfilmed almost entirely in english ( even so , the voices of some english-speaking actors are laughably dubbed ) , mr . nice guy hints at jackie chan's latest transition to hollywood productions ( he made ill-fated attempts with 1980's the big brawl and 1985's the protector ) ; next in the pipeline is rush hour , a stateside production co-starring chris tucker . \nhopefully that film will be a mere diversion in tinseltown , and chan will continue with exuberant hong kong productions such as mr . nice guy , for his unique charm and reckless abandon are sure to be diluted by american hands , much like they have been before . \n"
# phew , what a mess ! \nfor his fifth collaboration with director rich- ard donner ( lethal weapon i-iii , maverick ) , mel gibson plays a motormouth , maybe mentally ill new york city cabbie , jerry , whose wild conspiracy theories are all but ignored by alice ( julia roberts , acting all serious ) , the justice department employee that he has a crush on . \nshe not interested , but another person is : a cia psychiatrist ( patrick stewart ) who promptly kidnaps him . \nis one of jerry's conjectures correct ? \n * is * the metal strip in the new $100 bill being used to track your movements ? \nis oliver stone still alive , because he cut a deal with george bush to spread * dis * information ? \nis this movie really about * any * of the crazed cabbie's theories ? \nno , no , and no . \nas it turns out , there's some other nonsense going on here , involving and revolving around jerry's background . \n ( hint : pay attention to an early scene where jerry blacks out and flashes back , in quick succession , to images of an interrogation room , hypodermic needles , and ms . roberts herself . ) \nthe * initial * premise is pretty good and is played , for a while , at a delightfully dizzying clip . \nmel is wider-open that we've ever seen him and , if his character's relationship with roberts' initially strains credibility , their combined star power is blissfully intoxicating . \n ( the highest wattage of the summer , perhaps ? ) \neven when the plot contrivances begin to intrude , the two remain a randy dandy screen pair . \nthere's a great scene in jerry's fortress , er , apartment , with alice trying to act casual as her hyperactive host tries to remember the combination to a locked coffee bean container . \n ( which he stores in another locked con- tainer , his fridge . ) \nother hilarious moments , of which there are many , include a trio of memorable convention-breakers , where alice ditches a tail , jerry cold-cocks someone , and , later , eludes a foot pursuit , each in a uproariously unexpected fashion . \n ( that's donner's own ladyhawke playing in the theater , btw . ) \nlet's see , other pleasures include . . . \na brilliant title sequence , a jazzy score from carter burwell , and the worth-paying-to-see sight of roberts pumping lead into one bad guy and slamming another's head into a wall . \noh , pretty woman ! \ngetting to the latter , however , requires slogging through an increasingly overburdened and ultimately unappealing story . \nthe last hour of conspiracy theory devolves from tolerable to torturous to almost unwatchable . \nmore stuff happens of the stupid shit variety than is worth mentioning here , except , perhaps , for a late sequence that has alice locating jerry in an abandoned wing of a mental hospital by hearing his voice carrying through the air ducts . \nand here i thought it was wabbit season . \ngood god , who rewrites these movies ? \nand do they arrive in nondescript black vehicles ? \n"


#==============================================================================
# LA: KNN
# Preprocessing knobs: min_df(3, 7, 0.02,0.033,0.04, 0.05), max_df(0.95)
#                      ngram_range: (1, 1), (1, 2)
#                      use_idf: True(tf-idf), False(tf)
#                      binary: False, True(use_idf=False, norm=None)
# LA Knobs: n_neighbors: [1-15]
#           weights: uniform, distance
#           metric: ["euclidean", cosine", "manhattan", "cityblock"]
# CV: stratified 10-fold
#     stratified shuffle split, n_iter = 5, 10, test_size = 0.25
#==============================================================================
tfidf_knn = text.TfidfVectorizer()
tfidf_knn.set_params(analyzer="word", max_df=0.95, ngram_range=(1, 1), use_idf=False, min_df=0.02,
                     binary=True)
knn = nbrs.KNeighborsClassifier(weights="distance", metric="euclidean")
pip_knn = pipes.Pipeline([("tfidf", tfidf_knn), ("lalg", knn)])
parameter_grid = [ {#"tfidf__min_df":[3, 7, 0.02, 0.033, 0.04, 0.05], 
                    #"tfidf__ngram_range":[(1, 1), (1, 2)], 
                    #"tfidf__use_idf":[True, False],
                    #"tfidf__binary":[False, True],
                    "tfidf__norm":[None, "l2"],
                    "lalg__n_neighbors": range(1, 15),
                    #"lalg__metric": ["euclidean", "cosine", "manhattan", "cityblock"] 
                    #"lalg__weights": ["uniform", "distance"],
                    #"lalg__p": [2, 3, 4, 5]
                    } ]
gs_knn_model = gs.GridSearchCV(pip_knn, parameter_grid, 
                               scoring=metrics.make_scorer(metrics.accuracy_score, True), 
                               n_jobs=1, verbose=3, 
                               cv=cv.StratifiedKFold(y_train, n_folds=5))            
gs_knn_model.fit(X_train, y_train)
displayParameters(gs_knn_model)    
displayBestParameters(gs_knn_model)
evaluateModel(gs_knn_model.best_estimator_, X_test, y_test)

# pre-process the data before plotting the learning curves
fitted_model_knn = pipes.Pipeline([("tfidf", text.TfidfVectorizer(analyzer="word", max_df=0.95, ngram_range=(1, 1), use_idf=False, min_df=0.02, binary=True)), 
                                   ("lalg", nbrs.KNeighborsClassifier(metric="euclidean", 
                                                                      n_neighbors=14, 
                                                                      weights="distance"
                                                                      ))])
x = learnCurves(fitted_model_knn, X_train, y_train, 5)
print x[2]
plotLearningCurves(x[0], x[1], x[2])

# best values set 1: Training set accuracy = 0.676667
# {'lalg__n_neighbors': 7, 'lalg__weights': 'distance', 'lalg__p': 2}
#==============================================================================
# 0.684
# 
# [[148  63]
# [ 95 194]]
#==============================================================================

# Analyze KNN model results
tfidf_anz = text.TfidfVectorizer(analyzer="word", max_df=0.95, ngram_range=(1, 1), 
                                 use_idf=False, min_df=0.02, binary=True, norm="l2")
tfidf_anz.fit(X_train)
Xtrain_transformed = tfidf_anz.transform(X_train)
knn_anz = nbrs.KNeighborsClassifier(weights="distance", metric="euclidean", n_neighbors=14)
knn_anz.fit(Xtrain_transformed, y_train)
Xtest_transformed = tfidf_anz.transform(X_test)
ypred = knn_anz.predict(Xtest_transformed)
print metrics.confusion_matrix(ypred, y_test)
print metrics.accuracy_score(y_test, ypred)
temp = zip(ypred, y_test)
pred_0_act_1 = [idx for idx in range(0, len(temp)) if temp[idx][0] == 0 and temp[idx][1] == 1]
pred_1_act_0 = [idx for idx in range(0, len(temp)) if temp[idx][0] == 1 and temp[idx][1] == 0]
print pred_0_act_1
print pred_1_act_0
dist, ind = knn_anz.kneighbors(Xtest_transformed[325, :])
print dist, ind
print [y_train[i] for i in ind]
X_test[24]
# our observation on pred_0_act_1: it seems that the test point was placed in the vicinity of neg 
#       short distances and pos reviews were far from the test point. May our preprocessing metric
#       was wrong which had placed the test point in the vicinity of neg points. (24, 376)
# our observation on pred_1_act_0: it seems that for few test points, majority vote isn't working in 
#       favor of them as the neg points are much to closer to the test point. In some cases, pos points 
#       are computed nearby whereas neg points are far apart as in the the 1st case. (325, 321)
# TF-IDF based transformation may not be working in case of KNN
# By binarization and normalizing our features, we see an improvement of 7% (74.4%)
# [[190  75]
# [ 53 182]]
# By binarization, normalizing our features and k=14, we see further improvement of 4% (78.6%)
# [[199  63]
# [ 44 194]]
# Conclusion: choose an apt normalization procedure, distance metric, tie-breaking strategy, or reduce dimensionality  
#             to get better results



