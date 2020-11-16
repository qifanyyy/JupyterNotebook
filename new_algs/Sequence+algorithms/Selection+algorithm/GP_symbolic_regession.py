import random
import operator
import numpy as np
import datetime
import math

from deap import algorithms,base,creator,tools,gp

seed = 1234
random.seed(seed)
np.random.seed(seed)

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0


#Global values
sample = np.random.uniform(low=-10, high=10, size=(1000,))
avg_sample = float('%.4f'%np.average(sample))


#Set GP
pset = gp.PrimitiveSet("MAIN", 1, "X")
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def reg_func(x):
    ''' part 4 question function'''
    if x > 0:
        return 1/x + math.sin(x)
    else:
        return 2*x + math.pow(x,2) + 3.0

def count_R2(func):
    MSE,divisor = 0.0,0.0

    for s in sample:
        x = float('%.4f'%(s))
        MSE += math.pow( (reg_func(x) - func(x)),2)

        divisor += math.pow( (reg_func(s) - reg_func(avg_sample)),2)
    MSE,divisor = float(MSE / len(sample)),float(divisor / len(sample))
    R2 = 1 - float( MSE/divisor)
    return R2

def evalFitness(individual):
    func = toolbox.compile(expr=individual)

    R2 = count_R2(func)
    return R2,

toolbox.register("evaluate", evalFitness)
toolbox.register("select", tools.selTournament, tournsize=3)
#Executes a one point crossover
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
#a depth limit
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))

def main():
    pop = toolbox.population(n=500)
    # top 3
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.8, 0.15, 30, stats, halloffame=hof)
    return pop, stats, hof


if __name__ == "__main__":


    start_time = datetime.datetime.now()  # Track search starting time
    pop, stats, hof = main()
    end_time = datetime.datetime.now()  # Track search ending time
    exection_time = (end_time - start_time).total_seconds()  # Track execution time
    print('searching time= %.4f'%exection_time)
    print('best 3 results:')
    for i in hof:
        print('R2=%.2f'%evalFitness(i),i)



