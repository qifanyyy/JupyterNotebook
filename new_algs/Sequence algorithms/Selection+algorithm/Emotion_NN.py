import numpy as np
import random
import datetime
import matplotlib.pyplot as plt
from part3.process_data import process_data
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split,learning_curve,ShuffleSplit

#Global values
data,labels = process_data()

def make_pred(train_data,train_labels,test_data):
    clas = MLPClassifier(hidden_layer_sizes=(8,7,),solver='sgd',momentum=0.3,
                         learning_rate_init=0.04,activation='logistic',max_iter=10000)
    clas.fit(train_data,train_labels)
    predict = clas.predict(test_data)
    return predict

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

if __name__ == '__main__':

    seed = 4555
    random.seed(seed)
    np.random.seed(seed)
    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.3, shuffle=True)
    #print(np.shape(train_data))

    seed = 2834
    random.seed(seed)
    np.random.seed(seed)

    start_time = datetime.datetime.now()  # Track learning starting time
    result = make_pred(train_data, train_labels, test_data)
    end_time = datetime.datetime.now()  # Track learning ending time
    exection_time = (end_time - start_time).total_seconds()  # Track execution time
    acc = accuracy_score(test_labels, result)
    print('time spend=%.4f sec & acc=%.2f' % (exection_time, acc))

    title = 'Learning Curve MLP'
    clas = MLPClassifier(hidden_layer_sizes=(8, 7,), solver='sgd', momentum=0.3,
                         learning_rate_init=0.04, activation='logistic', max_iter=10000)
    cv = ShuffleSplit(n_splits=100,test_size=0.3,random_state=2834)
    plot_learning_curve(clas,title,data,labels,cv=cv,n_jobs=10)
    plt.savefig('../part3/NN_learning_curve.png')





