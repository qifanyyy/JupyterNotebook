import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import namedtuple

NsgaIndividual = namedtuple("NsgaIndividual", "Id Chrom Accur NumBits Time")


def plot_gen_vs_fitness(file_name, title, fig_text):
    data = np.loadtxt(file_name)
    gen, min_val, avg_val, max_val = data[:, 0], data[:, 1], data[:, 2], data[:, 3]

    plt.plot(gen, max_val, 'b-', label="Max", linewidth=2.0)
    plt.plot(gen, avg_val, 'g-', label="Avg", linewidth=2.0)
    plt.plot(gen, min_val, 'r-', label="Min", linewidth=2.0)
    plt.legend(loc='best')

    plt.xlabel("GA Generation")
    plt.ylabel("Fitness (Percent Accuracy)")
    plt.title(title)
    plt.figtext(0.2, 0.009, fig_text)

    plt.show()

    return


def plot_pareto_front(file_name, title, fig_text):
    nsga_data = load_nsga_data(file_name)

    unique_individuals = get_unique_individuals(nsga_data)

    unique_individuals.sort(key=lambda individual: individual.NumBits)

    accuracy = []
    num_bits = []
    for individual in unique_individuals:
        accuracy.append(individual.Accur)
        num_bits.append(individual.NumBits)

    plt.plot(num_bits, accuracy, 'g-', linewidth=2.0)
    plt.scatter(num_bits, accuracy)
    plt.gca().invert_xaxis()
    plt.legend(loc='best')

    plt.xlabel("Number of Features")
    plt.ylabel("Percent Accuracy")
    plt.title(title)
    plt.figtext(0.2, 0.009, fig_text)

    plt.show()

    return


def plot_pareto_front_multi_file(file_names, plot_label, plot_colors, title):
    counter = 0
    for file_name in file_names:
        nsga_data = load_nsga_data(file_name)

        unique_individuals = get_unique_individuals(nsga_data)

        unique_individuals.sort(key=lambda individual: individual.NumBits)

        accuracy = []
        num_bits = []
        for individual in unique_individuals:
            accuracy.append(individual.Accur)
            num_bits.append(individual.NumBits)

        plt.plot(num_bits,
                 accuracy,
                 plot_colors[counter],
                 label=plot_label[counter],
                 linewidth=2.0)

        # plt.scatter(num_bits, accuracy)
        counter += 1

    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((x1, x2, y1, 100))
    # plt.yticks(np.arange(y1, 102, 0.5))
    plt.gca().invert_xaxis()
    plt.legend(loc='best')

    plt.xlabel("Number of Features")
    plt.ylabel("Percent Accuracy")
    plt.title(title)

    plt.show()

    return


def plot_gen_vs_max_fit_multi_file(file_names, plot_label, plot_colors, title):
    counter = 0
    for file_name in file_names:
        data = np.loadtxt(file_name)
        gen, max_val = data[:, 0], data[:, 3]

        plt.plot(gen,
                 max_val,
                 plot_colors[counter],
                 label=plot_label[counter],
                 linewidth=2.0)

        counter += 1

    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, y1, 100))

    plt.legend(loc='best')
    plt.xlabel("GA Generation")
    plt.ylabel("Fitness (Percent Accuracy)")
    plt.title(title)

    plt.show()

    return


def get_unique_individuals(nsga_data):
    seen = set()
    seen_add = seen.add

    return [data for data in nsga_data if
            not (data.Chrom + "_" + str(data.NumBits) in seen or seen_add(data.Chrom + "_" + str(data.NumBits)))]


def load_nsga_data(file_name):
    nsga_data = list()

    with open(file_name) as inFile:
        user_reader = csv.DictReader(inFile)
        for line in user_reader:
            data = NsgaIndividual(int(line['Id']),
                                  line['Chrom'],
                                  float(line['Accuracy']),
                                  int(line['NumBits']),
                                  float(line['Time']))

            nsga_data.append(data)

    return nsga_data


def get_non_dominated_list(nsga_data):
    nondominated_front = []

    for current in nsga_data:
        num_dominate_me = 0

        for other in nsga_data:
            if current.Chrom == other.Chrom:
                continue

            if pareto_dominates(other, current):
                num_dominate_me += 1

        if num_dominate_me == 0:
            nondominated_front.append(current)

    return nondominated_front


# if this dominates opponent
def pareto_dominates(this, opponent):
    return (not (this.Accur < opponent.Accur)) and (not (this.NumBits > opponent.NumBits))


def pareto_front(file_name, title, fig_text):
    nsga_data = load_nsga_data(file_name)

    non_dominated_front = get_non_dominated_list(nsga_data)
    print (len(non_dominated_front))

    accuracy = []
    num_bits = []
    for individual in non_dominated_front:
        accuracy.append(individual.Accur)
        num_bits.append(individual.NumBits)

    plt.plot(num_bits, accuracy, 'g-', linewidth=2.0)
    plt.scatter(num_bits, accuracy)
    plt.legend(loc='best')

    plt.xlabel("Number of Features")
    plt.ylabel("Percent Accuracy")
    plt.title(title)
    plt.figtext(0.2, 0.009, fig_text)

    plt.show()

    return


# plot_gen_vs_fitness(
#     "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/part/Part-0.010-0.950.tsv",
#     "Partition List",
#     " ")

# plot_gen_vs_max_fit_multi_file(
#     [
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/bayes/BayesianNet-0.010-0.950.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/decision_tree/DecisionTable-0.010-0.950.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/part/Part-0.010-0.950.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/random_forest/RandomForest-0.010-0.950.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/random_tree/RandomTree-0.010-0.950.tsv"],
#     ["BayesianNet",
#      "DecisionTree",
#      "PartitionList",
#      "RandomForest",
#      "RandomTree"],
#     ['b-',
#      'g-',
#      'r-',
#      'c-',
#      'm-'],
#     "Best Fitness over Generations"
# )

# plot_pareto_front(
#     "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/random_tree/RandomTree_NSGA_lastGen.tsv",
#     "Random Tree - NSGA II",
#     " ")

# plot_pareto_front_multi_file(
#     [
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/bayes/BayesianNetwork_NSGA_LastGen.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/decision_tree/DecisionTree_NSGA_LastGen.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/part/PartitionTable_NSGA_LastGen.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/random_forest/RandomForest_NSGA_LastGen.tsv",
#         "/Users/harpreetsingh/github/genetic-algorithms-submit/twitter-subset-selection/weka_social_temp/random_tree/RandomTree_NSGA_lastGen.tsv"],
#     ["BayesianNet",
#      "DecisionTree",
#      "PartitionList",
#      "RandomForest",
#      "RandomTree"],
#     ['b-',
#      'g-',
#      'r-',
#      'c-',
#      'm-'],
#     "Pareto Fronts"
# )
