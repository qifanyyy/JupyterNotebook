import random, copy, operator
import matplotlib.pyplot as plt


class Genetic:
    logger = None
    tmpLastSolution = None
    tmpEilteValue = -100
    debugMode = False

    def __init__(self):
        self.logger = None

    def find_optimum_allocation(self, numberOfColors, numberOfNodes, edges, numberOfGenerations, chanceOfMutation):

        self.tmpEilteValue = -100
        # self.debugMode = debugMode
        populationSize = 1000
        tornument_size = 2
        numberOfChildren = tornument_size*2

        # print("number of Generations: ", numberOfGenerations, " pop size: ", populationSize, " best sample: ", bestSample, " lucky few: ", luckyFew)
        bestSolution = self.multipleGeneration(populationSize, int(tornument_size), edges, numberOfGenerations, numberOfChildren, chanceOfMutation, numberOfNodes, numberOfColors)

        # # if self.debugMode: self.evolutionBestFitness(generations, lastSolution)
        #
        # # print("Best solution found by Genetic Alg: ", self.fitness(bestSolution, jobs, clusters))
        #
        # self.decode(bestSolution, jobs, clusters)
        #
        # return jobs, clusters

    def getBestIndividualFromPopulation(self, population, edges):
        return self.computePerfPopulation(population, edges)[0]

    def generate_random_solution(self, numberOfNodes, numberOfColors):
        randomSol = []
        for i in range(numberOfNodes):
            randomSol.append(random.randrange(1, numberOfColors + 1, 1))
        return randomSol

    def generate_first_poulation(self, pop_size, numberOfNodes, numberOfColors):

        population = []
        i = 0
        while i < pop_size:
            population.append(self.generate_random_solution(numberOfNodes, numberOfColors))
            i += 1

        # if self.debugMode: self.logger.debug("first population:")
        # for r in population:
        #     if self.debugMode: self.logger.debug("    value: " + str(self.fitness(r, jobs, clusters)) + " sol: " + str(r))

        return population


    def computePerfPopulation(self, population, edges):

        populationPerf = {}
        for individual in range(len(population)):
            populationPerf[individual] = self.fitness(population[individual], edges)

        sorted_pop = []
        c = 0
        for i in sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=True):
            sorted_pop.append(population[i[0]])

        return sorted_pop

    def get_best_worst_avg_value(self, population, edges):

        populationPerf = {}
        sumt = 0
        for individual in range(len(population)):
            tmp = self.fitness(population[individual], edges)
            sumt += tmp
            populationPerf[individual] = tmp

        sortedl = sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=True)
        c = []
        c.append(sortedl[0][1])
        c.append(sortedl[len(population) - 1][1])
        c.append(sumt/len(population))
        # print(c)
        return c

    def selectFromPopulation(self, population, tornument_size, edges):
        selectedPop = []
        tmpList = []
        random.shuffle(population)
        counter = 0
        for i in range(len(population)):
            counter = counter + 1
            tmpList.append(population[i])
            if counter % tornument_size == 0:
                ttt = self.getBestIndividualFromPopulation(tmpList, edges)
                # print("best: " + str(ttt))
                selectedPop.append(ttt)
                tmpList = []

        return selectedPop

    def create_children(self, breeders, numberOfChildren, edges):
        nextPopulation = []
        for i in range(int(len(breeders) / 2)):
            parent1 = breeders[i]
            parent2 = breeders[len(breeders) - 1 - i]
            # if self.debugMode: self.logger.debug("  parent #1: " + str(parent1) + " value: " + str(self.fitness(parent1, jobs, clusters)))
            # if self.debugMode: self.logger.debug("  parent #2: " + str(parent2) + " value: " + str(self.fitness(parent2, jobs, clusters)))

            children = self.create_child(parent1, parent2, numberOfChildren, edges)

            # if self.debugMode: self.logger.debug("  children:")
            i = 1
            for individual in children:
                nextPopulation.append(individual)
                # if self.debugMode: self.logger.debug("      child #" + str(i) + ": " + str(individual) + " value: " + str(self.fitness(individual, jobs, clusters)))

            # if self.debugMode: self.logger.debug("")

        return nextPopulation

    def mutateSolution(self, solution, isElite, jobs, clusters):

        index_modification = int(random.random() * len(solution))
        preAllocatedCluster = solution[index_modification]
        preMutateValue = self.fitness(solution, jobs, clusters)
        solution[index_modification] = random.randrange(1, len(clusters), 1)
        postMutateValue = self.fitness(solution, jobs, clusters)
        if isElite and preMutateValue > postMutateValue:
            solution[index_modification] = preAllocatedCluster

        return solution

    def mutatePopulation(self, population, number_of_mutated_genomes, number_of_colors):
        mutated_pop = []
        random.shuffle(population)
        counter = number_of_mutated_genomes
        for tmp in population:
            counter = counter - 1
            if counter >= 0:

                tmp2 = copy.deepcopy(tmp)
                tmp2[random.randrange(0, len(tmp), 1)] = random.randrange(1, number_of_colors + 1, 1)
                # print("before mutate: " + str(tmp))
                # print("after        : " + str(tmp2))
                mutated_pop.append(tmp2)
            else:
                mutated_pop.append(tmp)

        return mutated_pop

    def multipleGeneration(self, populationSize, tornument_size, edges,
                           numberOfGenerations, number_of_children, chance_of_mutation, numberOfNodes, numberOfColors):

        bests = []
        worsts = []
        avgs = []

        first_pop = self.generate_first_poulation(populationSize, numberOfNodes, numberOfColors)
        best_of_all = copy.deepcopy(self.computePerfPopulation(first_pop, edges)[0])
        best_of_all_value = self.fitness(best_of_all, edges)
        counter = 1
        # bests.append(best_of_all_value)
        # print("---> best of first Gen: ", " value ", best_of_all_value)


        previous_generation = first_pop
        # no_progress_counter = 30

        while numberOfGenerations >= 0:
            # if self.debugMode: self.logger.debug("\n\n--------------    generation #" + str(counter) + "    --------------\n\n")
            counter += 1
            # print("generation #:" + str(counter))
            # for a in previous_generation:
            #     print(str(a) + " " + str(self.fitness(a, edges)))
            bwa = self.get_best_worst_avg_value(previous_generation, edges)
            bests.append(bwa[0])
            worsts.append(bwa[1])
            avgs.append(bwa[2])
            previous_generation = self.nextGeneration(previous_generation, tornument_size, edges, number_of_children, chance_of_mutation*populationSize*numberOfNodes, numberOfColors)

            best_of_generation = self.computePerfPopulation(previous_generation, edges)[0]
            value_of_best_of_generation = self.fitness(best_of_generation, edges)
            # print("---> gen #: ", counter, " sol: ", best_of_generation, " value ",
            #       value_of_best_of_generation)

            if value_of_best_of_generation > best_of_all_value:
                # print("-------> new best in gen #: ", counter, " sol: ", best_of_generation, " value ", value_of_best_of_generation)
                best_of_all_value = value_of_best_of_generation
                best_of_all = copy.deepcopy(best_of_generation)
                no_progress_counter = 10

            # no_progress_counter -= 1
            numberOfGenerations -= 1

        print("Best of Gen: ", best_of_all, " fitness:", self.fitness(best_of_all, edges))

        xlist = range(len(bests))
        plt.plot(xlist, bests, label="bestVals")
        plt.plot(xlist, worsts, label="worstVals")
        plt.plot(xlist, avgs, label="avgVals")
        plt.legend()
        plt.show()

        return best_of_all

    def nextGeneration(self, currentGeneration, tornument_size, edges, numberOfChildren, number_of_mutated_genomes, number_of_colors):

        populationSorted = self.computePerfPopulation(currentGeneration, edges)
        # if self.debugMode: self.logger.debug("\n\n--------> sorted population:")
        # for r in populationSorted:
        #     if self.debugMode: self.logger.debug("    value: " + str(self.fitness(r, jobs, clusters)) + " sol: " + str(r))

        nextBreeders = self.selectFromPopulation(populationSorted, tornument_size, edges)

        # if self.debugMode: self.logger.debug("\n\n--------> breeding phase:")
        nextPopulation = self.create_children(nextBreeders, numberOfChildren, edges)
        # if self.debugMode: self.logger.debug("\n\n--------> population of childs:")
        # for r in nextPopulation:
        #     if self.debugMode: self.logger.debug("    value: " + str(self.fitness(r, jobs, clusters)) + " sol: " + str(r))

        # if self.debugMode: self.logger.debug("\n\n--------> mutation phase:")
        nextGeneration = self.mutatePopulation(nextPopulation, number_of_mutated_genomes, number_of_colors)

        return nextGeneration

    def fitness(self, solution, edges):

        value = 0

        for edge in edges:
            if solution[edge[0]] != solution[edge[1]]:
                value = value + 1
        # print(str(solution) + " " + str(value))

        # if value > self.tmpEilteValue and not isInvalid:
        #     if self.debugMode: self.logger.debug("\n\n******** new best solution value: " + str(value) + " solution: " + str(solution) + " ********\n\n")
        #     self.tmpEilteValue = value

        return value

    def create_child(self, solution1, solution2, numberOfChildren, edges):

        children = []

        fitness1 = self.fitness(solution1, edges)
        fitness2 = self.fitness(solution2, edges)

        for i in range(numberOfChildren - 2):
            child = []
            for j in range(len(solution1)):
                r = random.random()
                if r < fitness1/(fitness1 + fitness2):
                    child.append(solution1[j])
                else:
                    child.append(solution2[j])
            children.append(child)

        children.append(solution1)
        children.append(solution2)

        return children
