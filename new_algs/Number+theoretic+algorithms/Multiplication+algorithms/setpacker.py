# Plotkin Shmoys Tardos approximation algorithm for fractional set packing
# https://www.satyenkale.com/papers/mw-survey.pdf sections 2, 3, 3.3, 3.3.4

# $ python setpacker.py
# to see a solution to a randomly generated instance from terminal, or
# $ python -i setpacker.py
# to play with the functions in a REPL

import math
import numpy
import random

# generates a list of sets of integers between 0 and u
def generate_sets(numsets, u):
    setlist = []
    # weight towards smaller set size
    weighted_size_list = []
    for size in range(1,u+1):
        for n in range(((u + 1) - (size))**2):
            weighted_size_list.append(size)
            
    # create sets    
    for i in range(numsets):
        s = set()
        
        max_set_size = random.choice(weighted_size_list)

        # alternatively, choose set_size uniformly at random
        # max_set_size = random.randint(1,u+1)
        
        for n in range(max_set_size):
            elt = random.randint(0,u)
            s.add(elt)
        setlist.append(s)

    return setlist


# input: a list of sets of integers and error parameter epsilon
# uses MWU implementation of PST algorithm, described in section 3.3 and
# 3.3.4 of the paper, to solve for -Ax >= -b - epsilon, where b is
# the all-1s vector and A is an m by n matrix of constraints
# (one constraint per element, so no two sets can share a specific element)
# and x is a point in a convex subset of R^n between 0 and 1
# the x_vector returned is an approximate fractional solution to the more
# difficult set-packing problem where each entry can be either a 0 or a 1
# (representing a set being left out or included in a setpacking solution)
def pack(sets, epsilon):
    # create reverse lookup table: for each element, which sets contain it 
    elt_dict = {}
    for set_index in range(len(sets)):
        for elt in sets[set_index]:
            if elt in elt_dict:
                elt_dict[elt].append(set_index)
            else:
                elt_dict[elt] = [set_index]

    # let rho (width of problem) be max # of sets that share a specific elt
    rho = 0
    for elt in elt_dict:
        rho = max(rho, len(elt_dict[elt]))
        
    m = len(elt_dict) # size of universe
    n = len(sets) 

    # input p is a dictionary 'vector' mapping each element to a probability
    # the oracle solves the one-constraint problem -pAx >= -p by maximizing
    # -pAx (by associating as many entries with a 1 value as possible)
    def oracle(p):
        # associate each set with a probability (not a distribution)
        ps_list = [0] * n
        for set_index in range(len(sets)):
            for elt in sets[set_index]:
                ps_list[set_index] += p[elt]

        order = numpy.argsort(ps_list) # sets in ascending order of prob

        running_total = 0
        n_i = 0
        next_set = order[n_i]
        x_vector = [0] * n
        
        # maximize sum of x-vector by greedily filling with 1-values
        while (running_total + ps_list[next_set] < 1) and (n_i < (n-1)):
            running_total += ps_list[next_set]
            x_vector[next_set] = 1
            n_i += 1
            next_set = order[n_i]

        # so prob_vec*x_vec = 1: fill this entry with difference, rest are 0s
        x_vector[next_set] = (1 - running_total)/ps_list[next_set]

        return x_vector

    # MW algorithm:
    # initialize p to uniform distribution
    curr_prob = {k:(1.0/m) for k in elt_dict.keys()} 
    best_prob = {k:0.0 for k in elt_dict.keys()}
    best_v = n # number of packable sets
    total_x = [0.0] * n  # sum of all x-vectors, to be averaged later
    
    eta = epsilon/4.0 # from paper section 3.3 
    T = math.ceil(8.0*rho*math.log(m)/(epsilon**2)) # from paper section 3.3
    
    for i in range(int(T)): 
        x_vector = oracle(curr_prob)
        total_x = [sum(x) for x in zip(total_x, x_vector)] # add x_vec to total
        curr_v = sum(x_vector)
        if curr_v < best_v: # each v found is an upper bound on # sets packable
            best_v = curr_v
            best_prob = {k:v for (k,v) in curr_prob.items()}

        cost = {}
        for elt in elt_dict:
            cost[elt] = 0
            for set_index in elt_dict[elt]:
                cost[elt] += x_vector[set_index]

            cost[elt] = -(cost[elt] - 1)/rho # cost from section 3.3

        total_weight = 0
        for elt in curr_prob.keys():
            curr_prob[elt] = curr_prob[elt]*(1 - eta*cost[elt]) # weights (2.1)
            total_weight += curr_prob[elt]

        for elt in curr_prob.keys():
            curr_prob[elt] = curr_prob[elt]/total_weight # make distribution

    return ([x/T for x in total_x], best_prob, best_v)

# print the output of pack()
def pretty_print(avg_x, best_prob, best_v, sets):
    v_hat = int(math.floor(best_v))
    print("\n\n")
    print("You can pack approximately " + str(best_v) + " sets. The " +
          str(v_hat + 1) + " best sets are:")
    order = numpy.argsort(avg_x)[::-1] # set indices in descending order
    for i in range(v_hat + 1):
        if i < len(order):
            print(sets[order[i]])

    all_sets = raw_input("\n View all " + str(len(sets)) + " sets? (y/n) ")
    if (all_sets == "y") or (all_sets == "Y"):
        for i in range(len(order)):
            print("%.2f" % (avg_x[order[i]] * 100) + "%: " + str(sets[order[i]]))
        
        
def main():
    print("\ngenerating sets...")
    sets = generate_sets(random.randint(2,50), random.randint(2,100))
    print("packing sets...")
    avg_x, best_prob, best_v = pack(sets, .1)
    pretty_print(avg_x, best_prob, best_v, sets)
    

if __name__ == "__main__":
    main()
    
    
    

