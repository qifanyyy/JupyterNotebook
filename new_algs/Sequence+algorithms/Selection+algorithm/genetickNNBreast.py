import random
import math
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

names = ["1","2","3","4","5","6","7","8","9","10"]
dataset = pd.read_csv("BreastNorm.csv", names=names)

x_values = list()
y_values = list()


def randSelection(x):
    return [random.randint(0, 1) for i in range(x)]


def mcc_func(tp, tn, fp, fn):
    num = tp*tn - fp*fn
    den = math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    if den != 0:
        return num/den
    else:
        return 0


def cross(vector_1, vector_2):
    vector_3 = [vector_1[0], vector_1[1], vector_1[2], vector_1[3], vector_1[4],
                vector_2[5], vector_2[6], vector_2[7], vector_2[8]]
    return(vector_3)


def mutate(vector_1):
    flip_bit = random.randint(0, 8)
    vector_1[flip_bit] = 1-vector_1[flip_bit]
    return vector_1


def getFitness(dataset, vector_1):
    i = 0
    (tp, tn, fp, fn) = (0, 0, 0, 0)
    y = dataset.iloc[:, 9].values  # labels
    print(y)
    classifier = KNeighborsClassifier(n_neighbors=49)
    chose_columns = []
    while(i < len(vector_1)):
        if(vector_1[i] == 1):
            chose_columns.append(i)
        i += 1
    # all features
    X = dataset.iloc[:, chose_columns].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    # print(y_pred)
    for k in range(len(y_test)):
        if y_pred[k] == 1 and y_test[k] == 1:
            tp += 1
        elif y_pred[k] == 0 and y_test[k] == 1:
            fn += 1
        elif y_pred[k] == 1 and y_test[k] == 0:
            fp += 1
        else:
            tn += 1
    return mcc_func(tp, tn, fp, fn)


parent_1 = randSelection(9)
parent_2 = randSelection(9)
parent_3 = randSelection(9)
parent_4 = randSelection(9)
parent_5 = randSelection(9)
parent_6 = randSelection(9)
parent_7 = randSelection(9)
parent_8 = randSelection(9)
counter = 0
loop_counter = 0
while(loop_counter <= 10):
    mcc_1 = getFitness(dataset, parent_1)
    mcc_2 = getFitness(dataset, parent_2)
    mcc_3 = getFitness(dataset, parent_3)
    mcc_4 = getFitness(dataset, parent_4)
    mcc_5 = getFitness(dataset, parent_5)
    mcc_6 = getFitness(dataset, parent_6)
    mcc_7 = getFitness(dataset, parent_7)
    mcc_8 = getFitness(dataset, parent_8)
    mcc_df = pd.DataFrame({
        'mcc': [mcc_1, mcc_3, mcc_3, mcc_4, mcc_5, mcc_6, mcc_7, mcc_8],
        'parents': [parent_1, parent_2, parent_3, parent_4, parent_5, parent_6, parent_7, parent_8],
    })
    mcc_df = mcc_df.sort_values(by=['mcc'])
    print(mcc_df)
    new_pool_parent_1 = mcc_df.iloc[7].parents  # highest
    new_pool_parent_2 = mcc_df.iloc[6].parents
    new_pool_parent_3 = mcc_df.iloc[5].parents
    new_pool_parent_4 = mcc_df.iloc[4].parents

    crossover_1 = cross(new_pool_parent_1, new_pool_parent_2)
    crossover_2 = cross(new_pool_parent_2, new_pool_parent_3)
    crossover_3 = cross(new_pool_parent_3, new_pool_parent_4)
    crossover_4 = cross(new_pool_parent_4, new_pool_parent_1)

    mutation_1 = mutate(crossover_1)
    mutation_2 = mutate(crossover_2)
    mutation_3 = mutate(crossover_3)
    mutation_4 = mutate(crossover_4)

    parent_1 = new_pool_parent_1
    parent_2 = new_pool_parent_2
    parent_3 = new_pool_parent_3
    parent_4 = new_pool_parent_4
    parent_5 = mutation_1
    parent_6 = mutation_2
    parent_7 = mutation_3
    parent_8 = mutation_4

    counter = counter+1
    x_values.append(counter)
    y_values.append(mcc_df.iloc[7].mcc)
    loop_counter += 1
plt.ion()
fig = plt.figure()
plt.scatter(x_values, y_values)
plt.show(block=True)
