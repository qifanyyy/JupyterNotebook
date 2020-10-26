import random
import operator
import numpy as np
import datetime

from deap import algorithms,base,creator,tools,gp

seed = 1234
random.seed(seed)
np.random.seed(seed)

#Global values
x = np.array([[1,1],[1,0],[0,1],[0,0]])
y = np.array([0, 1, 1, 0])

#Set GP
pset = gp.PrimitiveSet("MAIN", 2, "X")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalXOR(individual):
    func = toolbox.compile(expr=individual)
    ret = sum(func(*in_) == out for in_, out in zip(x, y))
    return ret,

toolbox.register("evaluate", evalXOR)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    pop = toolbox.population(n=30)
    # top 3
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.8, 0.1, 30, stats, halloffame=hof)
    return pop, stats, hof


if __name__ == "__main__":
    start_time = datetime.datetime.now()  # Track search starting time
    pop, stats, hof = main()
    end_time = datetime.datetime.now()  # Track search ending time
    exection_time = (end_time - start_time).total_seconds()  # Track execution time
    print('searching time= %.4f'%exection_time)
    print('best 3 results:')
    for i in hof:
        print('acc=%.2f'%evalXOR(i),i)
