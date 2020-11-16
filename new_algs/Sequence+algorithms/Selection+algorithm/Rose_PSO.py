import operator
import random
import numpy
from deap import base,benchmarks,creator,tools

seed = 19
random.seed(seed)
numpy.random.seed(seed)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list,
               smin=None, smax=None, best=None)


def generate(size, pmin, pmax, smin, smax):
    '''
    size = D
    part speed = w [sin,smax] dynamically changing inertia weight
    [pmin,pmax] = x = [lowerbound, upperbound]
    '''
    part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size))
    part.speed = [random.uniform(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part


def updateParticle(part, best, phi1, phi2):
    '''u1 u2 = c1 c2'''
    u1 = (random.uniform(0, phi1) for _ in range(len(part)))
    u2 = (random.uniform(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if speed < part.smin:
            part.speed[i] = part.smin
        elif speed > part.smax:
            part.speed[i] = part.smax
    part[:] = list(map(operator.add, part, part.speed))


toolbox = base.Toolbox()
toolbox.register("particle", generate, size=20, pmin=-30, pmax=30, smin=-1, smax=1)
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=1.5, phi2=1.5)
#benchmarks.rosenbrock = Rosenbrock's function
toolbox.register("evaluate", benchmarks.rosenbrock)


def main():
    '''
    0. topology is star Full-connected
    1. get the best fitness value
    2. iterate of whole population pi
    3. if pi's fitness value small than best then reproduce pi and calculate fitness value
    :return:
    '''

    pop = toolbox.population(n=1000)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = 200
    best = None

    for g in range(GEN):
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        #print(logbook.stream)

    best_value = toolbox.evaluate(best)

    return pop, logbook, best, best_value


if __name__ == "__main__":
    _, logbook, best, best_value = main()
    print(logbook)
    print(best)
    print(best_value)

