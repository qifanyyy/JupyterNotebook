import subprocess
import sys
import time
import graphics_alg as alg
#########################################################
# Execute QR_SearchingAlgorithm on generated files
#########################################################
ga_dict = {
    # genetic algorithm
    'ga1': ["ga", "1", "1", "1"],
    'ga2': ["ga", "1", "2", "1"],
    'ga3': ["ga", "1", "3", "1"],
    'ga4': ["ga", "1", "4", "1"],
    'ga5': ["ga", "2", "2", "1"],
    'ga6': ["ga", "2", "3", "1"],
    'ga7': ["ga", "2", "4", "1"],
    'ga8': ["ga", "4", "3", "1"],
    'ga9': ["ga", "4", "4", "1"],
    'ga10': ["ga", "1", "1", "2"],
    'ga11': ["ga", "1", "2", "2"],
    'ga12': ["ga", "1", "3", "2"],
    'ga13': ["ga", "1", "4", "2"],
    'ga14': ["ga", "2", "2", "2"],
    'ga15': ["ga", "2", "3", "2"],
    'ga16': ["ga", "2", "4", "2"],
    'ga17': ["ga", "4", "3", "2"],
    'ga18': ["ga", "4", "4", "2"],
}
ga_sa_dict = {
    # simulated annealing
    'ga_sa1': ["ga_sa", "1", "1", "2"],
    'ga_sa2': ["ga_sa", "1", "2", "2"],
    'ga_sa3': ["ga_sa", "1", "3", "2"],
    'ga_sa4': ["ga_sa", "1", "4", "2"],
    'ga_sa5': ["ga_sa", "2", "2", "2"],
    'ga_sa6': ["ga_sa", "2", "3", "2"],
    'ga_sa7': ["ga_sa", "2", "4", "2"],
    'ga_sa8': ["ga_sa", "4", "3", "2"],
    'ga_sa9': ["ga_sa", "4", "4", "2"],
}
ga_hc_dict = {
    # hill climbing
    'ga_hc1': ["ga_hc", "1", "1", "2"],
    'ga_hc2': ["ga_hc", "1", "2", "2"],
    'ga_hc3': ["ga_hc", "1", "3", "2"],
    'ga_hc4': ["ga_hc", "1", "4", "2"],
    'ga_hc5': ["ga_hc", "2", "2", "2"],
    'ga_hc6': ["ga_hc", "2", "3", "2"],
    'ga_hc7': ["ga_hc", "2", "4", "2"],
    'ga_hc8': ["ga_hc", "4", "3", "2"],
    'ga_gc9': ["ga_hc", "4", "4", "2"],
}
ga_bb_dict = {
    # Building Blocks
    'ga_bb1': ["ga_bb", "1", "1", "2"],
    'ga_bb2': ["ga_bb", "1", "2", "2"],
    'ga_bb3': ["ga_bb", "1", "3", "2"],
    'ga_bb4': ["ga_bb", "1", "4", "2"],
    'ga_bb5': ["ga_bb", "2", "2", "2"],
    'ga_bb6': ["ga_bb", "2", "3", "2"],
    'ga_bb7': ["ga_bb", "2", "4", "2"],
    'ga_bb8': ["ga_bb", "4", "3", "2"],
    'ga_bb9': ["ga_bb", "4", "4", "2"],
}
#########################################################
# Global variables
r_list = list()
# max number of columns
n_max = 10
# number of files to be generated and verified
n = 10
# number of iterations for algorithms to be compared on generated files
n_iterations = 1
# number of configurations of alg
n_config = 2
# details of files to be first generated and then checked
name = "GData"
type_file = ".txt"
#########################################################


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


def execute_r():
    global r_list

    # number of files to be generated and verified
    global n
    # path to output files
    global name
    global type_file

    path_script = "./r_generator/generate_data.R"
    command = 'Rscript'

    # execute R Script
    try:
        for i in range(n):
            # Define arguments
            file_path = [name + str(i)+type_file]

            # Build subprocess command
            cmd = [command, path_script] + file_path
            x = subprocess.check_output(cmd).splitlines()

            print(x)

            # Get output
            out = x[1].decode(sys.stdout.encoding)
            out2 = x[3].decode(sys.stdout.encoding)

            new_l = list_prepare(out)
            new_e = list_prepare2(out2)

            new_l.append(new_e)
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


def min_max(a, b):

    if a<b:
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
    min_dif = 0.001

    for i in range(n_obsv):
        [temp_min, temp_max] = min_max(list1[i][2], list2[i][2])
        temp_dif = temp_max - temp_min

        # print("DIF: ", temp_dif)

        if temp_dif > min_dif:
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

    execute_r()

    print("==========================================")

    # combine all dictionaries into one
    dicts = list()

    dicts.append(ga_dict)
    dicts.append(ga_hc_dict)
    dicts.append(ga_sa_dict)
    dicts.append(ga_bb_dict)

    # compare results
    try:

        for d in dicts:
            temp_dict = {k: d[k] for k in list(d)[:n_config]}

            t_p1 = t_p2 = t_p3 = t_p4 = 0

            for k in temp_dict.keys():
                print(temp_dict[k])

                p1 = p2 = p3 = p4 = 0
                for i in range(n_iterations):

                    c_list = list()
                    execute_c(c_list, temp_dict[k])

                    p1 += matching_all_columns(r_list, c_list)
                    p2 += matching_some_columns(r_list, c_list)
                    p3 += matching_rss(r_list, c_list)
                    p4 += average_time(c_list)

                    '''
                    print("iteration" , i)
                    print("Matching report by all columns: ", p1)
                    print("Matching report by some columns: ", p2)
                    print("Average difference: ", p3)
                    print("Average time execution: ", p4)
                    print("==========================================\n")
                    '''
                list_p = [p1, p2, p3, p4]
                list_p = [x / n_iterations for x in list_p]

                t_p1 += list_p[0]
                t_p2 += list_p[1]
                t_p3 += list_p[2]
                t_p4 += list_p[3]

            list_t_p = [t_p1, t_p2, t_p3, t_p4]
            list_t_p = [x / n_config for x in list_t_p]

            print("Matching report by all columns: ", list_t_p[0])
            print("Matching report by some columns: ", list_t_p[1])
            print("Average difference: ", list_t_p[2])
            print("Average time execution: ", list_t_p[3])
            print("==========================================\n")
            f.write("{},{},{},{}\n".format(list_t_p[0], list_t_p[1], list_t_p[2], list_t_p[3]))

    except Exception as err:
        print(err)


def compare_outputs_tuning_alg(alg):
    global r_list
    global n_iterations

    # file path for outputs of reports
    filepath = "./output_individuals/Out_Algorithms_Tuning.csv"
    f = open(filepath, "w+")

    execute_r()

    print("==========================================")

    # combine all dictionaries into one
    dicts = {}

    try:
        if alg.lower() == "ga":
            print("yes")
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

                c_list = list()
                execute_c(c_list, dicts[k])

                print(r_list)
                print(c_list)

                p1 += matching_all_columns(r_list, c_list)
                p2 += matching_some_columns(r_list, c_list)
                p3 += matching_rss(r_list, c_list)
                p4 += average_time(c_list)

            p1 = p1 / n_iterations
            p2 = p2 / n_iterations
            p3 = p3 / n_iterations
            p4 = p4 / n_iterations
            print("Matching report by all columns: ", p1)
            print("Matching report by some columns: ", p2)
            print("Average difference: ", p3)
            print("Average time execution: ", p4)
            print("==========================================\n")

            f.write("{},{},{},{}\n".format(p1, p2, p3, p4))

    except Exception as err:
        print(err)


#compare_outputs_nr_files_size()
#alg.execute()

alg_to_compare = "ga_bb"
compare_outputs_tuning_alg(alg_to_compare)
alg.execute_tuning(alg_to_compare)


