from multiprocessing.dummy import Pool
import random
import time
import json
import os

def generate_graph(size):
    graph = [[float("inf") for j in range(size)] for i in range(size)]
    decision = (True, False)
    for i in range(size):
        for j in range(size):
            if i == j:
                graph[i][j] = 0
                continue
            if random.choice(decision):
                #50% chance of skipping an element and leaving no path at between i and j
                continue
            graph[i][j] = random.randint(1, 15)
    return graph

#Initial declaration of global data. May change after input for final implementation
v = 100
#weightGraph = generate_graph(v)


def generate_distances(weights):
    """Generate a 3D matrix of distances between nodes"""
    return [[[weights[i][j]] for j in range(v)] for i in range(v)]


def next_matrix(weights):
    """Different path matrix maker"""
    next_path = [[[float("inf")] for j in range(v)] for i in range(v)]
    for i in range(v):
        for j in range(v):
            if weights[i][j] != float("inf"):
                next_path[i][j][0] = i
    return next_path


def find_paths(weights, asynchronous=False, cores=4):
    """Return a distances matrix with minimal paths between nodes and a path matrix recording the routes taken"""
    dist = generate_distances(weights)
    from_to = next_matrix(weights)
    #Perform algorithm twice
    for x in range(2):
        if asynchronous:
            async_compute_paths(dist, from_to, cores)
        else:
            compute_paths(dist, from_to)

    return dist, from_to


def compute_paths(dist, from_to):
    """Modified Floyd-Warshall algorithm"""
    PATH_LIMIT = 3
    for k in range(v):
        for i in range(v):
            for j in range(v):
                idx = insert_in_order((dist[i][k][0] + dist[k][j][0]), dist[i][j])
                if idx != -1:
                    from_to[i][j].insert(idx, from_to[k][j][0])
                    enforce_limit(PATH_LIMIT, from_to[i][j], dist[i][j])


def async_compute_paths(dist, from_to, core_count):
    """Identical function to compute_paths but performs the second loop in parallel utilizing multiple cores"""
    PATH_LIMIT = 3
    pool = Pool(core_count)

    def map_function(i):
        for j in range(v):
            idx = insert_in_order((dist[i][k][0] + dist[k][j][0]), dist[i][j])
            if idx != -1:
                from_to[i][j].insert(idx, from_to[k][j][0])
                enforce_limit(PATH_LIMIT, from_to[i][j], dist[i][j])

    for k in range(v):
        pool.map(map_function, range(v))


def insert_in_order(item, collection):
    """Inserts a path weight into the correct position in a list, up to the max path number and returns that position"""
    end = len(collection)
    if item > collection[-1]:
        collection.append(item)
        return end
    if item == float("inf") or item in collection:
        return -1
    i = 0
    while i <= end:
        if i == end:
            collection.insert(i, item)
            return i
        if item < collection[i]:
            collection.insert(i, item)
            return i
        else:
            i += 1
    return -1


def enforce_limit(size, *collections):
    """If the passed in collections are over the given size, remove the last element"""
    for col in collections:
        if len(col) > size:
            del col[-1]


def partition_list(collection):
    """Partitions a list into a list of lists of equal value"""
    lower_bound = 0
    return_values = list()
    temp = list()
    for i in range(len(collection)):
        if collection[i] == collection[lower_bound]:
            temp.append(collection[i])
        else:
            return_values.append(temp)
            temp = list()
            temp.append(collection[i])
            lower_bound = i
    return_values.append(temp)
    return return_values


def list_paths(path_matrix, i, j):
    """Returns a list of lists, each list containing a path from i to j in ascending order of cost"""
    if path_matrix[i][j][0] == float("inf"):
        raise ValueError
    if i < 0 or j < 0:
        raise IndexError
    end = j
    route_beginnings = partition_list(path_matrix[i][j])
    path_list = list()
    for route in route_beginnings:
        if route[0] == float("inf"):
            path_list.append("NO PATH")
            continue
        j = end
        if len(route) > 1:
            return list_paths_subordinate(path_matrix, i, j)
        this_path = list()
        this_path.append(j)
        j = route[0]
        while i != j:
            if i != j:
                this_path.append(j)
            j = path_matrix[i][j][0]

        this_path.append(i)
        this_path.reverse()
        #Edge case where 2 routes through same predecessor node
        #But those two routes are not sequential
        if this_path in path_list:
            this_path = list()
            j = end
            this_path.append(j)
            j = route[0]
            this_path.append(j)
            j = path_matrix[i][j][1]
            while i != j:
                if i != j:
                    this_path.append(j)
                j = path_matrix[i][j][0]
            this_path.append(i)
            this_path.reverse()

        path_list.append(this_path)
    return path_list


def list_paths_subordinate(path_matrix, i, j):
    """Subordinate path finding function to handle multiple routes through same predecessor node"""
    if i == j:
        return [[j]]
    collection = partition_list(path_matrix[i][j])
    final_routes = list()
    for predecessors in collection:
        new_j = predecessors[0]
        routes = list_paths(path_matrix, i, new_j)
        final_routes = final_routes+routes[:len(predecessors)]
    for path in final_routes:
        path.append(j)
    return final_routes


def zip_paths(path_matrix, distance_matrix, i, j):
    """Combines path weights with their associated path"""
    distance_list = distance_matrix[i][j]
    list_of_paths = list_paths(path_matrix, i, j)
    return zip(distance_list, list_of_paths)


def has_no_cycles(collection):
    """Returns True if a passed in path list contains no cycle"""
    return len(collection) == len(set(collection))


def load_json(filename):
    global v
    test_data = json.loads(open(filename).read())
    paths_to_print = test_data.pop('ResultNodePair')
    v = len(test_data.keys())
    graph = [[float("inf") for j in range(v)] for i in range(v)]
    for key in test_data:
        i = int(key)
        for subkey in test_data[key]:
            j = int(subkey)
            if test_data[key][subkey] >= 9999999:
                continue
            graph[i][j] = test_data[key][subkey]
    return graph, paths_to_print


def sort_by_cost(collection):
    return collection[0]


def sort_by_length(collection):
    return len(collection[1])


def display_results(start, finish, dist, path_matrix):
    try:
        results = zip_paths(path_matrix, dist, start, finish)
    except ValueError:
        print("No path from {} to {}".format(start, finish))
        return
    except IndexError:
        print("Invalid path from {} to {}".format(start, finish))
        print("Requested boundary node out of range. Nodes are from 0 to {}".format(v-1))
        return
    without_cycles = [x for x in filter(lambda x: has_no_cycles(x[1]), results)]
    print("From node {} to Node {}".format(start, finish))
    #Change key to sort_by_length to instead list results by shortest path length
    without_cycles.sort(key=sort_by_cost)
    for idx in range(len(without_cycles)):
        path = without_cycles[idx][1]
        if path == "NO PATH":
            continue
        printable = "->".join([str(x) for x in path])
        print("Path {}: {} with cost {}".format(idx+1, printable, without_cycles[idx][0]))


def write_results(start, finish, dist, path_matrix, output_file):
    try:
        results = zip_paths(path_matrix, dist, start, finish)
    except ValueError:
        output_file.write("No path from {} to {}\n".format(start, finish))
        return
    except IndexError:
        output_file.write("Invalid path from {} to {}\n".format(start, finish))
        output_file.write("Requested boundary node out of range. Nodes are from 0 to {}\n".format(v-1))
        return
    without_cycles = [x for x in filter(lambda x: has_no_cycles(x[1]), results)]
    output_file.write("From node {} to Node {}\n".format(start, finish))
    #Change key to sort_by_length to instead list results by shortest path length
    without_cycles.sort(key=sort_by_cost)
    for idx in range(len(without_cycles)):
        path = without_cycles[idx][1]
        if path == "NO PATH":
            continue
        printable = "->".join([str(x) for x in path])
        output_file.write("Path {}: {} with cost {}\n".format(idx+1, printable, without_cycles[idx][0]))


###The Below code can be used to analyze all files in a directory as opposed to the interaction
###version below it
# files = filter(lambda x: x.endswith(".json"), os.listdir())
# #files = ["net4-80.json", "net9-50.json"]
# output = open("output.txt", "w")
# for file in files:
#     print("Working on file {}".format(file))
#     output.write("\nTesting file: {} \n".format(file))
#     weightGraph, paths_to_print = load_json(file)
#     #Run multi core version if 35 or more nodes in graph
#     before = time.time()
#     if v >= 35:
#         distances, paths = find_paths(weightGraph, True, 10)
#     else:
#         distances, paths = find_paths(weightGraph)
#     time_spent = time.time() - before
#
#     for item in paths_to_print:
#         for key in item:
#             start = int(key)
#             finish = int(item[key])
#             write_results(start, finish, distances, paths, output)
#     output.write("CPU time measured: {} seconds\n".format(time_spent))
# output.close()


running = True
while running:
    filename = ""
    getting_file = True
    while getting_file:
        print("Enter an absolute path unless the json file is in this program's directory...")
        filename = input("Please enter the path to a json file: ")
        try:
            weightGraph, paths_to_print = load_json(filename)
            getting_file = False
        except IOError:
            print("Invalid file path")
            continue
    #Run multi core version if 35 or more nodes in graph
    before = time.time()
    if v >= 35:
        distances, paths = find_paths(weightGraph, True, 10)
    else:
        distances, paths = find_paths(weightGraph)
    time_spent = time.time() - before

    for item in paths_to_print:
        for key in item:
            start = int(key)
            finish = int(item[key])
            display_results(start, finish, distances, paths)

    print("CPU time measured: {} seconds".format(time_spent))
    print("\nWould you like to test another graph?")
    check = input("Yes [Y] or No [N] -> ")
    if check.lower() != "y" and check.lower() != "yes":
        running = False










