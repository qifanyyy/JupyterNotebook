#########################################################
# Execute QR_SearchingAlgorithm on generated files
#########################################################

import subprocess
import sys
import graphics_alg as alg
import generate_data as gen


#########################################################
# Global variables
r_list = list()

# number of files to be generated and verified
n = 10
# number of iterations for algorithms to be compared on generated files
n_iterations = 1

# method comparing alg:  1 for all alg, 2 for single alg tuning
method = 1
# alg to compare, in case method = 2
alg_to_compare = "ga"

# details of files to be first generated and then checked
name = "GData"
type_file = ".txt"
#########################################################

''' 
mutation1 - flip 
mutation2 - interchanging # number of columns is kept
mutation3 - interchanging absolute # interchanging different genes always # blocanta
mutation4 - reversing

crossover1 - 1 point # number of columns is kept
crossover2 - uniform 
crossover3 - RRC
crossover4 - 1 point simple
'''

# for comparing alg
compare_dict = {
    # one config for each alg
    'ga':    ["ga",    "4", "1", "2"],
    'ga_hc': ["ga_hc", "1", "1", "2"],
    'ga_sa': ["ga_sa", "1", "1", "2"],
    'ga_bb': ["ga_bb", "4", "3", "2"],
}

# for tuning algorithms
ga_dict = {
    # genetic algorithm
    'ga1': ["ga", "1", "1", "1"],
    'ga2': ["ga", "1", "2", "1"],
    'ga3': ["ga", "1", "3", "1"],
    'ga4': ["ga", "1", "4", "1"],
    'ga5': ["ga", "2", "1", "1"],
    'ga6': ["ga", "2", "2", "1"],
    'ga7': ["ga", "2", "3", "1"],
    'ga8': ["ga", "2", "4", "1"],
    'ga9': ["ga", "4", "1", "1"],
    'ga10': ["ga", "4", "2", "1"],
    'ga11': ["ga", "4", "3", "1"],
    'ga12': ["ga", "4", "4", "1"],
    'ga13': ["ga", "1", "1", "2"],
    'ga14': ["ga", "1", "2", "2"],
    'ga15': ["ga", "1", "3", "2"],
    'ga16': ["ga", "1", "4", "2"],
    'ga17': ["ga", "2", "1", "2"],
    'ga18': ["ga", "2", "2", "2"],
    'ga19': ["ga", "2", "3", "2"],
    'ga20': ["ga", "2", "4", "2"],
    'ga21': ["ga", "4", "1", "2"],
    'ga22': ["ga", "4", "2", "2"],
    'ga23': ["ga", "4", "3", "2"],
    'ga24': ["ga", "4", "4", "2"],
}

ga_sa_dict = {
    # simulated annealing
    'ga_sa1': ["ga_sa", "1", "1", "2"],
    'ga_sa2': ["ga_sa", "2", "2", "2"],
    'ga_sa3': ["ga_sa", "4", "3", "2"],
}
ga_hc_dict = {
    # hill climbing
    'ga_hc1': ["ga_hc", "1", "1", "2"],
    'ga_hc2': ["ga_hc", "2", "2", "2"],
    'ga_hc3': ["ga_hc", "4", "3", "2"],
}
ga_bb_dict = {
    # Building Blocks
    'ga_bb1': ["ga_bb", "1", "1", "1"],
    'ga_bb2': ["ga_bb", "1", "2", "1"],
    'ga_bb3': ["ga_bb", "1", "3", "1"],
    'ga_bb4': ["ga_bb", "1", "4", "1"],
    'ga_bb5': ["ga_bb", "2", "1", "1"],
    'ga_bb6': ["ga_bb", "2", "2", "1"],
    'ga_bb7': ["ga_bb", "2", "3", "1"],
    'ga_bb8': ["ga_bb", "2", "4", "1"],
    'ga_bb9': ["ga_bb", "4", "1", "1"],
    'ga_bb10': ["ga_bb", "4", "2", "1"],
    'ga_bb11': ["ga_bb", "4", "3", "1"],
    'ga_bb12': ["ga_bb", "4", "4", "1"],
}


def list_prepare(out):

    temp_list = list()

    temp = out.split(" ")
    temp = [maybe_int(v) for v in temp]
    temp = [v for v in temp if v is not None]

    temp.sort()
    temp_list.append(len(temp))
    temp_list.append(temp)

    return temp_list


def list_prepare2(out):

    temp = out.split(" ")
    temp = [maybe_float(v) for v in temp]
    temp = [v for v in temp if v is not None]

    return temp[0]


def maybe_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def maybe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def execute_py():
    global r_list

    # number of files to be generated and verified
    global n
    # path to output files
    global name
    global type_file

    # execute py Script
    try:
        for i in range(n):
            # Define arguments
            file_path = name + str(i) + type_file

            # Build subprocess command
            BEST, AIC = gen.write_to_file(file_path)

            new_l = list()
            new_l.append(len(BEST))
            new_l.append(BEST)
            new_l.append(AIC)

            r_list.append(new_l)

    except FileNotFoundError as err1:
        print("In Execute_r: ", err1)
    except IndexError as err2:
        print("\nIn Execute_r: ", err2)


def execute_c(c_list, par):

    # number of files to be generated and verified
    global n
    # path to output files
    global name
    global type_file

    command = "./Debug/QR_SearchingAlgorithm.exe"

    # execute c script
    try:
        for i in range(n):

            # Define arguments
            file_path = [name + str(i) + type_file]
            args = par

            # Build subprocess command
            cmd = [command] + args + file_path
            x = subprocess.check_output(cmd, cwd='./Debug').splitlines()

            # Get output
            out = x[5].decode(sys.stdout.encoding)
            out2 = x[6].decode(sys.stdout.encoding)  # AIC
            out3 = x[7].decode(sys.stdout.encoding)  # RSS
            out4 = x[9].decode(sys.stdout.encoding)

            new_l = list_prepare(out)
            new_aic = list_prepare2(out2)
            new_rss = list_prepare2(out3)
            new_exec_time = list_prepare2(out4)

            new_l.append(new_aic)
            new_l.append(new_exec_time)

            c_list.append(new_l)

    except FileNotFoundError as err1:
        print("In Execute_c: ", err1)
    except IndexError as err2:
        print("In Execute_c: ", err2)
    except subprocess.TimeoutExpired as err3:
        print("In Execute_c: ", err3.timeout)


def matching_all_columns(list1, list2):

    # this function find all matching solutions
    # a solution is matching if all columns are the same as columns of best solution
    n_obsv = len(list1)
    n_match = 0

    for i in range(n_obsv):
        if list1[i][0] == list2[i][0]:
            temp_n = [z for z, j in zip(list1[i][1], list2[i][1]) if z == j]
            if len(temp_n) == list1[i][0]:
                n_match += 1
    report = (float(n_match / n_obsv))
    return report


def matching_some_columns(list1, list2):

    # this function find all matching columns of an individual
    # the probability is computed obtaining all columns that are the same as columns of best solution
    n_obsv = len(list1)
    probability = 0

    for i in range(n_obsv):
        temp_n = 0
        for j in list1[i][1]:
            if j in list2[i][1]:
                temp_n += 1

        temp_p = float(temp_n) / list1[0][0]
        probability += temp_p

    report = (float(probability / n_obsv))
    return report


def missmatch_columns(list1, list2):

    # this function find all matching columns of an individual
    # the probability is computed obtaining all columns that are the same as columns of best solution
    n_obsv = len(list1)
    probability = 0

    for i in range(n_obsv):
        temp_n = 0
        for j in list1[i][1]:
            if j in list2[i][1]:
                temp_n += 1
        missmatch = list2[i][0] - temp_n
        temp_p = float(missmatch) / list2[i][0]
        probability += temp_p

    report = (float(probability / n_obsv))
    return report


def min_max(a, b):

    if a < b:
        min = a
        max = b
    else:
        min = b
        max = a

    return [min, max]


def matching_rss(list1, list2):

    # this function compute report between RSS given by generated script and output of heuristic alg
    n_obsv = len(list1)
    report = 0
    RSS_min_dif = 0.001
    AIC_min_dif = 4

    for i in range(n_obsv):
        [temp_min, temp_max] = min_max(list1[i][2], list2[i][2])
        temp_dif = temp_max - temp_min

        #if temp_dif > AIC_min_dif:
        report += abs(temp_dif/list1[i][2])

    report = (float(report / n_obsv))
    return report


def average_time(list2):

    # this function compute average time execution of an algorithm
    n_obsv = len(list2)
    report = 0

    for i in range(n_obsv):
        report += list2[i][3]

    report = (float(report / n_obsv))
    return report


def compare_outputs_nr_files_size():
    global r_list
    global n_iterations
    global n_config

    # file path for outputs of reports
    filepath = "./output_individuals/Out_Algorithms.csv"
    f = open(filepath, "w+")

    execute_py()

    print("==========================================")

    # compare results
    try:

        for k in compare_dict.keys():
            print(compare_dict[k])

            p2 = p3 = p4 = 0
            for i in range(n_iterations):

                c_list = list()
                execute_c(c_list, compare_dict[k])

                print(r_list)
                print(c_list)

                p1 = missmatch_columns(r_list, c_list)
                p2 += matching_some_columns(r_list, c_list)
                p3 += matching_rss(r_list, c_list)
                p4 += average_time(c_list)

                '''
                print("iteration" , i)
                print("MissMatching columns: ", p1)
                print("Matching columns: ", p2)
                print("AIC error: ", p3)
                print("Time execution: ", p4)
                print("==========================================\n")
                '''
            list_p = [p2, p3, p4, p1]
            list_p = [x / n_iterations for x in list_p]

            print("Matching columns: ", list_p[0])
            print("AIC error: ", list_p[1])
            print("Time execution: ", list_p[2])
            print("Missmatch columns: ", list_p[3])
            print("==========================================\n")
            f.write("{},{},{},{}\n".format(list_p[0], list_p[1], list_p[2], list_p[3]))

    except Exception as err:
        print("In compare_outputs_nr_files_size: ", err)


def compare_outputs_tuning_alg(alg):
    global r_list
    global n_iterations

    # file path for outputs of reports
    filepath = "./output_individuals/Out_Algorithms_Tuning.csv"
    f = open(filepath, "w+")

    execute_py()

    print("==========================================")

    # combine all dictionaries into one
    dicts = {}

    try:
        if alg.lower() == "ga":
            dicts = ga_dict.copy()
        if alg.lower() == 'ga_hc':
            dicts = ga_hc_dict.copy()
        if alg.lower() == 'ga_sa':
            dicts = ga_sa_dict.copy()
        if alg.lower() == 'ga_bb':
            dicts = ga_bb_dict.copy()

    except Exception as err:
        print(err)

    # compare results
    try:
        for k in dicts.keys():
            print(dicts[k])

            p1 = p2 = p3 = p4 = 0
            for i in range(n_iterations):

                print(i)
                c_list = list()
                execute_c(c_list, dicts[k])

                print(r_list)
                print(c_list)

                p1 += missmatch_columns(r_list, c_list)
                p2 += matching_some_columns(r_list, c_list)
                p3 += matching_rss(r_list, c_list)
                p4 += average_time(c_list)

            pi = p1 / n_iterations
            p2 = p2 / n_iterations
            p3 = p3 / n_iterations
            p4 = p4 / n_iterations
            print("MissMatching columns: ", p1)
            print("Matching columns: ", p2)
            print("AIC error: ", p3)
            print("Time execution: ", p4)
            print("==========================================\n")

            f.write("{},{},{},{}\n".format(p2, p3, p4, p1))

    except Exception as err:
        print("In compare_outputs_tuning_alg: ", err)


# compare output between all algorithms
if method == 1:
    compare_outputs_nr_files_size()
    alg.execute()
# compare output between different configurations of an algorithm
elif method == 2:
    compare_outputs_tuning_alg(alg_to_compare)
    alg.execute_tuning(alg_to_compare)



