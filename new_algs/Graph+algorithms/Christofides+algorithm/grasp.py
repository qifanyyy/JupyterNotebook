import random
import numpy
from copy import copy, deepcopy
import sys
import time

class grasp:
    def __init__(self, tsp_file, best_solution): 
        self.alpha = 0.1
        self.tsp_file = tsp_file
        self.best_solution = self.convert_from_true_false_matrix(best_solution)
        self.best_solution_cost = self.compute_cost(self.best_solution)

    def grasp(self):
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time <= 120:
            candidate_solution = self.greedy_randomized_construction()
            candidate_solution = self.local_search(candidate_solution)
            candidate_solution_cost = self.compute_cost(candidate_solution)

            if candidate_solution_cost < self.best_solution_cost:
                self.best_solution = candidate_solution
                self.best_solution_cost = candidate_solution_cost
            elapsed_time = time.time() - start_time

        return self.convert_from_integer_array_to_true_false_matrix(self.best_solution)

    def greedy_randomized_construction(self):
        candidate_solution = [-1] * self.tsp_file.dimension
        current_node = 0
        while -1 in candidate_solution:
            possible_next_nodes = []
            for i in range(self.tsp_file.dimension):
                if candidate_solution[i] == -1 and i != current_node:
                    possible_next_nodes.append(i)
            RCL = []
            Fcost_min = sys.maxsize
            Fcost_max = -1
            for i in range(self.tsp_file.dimension):
                if i in possible_next_nodes:
                    if self.tsp_file.adjacency_matrix[current_node][i] < Fcost_min:
                        Fcost_min = self.tsp_file.adjacency_matrix[current_node][i]
                    if self.tsp_file.adjacency_matrix[current_node][i] > Fcost_max:
                        Fcost_max = self.tsp_file.adjacency_matrix[current_node][i]
            for i in range(self.tsp_file.dimension):
                if i in possible_next_nodes:
                    cost = self.tsp_file.adjacency_matrix[current_node][i]
                    if cost <= (Fcost_min + self.alpha * (Fcost_max - Fcost_min)):
                        RCL.append(i)
            if  len(RCL) == 0:
                next_node = 0
            else:
                next_node = random.choice(RCL)
            candidate_solution[current_node] = next_node
            current_node = next_node
        
        return candidate_solution

    def local_search(self, candidate_solution):
        generated_solutions = [0] * 20
        generated_solutions_cost = [0] * 20
        for i in range(20):
            generated_solutions[i] = deepcopy(candidate_solution)

        smaller_cost = sys.maxsize
        index_smaller_cost = 0
        for i in range(20):
            nodes = numpy.random.random_integers(0, (self.tsp_file.dimension - 1), size=(1, 1))
            
            node_1 = nodes[0][0]
            sucessor_node_1 = generated_solutions[i][node_1]
            sucessor_sucessor_node_1 = generated_solutions[i][sucessor_node_1]
            antecessor_node_1 = -1
            for j in range(self.tsp_file.dimension):
                if generated_solutions[i][j] == node_1:
                    antecessor_node_1 = j
                    break
            
            generated_solutions[i][node_1] = sucessor_sucessor_node_1
            generated_solutions[i][sucessor_node_1] = node_1
            generated_solutions[i][antecessor_node_1] = sucessor_node_1

            next = 0
            for j in range(self.tsp_file.dimension):
                generated_solutions_cost[i] += self.tsp_file.adjacency_matrix[next][generated_solutions[i][next]]
                next = generated_solutions[i][next]
            if generated_solutions_cost[i] < smaller_cost:
                smaller_cost = generated_solutions_cost[i]
                index_smaller_cost = i
            
        return generated_solutions[index_smaller_cost]

    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return False
        else:
            return True

        # d = (det(*line1), det(*line2))
        # x = det(d, xdiff) / div
        # y = det(d, ydiff) / div
        # return x, y

    def compute_cost(self, solution):
        cost = 0
        next = 0
        for i in range(self.tsp_file.dimension):
            cost += self.tsp_file.adjacency_matrix[next][solution[next]]
            next = solution[next]
        return cost

    def convert_from_true_false_matrix(self, true_false_matrix):
        next = 0
        result = [0] * self.tsp_file.dimension
        for i in range(self.tsp_file.dimension):
            for j in range(self.tsp_file.dimension):
                if true_false_matrix[next][j] == True:
                    result[next] = j
                    next = j
                    break
        return result

    def convert_from_integer_array_to_true_false_matrix(self, integer_array):
        result = [False] * self.tsp_file.dimension
        for i in range(self.tsp_file.dimension):
            result[i] = [False] * self.tsp_file.dimension
        
        for i in range(self.tsp_file.dimension):
            for j in range(self.tsp_file.dimension):
                if integer_array[i] == j:
                    result[i][j] = True
                    break
        return result
