#######################################################################################################################
# libraries section
import os
import random
from datetime import datetime
from csv import writer
import copy


#######################################################################################################################
# custom functions and helpers

# the population crowdness in the environment
# as the population increases, the probability of dividing
# lowers as the population takes more space
# environment is the actual surface calculated in (population.size) metric **2
def crowding_effect(population,
                    environment=(400, 400)):
    # define the space occupied by the population
    crowd_effect = 1
    pop_space = 0
    for person in population:
        pop_space += person.size ** 2

    return pop_space / (environment[0] * environment[1]) * 10


# create an individual though the function
# create an individual with the life expectancy between 1 and 4 generations
def random_start_population(genes):
    individual = Individual(genes=genes,life_exp=random.randint(1, 4)).mutation(0)
    return individual


# print the whole population
def print_alive_individuals_population(population):
    for i in population:
        print(i)


# get the average of the gene values per individual
def average_ind_gene_value(ind):
    nr_average = 0
    for i in iter(ind.genes):
        nr_average += i
    return nr_average / len(ind.genes)


# get the average of the gene values per population
def average_pop_gene_value(population):
    nr_average = 0
    for i in population:
        nr_average += average_ind_gene_value(i)
    return nr_average / len(population)


#######################################################################################################################
# actual code
class Individual:
    # initialization method
    # Default values
    # life_exp = 3           # the number of generations before it dies
    # generation = x         # The generation when it was born
    # speed = 4              # the speed of the individual
    # strength = 10          # strength of the individual
    # genes = array          # an array of genes for individual that increase/decrease the fitness
    def __init__(self, energy_available=3000, life_exp=3, generation=0, speed=4, strength=5, size=5,
                 genes=[-98, -69, -65, -46, 49, 50, 74, 91, 117, 178]):
        self.energy = energy_available
        self.life_exp = life_exp
        self.generation = generation
        self.speed = speed
        self.strength = strength
        self.size = size
        self.genes = genes

        self.attr_list = ['speed', 'strength', 'size', 'genes']

    # the fitness function represents the expectancy of the individual's survival
    def fitness_function(self):
        sum_genes = 0
        for i in iter(self.genes):
            sum_genes += i

        return round(self.energy - self.speed * self.strength * self.size ** 3 - sum_genes, 3)

    # define the mutation that occurs
    def mutation(self, generation):
        # the probability of custom gene modification
        probability_gene_modification = 0.3

        # generate the random seed
        random.seed()

        child = copy.copy(self)
        child.generation = generation
        # make the mutant's life expectancy the same as the parent's
        child.life_exp = self.life_exp + random.randint(-2, 2)
        if child.life_exp <= 0:
            child.life_exp = self.life_exp + random.randint(1, 4)

        # generate the random seed
        random.seed()

        # the random function will generate the number of mutated features(0 to 5)
        nr_of_mutations = int(random.uniform(1, len(child.attr_list)))

        # get the list of attributes that can be mutated
        attr_list = child.attr_list.copy()

        # search a number of attributes equal to the nr_of_mutations
        for mutation in range(0, nr_of_mutations):
            # get the attribute
            rand_attr = random.choice(attr_list)

            # remove it from list, in order to ensure that it isn't modified
            if rand_attr in attr_list:
                attr_list.remove(rand_attr)

            if rand_attr == 'genes':
                genes = []
                for i in iter(self.genes):
                    gene = i

                    if random.uniform(0, 1) <= probability_gene_modification:
                        gene = gene + random.uniform(-i / 100, i / 100)
                        gene = round(gene, 3)
                    genes.append(gene)
                setattr(child, rand_attr, genes)

            else:
                attr_value = getattr(child, rand_attr)
                # store the mutation value
                random_mutation_value = (random.uniform(-1, 1) * attr_value / 100)

                # if the mutated attribute is less than 0, then don't mutate
                if attr_value + random_mutation_value > 0:
                    # the attribute can be modified with 1% percent of the actual value
                    setattr(child, rand_attr, round(attr_value + random_mutation_value, 3))
                else:
                    continue

        return child

    # standard methods
    def __str__(self):
        return_string = "Individual with life exp at {:>4} " \
                        "created in generation {:>4}, " \
                        "with fitness at {:4.4f} " \
                        "and attributes: {:4.4f}  speed |" \
                        " {:4.4f} strength | " \
                        "{:4.4f} size | ".format(self.life_exp, self.generation, self.fitness_function(), self.speed,
                                                 self.strength, self.size)

        return_string += "with gene values: "
        for i in iter(self.genes):
            return_string += str("{:4.4f} ").format(i)

        return return_string

    # create the header of the save file
    def create_header(self, file_path='natural_selection_data.csv'):
        # open the .csv and start writing the head of the file
        with open(file_path, 'w', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            list_of_elem = ['Generation', 'Life_Expectancy', 'Born_Generation', 'Speed', 'Strength', 'Size']
            i = 0
            for gene in range(len(self.genes)):
                list_of_elem.append('Gene' + str(i))
                i += 1

            list_of_elem.append('Fitness')
            csv_writer.writerow(list_of_elem)

    # save the current individual to the csv file
    def save_individual(self, file_path='natural_selection_data.csv', generation=0):
        if not os.path.exists(file_path):
            self.create_header(file_path)
        # Open file in append mode
        with open(file_path, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            list_of_elem = [generation,
                            self.life_exp,
                            self.generation,
                            self.speed,
                            self.strength,
                            self.size]

            # append the list of genes
            for i in iter(self.genes):
                list_of_elem.append(i)

            # append the fitness_function
            list_of_elem.append(self.fitness_function())

            csv_writer.writerow(list_of_elem)
