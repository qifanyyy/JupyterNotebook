import math, statistics as stats
from random import choice, random, randint, shuffle

__author__ = "Michael Suggs // mjs3607@uncw.edu"


class GeneticTSP:
    """ Summary here.

    Long summary...

    Attributes:
        attr1: beep boop
        attr2: boop beep
    """

    # TODO init summary.
    def __init__(self, city_dictionary, init_pop):
        """ Summary here.

        :param city_dictionary:
        :param init_pop:
        """
        self.city_dict = city_dictionary
        self.curr_pop = {}
        self.offspring = {}
        self.curr_keys = []

        self.generate_initial_pop(init_pop)

    def get_current_population(self):
        return self.curr_pop

    def get_best_solution(self):
        best = min(self.curr_pop, key=self.curr_pop.get)
        return best, self.curr_pop[best]

    # TODO gen_init summary
    def generate_initial_pop(self, init_pop):
        """ Summary here.

        Generates a dictionary containing init_pop number of individuals with each
        individual representing a singular trip through the entire set of
        cities. Dictionary format is given as {trip_list : fitness} with fitness
        representing the inverse of the total trip distance of the individual.

        :param city_dict: Dictionary of cities and their [x, y] points {city:[x,y]}
        :param init_pop: Number of initial indivuduals to generate
        :return: Dictionary of all randomly generated trip permutations and their
                    fitness.
        """
        city_list = list(self.city_dict.keys())
        self.curr_pop = {}

        # Generates a random population and their fitness scores as {trip : fit}
        while len(self.curr_pop) < init_pop:
            shuffle(city_list)
            self.curr_pop[''.join(city_list)] = self.fitness(city_list)

        self.curr_keys = list(self.curr_pop.keys())

    # TODO Fitness summary
    def fitness(self, individual):
        """ Summary here.

        Calculates the total trip distance when given an input list containing a
        list of consecutive keys and a dictionary of said keys with appropriate
        values for each. Returns the inverse of this value, making smaller trip
        distances more "fit."

        :param individual: list containing a sequence of dictionary keys in the
                        order to be calculated
        :return: Inverse square root of the sum of the squared differences of
                        x and y coords
        """
        total_dist = 0
        for i in range(len(individual)):
            total_dist += math.sqrt(
                ((self.city_dict[individual[(i + 1) % len(individual)]][0] -
                                      self.city_dict[individual[i]][0]) ** 2) +
                ((self.city_dict[individual[(i + 1) % len(individual)]][1] -
                                      self.city_dict[individual[i]][1]) ** 2))
        return 1 / total_dist

    # TODO parent selection summary
    def select_parents(self, mean, stdev, max_tries=3):
        """ Summary here.

        :param mean:
        :param stdev:
        :param max_tries:
        :return:
        """
        for chance in range(max_tries):
            parent1 = choice(self.curr_keys)
            if self.curr_pop[parent1] > (mean + 2 * stdev):
                break

        for chance in range(max_tries):
            parent2 = choice(self.curr_keys)
            if self.curr_pop[parent2] > (mean + 2 * stdev):
                break

        return parent1, parent2

    # TODO crossover summary
    def crossover(self, parent1, parent2):
        """ Summary here.

        :param parent1:
        :param parent2:
        :return:
        """
        parent1 = list(parent1)
        parent2 = list(parent2)

        child1 = parent1[:(len(parent1) // 2)]
        child1 += list(set(parent2) - set(child1))

        child2 = parent2[:(len(parent2) // 2)]
        child2 += list(set(parent1) - set(child2))

        return ''.join(child1), ''.join(child2)

    # TODO mutation summary
    def mutate(self, individual, mut_prob):
        """ Summary here.

        :param individual:
        :param mut_prob:
        :return:
        """
        individual = list(individual)
        if random() < mut_prob:
            s1 = randint(0, len(individual) - 1)
            s2 = randint(0, len(individual) - 1)
            individual[s1], individual[s2] = individual[s2], individual[s1]

        return ''.join(individual)

    # TODO main algorithm summary
    def genetic_tsp(self, gen_lim, cross_prob=.75, mut_prob=.01):
        """ Summary here.

        Long summary here...

        :param gen_lim: Maximum number of generations
        :param cross_prob: Percent of next generation created by crossover
        :param mut_prob: Chance of a mutation happening after crossover
        :return:
        """
        curr_gen = 0
        while curr_gen < gen_lim:
            # total_fitness = sum(self.curr_pop.values())
            mean = stats.mean(self.curr_pop.values())
            stdev = stats.stdev(self.curr_pop.values(), mean)

            # Propagate next generation with up to 50 of the best individuals
            #  from the current generation.
            for trip in self.curr_pop.keys():
                if self.curr_pop[trip] >= mean + 3 * stdev:
                    self.offspring[trip] = self.curr_pop[trip]
                if len(self.offspring) >= 50:
                    break

            while len(self.offspring) < (1 - cross_prob) * len(self.curr_pop):
                survivor = choice(self.curr_keys)
                self.offspring[survivor] = self.curr_pop[survivor]

            # While next generation has less than the current generation,
            #  select individuals and crossover / mutate to populate the next
            #  generation. Then, clear the current generation and proceed.
            while len(self.offspring) < len(self.curr_pop):
                parent1, parent2 = self.select_parents(mean, stdev)

                # Cross over and mutate
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, mut_prob)
                child2 = self.mutate(child2, mut_prob)

                # Populate next generation
                self.offspring[child1] = self.fitness(child1)
                self.offspring[child2] = self.fitness(child2)

            self.curr_pop = self.offspring
            self.curr_keys = list(self.curr_pop.keys())
            self.offspring = {}
            curr_gen += 1


if __name__ == '__main__':
    # cities = {'a': [0.372090608, 0.432608199],
    #           'b': [0.38029396,  0.713361671],
    #           'c': [0.898119767, 0.772681874],
    #           'd': [0.167702257, 0.99219988],
    #           'e': [0.686992927, 0.93838682],
    #           'f': [0.274830532, 0.127452799],
    #           'g': [0.424618695, 0.817378304],
    #           'h': [0.478824774, 0.093485707],
    #           'i': [0.656087536, 0.875909204],
    #           'j': [0.240264048, 0.324621796],
    #           'k': [0.830124281, 0.076594979],
    #           'l': [0.72887909,  0.622051319],
    #           'm': [0.442833825, 0.387846749],
    #           'n': [0.088127924, 0.547910343]}

    short_cities = {'a': [0.372090608, 0.432608199],
                    'b': [0.38029396,  0.713361671],
                    'c': [0.898119767, 0.772681874],
                    'd': [0.167702257, 0.99219988],
                    'e': [0.686992927, 0.93838682],
                    'f': [0.274830532, 0.127452799]}

    ga = GeneticTSP(short_cities, 100)
    ga.genetic_tsp(100)
    print("Population: {}".format(ga.get_current_population()))
    ga_trip, ga_dist = ga.get_best_solution()
    print("Best trip: {} : {}".format(ga_trip, ga_dist))
