import numpy as np
import copy
import torch

import data_handler as dh
import test_net as tst
from construct_model import construct_model

# define GA settings
POP_SIZE = 75  # population size
CROSS_RATE = 0.9  # DNA crossover probability
MUTATION_RATE = 0.75  # mutation probability
N_GENERATIONS = 25  # generation size


def translate_dna(df, dna):
    """
    convert binary DNA into relevant data frame with correct inputs
    Args: pop_size (int): number of networks to generate
    """
    dna = np.insert(dna, 0, 1., axis=0)  # to ensure 'output' is not removed
    tdf = copy.copy(df)

    for col in df.columns:
        col_index = df.columns.get_loc(col)
        if dna[col_index] == 0:
            tdf = tdf.drop(col, 1)

    return tdf


def select(pop, fitness):
    """
    define population select function based on fitness value
    population with higher fitness value has higher chance to be selected
    """
    zipped = zip(pop, fitness)
    zip_sorted = sorted(zipped, key=lambda x: x[1], reverse=True)
    s_pop = next(zip(*zip_sorted))
    return np.vstack(s_pop)


def crossover(parent, pop, dna_size, pr_multiplier):
    """
    apply crossover with another parent in the population.
    args: pr_multiplier(float): the better performing the dna is, the less likely we perform crossover
    """
    if np.random.rand() < (CROSS_RATE * pr_multiplier):
        # randomly select another individual from population
        i = np.random.randint(0, round(POP_SIZE * 0.25), size=1)
        # choose crossover points(bits)
        cross_points = np.random.randint(0, 2, size=dna_size).astype(np.bool)
        # produce one child
        parent[cross_points] = pop[i, cross_points]
    return parent


def mutate(child, dna_size, pr_multiplier):
    """
    applies mutation to child dna.
    args: pr_multiplier(float): the better performing the parent dna is, the less likely we are to mutate the dna
    """
    for point in range(dna_size):
        if np.random.rand() < (MUTATION_RATE*pr_multiplier):
            child[point] = 1 if child[point] == 0 else 0
    return child


def get_fitness(in_sample_df, pop):
    """
    Return the testing accuracy, which is our fitness function.
    """
    fitness = []

    for p in pop:
        p_df = translate_dna(in_sample_df, p)

        # getting test and training
        train_df, test_df = dh.split_data(p_df, 0.63)
        # split x (features) and y (target)
        training_array = train_df.as_matrix()
        x_array, y_array = training_array[:, 1:], training_array[:, 0]
        # create Tensors to hold inputs and outputs, and wrap them in Variables,
        x = torch.tensor(x_array, dtype=torch.float, requires_grad=True)
        y = torch.tensor(y_array, dtype=torch.float, requires_grad=False)

        # construct and train model
        model, optimiser, trained_model, model_se = construct_model(x, y)

        # test the nn using test data
        model_accuracy = tst.test_net(trained_model, test_df)
        fitness.append(model_accuracy)

    return fitness


def main_GA(df):
    """
    Generate a network with the genetic algorithm.
    Args: df (data frame): all data
    """
    dna_size = len(df.columns) - 1  # dna for input vector
    pop = np.random.randint(2, size=(POP_SIZE, dna_size))

    # get validation data set (10% of data set)
    validation_df, in_sample_df = dh.split_data(df, 0.1)

    for g in range(N_GENERATIONS):
        fitness = get_fitness(in_sample_df, pop)
        generational_best = [pop[np.argmax(fitness), :]]
        print(" Most fitted DNA: ", generational_best[0], "best =", np.max(fitness),
              ", generational average =", np.mean(fitness))

        pop = select(pop, fitness)
        pop1 = copy.copy(pop)
        children = 0

        for parent in pop:
            pr_multiplier = min(10 / (len(pop) - children), 1)
            # produce a child by crossover operation
            child = crossover(parent, pop1, dna_size, pr_multiplier)
            # mutate child
            child = mutate(child, dna_size, pr_multiplier)
            # replace parent with its child
            parent[:] = child
            children += 1

    # validate best model in last generation but first need to train based on chromosome
    val_train_df = translate_dna(in_sample_df, generational_best[0])
    training_array = val_train_df.as_matrix()
    x_array, y_array = training_array[:, 1:], training_array[:, 0]
    # create Tensors to hold inputs and outputs, and wrap them in Variables,
    x = torch.tensor(x_array, dtype=torch.float, requires_grad=True)
    y = torch.tensor(y_array, dtype=torch.float, requires_grad=False)
    # construct and train model
    model, optimiser, trained_model, model_se = construct_model(x, y)

    val_test_df = translate_dna(validation_df, generational_best[0])
    validation_results = tst.test_net(trained_model, val_test_df)
    print("generational best: ", generational_best)
    print("validation results: " + str(validation_results))


if __name__ == "__main__":
    df = dh.get_data()  # returns data frame
    print(df.columns)
    main_GA(df)
