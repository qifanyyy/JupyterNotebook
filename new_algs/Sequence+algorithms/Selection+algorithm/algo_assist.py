import time
import pandas as pd
from .cleaning import clean_df

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, RandomForestRegressor, ExtraTreesRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, SGDClassifier, SGDRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score
from sklearn.svm import SVC, SVR


REGRESSION_ALGOS = [LinearRegression, RandomForestRegressor, ExtraTreesRegressor, DecisionTreeRegressor, SGDRegressor, SVR, GradientBoostingRegressor, KNeighborsRegressor, AdaBoostRegressor]
CLASSIFICATION_ALGOS = [RandomForestClassifier, ExtraTreesClassifier, LogisticRegression, DecisionTreeClassifier, SGDClassifier, SVC, GradientBoostingClassifier, KNeighborsClassifier, GaussianNB, AdaBoostClassifier]


REGRESSION_METRICS = [mean_absolute_error, mean_squared_error, explained_variance_score]
CLASSIFICATION_METRICS = [f1_score, precision_score, recall_score, accuracy_score]

REGRESSION = "Reg"
CLASSIFICATION = "Cla"

DEFAULT_REGRESSION_METRIC = mean_absolute_error
DEFAULT_CLASSIFICATION_METRIC = accuracy_score

DASH_LENGTH = 30


class SplitNotInRange(Exception):
    pass

class RegOrClassNotDefined(Exception):
    pass


class NotPandasDataFrame(Exception):
    pass


class NotPandasSeries(Exception):
    pass


class MetricNotDefined(Exception):
    pass


class AlgoToBeComparedNotDefined(Exception):
    pass


class NotString(Exception):
    pass


class ColumnNotDefined(Exception):
    pass


def compare_algos(df, y, split = 0.7, reg_or_class = '', metric = None, algos_to_be_compared = []):
    '''

    A function compare the algorithms that are suitable for the dataset and get the best algorithm
    in terms of accuracy, time of execution etc.

    Parameters
    ----------
    df: Pandas Dataframe, Required
        - Dataframe with the whole dataset, splitting is done by default or as specified by you.
    
    Y: String, Required
        - The name of the column on which prediction is being done.

    split: Float, Optinal(default = 0.7)
        - Values between 0 and 1(exclusive) are only allowed.
    
    metric: sklearn.metrics object(default=accuracy_score(classification) or mean_absolute_error(regression))
        - Metrics Allowed:
            * Regression     : mean_absolute_error, mean_squared_error, explained_variance_score
            * Classification : f1_score, precision_score, recall_score, accuracy_score
        - Eg: compare_algos(df, y, metric = f1_score)

    reg_or_class: String, Optional(default = '')
        - If '' then the algorithm checks for the distribution in the y_train using the formula: distribution = len(y_train.unique())/len(y_train) * 100. If the distribution is less than 10 classification algorithms are run, else regression algorithms are run.
        - If String the allowed values are "Regression" or "Classification".

    algos_to_be_compared: List of sklearn model objects, Optional

        - If nothing is given, all the Regression or Classification algorithms will be run.
        - If specified the given set of algorithms will be run.
        - Defined Regression algorithms are: LinearRegression, RandomForestRegressor, ExtraTreesRegressor, DecisionTreeRegressor, SGDRegressor, SVR, GradientBoostingRegressor, KNeighborsRegressor, AdaBoostRegressor
        - Defined Classification algorithms are: RandomForestClassifier, ExtraTreesClassifier, LogisticRegression, DecisionTreeClassifier, SGDClassifier, SVC, GradientBoostingClassifier, KNeighborsClassifier, GaussianNB, AdaBoostClassifier

    '''

    do_error_checking(df, y, split, reg_or_class, metric, algos_to_be_compared)

    if bool(df.isnull().values.any()) or bool((df.applymap(type) == str).values.any()):
        print_dash()
        df = clean_df(df, y)
        print_dash()

    print(df.info())
    
    df_y = df[y]
    x = df.drop([y], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, df_y, test_size=1 - split, random_state=42)
    compare_algos_helper(x_train, x_test, y_train, y_test, reg_or_class, metric,algos_to_be_compared)


def compare_algos_helper(x_train, x_test, y_train, y_test, reg_or_class, metric, algos_to_be_compared):

    algos_to_be_compared, algo_type = get_algos_to_be_compared(y_train, reg_or_class, algos_to_be_compared)
    metric = get_metric(algo_type, metric)

    accuracies = []
    index = 0
    total_time = 0
    times_taken = []

    for algo in algos_to_be_compared:
        start_time = time.time()
        model = algo()
        model.fit(x_train, y_train)
        print(algo.__name__," has completed training")
        y_pred = model.predict(x_test)

        accuracy = get_accuracy(y_test, y_pred, metric)

        accuracies.append(accuracy)
        end_time = time.time()
        time_taken = end_time - start_time
        times_taken.append(time_taken)
        total_time += time_taken
        index += 1

    pp_accuracies(algos_to_be_compared, algo_type, metric, accuracies, times_taken)


def do_error_checking(df, y, split, reg_or_class, metric, algos_to_be_compared):
    if y not in df.columns:
        raise ColumnNotDefined("The column " + y + "is not defined the given dataframe")

    if split < 0  or split > 1:
        raise SplitNotInRange("Split range should be between 0 and 1")

    if not (isinstance(df, pd.DataFrame)):
        raise NotPandasDataFrame("The given dataframe is not a pandas dataframe")

    if not (isinstance(y, str)):
        raise NotString("Y attribute should be a string")

    if (reg_or_class != REGRESSION and
            reg_or_class != CLASSIFICATION and
            reg_or_class != ''
    ):
        raise RegOrClassNotDefined("reg_or_class should be either 'Reg' or 'Cla' or empty.")

    if metric != None and not (callable(metric)):
        raise MetricNotDefined("Metric should be a callable from sklearn.metrics")

    if metric and not (metric in CLASSIFICATION_METRICS or
                metric in REGRESSION_METRICS
    ):
        raise MetricNotDefined(metric.__name__ + " metric is not included")

    regression_algos_set = set(list(map(lambda x:x.__name__, REGRESSION_ALGOS)))
    classification_algos_set = set(list(map(lambda x:x.__name__,CLASSIFICATION_ALGOS)))
    algos_to_be_compared_set = set(list(map(lambda x:x.__name__,algos_to_be_compared)))

    if not (algos_to_be_compared_set.issubset(regression_algos_set) or
            algos_to_be_compared_set.issubset(classification_algos_set)
    ):
        if reg_or_class == REGRESSION:
            print("The regression algorithms allowed are:", REGRESSION_ALGOS)
        else:
            print("The classification algorithms allowed are:", CLASSIFICATION_ALGOS)

        raise AlgoToBeComparedNotDefined("One or more algorithm(s) in algos_to_be_compared list is not defined")


def get_distribution(y_train):
    unique_values = len(y_train.unique())
    total_values = len(y_train)
    distribution = (unique_values / total_values) * 100

    return distribution

def get_metric(algo_type, metric):
    # Error Checking
    if metric:
        if algo_type == REGRESSION and metric not in REGRESSION_METRICS:
            raise MetricNotDefined("The given metric is not a regression metric")
        if algo_type == CLASSIFICATION and metric not in CLASSIFICATION_METRICS:
            raise MetricNotDefined("The given metric is not a classification metric")
    # Error Checking Done

    # Placing the default Metric
    if not metric:
        if algo_type == REGRESSION:
            metric = DEFAULT_REGRESSION_METRIC
        elif algo_type == CLASSIFICATION:
            metric = DEFAULT_CLASSIFICATION_METRIC
    
    return metric

def get_accuracy(y_test, y_pred, metric):
    
    accuracy = 0
    accuracy = metric(y_test, y_pred)
    return accuracy


def get_algos_to_be_compared(y_train, reg_or_class, algos_to_be_compared):
    algo_type = ''

    if algos_to_be_compared:
        if algos_to_be_compared[0] in REGRESSION_ALGOS:
            algo_type = REGRESSION
        else:
            algo_type = CLASSIFICATION

        return algos_to_be_compared, algo_type
    
    else:
        if reg_or_class:
            if reg_or_class == REGRESSION:
                algos_to_be_compared = REGRESSION_ALGOS
                algo_type = REGRESSION
            elif reg_or_class == CLASSIFICATION:
                algos_to_be_compared = CLASSIFICATION_ALGOS
                algo_type = CLASSIFICATION
        else:
            distribution = get_distribution(y_train)

            if distribution < 10:
                algos_to_be_compared = CLASSIFICATION_ALGOS
                algo_type = CLASSIFICATION
            else:
                algos_to_be_compared = REGRESSION_ALGOS
                algo_type = REGRESSION

        return algos_to_be_compared, algo_type


def pp_accuracies(algos_to_be_compared, algo_type, metric, accuracies, times_taken):
    d = {}
    header = ['Algorithm Name']

    for i in range(len(accuracies)):
        d[algos_to_be_compared[i].__name__] = accuracies[i]

    if algo_type == REGRESSION:
        header.append(metric.__name__)
        d = dict(sorted(d.items(), key = lambda x : x[1]))
    else:
        header.append(metric.__name__)
        d = dict(sorted(d.items(), key = lambda x : x [1], reverse = True))

    header.append('Time Taken')
    data = []
    index = []
    j = 1

    for i in d:
        data.append([i, round(d[i], 4), round(times_taken[j-1], 4)])
        index.append(j)
        j += 1

    pp_df = pd.DataFrame(data, index, header)
    print_dash()
    print(pp_df)


def print_dash():
    print('-' * DASH_LENGTH)