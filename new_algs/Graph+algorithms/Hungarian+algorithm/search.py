
# import the required libraries
import time
import math
import sys
import heapq

# redefine the coordinate system for equator, longitude 1 and longitude 2 for simplicity
AXIS = [[10, 22, 23, 12, 24, 25, 11, 26, 27, 13, 28, 29],
        [0, 4, 8, 12, 16, 20, 1, 21, 17, 13, 9, 5],
        [0, 2, 6, 10, 14, 18, 1, 19, 15, 11, 7, 3]]


# retrieve the data from the file by preprocessing
def init(input_file):
    mapping = dict()
    given_state = dict()
    init_state = dict()
    final_state = dict()
    count = 0
    for _ in input_file.split("\n")[1:-2]:
        x = _.split(" ")
        map_val = x[2][x[2].index('t')+1:-1]
        final_state[map_val] = count
        new_val = x[1][:-1]
        given_state[map_val] = new_val
        count += 1

    # change initial state from coordinate system to integer indexes from 0 to 29
    for (a, b), (c, d) in zip(given_state.items(), final_state.items()):
        init_state[b] = d

    # generate a dictionary of the index value of final state with value of index value of initial state
    for (a, b), (_, _) in zip(final_state.items(), init_state.items()):
        mapping[final_state[a]] = init_state[a]
    return final_state, mapping


# perform a rotation operation after getting the direction and axis as argument
def shift(mapping, direction, elem):
    a = []
    new_elem = elem.copy()
    if direction == 0:
        a.append(new_elem.pop())
        new_elem = a + new_elem
    elif direction == 1:
        temp = new_elem[0]
        new_elem = new_elem[1:]
        new_elem.append(temp)
    for key in mapping.keys():
        if mapping[key] in elem:
            mapping[key] = new_elem[elem.index(mapping[key])]
    return mapping


# generate a unique hash value for each state
# Since my coordinates are integers, i concatenate all the states and us the unique string value as my hash
def get_hash(new_map):
    hash_val = ''
    for _ in new_map:
        if _ in range(10):
            hash_val = hash_val + '0' + str(_)
        else:
            hash_val = hash_val + str(_)
    return hash_val


# final condition to check if the node in argument resembles the goal state
def is_sorted(mapping):
    for _ in mapping.keys():
        if _ != mapping[_]:
            return False
    return True


# to create 6 child nodes for a given parent node
def create_node(mapping, state, nodes, visited, path, level):
    flag = 0
    for arr in AXIS:
        for d in [0, 1]:
            new_state = shift(state.copy(), d, arr)
            new_hash = get_hash(list(new_state.values()))
            if new_hash not in visited:
                nodes.append(new_state)
                visited.add(get_hash(list(new_state.values())))
                path[new_hash] = get_hash(list(state.values())), level
            if is_sorted(new_state):
                mapping = new_state
                flag = 1
                break
        if flag == 1:
            break
    return mapping, nodes, path, flag


# from the hash table of {child_path : parent_path, level} I backtrack to determine the path
def get_path(path, final_state):
    goal = {}
    for key, value in final_state.items():
        goal[value] = key
    first = []
    c_first = []
    curr = '000102030405060708091011121314151617181920212223242526272829'
    while path[curr][0] != 0:
        last = []
        c_last = []
        state = [curr[i:i+2] for i in range(0, len(curr), 2)]
        coordinate = []
        for _ in state:
            coordinate.append(goal[int(_)])
        last.append(state)
        c_last.append(coordinate)
        first = last + first
        c_first = c_last + c_first
        curr = path[curr][0]
    c = list()
    c.append([curr[i:i + 2] for i in range(0, len(curr), 2)])
    d = []
    for _ in c[0]:
        d.append(goal[int(_)])
    c_first = [d] + c_first
    first = c + first
    steps = []
    cood1 = {0: "Increment Equator", 1: "Decrement Equator", 2: "Increment Long 90/270",
             3: "Decrement Long 90/270", 4: "Increment Long 0/180", 5: "Decrement Long 0/180"}
    for i in range(len(first)-1):
        test = []
        n_list = []
        test.append(first[i])
        test.append(first[i+1])
        for mapp in test:
            switch = 0
            node = {}
            for x in mapp:
                dd = int(x)
                node[switch] = dd
                switch += 1
            n_list.append(node)
        count = 0
        arr = []
        for v in AXIS:
            for d in [0, 1]:
                qq = shift(n_list[0].copy(), d, v)
                if qq == n_list[1]:
                    steps.append(cood1[count])
                count += 1
                arr.append(qq)
    return c_first, steps


# algorithm to run breadth first search for the problem statement
def bfs(mapping):
    solution = []
    nodes = list()
    visited = set()
    path = dict()
    level = 0
    count = 0
    states_expanded = 0
    nodes.append(mapping)
    visited.add(get_hash(list(mapping.values())))
    path[get_hash(list(mapping.values()))] = (0, 0)
    while nodes:
        level += 1
        for state in nodes:
            count += 1
            nodes = nodes[1:]
            mapping, nodes, path, flag = create_node(mapping, state, nodes, visited, path, level)
            states_expanded = states_expanded + 1
            if flag == 1:
                solution = path
                del nodes[:]
                break
    return solution, states_expanded, len(visited)


# developing a novel heuristic for a configuration by computing the list of Manhattan distance of all pieces
def get_dist(mapping):
    coordinates = []
    for arr in AXIS:
        temp = []
        for elem in arr:
            temp.append(mapping[elem])
        coordinates.append(temp)
    r_pairs = {(0, 1): 3, (1, 2): 0, (1, 0): 3, (2, 1): 0}
    big_coordinates = coordinates.copy()
    d_dict = {}
    i = 0
    j = 0
    for x in big_coordinates:
        for val in x:
            l1 = []
            l2 = []
            for q in coordinates:
                if val in q:
                    i = coordinates.index(x)
                    l1 = q.index(val)+1
                    break
            for row in AXIS:
                if val in row:
                    j = AXIS.index(row)
                    l2 = row.index(val)+1
                    break
            if i == j:
                dist = min(abs(l2 - l1), 12 - abs(l2 - l1))
            else:
                if (i, j) in list(r_pairs.keys()):
                    ops = r_pairs[(i, j)]
                    curr_loc = coordinates[i].index(val)
                    target_loc = AXIS[j].index(val)
                    dist = min((abs(ops - curr_loc) + abs(ops - target_loc)),
                               12 - (abs(ops - curr_loc) + abs(ops - target_loc)))
                else:
                    tt = coordinates[i].copy()
                    b = tt[3:] + tt[:3]
                    dist = min((abs(b.index(val)) + abs(AXIS[j].index(val))),
                               abs(12 - (b.index(val) + AXIS[j].index(val))))
            if val in d_dict.keys():
                if d_dict[val] > dist:
                    d_dict[val] = abs(dist)
            else:
                d_dict[val] = abs(dist)
    return list(d_dict.values())


# for the a* algorithm, the following function generates the heap with the added child nodes
def create_heap(mapping, state, heap, visited, path, level):
    flag = 0
    for arr in AXIS:
        for d in [0, 1]:
            new_state = shift(state.copy(), d, arr)
            new_hash = get_hash(list(new_state.values()))
            if new_hash not in visited:
                level = path[get_hash(list(state.values()))][1]
                level += 1
                heapq.heappush(heap, (sum(get_dist(new_state))/12 + level, new_hash))
                visited.add(get_hash(list(new_state.values())))
                path[new_hash] = get_hash(list(state.values())), level
            if is_sorted(new_state):
                mapping = new_state
                flag = 1
                break
        if flag == 1:
            break
    return mapping, heap, path, flag, level


# algorithm to run A* search for the given problem statement
def a_star(mapping):
    solution = []
    heap = []
    visited = set()
    path = dict()
    level = 0
    node = {}
    flag = 0
    states_expanded = 0
    heapq.heappush(heap, (sum(get_dist(mapping))/12, get_hash(list(mapping.values()))))
    visited.add(get_hash(list(mapping.values())))
    path[get_hash(list(mapping.values()))] = (0, 0)
    while flag == 0:
        state = heap[0]
        temp = [state[1][i:i+2] for i in range(0, len(state[1]), 2)]
        switch = 0
        heapq.heappop(heap)
        for i in temp:
            dd = int(i)
            node[switch] = dd
            switch += 1
        mapping, heap, path, flag, level = create_heap(mapping, node, heap, visited, path, level)
        states_expanded += 1
        # heapq.heapify(heap)
        if flag == 1:
            solution = path
            del heap[:]
            break
    return solution, states_expanded, len(visited)


# generating the steps
def rbfs_path(first):
    first = first.split(',')
    ss = []
    for _ in first:
        temp = [_[i:i+2] for i in range(0, len(_), 2)]
        ss.append(temp)
    first = ss
    steps = []
    cood1 = {0: "Increment Equator", 1: "Decrement Equator", 2: "Increment Long 90/270",
             3: "Decrement Long 90/270", 4: "Increment Long 0/180", 5: "Decrement Long 0/180"}
    for i in range(len(first) - 1):
        test = []
        n_list = []
        test.append(first[i])
        test.append(first[i + 1])
        for mapp in test:
            switch = 0
            node = {}
            for x in mapp:
                dd = int(x)
                node[switch] = dd
                switch += 1
            n_list.append(node)
        count = 0
        arr = []
        for v in AXIS:
            for d in [0, 1]:
                qq = shift(n_list[0].copy(), d, v)
                if qq == n_list[1]:
                    steps.append(cood1[count])
                count += 1
                arr.append(qq)
    return steps


# recursive function to perform recursive best first search
def rbfs(final_state, pn, failure, f_limit):
    node = pn[0]
    successors = []
    parent_hash = pn[1]
    if is_sorted(node):
        print("Number of states expanded: ", int(math.pow(6,len(rbfs_path(parent_hash)) - 1)))
        print("The maximum size of the queue during search: 6")
        print("The final path length: ", len(rbfs_path(parent_hash)) - 1)
        print("Final Path as a sequence of steps: ", ' ---> '.join(rbfs_path(parent_hash)))
        sys.exit()
    for arr in AXIS:
        for d in [0, 1]:
            new_state = shift(node.copy(), d, arr)
            x = get_hash(list(new_state.values()))
            y = sum(get_dist(new_state))/12
            successors.append((y, x, str(parent_hash+str(',') + x)))

    while True:
        successors = sorted(successors)
        best = successors[0]
        path_s = best[2]
        if best[0] > f_limit:
            return False, best[0]
        alternative = successors[1]
        state = best[1]
        temp = [state[i:i + 2] for i in range(0, len(state), 2)]
        switch = 0
        node = {}
        for i in temp:
            dd = int(i)
            node[switch] = dd
            switch += 1
        pn = (node, path_s)
        flag, result = rbfs(final_state, pn, failure, min(alternative[0], f_limit))
        if flag is True:
            sys.exit()
        else:
            successors[0][0] = result


# passing the initial node into recursive function for rbfs
def rbfs_call(mapping, final_state):
    return rbfs(final_state, (mapping, get_hash(list(mapping.values()))), "fail", 1000)


# main file to execute the program
def main():
    # retrieving data from a file
    data = open(str(sys.argv[2]), "r")
    data.seek(0)
    final_state, mapping = init(data.read())
    max_queue_len = 0
    if sys.argv[1] == "BFS":
        solution, states_expanded, max_queue_len = bfs(mapping)
    elif sys.argv[1] == "AStar":
        solution, states_expanded, max_queue_len = a_star(mapping)
    elif sys.argv[1] == "RBFS":
        solution, states_expanded = rbfs_call(mapping, final_state)
    else:
        solution = []
        states_expanded = 0
        print("Please enter a valid call")
    path, steps = get_path(solution, final_state)
    print("Number of states expanded: ", states_expanded)
    print("The maximum size of the queue during search: ", max_queue_len)
    print("The final path length: ", len(path)-1)
    print("Final Path as a sequence of steps: ", ' ---> '.join(steps))


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Running time: %s secs" % (time.time() - start_time))

