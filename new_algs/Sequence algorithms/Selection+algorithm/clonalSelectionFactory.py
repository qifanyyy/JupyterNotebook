import math
from random import random
from copy import deepcopy

class ClonALG:
    def __init__(self):
        self.memoryset = []
        self._iteration = 0
        self._antibodies = []

    def random_antibody_fcn(self):
        raise NotImplemented()

    def calculate_affinity_fcn(self, antibodies):
        raise NotImplemented()

    def clone_antibodies_fcn(self, antibodies, clone_rate):
        clones = []
        for a in antibodies:
            clones += [deepcopy(a)] * int(math.ceil(len(antibodies) * a.affinity * clone_rate))
        return clones

    def mutation_fcn(self, clones, mutation_exp):
        for i in range(0, len(clones)):
            mutation_rate = math.exp(-clones[i].affinity * mutation_exp)
            clones[i] = self.point_mutation(clones[i], mutation_rate)
        return clones

    def selection_fcn(self, antibodies):
        return sorted(antibodies, key=lambda x: x.affinity, reverse=True)

    def stop_criterion(self):
        raise NotImplemented()

    def remove_antibodies(self, antibodies, max_antibodies):
        antibodies = self.selection_fcn(antibodies)[:max_antibodies]
        return antibodies

    def print_info(self, iteration):
        raise NotImplemented()

    def rand_paratope(self):
        raise NotImplemented()

    def point_mutation(self, clone, mutation_rate):
        """
        Iterates over each clone's paratope and mutates it accordingly to the mutation rate
        :param clone: The clone on which perform the mutation
        :param mutation_rate: The mutation's occurrence rate
        :return: The mutated clone
        """
        for i in range(0, len(clone.paratopes)):
            if random() < mutation_rate:
                clone.paratopes[i] = self.rand_paratope()
        return clone

    def run(self, number_of_antibodies, clone_rate, mutation_exp, to_memory,
            num_remove=2, max_antibodies=100, verbose=False):
        """
        Runs the Clonal Selection Algorithm and returns the computed memory set containing the best antibodies.
        :param number_of_antibodies: Initial number of antibodies.
        :param clone_rate: The clonation's occurrence rate.
        :param mutation_exp: Mutation exponent, mutation probability is proportional to exp(-affinity*mutation_exp).
        :param to_memory: The number of antibodies being returned.
        :param num_remove: The number of the worst antibodies that are removed on each iteration.
        :param max_antibodies: The maximum number of antibodies that are kept between subsequent iterations.
        :param verbose: If set, prints some execution details and executes "print_info" function on each iteration
        :return: The memory set containing the best antibodies.
        """
        # Initialization of the variable contatining the index of the iteration and of the antibodies set
        self._iteration = 0
        self._antibodies = []

        if verbose:
            print("Generating random antibodies")
        # Antibodies creation
        for i in range(0, number_of_antibodies):
            self._antibodies.append(self.random_antibody_fcn())
        if verbose:
            print("Antibodies have been generated")

        while not self.stop_criterion():
            # Increment the iteration number
            self._iteration += 1

            # Calculate affinity for each antibody
            self.calculate_affinity_fcn(self._antibodies)

            # Clonation
            clones = self.clone_antibodies_fcn(self._antibodies, clone_rate)

            # Hypermutation
            clones = self.mutation_fcn(clones, mutation_exp)

            # Computes the clones' affinity
            self.calculate_affinity_fcn(clones)

            # Add the clones to the antibodies list
            self._antibodies += clones

            # This is needed in order to remove identical/unnecessary antibodies
            self._antibodies = self.remove_antibodies(self._antibodies, max_antibodies)

            # Assignment of the best antibodies to the memory set
            self.memoryset = self._antibodies[:to_memory]

            if len(self._antibodies) - num_remove > 0:
                for i in range(len(self._antibodies) - num_remove, len(self._antibodies)):
                    self._antibodies[i] = self.random_antibody_fcn()

            if verbose:
                self.print_info(iteration=self._iteration)

        return self.memoryset
