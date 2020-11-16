from datetime import datetime
from itertools import combinations

from _helpers.GenericModel import GenericModel
from config import DB_TEST_FEATURE_TABLE, DIR, TEST_DATA, TRAIN_TARGET_OUTPUT, TRAIN_DATA, DB_TRAIN_FEATURE_TABLE


def bulk(algorithm_obj, length_class):
    arr_feature_cols = ['average', 'mean', 'std_deviation', 'variance', 'avg_diff', 'sorted_percentage']

    for i in range(1, len(arr_feature_cols)):
        comb = combinations(arr_feature_cols, i)

        for feature_cols in list(comb):
            algorithm_obj['feature_cols'] = feature_cols
            try:
                GenericModel.apply_model_by_class(algorithm, length_class)
            except Exception as e:
                print(str(e))


CHUNKSIZE = 10

####### FEATURE ENGINEERING
start_time = datetime.now()

# if EXTRACT_FEATURES:
iterations = GenericModel.extract_features(DIR + TRAIN_TARGET_OUTPUT, DIR + TRAIN_DATA, CHUNKSIZE, DB_TRAIN_FEATURE_TABLE, FORCE=False)
if iterations == 0:
    print('Extract Feature is disabled. CSV file was generated')
else:
    delta_time = (datetime.now() - start_time)
    print('Feature Extraction ended in {} seconds: completed {} iterations of {} chunk'.format(delta_time, iterations, CHUNKSIZE))
###########################################################################

GenericModel.extract_features(None, DIR + TEST_DATA, CHUNKSIZE, DB_TEST_FEATURE_TABLE, FORCE=False)

# Random Forest
# algorithm = {
#     'name': 'random_forest',
#     'parameters': {'criterion': 'entropy', 'max_depth': 3, 'max_features': 'auto', 'n_estimators': 200},
#     'feature_cols': ['sorted_percentage', 'dist_min_max']
# }

# Ada Boost
algorithm = {
    'name': 'ada_boost',
    'parameters': {},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Gradient Boost
algorithm = {
    'name': 'gradient_boost',
    'parameters': {"n_estimators": 50, "learning_rate": 0.05},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# SVM
algorithm = {
    'name': 'svm',
    'parameters': {},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# NN
algorithm = {
    'name': 'neural_networks',
    'parameters': {"solver": 'lbfgs', "alpha": 1e-5, "hidden_layer_sizes": (5, 2), "random_state": 1},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# RANDOM FOREST
algorithm = {
    'name': 'random_forest',
    'parameters': {'criterion': 'entropy', 'max_depth': 8, 'max_features': 'sqrt', 'n_estimators': 100},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Extra Trees
algorithm = {
    'name': 'extra_trees',
    'parameters': {'criterion': 'entropy', 'max_depth': 8, 'n_estimators': 100},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Gaussian Naive Bayes
algorithm = {
    'name': 'gaussian_naive_bayes',
    'parameters': {},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Gaussian Naive Bayes
algorithm = {
    'name': 'multinomial_naive_bayes',
    'parameters': {},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Gaussian Naive Bayes
algorithm = {
    'name': 'decision_tree',
    'parameters': {'criterion': 'entropy', 'max_depth': 8},
    'feature_cols': []
}
bulk(algorithm, 1000000)

# Gaussian Naive Bayes
algorithm = {
    'name': 'knn',
    'parameters': {'n_neighbors': 3},
    'feature_cols': []
}
bulk(algorithm, 1000000)
