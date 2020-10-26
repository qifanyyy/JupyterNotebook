from datetime import datetime

from _helpers.GenericModel import GenericModel
from config import DB_TEST_FEATURE_TABLE, DIR, TEST_DATA, TRAIN_TARGET_OUTPUT, TRAIN_DATA, DB_TRAIN_FEATURE_TABLE

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

feature_cols = ["length", "average"]

# DECISION TREE
# algorithm = 'decision_tree'
# bin_model_file_name = 'decision_tree_with_length.sav'
# output_file_name = 'decision_tree.csv'
# test_size = 0.3
#
# parameters = {
#     'criterion': 'entropy',  # gini
#     'random_state': 0
# }
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)
#
# # RANDOM FOREST
# algorithm = 'random_forest'
# bin_model_file_name = 'random_forest.sav'
# output_file_name = 'random_forest_output.csv'
# test_size = 0.1
#
# parameters = {'criterion': 'gini', 'max_depth': 6, 'max_features': 'log2', 'n_estimators': 500}

# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)

# feature_cols = [
#     'length',
#     'max',
#     'min',
#     'dist_min_max',
#     # 'average',
#     # 'mean',
#     # 'q1', 'q2', 'q3',
#     # 'std_deviation',
#     # 'variance',
#     'avg_diff',
#     'sorted_percentage',
#     # 'target'
# ]
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)

# GenericModel.recursive_feature_elimination(feature_cols, algorithm, parameters)
# GenericModel.grid_search(algorithm, feature_cols, test_size)


# Neural Networks
# algorithm = 'neural_networks'
# bin_model_file_name = 'neural_networks.sav'
# output_file_name = 'neural_networks.csv'
# test_size = 0.3
#
# parameters = {"solver": 'lbfgs', "alpha": 1e-5, "hidden_layer_sizes": (5, 2), "random_state": 1}
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)
#
# # Extra Trees
# algorithm = 'extra_trees'
# bin_model_file_name = 'extra_trees.sav'
# output_file_name = 'extra_trees.csv'
# test_size = 0.3
#
# parameters = {"n_estimators": 10, "criterion": 'gini', "max_depth": None, "min_samples_split": 2, "random_state": 0}
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)
#
# # Ada Boost
# algorithm = 'ada_boost'
# bin_model_file_name = 'ada_boost.sav'
# output_file_name = 'ada_boost.csv'
# test_size = 0.3
#
# parameters = {"n_estimators": 50, "learning_rate": 0.5, "random_state": None}
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, feature_cols, bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)
#
# # Gradient Boost
# algorithm = 'gradient_boost'
# bin_model_file_name = 'gradient_boost.sav'
# output_file_name = 'gradient_boost.csv'
# test_size = 0.3
#
# parameters = {"n_estimators": 100, "learning_rate": 0.05}
#
# bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'avg_diff'], bin_model_file_name, test_size)
# GenericModel.predict(bin_model, feature_cols, output_file_name)





# Gradient Boost
algorithm = 'gradient_boost'
bin_model_file_name = 'test1.sav'
output_file_name = 'test1_gradient_boost.csv'
test_size = 0.3

parameters = {"n_estimators": 100, "learning_rate": 0.05}

bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'avg_diff'], bin_model_file_name, test_size)
GenericModel.predict(bin_model, ['length', 'avg_diff'], output_file_name)

# RANDOM FOREST
algorithm = 'random_forest'
bin_model_file_name = 'test2.sav'
output_file_name = 'test2_random_forest_output.csv'
test_size = 0.1

parameters = {'criterion': 'entropy', 'max_depth': 8, 'max_features': 'sqrt', 'n_estimators': 100}

bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'avg_diff'], bin_model_file_name, test_size)
GenericModel.predict(bin_model, ['length', 'avg_diff'], output_file_name)

# Ada Boost
algorithm = 'ada_boost'
bin_model_file_name = 'test3.sav'
output_file_name = 'test3_ada_boost.csv'
test_size = 0.3

parameters = {"n_estimators": 100, "learning_rate": 1}

bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'avg_diff'], bin_model_file_name, test_size)
GenericModel.predict(bin_model, ['length', 'avg_diff'], output_file_name)

# SVM
algorithm = 'svm'
bin_model_file_name = 'test4.sav'
output_file_name = 'test4_svm.csv'
test_size = 0.3

parameters = {}

bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'sorted_percentage'], bin_model_file_name, test_size)
GenericModel.predict(bin_model, ['length', 'sorted_percentage'], output_file_name)


# Gradient Boost 2
algorithm = 'gradient_boost'
bin_model_file_name = 'test5.sav'
output_file_name = 'test5_gradient_boost.csv'
test_size = 0.3

parameters = {"n_estimators": 50, "learning_rate": 0.05}

bin_model, _ = GenericModel.apply_model(algorithm, parameters, ['length', 'sorted_percentage'], bin_model_file_name, test_size)
GenericModel.predict(bin_model, ['length', 'sorted_percentage'], output_file_name)
