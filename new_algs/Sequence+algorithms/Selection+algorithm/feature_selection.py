from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score
import random
import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import copy


# Set random seed
random.seed(1)
time.sleep(1)

# Calculate the fitness of using the selected features
# The fitness is defined as the classification accuracy
# when using k nearest neighbors as the classification model
def fitness_function(dataset):
    y = dataset["num"].values
    dataset = dataset.drop(columns = ["num"])
    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.30)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    classifier =  KNeighborsClassifier(3)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    return(accuracy_score(y_test, y_pred))


## Function to generate a completely random solution ##
def generate_random_solution (dataset):
    num_features = 13
    features_selected = []
    for feature_idx in range(num_features):
        feature = random.randrange(len(dataset.columns))
        #Make sure its not a feature we already selected
        while (feature in features_selected):
            feature = random.randrange(len(dataset.columns))
        features_selected.append(feature)
    selected_data = dataset.iloc[:, features_selected]
    # Always need to have classification column in dataframe
    pd.options.mode.chained_assignment = None  # default='warn'
    selected_data["num"] = dataset["num"]
    return selected_data

# Creates a crossover of two solutions, where the crossover point is chosen at random
def random_crossover(dataset1, dataset2):
    y = dataset1["num"].values
    dataset1 = dataset1.drop(columns = ["num"])
    dataset2 = dataset2.drop(columns = ["num"])
    crossover_point = random.randrange(1, len(dataset1.columns))
    subset_1 = dataset1.iloc[:, 0: crossover_point]
    subset_2 = dataset2.iloc[:, crossover_point: ]
    new_dataframe = pd.concat([subset_1, subset_2], axis=1)
    new_dataframe["num"] = y
    return new_dataframe

# Creates a crossover of two solution, where the crossover point is always selected
# such that half the solution is from solution 1 and the other half is from solution 2
def half_crossover(dataset1, dataset2):
    y = dataset1["num"].values
    dataset1 = dataset1.drop(columns = ["num"])
    dataset2 = dataset2.drop(columns = ["num"])
    crossover_point = int(len(dataset1.columns)/2)
    subset_1 = dataset1.iloc[:, 0: crossover_point]
    subset_2 = dataset2.iloc[:, crossover_point: ]
    new_dataframe = pd.concat([subset_1, subset_2], axis=1)
    new_dataframe["num"] = y
    return new_dataframe

# Creates two random mutations in the feature set
def mutation(dataset, all_features):
    y = dataset["num"].values
    dataset = dataset.drop(columns = ["num"])
    mutation_index_1 = random.randrange(len(dataset.columns)-1)
    dataset = dataset.drop(dataset.columns[mutation_index_1], axis=1)
    mutation_index_2 = random.randrange(len(dataset.columns)-1)
    dataset = dataset.drop(dataset.columns[mutation_index_2], axis=1)
    new_feature_index_1 = random.randrange(len(all_features.columns))
    new_feature_index_2 = random.randrange(len(all_features.columns))
    new_feature_name_1 = all_features.columns[new_feature_index_1]
    new_feature_name_2 = all_features.columns[new_feature_index_2]
    dataset[new_feature_name_1] = all_features[new_feature_name_1]
    dataset[new_feature_name_2] = all_features[new_feature_name_2]
    dataset["num"] = y
    return dataset

# Sort the population based on fitness
def sort_pop(population, population_fitness):
    population_fitness_sorted = copy.deepcopy(population_fitness)
    population_sorted = copy.deepcopy(population)
    population_fitness_sorted, population_sorted = [list(x) for x in zip(*sorted(zip(population_fitness_sorted, population_sorted), key=lambda pair: pair[0], reverse=True))]
    return population_sorted, population_fitness_sorted

# TODO: remove duplicates from mutation and crossover
def remove_duplicates(dataset, all_features):
    dataset = dataset.loc[:,~dataset.columns.duplicated()]
    while (len(dataset.columns) < 14):
        new_feature_index = random.randrange(len(all_features.columns))
        new_feature_name = all_features.columns[new_feature_index]
        dataset[new_feature_name] = all_features[new_feature_name]
    return dataset
