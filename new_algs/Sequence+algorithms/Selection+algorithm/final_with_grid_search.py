from datetime import datetime
from itertools import combinations

from _helpers.GenericModel import GenericModel
from _helpers.LoggerHelper import Logger
from config import DB_TEST_FEATURE_TABLE, DIR, TEST_DATA, TRAIN_TARGET_OUTPUT, TRAIN_DATA, DB_TRAIN_FEATURE_TABLE

CHUNKSIZE = 10
Logger.send('Starting...')

# FEATURE ENGINEERING
start_time = datetime.now()
iterations = GenericModel.extract_features(DIR + TRAIN_TARGET_OUTPUT, DIR + TRAIN_DATA, CHUNKSIZE, DB_TRAIN_FEATURE_TABLE, FORCE=False)
if iterations == 0:
    print('Extract Feature is disabled. CSV file was generated')
else:
    delta_time = (datetime.now() - start_time)
    print('Feature Extraction ended in {} seconds: completed {} iterations of {} chunk'.format(delta_time, iterations, CHUNKSIZE))

GenericModel.extract_features(None, DIR + TEST_DATA, CHUNKSIZE, DB_TEST_FEATURE_TABLE, FORCE=False)

# Grid Search for every model for various combinations of features
arr_feature_cols = [
    'length',
    # 'max',
    # 'min',
    'dist_min_max',
    'average',
    'mean',
    # 'q1', 'q2', 'q3',
    'std_deviation',
    'variance',
    'avg_diff',
    'sorted_percentage'
]

algorithms_for_grid = ['neural_networks', 'random_forest', 'knn', 'decision_tree', 'gradient_boost', 'ada_boost', 'extra_trees']
algorithms = ['svm', 'gaussian_naive_bayes', 'multinomial_naive_bayes']

for length in range(1, len(arr_feature_cols)):
    comb = combinations(arr_feature_cols, length)

    for feature_cols in list(comb):
        for algorithm in algorithms:
            try:
                model_start_time = datetime.now()
                bin_model, _ = GenericModel.apply_model(algorithm, {}, feature_cols, 'test.csv', 0.3)
                Logger.send('Partially End in: ' + str(datetime.now() - model_start_time))
            except Exception as e:
                Logger.send('Exception: ' + str(e))
        for algorithm in algorithms_for_grid:
            try:
                grid_start_time = datetime.now()
                GenericModel.grid_search(algorithm, feature_cols, 0.3)
                Logger.send('Partially End in: ' + str(datetime.now() - grid_start_time))
            except Exception as e:
                Logger.send('Exception: ' + str(e))


Logger.send('Ended in: ' + str(datetime.now() - start_time))

Logger.send('...Ending')
