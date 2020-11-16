from datetime import datetime

from _helpers.GenericModel import GenericModel
from config import DB_TEST_FEATURE_TABLE, DIR, TEST_DATA, TRAIN_TARGET_OUTPUT, TRAIN_DATA, DB_TRAIN_FEATURE_TABLE

CHUNKSIZE = 10
test_size = 0.3

# FEATURE ENGINEERING
start_time = datetime.now()

# if EXTRACT_FEATURES:
iterations = GenericModel.extract_features(DIR + TRAIN_TARGET_OUTPUT, DIR + TRAIN_DATA, CHUNKSIZE, DB_TRAIN_FEATURE_TABLE, FORCE=False)
if iterations == 0:
    print('Extract Feature is disabled. CSV file was generated')
else:
    delta_time = (datetime.now() - start_time)
    print('Feature Extraction ended in {} seconds: completed {} iterations of {} chunk'.format(delta_time, iterations, CHUNKSIZE))

GenericModel.extract_features(None, DIR + TEST_DATA, CHUNKSIZE, DB_TEST_FEATURE_TABLE, FORCE=False)
###########################################################################
classes = [
    {
        'len': 10,
        'algorithms': [
            {
                'name': 'random_forest',
                'parameters': {'criterion': 'gini', 'max_depth': 6, 'max_features': 'log2', 'n_estimators': 500},
                'feature_cols': ['sorted_percentage', 'dist_min_max']
            },
            {
                'name': 'decision_tree',
                'parameters': {'criterion': 'gini'},
                'feature_cols': ['dist_min_max']
            },
            {
                'name': 'neural_networks',
                'parameters': {"solver": 'lbfgs', "alpha": 1e-5, "hidden_layer_sizes": (5, 2), "random_state": 1},
                'feature_cols': ['sorted_percentage']
            }
        ]
    },

    {
        'len': 100,
        'algorithms': [
            {
                'name': 'svm',
                'parameters': {},
                'feature_cols': ["average", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'gradient_boost',
                'parameters': {"n_estimators": 50, "learning_rate": 0.05},
                'feature_cols': ["average", "std_deviation", "variance", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'neural_networks',
                'parameters': {"solver": "lbfgs", "alpha": 1e-05, "hidden_layer_sizes": [5, 2], "random_state": 1},
                'feature_cols':["average", "mean", "variance", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'gaussian_naive_bayes',
                'parameters': {},
                'feature_cols': ["mean", "std_deviation", "variance", "sorted_percentage"]

            },
            {
                'name': 'random_forest',
                'parameters': {"criterion": "entropy", "max_depth": 8, "max_features": "sqrt", "n_estimators": 100},
                'feature_cols': ["mean", "std_deviation", "variance", "sorted_percentage"]
            }
        ]
    },

    {
        'len': 1000,
        'algorithms': [
            {
                'name': 'svm',
                'parameters': {},
                'feature_cols': ["average", "mean", "std_deviation", "variance"]
            },
            {
                'name': 'gaussian_naive_bayes',
                'parameters': {},
                'feature_cols': ["average", "mean", "std_deviation", "variance", "avg_diff"]
            },
            {
                'name': 'multinomial_naive_bayes',
                'parameters': {},
                'feature_cols': ["variance", "sorted_percentage"]
            },
            {
                'name': 'random_forest',
                'parameters': {"criterion": "entropy", "max_depth": 8, "max_features": "sqrt", "n_estimators": 100},
                'feature_cols': ["mean", "variance", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'neural_networks',
                'parameters': {"solver": "lbfgs", "alpha": 1e-05, "hidden_layer_sizes": [5, 2], "random_state": 1},
                'feature_cols':  ["average", "mean", "std_deviation", "avg_diff"]
            }
        ]
    },

    {
        'len': 10000,
        'algorithms': [
            {
                'name': 'gaussian_naive_bayes',
                'parameters': {},
                'feature_cols': ["std_deviation", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'gradient_boost',
                'parameters': {"n_estimators": 50, "learning_rate": 0.05},
                'feature_cols': ["avg_diff", "sorted_percentage"]
            },
            {
                'name': 'ada_boost',
                'parameters': {},
                'feature_cols': ["average", "mean", "avg_diff"]
            },
            {
                'name': 'extra_trees',
                'parameters': {"criterion": "entropy", "max_depth": 8, "n_estimators": 100},
                'feature_cols': ["average", "avg_diff"]
            },
            {
                'name': 'random_forest',
                'parameters': {"criterion": "entropy", "max_depth": 8, "max_features": "sqrt", "n_estimators": 100},
                'feature_cols': ["mean", "avg_diff"]
            }
        ]
    },

    {
        'len': 100000,
        'algorithms': [
            {
                'name': 'neural_networks',
                'parameters': {"solver": "lbfgs", "alpha": 1e-05, "hidden_layer_sizes": [5, 2], "random_state": 1},
                'feature_cols':  ["variance"]
            },
            {
                'name': 'random_forest',
                'parameters': {"criterion": "entropy", "max_depth": 8, "max_features": "sqrt", "n_estimators": 100},
                'feature_cols': ["average", "std_deviation"]
            },
            {
                'name': 'extra_trees',
                'parameters': {"criterion": "entropy", "max_depth": 8, "n_estimators": 100},
                'feature_cols': ["average", "std_deviation", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'gaussian_naive_bayes',
                'parameters': {},
                'feature_cols': ["sorted_percentage", "avg_diff"]
            },
            {
                'name': 'gradient_boost',
                'parameters': {"n_estimators": 50, "learning_rate": 0.05},
                'feature_cols': ["avg_diff", "sorted_percentage"]
            }
        ]
    },

    {
        'len': 1000000,
        'algorithms': [
            {
                'name': 'ada_boost',
                'parameters': {},
                'feature_cols': ["mean", "variance", "avg_diff"]
            },
            {
                'name': 'gradient_boost',
                'parameters': {"n_estimators": 50, "learning_rate": 0.05},
                'feature_cols': ["average", "mean", "std_deviation", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'svm',
                'parameters': {},
                'feature_cols': ["mean", "std_deviation", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'neural_networks',
                'parameters': {"solver": "lbfgs", "alpha": 1e-05, "hidden_layer_sizes": [5, 2], "random_state": 1},
                'feature_cols':  ["mean", "avg_diff", "sorted_percentage"]
            },
            {
                'name': 'random_forest',
                'parameters': {"criterion": "entropy", "max_depth": 8, "max_features": "sqrt", "n_estimators": 100},
                'feature_cols': ["mean", "variance", "avg_diff", "sorted_percentage"]
            }
        ]
    }
]

# Train models
bin_models = []
for _class in classes:
    bin_model = {'len': _class['len'], 'models': []}

    # for each algorithm -> get bin file
    for algorithm in _class['algorithms']:
        model_file, _ = GenericModel.apply_model_by_class(algorithm, _class['len'], test_size)
        bin_model['models'].append({
            'model_file': model_file,
            'feature_cols': algorithm['feature_cols']
        })

    bin_models.append(bin_model)

GenericModel.predict_with_voting_system_by_class(bin_models, 'voting_system_by_class.csv')
