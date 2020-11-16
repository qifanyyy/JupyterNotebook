import numpy as np


def _best(population, fitness_func, best, fbest):

    # best, fbest = None, None
    for i in range(population[0].shape[0]):

        if population[1][i] > -1.0:
            tmp = population[1][i]
        else:
            tmp = fitness_func(population[0][i][np.newaxis, :])
            population[1][i] = tmp

        if best is None or tmp < fbest:
            best = population[0][i][np.newaxis, :]
            fbest = tmp

    return best.copy(), fbest.copy()


def _tournament_selection(population, fitness_func):

    # k == 2
    idxs = np.random.permutation(np.arange(population[0].shape[0]))

    parent1 = population[0][idxs[0], :][np.newaxis, :]
    parent2 = population[0][idxs[1], :][np.newaxis, :]

    if population[1][idxs[0]] > -1.0:
        fitness1 = population[1][idxs[0]] 
    else:
        fitness1 = fitness_func(parent1)
        population[1][idxs[0]] = fitness1

    if population[1][idxs[1]] > -1.0:
        fitness2 = population[1][idxs[1]] 
    else:
        fitness2 = fitness_func(parent2)
        population[1][idxs[1]] = fitness2

    return parent1 if fitness1 < fitness2 else parent2


def _individuals(size):
    return np.random.randint(2, size=size)


# Function that mutates an individual
def _mutate(individual):

    idx = np.random.randint(low=0, high=individual.shape[0])
    individual[idx] = 1 - individual[idx] # bit flip
    return individual

# Given two parents, it returns the offspring of them
# def _crossover(male, female):
#     """
#     one-point fixed crossover
#     """

#     idx = male.shape[1] // 2

#     offspring1 = np.hstack((male[0, :idx], female[0, idx:]))[np.newaxis, :]
#     offspring2 = np.hstack((female[0, :idx], male[0, idx:]))[np.newaxis, :]

#     return offspring1, offspring2


def _crossover(male, female):
    """
    two-point random crossover
    """
    idx = np.random.randint(0, male.shape[1], 2)
    idx.sort()
    
    offspring1 = np.hstack((male[0, :idx[0]], female[0, idx[0]:idx[1]], male[0, idx[1]:]))[np.newaxis, :]
    offspring2 = np.hstack((female[0, :idx[0]], male[0, idx[0]:idx[1]], female[0, idx[1]:]))[np.newaxis, :]

    return offspring1, offspring2    


def genetic_algorithm(fitness_func, dim, n_individuals=10, epochs=50, crossover_rate=0.9, mutation_rate=0.1):
    
    assert n_individuals % 2 == 0
    
    population = [np.array([_individuals(dim) for _ in range(n_individuals)]),
                  np.zeros(n_individuals) - 1.0]

    children = np.zeros((n_individuals, dim))

    best, fbest = None, None

    for e in range(epochs):
        for c in range(0, n_individuals, 2):

            parent1 = _tournament_selection(population, fitness_func)
            parent2 = _tournament_selection(population, fitness_func)

            while np.array_equal(parent1, parent2):
                parent2 = _tournament_selection(population, fitness_func)

            if np.random.uniform() < crossover_rate:
                offspring1, offspring2 = _crossover(parent1, parent2)
                children[c, :] = offspring1
                children[c+1, :] = offspring2
            else:
                children[c, :] = parent1
                children[c+1, :] = parent2

            if np.random.uniform() < mutation_rate:
                children[c, :] = _mutate(children[c, :])

            if np.random.uniform() < mutation_rate:
                children[c+1, :] = _mutate(children[c+1, :])

        best, fbest = _best(population, fitness_func, best, fbest)

        population[0][:] = children[:]
        population[1][:] = -1.0
        children[:] = 0.0

        print('epoch {:2d}, best fitness = {:.10f}'.format(e, fbest))

    return best, fbest
    