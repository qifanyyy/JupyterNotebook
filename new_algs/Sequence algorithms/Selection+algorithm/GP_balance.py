import random
import operator
import numpy as np

from deap import algorithms,base,creator,tools,gp
from part6.part6_data import get_balance_data
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

#Global values
balance_values,balance_labels = get_balance_data()
seed = 1234
random.seed(seed)
np.random.seed(seed)

KNN = KNeighborsClassifier(n_neighbors=7)

#Set GP
pset = gp.PrimitiveSet("MAIN", 4, "feature")
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addEphemeralConstant("rand101", lambda: random.randint(-10, 10)/10)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def construction_set(func):
    cons_set = []
    for i in balance_values:
        value = func(*i)
        cons_set.append([value])

    return np.array(cons_set)

def evalFitness(individual):
    func = toolbox.compile(expr=individual)
    cons_set = construction_set(func)

    KNN.fit(cons_set,balance_labels)
    KNN.score(cons_set,balance_labels)
    score = KNN.score(cons_set,balance_labels)
    return score,

toolbox.register("evaluate", evalFitness)
toolbox.register("select", tools.selTournament, tournsize=5)
#Executes a one point crossover
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
#a depth limit
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))

def main():
    pop = toolbox.population(n=300)
    # top 3
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.8, 0.15, 10, stats, halloffame=hof)
    return pop, stats, hof


if __name__ == "__main__":
    pop, stats, hof = main()

    best_individual = hof[0]
    print(best_individual)
    func = toolbox.compile(expr=best_individual)
    test_set = construction_set(func)

    NB = GaussianNB()
    NB.fit(balance_values,balance_labels)
    original = NB.score(balance_values,balance_labels)
    print('NB balance original Accuracy: %0.2f' % original)
    NB.fit(test_set,balance_labels)
    scores = cross_val_score(NB,test_set,balance_labels,cv=10)
    print('NB feature construction on balance over 10 times cross validation')
    print('Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

    DT = DecisionTreeClassifier()
    DT.fit(balance_values,balance_labels)
    original = DT.score(balance_values,balance_labels)
    print('DT balance original Accuracy: %0.2f'%original)
    DT.fit(test_set, balance_labels)
    scores = cross_val_score(DT, test_set, balance_labels, cv=10)
    print('DT feature construction on balance over 10 times cross validation')
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))