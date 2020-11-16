import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


def pso_optimize(mean_daily_returns, cov_matrix):
    """
    Function for Particle Swarm Optimization
    """
    dimensions = 470 # dimensions - number of stocks in the portfolio
    iterations = 4
    swarm_size = 500 # 500 particles in swarm

    # Initializing random positions for particles in the swarm
    swarm_position = []
    for particle in range(swarm_size):
        position = [0]*dimensions   # defining size of position vector of a particle
        for dimension in range(dimensions):
            position[dimension] = random.random() # assigning random position to a particle along all dimensions
        swarm_position.append(position)

    # Initializing random velocities for particles in the swarm
    swarm_velocity = []
    for particle in range(swarm_size):
        velocity = [0]*dimensions
        for dimension in range(dimensions):
            velocity[dimension] = random.random()
        swarm_velocity.append(velocity)

    swarm_position = np.array([np.array(p) for p in swarm_position])
    swarm_velocity = np.array([np.array(v) for v in swarm_velocity])
    particles_pbest = swarm_position # Initializing pbest of all particles
    swarm_gbest = particles_pbest[0] # Initializing gbest

    avg_sharpe_list = []
    portfolio_return = []
    portfolio_vol = []
    portfolio_sharpe = []
    portfolio_weights = []

    for iteration in range(iterations):
        sharpe_pbest_all = []
        for particle in range(swarm_size):
            for dimension in range(dimensions):
                r1 = random.random()
                r2 = random.random()
                # Incorporating time-variant forms of w, c1 and c2
                w = (0.9 - 0.4)*((iterations - iteration)/iterations) + 0.4 # w at iteration, where initial_w = 0.9 & final_w = 0.4
                c1 = (0.5 - 2.5)*(iteration/iterations) + 2.5 # c1 at iteration, where min_c1 = 0.5 & max_c1 = 2.5
                c2 = (2.5 - 0.5)*(iteration/iterations) + 0.5 # c2 at iteration, where max_c2 = 2.5 & min_c2 = 0.5

                swarm_velocity[particle][dimension] = w * swarm_velocity[particle][dimension] + c1 * r1 * np.linalg.norm(particles_pbest[particle][dimension] - swarm_position[particle][dimension]) + c2 * r2 * np.linalg.norm(swarm_gbest[dimension] - swarm_position[particle][dimension]) # Update velocity in every dimension
                swarm_position[particle][dimension] = swarm_position[particle][dimension] + swarm_velocity[particle][dimension] # Update position in every direction

            sharpe_pbest = sharpe(particles_pbest[particle], mean_daily_returns, cov_matrix) # Evaluating sharpe of existing pbest position
            if sharpe(swarm_position[particle], mean_daily_returns, cov_matrix) > sharpe_pbest: # Is new position better than the existing pbest position?
                particles_pbest[particle] = swarm_position[particle] # Update pbest to new position
                sharpe_pbest = sharpe(particles_pbest[particle], mean_daily_returns, cov_matrix) # Update sharpe of pbest
            sharpe_pbest_all.append(sharpe_pbest) # Add to list of sharpe ratios of all pbest positions

        if max(sharpe_pbest_all) > sharpe(swarm_gbest, mean_daily_returns, cov_matrix): # Is largest sharpe ratio of all pbests better than sharpe of existing gbest?
            max_index = sharpe_pbest_all.index(max(sharpe_pbest_all)) # Get index of the largest sharpe ratio among all pbests
            swarm_gbest = particles_pbest[max_index] # Update gbest using retrieved index

        avg_sharpe = sum(sharpe_pbest_all)/len(sharpe_pbest_all) # average of sharpe ratios of all pbests for a particular iteration
        avg_sharpe_list.append(avg_sharpe) # Adding average sharpe ratio to a list at the end of each iteration
        portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights = optimized_solution(iteration, swarm_gbest, mean_daily_returns, cov_matrix, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights)

    return avg_sharpe_list, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights

def ga_optimize(mean_daily_returns, cov_matrix):
    """
    Function for Genetic Algorithm
    """
    pop_size = 500
    dna_size = 470
    generations = 200
    crossover_rate = 0.85

    avg_sharpe_list = []
    portfolio_return = []
    portfolio_vol = []
    portfolio_sharpe = []
    portfolio_weights = []

    population = []
    for j in range(pop_size):
            ind = [0]*dna_size
            for i in range(dna_size):
                ind[i] = random.random()
            population.append(ind)

    for g in range(generations):
        pop_with_fitness = []
        for individual in population:
            fitness_val = sharpe(individual, mean_daily_returns, cov_matrix)
            pair = (individual, fitness_val)
            pop_with_fitness.append(pair)

        population = []

        for i in range(int(pop_size/2)): # Replacing the entire population with new population by fitness-proportionate selection, single-point crossover and mutation
            # Selection
            ind1 = selection(pop_with_fitness)
            ind2 = selection(pop_with_fitness)

            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(ind1, ind2)
                # Elitism, Mutation and adding back to the population
                child1 = mutate(child1)
                child2 = mutate(child2)
                sh1 = sharpe(ind1, mean_daily_returns, cov_matrix)
                sh2 = sharpe(ind2, mean_daily_returns, cov_matrix)
                ch1 = sharpe(child1, mean_daily_returns, cov_matrix)
                ch2 = sharpe(child2, mean_daily_returns, cov_matrix)
                if sh1 > sh2: # ind1 is fitter than ind2
                    if ch1 > sh1: # child1 is fitter than ind1
                        population.append(child1)
                    else:
                        population.append(ind1)

                    if ch2 > sh1: # child 2 is fitter than ind1
                        population.append(child2)
                    else:
                        population.append(ind1)

                else: # ind2 is fitter than ind1
                    if ch1 > sh2:
                        population.append(child1)
                    else:
                        population.append(ind2)

                    if ch2 > sh2:
                        population.append(child2)
                    else:
                        population.append(ind2)
            else: # if crossover did not occur
                population.append(ind1)
                population.append(ind2)


        ind_fitness_all = []
        for individual in population:
            ind_fitness = sharpe(individual, mean_daily_returns, cov_matrix)
            ind_fitness_all.append(ind_fitness)

        max_index = ind_fitness_all.index(max(ind_fitness_all))
        fittest_individual = population[max_index]

        avg_fitness = sum(ind_fitness_all)/len(ind_fitness_all)
        avg_sharpe_list.append(avg_fitness)
        portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights = optimized_solution(g, fittest_individual, mean_daily_returns, cov_matrix, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights)

    return avg_sharpe_list, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights


def selection(items):
    """
    Selecting individuals from population for crossover (Genetic Algorithm)
    """
    weight_total = sum((item[1] for item in items))
    n = random.uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item

def crossover(male, female):
    """
    Crossover between selected individuals (Genetic Algorithm)
    """
    pos = int(random.random()*470)
    return (male[:pos] + female[pos:], female[:pos] + male[pos:])


def mutate(dna):
    """
    Indtroducing mutation in offspring produced after crossover (Genetic Algorithm)
    """
    mutation_rate = 0.025
    dna_out = [0]*470
    for c in range(470):
        if random.random() < mutation_rate:
            dna_out[c] = random.random()
        else:
            dna_out[c] = dna[c]
    return dna_out

def sharpe(weights, mean_daily_returns, cov_matrix):
    """
    Function to calculate Sharpe ratio
    """
    weights = [w/sum(weights) for w in weights] # Making sure all weights represent proportions that add up to 1
    weights = np.matrix(weights)
    port_return = np.round(np.sum(weights * mean_daily_returns.T) * 1259, 2)/5 # 1259 trading days over 5 year period
    port_std_dev = np.round(np.sqrt(weights * cov_matrix * weights.T) * np.sqrt(1259), 2)/np.sqrt(5)
    port_std_dev = float(port_std_dev)
    sharpe_ratio = (port_return - 2.57)/ port_std_dev # 2.57 represents annual return of risk free security - 5-year US Treasury

    return sharpe_ratio

def optimized_solution(i, weights, mean_daily_returns, cov_matrix, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights):
    """
    Printing optimized solution at the end of each iteration
    """
    weights = [w/sum(weights) for w in weights] # Making sure all weights represent proportions that add up to 1
    weights = np.matrix(weights)
    port_return = np.round(np.sum(weights * mean_daily_returns.T) * 1259, 2)/5 # 1259 trading days over 5 year period
    port_std_dev = np.round(np.sqrt(weights * cov_matrix * weights.T) * np.sqrt(1259), 2)/np.sqrt(5)
    port_std_dev = float(port_std_dev)
    sharpe_ratio = (port_return - 2.57)/ port_std_dev # 2.57 represents annual return of risk free security - 5-year US Treasury

    print("Iteration: ", i)
    print("Portfolio Return: ", port_return)
    print("Portfolio Risk: ", port_std_dev)
    print("Portfolio Sharpe Ratio", sharpe_ratio)

    portfolio_return.append(port_return) # Adding portfolio return of a given solution to a list of returns for all solutions
    portfolio_vol.append(port_std_dev) # Adding portfolio standard deviation of a given solution to a list of standard deviations for all solutions
    portfolio_sharpe.append(sharpe_ratio)
    portfolio_weights.append(weights)

    return portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights

def main():
    random.seed(1234)
    data = pd.read_csv("S&P_data_modified.csv")
    stock_counter = 1
    mean_daily_returns = []
    cov_input = []

    while stock_counter <= 470:
        indv_stock = data[data.Stock_No == stock_counter]
        avg_return = indv_stock.Daily_Returns.mean()
        mean_daily_returns.append(avg_return)
        cov_input.append(indv_stock.Daily_Returns.tolist())
        stock_counter += 1

    mean_daily_returns = np.matrix(mean_daily_returns)
    cov_input = np.matrix(cov_input)
    cov_matrix = np.cov(cov_input)

    choice = input("Please enter the algorithm you want to run - pso or ga: ")

    while (choice != "pso" and choice != "ga"):
        print("Invalid input, please try again")
        choice = input("Please enter the algorithm you want to run - pso or ga: ")

    if choice == "pso":
        avg_sharpe_list, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights = pso_optimize(mean_daily_returns, cov_matrix)
    elif choice == "ga":
        avg_sharpe_list, portfolio_return, portfolio_vol, portfolio_sharpe, portfolio_weights = ga_optimize(mean_daily_returns, cov_matrix)


    portfolios = {'Returns': portfolio_return,
                 'Volatility': portfolio_vol,
                 'Sharpe Ratio': portfolio_sharpe,
                 'Weights': portfolio_weights}
    portfolios_df = pd.DataFrame(portfolios)

    averages = {'Average Sharpe Ratio': avg_sharpe_list}
    averages_df = pd.DataFrame(averages)

    max_sharpe = portfolios_df['Sharpe Ratio'].max()
    print("\n\nMaximum sharpe ratio: ", max_sharpe)

    optimal_portfolio = portfolios_df.loc[portfolios_df['Sharpe Ratio'] == max_sharpe]
    print("Optimal Return: ", optimal_portfolio.Returns)
    print("Optimal Risk: ", optimal_portfolio.Volatility)
    print('Optimal Weights:')
    for item in optimal_portfolio.Weights:
        print(item)

    portfolios_df['Sharpe Ratio'].plot()
    plt.xlabel('Iterations')
    plt.ylabel('Best Sharpe-Ratio')
    plt.show()

    averages_df['Average Sharpe Ratio'].plot()
    plt.xlabel('Iterations')
    plt.ylabel('Average Sharpe-Ratio')
    plt.show()

if __name__ == "__main__":
    main()
