from random_graph_generator import *

import dijkstra
import Bellman_Ford as Bellman_Ford
import argparse

import parameter as param

iteration       = param.iteration
node_size       = param.node_size
edge_node_ratio = param.ratio
repeat          = param.repeat
dict_node_pair  = param.dict_node_pair
percentage      = param.percentage

def get_parameter(iteration = iteration, node_size = node_size, percentage = percentage, ratio = edge_node_ratio, dict_node_pair = dict_node_pair, repeat = repeat):
    parser = argparse.ArgumentParser(description= "specify hyperparameter for shortest path algorithm")

    parser.add_argument("--iteration",
                        dest    = "iteration",
                        help    = "number of iteration to run on each algorithm",
                        # action  = "store_true",
                        default = iteration
                        )
    parser.add_argument("--size",
                        dest    = "size",
                        help    = "number of node",
                        # action  = "store_true",
                        default = node_size
                        )
    parser.add_argument("--ratio",
                        dest    = "ratio",
                        help    = "edge to node ratio",
                        # action  = "store_true",
                        default = ratio
                        )
    parser.add_argument("--repeat",
                        dest    = "repeat",
                        help    = "number of time to re-run each algorithm's file",
                        # action  = "store_true",
                        default = repeat
                        )
    parser.add_argument("--percentage",
                        dest    = "percentage",
                        help    = "specify num of edges = percentage of total possible edges ",
                        # action  = "store_true",
                        default = percentage
                        )
    parser.add_argument("--verbose",
                        dest    = "verbose",
                        help    = "be more verbose",
                        action  = "store_true",
                        )

    args = parser.parse_args()

    iteration       = args.iteration
    node_size       = args.size
    edge_node_ratio = args.ratio
    repeat          = args.repeat
    verbose         = args.verbose
    percentage      = args.percentage

    dict_node_pair = {}

    return int(iteration), int(node_size), int(percentage), int(edge_node_ratio), dict_node_pair, int(repeat), verbose

def find_average_time_list(y):
    # find average of each input size

    if not isinstance(y, list):
        print("Argument y in find_average() must be a list")
        exit()

    length = len(y)
    avg_time_list = []
    for time_list in y:
        sum = 0
        avg = 0
        for time in time_list:
            sum = sum + time

        avg = sum / length
        avg_time_list.append(avg)
    # print(y)
    # print(avg_time_list)
    # exit()
    return avg_time_list

def find_max_time_list(y):
    # find max constant
    # not complete; code is for finding max val in list
    # max = 0
    max_time_list = [ 0 for i in range(0,len(y))]

    if not isinstance(y, list):
        print("Argument y in find_average() must be a list")
        exit()

    for i,time_list in enumerate(y):
        max = 0
        for time in time_list:
            if time > max:
                max = time
        max_time_list[i] = max
    # print(y)
    # print(max_time_list)
    # exit()
    return max_time_list

def plot(edge_size_dict = None, node_size_list = None, Dijkstra_repeated_time_list = None ,Bellman_Ford_repeated_time_list = None, Dijkstra_theoritical_time = False, Bellman_Ford_theoritical_time = False):
    import matplotlib.pyplot as plt

    x1 = None # node_size
    y1 = None # Dijkstra or Bellman-Ford
    y2 = None # Bellman-Ford
    y3 = None # Dijkstra Theoritical RT or Bellman-Ford Theoritical RT
    y4 = None # Bellman-Ford Theoritical RT

    # print(edge_size_dict, node_size_list, Dijkstra_repeated_time_list, Bellman_Ford_repeated_time_list, Dijkstra_theoritical_time, Bellman_Ford_theoritical_time)
    # exit()

    if node_size_list is not None:
        node_size_list= node_size_list
        x1 = [i for i in node_size_list]
    else:
        print("Error: node_size_list is not given. Cannot plot x component in (x,y) ")
        exit()


    # print(Dijkstra_repeated_time_list )
    # exit()
    if Dijkstra_repeated_time_list is not None or Bellman_Ford_repeated_time_list is not None:

        if Dijkstra_repeated_time_list is not None and Bellman_Ford_repeated_time_list is not None:

            Dijkstra_repeated_time_list = Dijkstra_repeated_time_list
            # repeated_time_list = [val for dict in Dijkstra_repeated_time_list for key, val in dict.items()]
            repeated_time_list = [val for key, val in Dijkstra_repeated_time_list.items()]
            average_time_list1 = find_average_time_list(repeated_time_list)
            y1 = find_max_time_list(repeated_time_list)


            Bellman_Ford_repeated_time_list = Bellman_Ford_repeated_time_list
            # repeated_time_list = [val for dict in Bellman_Ford_repeated_time_list for key, val in dict.items()]

            repeated_time_list = [val for key, val in Bellman_Ford_repeated_time_list.items()]
            average_time_list2 = find_average_time_list(repeated_time_list) # find average of each input size
            y2 = find_max_time_list(repeated_time_list)


            # print(x1)
            # print(y1)
            # print(y2)
            print("Dijkstra_average_time_list = ", average_time_list1)
            print("Bellman_Ford_average_time_list = ", average_time_list2)
            # exit()
            plt.plot(x1, average_time_list1, label="Dijkstra RT")
            plt.plot(x1, average_time_list2, label="Bellman-Ford RT")
        else:
            if Dijkstra_repeated_time_list is not None:
                repeated_time_list = Dijkstra_repeated_time_list
                # repeated_time_list = [val for dict in repeated_time_list for key, val in dict.items()]
                repeated_time_list = [val for key, val in repeated_time_list.items()]
                average_time_list = find_average_time_list(repeated_time_list)
                y1 = find_max_time_list(repeated_time_list)
                # y1 = find_max_time_list(repeated_time_list)

                print("Dijkstra_time_list, ", repeated_time_list)

                plt.plot(x1, average_time_list, label="Dijkstra RT")

            if Bellman_Ford_repeated_time_list is not None:
                repeated_time_list = Bellman_Ford_repeated_time_list
                # repeated_time_list = [val for dict in repeated_time_list for key, val in dict.items()]
                repeated_time_list = [val for key, val in repeated_time_list.items()]
                average_time_list = find_average_time_list(repeated_time_list)
                y1 = find_max_time_list(repeated_time_list)
                # y1 = [time for time in repeated_time_list]

                print("Bellman_Ford_time_list, ", repeated_time_list)

                plt.plot(x1, average_time_list, label="Bellman-Ford RT")

    else:
        print("Error: Empirical_time_list is not given. Cannot plot y component in (x,y)")
        exit()

    if edge_size_dict is not None:
        edge_size_dict = edge_size_dict

    if x1 is not None or y1 is not None or y2 is not None:
        if y2 is not None:

            # y1 and y2 are not None
            if Dijkstra_theoritical_time:
                theoritical_time = Dijkstra_theoritical_time

                practice_time = y1
                theory_time = [n ** 2 for n in node_size_list]
                constant = [practice / theory for practice, theory in zip(practice_time, theory_time)]
                y3 = [constant * theory for constant, theory in zip(constant, theory_time)]

                plt.plot(x1, y3, label="Theoritical Dijkstra RT")

            if Bellman_Ford_theoritical_time:
                theoritical_time = Bellman_Ford_theoritical_time

                if edge_size_dict is None:
                    print("edge_size is not given to calculate Bellmanford_theoritical time")
                    exit()

                edge_size_list = [ val for key, val in edge_size_dict.items()]
                practice_time = y2

                theory_time = [n * e for n, e in zip(node_size_list, edge_size_list)]

                constant = [practice / theory for practice, theory in zip(practice_time, theory_time)]
                y4 = [constant * theory for constant, theory in zip(constant, theory_time)]

                plt.plot(x1, y4, label="Theoritical Bellman_Ford RT")
        else:
            # y1 is not None
            if Dijkstra_theoritical_time:
                theoritical_time = Dijkstra_theoritical_time

                practice_time = y1
                theory_time = [n **2 for n in node_size_list]
                constant = [ practice/theory for practice, theory in zip(practice_time,theory_time)]
                y3 = [ constant * theory for constant, theory in zip(constant, theory_time)]
                # print(y1)
                # print(y3)
                # exit()
                plt.plot(x1, y3, label="Theoritical Dijkstra RT")

            if Bellman_Ford_theoritical_time:
                theoritical_time = Bellman_Ford_theoritical_time

                if edge_size_dict is None:
                    print("edge_size is not given to calculate Bellmanford_theoritical time")
                    exit()

                edge_size_list = [ val for key, val in edge_size_dict.items()]

                practice_time = y1
                theory_time = [n * e for n, e in zip(node_size_list, edge_size_list)]
                # find constant and take the largest constant
                constant = [practice / theory for practice, theory in zip(practice_time, theory_time)]
                y3 = [constant * theory for constant, theory in zip(constant, theory_time)]

                plt.plot(x1, y3, label="Theoritical Bellman_Ford RT")

        plt.xlabel('Node Size')
        plt.ylabel('Time')
        plt.title('running time complexity')

        plt.legend()
        plt.show()
    else:
        print("Error: x or y is not given")
        print("x = node_size_list")
        print("y = Empirical_time_list ")
        exit()

def plot_rt(node_size_list = None,dict_node_pair = None,Dijkstra_repeated_time_list = None, Bellman_Ford_repeated_time_list = None, algo_vs_algo = False, theory_vs_practice = False):

    edge_size_dict = {}
    for key, val in dict_node_pair.items():
        edge_size_dict[key] = len(val)

    if node_size_list is not None:
        node_size_list = node_size_list
    else:
        print("Error: list of node size are not passed to plot_rt()")

    Dijkstra_theoritical_time = True
    Bellman_Ford_theoritical_time = True

    if algo_vs_algo:
        plot(edge_size_dict=edge_size_dict,
             node_size_list=node_size_list,
             Dijkstra_repeated_time_list=Dijkstra_repeated_time_list,
             Bellman_Ford_repeated_time_list=Bellman_Ford_repeated_time_list)

    if theory_vs_practice:
        if Dijkstra_repeated_time_list is not None:
            plot(edge_size_dict=edge_size_dict,
                 node_size_list=node_size_list,
                 Dijkstra_repeated_time_list=Dijkstra_repeated_time_list,
                 Dijkstra_theoritical_time=Dijkstra_theoritical_time)

        if Bellman_Ford_repeated_time_list is not None:
            plot(edge_size_dict  = edge_size_dict,
                 node_size_list = node_size_list,
                 Bellman_Ford_repeated_time_list = Bellman_Ford_repeated_time_list,
                 Bellman_Ford_theoritical_time = Bellman_Ford_theoritical_time)

def repeat_run(iteration, node_size_list, edge_node_ratio, dict_node_pair, repeat, verbose):
    #re-run both algorithms
    Dijkstra_repeated_time_list = {}
    Bellman_Ford_repeated_time_list = {}

    node_size_list = node_size_list

    Dijkstra_time_list = {}
    Bellman_ford_time_list = {}

    for size in node_size_list:

        Dijkstra_repeated_time_list[size] = []
        Bellman_Ford_repeated_time_list[size] = []

    node_size = node_size_list[0]

    for i in range(0,repeat):
        Generator = Data_Generator(iteration=iteration, node_size=node_size, percentage=percentage,
                                   edge_node_ratio=edge_node_ratio,
                                   dict_node_pair=dict_node_pair, verbose=verbose)
        dict_node_pair = Generator.run_random_model2()

        # adj_matrix = Generator.Generate_adjacency_matrix(node_size)
        # table = Generator.Generate_df_table(node_size)

        for j in range(0,iteration):

            node_size = node_size_list[j]
            Dijkstra_time_list[node_size] = []
            Bellman_ford_time_list[node_size] = []

            Dijkstra_time     = dijkstra.run_file(Generator,iteration_num = j, node_size = node_size, edge_node_ratio = edge_node_ratio, dict_node_pair = dict_node_pair, verbose = verbose)
            Bellman_ford_time = Bellman_Ford.run_file(Generator, iteration_num = j, node_size = node_size, edge_node_ratio = edge_node_ratio, dict_node_pair = dict_node_pair, verbose = verbose)


            Dijkstra_time_list[node_size].append(Dijkstra_time)
            Bellman_ford_time_list[node_size].append(Bellman_ford_time)

            # print(Dijkstra_time_list)
            # print(Bellman_ford_time_list)
            # exit()


        for key, val in Dijkstra_time_list.items():
            Dijkstra_repeated_time_list[key].append(val[0])

        for key, val in Bellman_ford_time_list.items():
            Bellman_Ford_repeated_time_list[key].append(val[0])

    theory_vs_practice = True
    plot_rt(node_size_list = node_size_list,
            dict_node_pair = dict_node_pair,
            Dijkstra_repeated_time_list = Dijkstra_repeated_time_list,
            Bellman_Ford_repeated_time_list= Bellman_Ford_repeated_time_list,
            theory_vs_practice =theory_vs_practice)

    # plot_rt(node_size_list = node_size_list,
    #         dict_node_pair = dict_node_pair,
    #         Bellman_Ford_repeated_time_list= Bellman_Ford_repeated_time_list,
    #         theory_vs_practice =theory_vs_practice)

    # print(Dijkstra_repeated_time_list)
    # print(Bellman_Ford_repeated_time_list)
    # exit()

    return Dijkstra_repeated_time_list, Bellman_Ford_repeated_time_list

# def  merged_dict_time

if __name__ == "__main__":

    iteration, node_size, percentage, edge_node_ratio, dict_node_pair, repeat, verbose = get_parameter()

    # print(iteration, node_size, percentage, edge_node_ratio, dict_node_pair, repeat, verbose )
    # print(percentage)
    # exit()

    Dijkstra_repeated_time_list = []
    Bellman_Ford_repeated_time_list = []

    if edge_node_ratio:
        edge_node_ratio = edge_node_ratio
    else:
        edge_node_ratio = node_size * node_size / 5

    # Generator = Data_Generator(iteration=iteration, node_size=node_size, percentage = percentage,edge_node_ratio=edge_node_ratio,
    #                            dict_node_pair=dict_node_pair, verbose=verbose)
    # dict_node_pair = Generator.run_random_model2()  # HERE  no node_pair generated

    # print(dict_node_pair)
    # exit()

    node_size_list = [node_size*(edge_node_ratio**i) for i in range(0,iteration)]
    Dijkstra_repeated_time_list, Bellman_Ford_repeated_time_list = repeat_run(iteration, node_size_list, edge_node_ratio, dict_node_pair, repeat, verbose)


    print("Dijkstra_repeated_time_list")
    print(Dijkstra_repeated_time_list)

    print("Bellman_Ford_repeated_time_list: ")
    print(Bellman_Ford_repeated_time_list)

    algo_vs_algo = True
    plot_rt(node_size_list = node_size_list,
            dict_node_pair = dict_node_pair,
            Dijkstra_repeated_time_list = Dijkstra_repeated_time_list,
            Bellman_Ford_repeated_time_list = Bellman_Ford_repeated_time_list,
            algo_vs_algo = algo_vs_algo)

