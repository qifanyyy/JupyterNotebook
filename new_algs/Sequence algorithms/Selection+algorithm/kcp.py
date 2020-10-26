import random
import datetime
import timeit
import math
import heapq
import os
import sys
import string

## FUNCTIONS #######################################################

# Get the cardinality of every vertex using best_known_size for the pruning
def cardinality():
    global card
    card = []
    for i in range(0,n):
        card.append(0)
    for i in range(0,n):
        for j in range(0,n):
            if matrix[i][j] < best_known_size:
                card[i] += 1


# Get the cardinality of every vertex using an input size for the pruning
def cardinality_size(size):
    global card
    card = []
    for i in range(0,n):
        card.append(0)
    for i in range(0,n):
        for j in range(0,n):
            if matrix[i][j] <= size:
                card[i] += 1

# Update Cardinality (i.e. do not take into account the previously dominated vertices)
#def update_cardinality(centers, max_index, s):
    #global dominated
    #global card
    #recently_dominated = []
    #for i in range(0,n):
        #recently_dominated.append(False)
    #for i in range(0,n):
        #if not dominated[i]:
            #for j in range(0,max_index):
                #if matrix[i][centers[j]] <= s:
                    #dominated[i] = True
                    #recently_dominated[i] = True
    #for i in range(0,n):
        #if recently_dominated[i]:
            #for j in range(0,n):
                #if matrix[j][i] <= s:
                    #card[j] -= 1
                    
def update_cardinality(centers, max_index, s):
    global dominated
    global card
    recently_dominated = []
    for i in range(0,n):
        if matrix[centers[max_index-1]][i] <= s \
                and not dominated[i]:
            recently_dominated.append(i)
            dominated[i] = True
    for i in recently_dominated:
        for j in range(0, n):
            if matrix[i][j] <= s and i != j:
                card[j] -= 1                    

# Update Distance. Get the distance from every vertex to its nearest center in the partial solution
def update_distance(centers, max_index):
    global distance
    for i in range(0, n):
        if matrix[i][centers[max_index]] < distance[i]:
            distance[i] = matrix[i][centers[max_index]]

# Get the farthest node
def farthest_node():
    max_dist = 0
    max_dist_nodes = []
    global distance
    for i in range(0,n):
        if distance[i] > max_dist:
            max_dist = distance[i]
    for i in range(0,n):
        if distance[i] == max_dist:
            max_dist_nodes.append(i)
    return max_dist_nodes[random.randint(0,len(max_dist_nodes)-1)]

# Get the farthest node
def farthest_node_in_guide_sol(guide_sol):
    max_dist = 0
    max_dist_node = 0
    global distance
    for i in range(0, len(guide_sol)):
        if distance[guide_sol[i]] > max_dist:
            max_dist = distance[guide_sol[i]]
            max_dist_node = guide_sol[i]
    return max_dist_node


# Get the set of critical neighbors
def get_critical_neighbors(node, s):
    l = []
    for i in range(0, n):
        if matrix[i][node] <= s:
            l.append(i)
    return l

# Get the set of critical neighbors
def reduced_critical_neighbors(cn, node, s):
    boolean_cn = []
    for i in range(0, n):
        boolean_cn.append(False)
    for i in range(0, len(cn)):
        boolean_cn[cn[i]] = True
    l = []
    for i in range(0, n):
        if matrix[i][node] <= s:
            l.append(i)
    l2 = []
    for i in range(0, len(l)):
        if boolean_cn[l[i]]:
            l2.append(l[i])
    if len(l2) == 0:
        return cn
    else:
        return l2


# Get the maximum cardinality vertex
def max_cardinality(l):
    max_card = 0
    max_card_nodes = []
    global card
    for i in l:
        if card[i] > max_card:
            max_card = card[i]
    for i in l:
        if card[i] == max_card:
            max_card_nodes.append(i)           
    return max_card_nodes[random.randint(0,len(max_card_nodes)-1)]

# Get the solution size of the currently constructed solution
def solution_size():
    max_dist = 0
    global distance
    for i in range(0,n):
        if distance[i] > max_dist:
            max_dist = distance[i]
    return max_dist


# Critical Dominating Set heuristic
def dominating_set2(s, guide_sol):
    C = []
    global card
    global dominated
    global distance
    global prob
    dominated = []
    distance = []
    for i in range(0,n):
        dominated.append(False)
        distance.append(float("inf"))
    critical_neighbors = get_critical_neighbors(random.randint(0, n-1), s)
    if random.random() <= prob:
        C.append(max_cardinality(critical_neighbors))
    else:
        C.append(random.randint(0,n-1))
    update_distance(C, 0)
    for i in range(1, k):
        update_cardinality(C, i, s)
        critical_neighbors = get_critical_neighbors(farthest_node(), s)
        critical_neighbors = reduced_critical_neighbors(critical_neighbors, farthest_node_in_guide_sol(guide_sol), s)
        if random.random() <= prob:
            C.append(max_cardinality(critical_neighbors))
        else:
            C.append(critical_neighbors[random.randint(0,len(critical_neighbors)-1)])
        update_distance(C, i)
    size = solution_size()
    out = [size, C]
    return out

def remaining_nodes(s):
    out = []
    for j in range(0, n):
        if distance[j] > 2 * s:
            out.append(j)
    return out

# Critical Dominating Set heuristic
def dominating_set_1(s):
    C = []
    global card
    global dominated
    global distance
    global prob
    dominated = []
    distance = []
    for i in range(0,n):
        dominated.append(False)
        distance.append(float("inf"))
    critical_neighbors = get_critical_neighbors(random.randint(0, n-1), s)
    if random.random() <= prob:
        C.append(max_cardinality(critical_neighbors))
    else:
        C.append(random.randint(0,n-1))
    update_distance(C, 0)
    for i in range(1, k):
        update_cardinality(C, i, s)
        critical_neighbors = get_critical_neighbors(farthest_node(), s)
        if random.random() <= prob:
            C.append(max_cardinality(critical_neighbors))
        else:
            C.append(critical_neighbors[random.randint(0,len(critical_neighbors)-1)])
        update_distance(C, i)
    size = solution_size()
    out = [size, C]
    return out

def dominating_set_2(s, init):
    C = []
    global card
    global dominated
    global distance
    global prob
    dominated = []
    distance = []
    for i in range(0,n):
        dominated.append(False)
        distance.append(float("inf"))
    if random.random() <= prob:
        C.append(init)
    else:
        C.append(random.randint(0,n-1))
    update_distance(C, 0)
    for i in range(1, k):
        update_cardinality(C, i, s)
        critical_neighbors = get_critical_neighbors(farthest_node(), s)
        if random.random() <= prob:
            C.append(max_cardinality(critical_neighbors))
        else:
            C.append(critical_neighbors[random.randint(0,len(critical_neighbors)-1)])
        update_distance(C, i)
    size = solution_size()
    out = [size, C]
    return out

def get_possible_centers(s):
    out = []
    for i in range(0, n):
        if distance[i] > 2 * s:
            out.append(i)
    return out

def reduce_T_boolean(neighbors, T_boolean, C, index, s):
    subset = []
    for i in range(0, n):
        if matrix[C[index]][i] <= s and neighbors:
            subset.append(i)
            neighbors[i] = False
    for i in subset:
        #if T_boolean[i]:
        for j in range(0, n):
            if matrix[j][i] <= s:
                T_boolean[j] = False
    return [T_boolean, neighbors]

def reduce_T(T_boolean):
    T = []
    for i in range(0, n):
        if T_boolean[i]:
            T.append(i)
    return T

def hs_algorithm(s):
    C = []
    global distance
    possible_new_center = []
    distance = []
    not_done = True
    neighbors = []
    for i in range(0, n):
        neighbors.append(True)
    T_boolean = []
    for i in range(0, n):
        T_boolean.append(True)
    T = []
    for i in range(0, n):
        T.append(i)
    #for i in range(0,n):
    #    distance.append(float("inf"))
    C.append(T[random.randint(0, n-1)])
    temp = T_boolean = reduce_T_boolean(neighbors, T_boolean, C, 0, s)
    T_boolean = temp[0]
    neighbors = temp[1]
    T = reduce_T(T_boolean)
    #update_distance(C, 0)
    i = 0
    while not_done:
        #possible_new_center = get_possible_centers(s)
        i = i + 1
        #if len(possible_new_center) > 0:
        if len(T) > 0:
            C.append(T[random.randint(0, len(T)-1)])
            temp = reduce_T_boolean(neighbors, T_boolean, C, i, s)
            T_boolean = temp[0]
            neighbors = temp[1]
            T = reduce_T(T_boolean)
            #update_distance(C, i)
        else:
            not_done = False
    size = solution_size_hs(C)
    out = [size, C]
    return out

def solution_size_hs(C):
    max_dist = 0
    for i in range(0, n):
        min_dist = float("inf")
        for j in range(0, len(C)):
            if matrix[i][C[j]] < min_dist:
                min_dist = matrix[i][C[j]]
        if min_dist > max_dist:
            max_dist = min_dist
    return max_dist

# This function generates a 2-approximated solution with the Gon algorithm
def gon():
    C = []
    global distance
    distance = []
    for i in range(0,n):
        distance.append(float("inf"))
    f = random.randint(0, n-1)
    C.append(f)
    update_distance(C, 0)
    for i in range(1, k):
        f = farthest_node()
        C.append(f)
        update_distance(C, i)
    size = solution_size()
    out = [size, C]
    return out



# Get the critical (farthest) node
def criticalNode(C):
    max_dist = 0
    farthest_node = 0
    for i in range(0, n):
        min_dist = float("inf")
        for j in range(0, k):
            if matrix[i][C[j]] <= min_dist:
                min_dist = matrix[i][C[j]]
        if min_dist > max_dist:
            max_dist = min_dist
            farthest_node = i
    return farthest_node

# Make the boolean version of the input solution
def getCurrentBoolean(in_sol):
    l = []
    for i in range(0, n):
        l.append(False)
    for i in range(0, len(in_sol)):
        l[in_sol[i]] = True
    return l

# Get First and Second closest centers
def firstAndSecond(in_sol):
    global F0
    global F1
    global D0
    global D1
    global M
    F0 = []
    F1 = []
    D0 = []
    D1 = []
    M = []
    for i in range(0, n):
        F0.append(0)
        F1.append(0)
        D0.append(0)
        D1.append(0)
        M.append(0)
    for i in range(0, n):
        min_dist = float("inf")
        for j in range(0, k):
            if matrix[i][in_sol[j]] < min_dist:
                min_dist = matrix[i][in_sol[j]]
                F0[i] = in_sol[j]
                D0[i] = min_dist
        min_dist = float("inf")
        for j in range(0, k):
            if matrix[i][in_sol[j]] < min_dist and in_sol[j] != F0[i]:
                min_dist = matrix[i][in_sol[j]]
                F1[i] = in_sol[j]
                D1[i] = min_dist

# Add facility to current solution
def addFacility(f):
    global F0
    global F1
    global D0
    global D1
    Sc = 0
    for i in range(0, n):
        if matrix[i][f] < D0[i]:
            D1[i] = D0[i]
            F1[i] = F0[i]
            D0[i] = matrix[i][f]
            F0[i] = f
        elif matrix[i][f] < D1[i]:
            D1[i] = matrix[i][f]
            F1[i] = f
        if D0[i] > Sc:
            Sc = D0[i]
    return Sc

# Remove facility to current solution
def removeFacility(f, current_sol):
    global F0
    global F1
    global D0
    global D1
    Sc = 0
    for i in range(0, n):
        if F0[i] == f:
            D0[i] = D1[i]
            F0[i] = F1[i]
            findNext(i, current_sol)
        elif F1[i] == f:
            findNext(i, current_sol)
        if D0[i] > Sc:
            Sc = D0[i]
    return Sc

# Find Next function
def findNext(f, current_sol):
    min_dist = float("inf")
    global D1
    global F1
    for i in range(0, k):
        if current_sol[i] != F0[f]:
            if matrix[current_sol[i]][f] < min_dist:
                F1[f] = current_sol[i]
                min_dist = matrix[current_sol[i]][f]
                D1[f] = min_dist

# Clean M array
def cleanMarray():
    global M
    M = []
    for i in range(0, n):
        M.append(0)


# Critical Interchange heuristic
def interchange(in_sol, bks, current_size):
    cardinality()
    current_sol = []
    global F0
    global F1
    global D0
    global D1
    global M
    global card
    global best_known_size
    best_size = current_size
    tabu_list = []
    list = []
    for i in range(0, n):
        list.append(False)
    for i in range(0, n):
        tabu_list.append(list)
    for i in range(0, k):
        current_sol.append(in_sol[i])
    while current_size < best_size:
        L = []
        # The critical node is also the farthest node
        current_sol_boolean = getCurrentBoolean(current_sol)
        firstAndSecond(current_sol)
        C = float("inf")
        for j in range(0, n):
            Sc = addFacility(j)
            if j > 0:
                current_sol_boolean[j-1] = False # Erase the previous added facility
            current_sol_boolean[j] = True # Check with true the new added facility
            cleanMarray()
            for m in range(0, n):
                if card[m] > 1:
                    if matrix[j][m] <= D1[m]:
                        if matrix[j][m] > M[F0[m]]:
                            M[F0[m]] = matrix[j][m]
                    elif D1[m] > M[F0[m]]:
                        M[F0[m]] = D1[m]
                    if Sc > M[F0[m]]:
                        M[F0[m]] = Sc
                else:
                    M[F0[m]] = float("inf")
            for m in range(0, k):
                if M[current_sol[m]] == 0:
                    M[current_sol[m]] = current_size
                if not tabu_list[current_sol[m]][j] or \
                        not tabu_list[j][current_sol[m]] or M[current_sol[m]] < best_size:
                    if M[current_sol[m]] == C:
                        L.append([current_sol[m], j])
                    elif M[current_sol[m]] < C:
                        L = []
                        L.append([current_sol[m], j])
                        C = M[current_sol[m]]
            Sc = removeFacility(j, current_sol)
        if len(L) == 0:
            tabu_list = []
            list = []
            for i in range(0, n):
                list.append(False)
            for i in range(0, n):
                tabu_list.append(list)
        else:
            selection = L[random.randint(0, len(L)-1)]
            tabu_list[selection[0]][selection[1]] = True
            tabu_list[selection[1]][selection[0]] = True
            for j in range(0, k):
                if current_sol[j] == selection[0]:
                    current_sol[j] = selection[1]
            current_size = C
        if current_size < best_size:
            best_size = current_size
        if best_size < best_known_size:
            best_known_size = best_size
            #print(best_known_size)
            cardinality()
        if best_known_size <= target[v-1]:
            break
    return best_known_size


    # Critical Interchange heuristic
def critical_interchange(in_sol, bks, current_size):
    cardinality()
    #rep = 2*n
    rep = math.floor(random.random() * 4 * n)
    current_sol = []
    global F0
    global F1
    global D0
    global D1
    global M
    global card
    global best_known_size
    best_size = current_size
    tabu_list = []
    list = []
    for i in range(0, n):
        list.append(False)
    for i in range(0, n):
        tabu_list.append(list)
    for i in range(0, k):
        current_sol.append(in_sol[i])
    for i in range(0, rep):
        L = []
        # The critical node is also the farthest node
        current_sol_boolean = getCurrentBoolean(current_sol)
        critical_neighbors = get_critical_neighbors(criticalNode(current_sol), bks)
        firstAndSecond(current_sol)
        C = float("inf")
        for j in range(0, len(critical_neighbors)):
            Sc = addFacility(critical_neighbors[j])
            if j > 0:
                current_sol_boolean[critical_neighbors[j-1]] = False # Erase the previous added facility
            current_sol_boolean[critical_neighbors[j]] = True # Check with true the new added facility
            cleanMarray()
            for m in range(0, n):
                if card[m] > 1:
                    if matrix[critical_neighbors[j]][m] <= D1[m]:
                        if matrix[critical_neighbors[j]][m] > M[F0[m]]:
                            M[F0[m]] = matrix[critical_neighbors[j]][m]
                    elif D1[m] > M[F0[m]]:
                        M[F0[m]] = D1[m]
                    if Sc > M[F0[m]]:
                        M[F0[m]] = Sc
                else:
                    M[F0[m]] = float("inf")
            for m in range(0, k):
                if M[current_sol[m]] == 0:
                    M[current_sol[m]] = current_size
                if not tabu_list[current_sol[m]][critical_neighbors[j]] or \
                        not tabu_list[critical_neighbors[j]][current_sol[m]] or M[current_sol[m]] < best_size:
                    if M[current_sol[m]] == C:
                        L.append([current_sol[m], critical_neighbors[j]])
                    elif M[current_sol[m]] < C:
                        L = []
                        L.append([current_sol[m], critical_neighbors[j]])
                        C = M[current_sol[m]]
            Sc = removeFacility(critical_neighbors[j], current_sol)
        if len(L) == 0:
            tabu_list = []
            list = []
            for i in range(0, n):
                list.append(False)
            for i in range(0, n):
                tabu_list.append(list)
        else:
            selection = L[random.randint(0, len(L)-1)]
            tabu_list[selection[0]][selection[1]] = True
            tabu_list[selection[1]][selection[0]] = True
            for j in range(0, k):
                if current_sol[j] == selection[0]:
                    current_sol[j] = selection[1]
            current_size = C
        if current_size < best_size:
            best_size = current_size
        if best_size < best_known_size:
            best_known_size = best_size
            #print(best_known_size)
            cardinality()
        if best_known_size <= target[v-1]:
            break
    return best_known_size


    # Critical Interchange heuristic
def critical_interchange2(in_sol, bks, current_size, guide_sol):
    cardinality()
    #rep = 2*n
    rep = math.floor(random.random() * 4 * n)
    current_sol = []
    global F0
    global F1
    global D0
    global D1
    global M
    global card
    global best_known_size
    best_size = current_size
    tabu_list = []
    list = []
    for i in range(0, n):
        list.append(False)
    for i in range(0, n):
        tabu_list.append(list)
    for i in range(0, k):
        current_sol.append(in_sol[i])
    for i in range(0, rep):
        L = []
        # The critical node is also the farthest node
        current_sol_boolean = getCurrentBoolean(current_sol)
        critical_neighbors = get_critical_neighbors(criticalNode(current_sol), bks)
        critical_neighbors = reduced_critical_neighbors(critical_neighbors, farthest_node_in_guide_sol(guide_sol), bks)
        firstAndSecond(current_sol)
        C = float("inf")
        for j in range(0, len(critical_neighbors)):
            Sc = addFacility(critical_neighbors[j])
            if j > 0:
                current_sol_boolean[critical_neighbors[j-1]] = False # Erase the previous added facility
            current_sol_boolean[critical_neighbors[j]] = True # Check with true the new added facility
            cleanMarray()
            for m in range(0, n):
                if card[m] > 1:
                    if matrix[critical_neighbors[j]][m] <= D1[m]:
                        if matrix[critical_neighbors[j]][m] > M[F0[m]]:
                            M[F0[m]] = matrix[critical_neighbors[j]][m]
                    elif D1[m] > M[F0[m]]:
                        M[F0[m]] = D1[m]
                    if Sc > M[F0[m]]:
                        M[F0[m]] = Sc
                else:
                    M[F0[m]] = float("inf")
            for m in range(0, k):
                if M[current_sol[m]] == 0:
                    M[current_sol[m]] = current_size
                if not tabu_list[current_sol[m]][critical_neighbors[j]] or \
                        not tabu_list[critical_neighbors[j]][current_sol[m]] or M[current_sol[m]] < best_size:
                    if M[current_sol[m]] == C:
                        L.append([current_sol[m], critical_neighbors[j]])
                    elif M[current_sol[m]] < C:
                        L = []
                        L.append([current_sol[m], critical_neighbors[j]])
                        C = M[current_sol[m]]
            Sc = removeFacility(critical_neighbors[j], current_sol)
        if len(L) == 0:
            tabu_list = []
            list = []
            for i in range(0, n):
                list.append(False)
            for i in range(0, n):
                tabu_list.append(list)
        else:
            selection = L[random.randint(0, len(L)-1)]
            tabu_list[selection[0]][selection[1]] = True
            tabu_list[selection[1]][selection[0]] = True
            for j in range(0, k):
                if current_sol[j] == selection[0]:
                    current_sol[j] = selection[1]
            current_size = C
        if current_size < best_size:
            best_size = current_size
        if best_size < best_known_size:
            best_known_size = best_size
            #print(best_known_size)
            cardinality()
        if best_known_size <= target[v-1]:
            break
    return best_known_size


    # Get First closest centers
def assignedCenter(in_sol):
    global F0
    F0 = []
    for i in range(0, n):
        F0.append(0)
        D0.append(0)
    for i in range(0, n):
        min_dist = float("inf")
        for j in range(0, k):
            if matrix[i][in_sol[j]] < min_dist:
                min_dist = matrix[i][in_sol[j]]
                F0[i] = in_sol[j]
                D0[i] = min_dist
        min_dist = float("inf")

# fix_dominating_set function
def fix_dominating_set(in_sol, bks, current_size):
    print("Start local search")
    rep = 10
    current_sol = []
    global F0
    global D0
    global card
    global distance
    global best_known_size
    distance_centers = []
    for i in range(0, n):
        distance_centers.append(float("inf"))
    for i in range(0,n):
        dominated.append(False)
        distance.append(float("inf"))
    best_size = current_size
    for i in range(0, k):
        current_sol.append(in_sol[i])

    for w in range(0, rep):
        cardinality()
        current_sol_boolean = getCurrentBoolean(current_sol)
        new_sol = []
        new_sol_boolean = getCurrentBoolean(new_sol)
        assignedCenter(current_sol)

        # Get the first center
        farthest_node = criticalNode(current_sol)
        nearest_center = F0[farthest_node]
        list = []
        for i in range(0, n):
            if matrix[i][nearest_center] < best_known_size and matrix[i][farthest_node] < best_known_size:
                list.append(i)
        max_card = 0
        max_card_element = 0
        for i in range(0, len(list)):
            if card[list[i]] > max_card:
                max_card = card[list[i]]
                max_card_element = list[i]
        if random.random() < 1:
            new_sol.append(max_card_element)
            new_sol_boolean[max_card_element] = True
        else:
            r = random.randint(0, len(list)-1)
            new_sol.append(list[r])
            new_sol_boolean[list[r]] = True
        current_sol_boolean[nearest_center] = False
        for i in range(0, k):
            if current_sol_boolean[current_sol[i]]:
                if matrix[current_sol[i]][max_card_element] < distance_centers[current_sol[i]]:
                    distance_centers[current_sol[i]] = matrix[current_sol[i]][max_card_element]

        # Restart the distance from every node to the new partial solution
        distance = []
        for i in range(0, n):
            distance.append(float("inf"))
        for i in range(0, n):
            if matrix[i][new_sol[0]] < distance[i]:
                distance[i] = matrix[i][new_sol[0]]

        # Get the next centers
        for i in range(1, k):
            update_cardinality(new_sol, i)
            nearest_center = 0
            min_dist = float("inf")
            list = []
            for j in range(0, k):
                if current_sol_boolean[current_sol[j]]:
                    if distance_centers[current_sol[j]] < min_dist:
                        min_dist = distance_centers[current_sol[j]]
                        nearest_center = current_sol[i]
            for j in range(0, n):
                if matrix[j][nearest_center] < best_known_size:
                    list.append(j)
            max_card = 0
            max_card_element = 0
            for j in range(0, len(list)):
                if card[list[j]] > max_card:
                    max_card = card[list[j]]
                    max_card_element = list[j]
            if random.random() < 1:
                new_sol.append(max_card_element)
                new_sol_boolean[max_card_element] = True
            else:
                r = random.randint(0, len(list)-1)
                new_sol.append(list[r])
                new_sol_boolean[list[r]] = True
            current_sol_boolean[nearest_center] = False
            #update_distance(new_sol, i)
            for j in range(0, n):
                if matrix[j][new_sol[i]] < distance[j]:
                    distance[j] = matrix[j][new_sol[i]]

        current_size = solution_size()

        for j in range(0, k):
            current_sol[j] = new_sol[j]

        if current_size < best_size:
            best_size = current_size
        if best_size < best_known_size:
            best_known_size = best_size
            cardinality()
        if best_known_size <= target[v-1]:
            break
        print(repr(current_size))
    print("End of local search")
    return best_known_size


# Orders the set of edges' cost
def heap_sort(items):
    """ Implementation of heap sort """
    heapq.heapify(items)
    items[:] = [heapq.heappop(items) for i in range(len(items))]
    return items

# Check if a 2-approximated solution is a dominating set in G^2
def gonDomSqrGraph(s):
    checked = []
    dom = []
    for i in range(0, n):
        checked.append(False)
        dom.append(False)
    dom_cnt = 0
    for i in gon_sol:
        for j in range(0, n):
            if not checked[j]:
                if matrix[i][j] <= s:
                    for q in range(0, n):
                        if matrix[j][q] <= s:
                            dom[q] = True
                checked[j] = True
    for i in range(0, n):
        if dom[i]:
            dom_cnt = dom_cnt + 1
    if dom_cnt == n:
        return True
    else:
        return False

# This function generates a 2-approximated solution with the Gon algorithm
def gon():
    C = []
    global distance
    distance = []
    for i in range(0,n):
        distance.append(float("inf"))
    f = random.randint(0, n-1)
    C.append(f)
    update_distance(C, 0)
    for i in range(1, k):
        f = farthest_node()
        C.append(f)
        update_distance(C, i)
    size = solution_size()
    out = [size, C]
    return out

# Check if a 2-approximated solution is a dominating set in G_2W
def gonDom2W(s):
    checked = []
    dom_cnt = 0
    for i in range(0, n):
        checked.append(False)
    for i in range(0, n):
        if not checked:
            for j in gon_sol:
                if matrix[i][j] <= 2*s:
                    checked[i] = True
                    dom_cnt = dom_cnt + 1
    if dom_cnt == n:
        return True
    else:
        return False

def loadInstance(instance):
    global n, m , k, matrix, ordered_sizes
    cwd = os.getcwd()
    path = os.path.abspath(cwd + '/Lib/' + instance + '.txt')
    #f = open(cwd + '/Lib/' + instance + '.txt', 'r')
    f = open(path, 'r')
    # Setting up the instance (BEGIN)***************************************************************
    #print("begin Instance set up")
    # Get the values of n, m and k
    str = f.readline()
    str = str.split()
    n = int(str[0])
    m = int(str[1])
    k = int(str[2])
    # Fill the Adjacencies Matrix
    matrix = []
    for i in range(0,n):
        list = []
        for j in range(0,n):
            list.append(float("inf"))
        matrix.append(list)
    for i in range(0, m):
        str = f.readline()
        str = str.split()
        v1 = int(str[0]) - 1
        v2 = int(str[1]) - 1
        weight = float(str[2])
        matrix[v1][v2] = weight
        matrix[v2][v1] = weight
    # Apply the Floyd-Marshal algorithm
    if instance[0:4] == "pmed":
        for i in range(0, n):
            matrix[i][i] = 0
        for i in range(0, n):
            for j in range(0, n):
                for l in range(0, n):
                    if matrix[i][j] == float("inf") or matrix[i][l] == float("inf"):
                        cost = float("inf")
                    else:
                        cost = matrix[i][j] + matrix[i][l]
                    if cost < matrix[j][l]:
                        matrix[j][l] = cost
    f.close()
    # Order the set of possible solutions' size
    ordered_sizes = []
    for i in range(0, n):
        for j in range(i, n):
            ordered_sizes.append(matrix[i][j])
    ordered_sizes = heap_sort(ordered_sizes)
    # Setting up the instance (END)***************************************************************
    #print("end Instance set up")

def run(algorithm, library, seed, repetitions, outputfile):
    global f, k
    f = open(outputfile, 'w')
    if algorithm == 'CDS_h' or algorithm == 'CDS+_h ' or algorithm == 'CDS_app' or algorithm == 'CDS+_app':
        f.write("best found size " + "   " + "last w(e_{mid})" + '\n')
    if library == 'ORLib':
        for i in range(1, 41): # 1 to 40
            loadInstance('pmed' + repr(i))
            if algorithm == 'CDS_app':
                CDS(seed, repetitions, "app")
            elif algorithm == 'CDS+_app':
                CDSP(seed, repetitions, "app")
            elif algorithm == 'CDS_h':
                CDS(seed, repetitions, "h")
            elif algorithm == 'CDS+_h':
                CDSP(seed, repetitions, "h")
            elif algorithm == 'CDS_gon':
                CDS(seed, repetitions, "gon")
            elif algorithm == 'CDS+_gon':
                CDSP(seed, repetitions, "gon")
            elif algorithm == 'CDS_n4':
                CDS_n4(seed, repetitions)
            elif algorithm == 'Gon':
                Gon(seed, repetitions)
            elif algorithm == 'Gon+':
                GonP(seed, repetitions)
            elif algorithm == 'Gr':
                Gr(seed, repetitions)
            elif algorithm == 'Gr+':
                GrP(seed, repetitions)
            elif algorithm == 'Scr':
                Scr()
            elif algorithm == "HS":
                HS(seed, repetitions)
    elif library == 'smallTSPLib':
        for i in range(0, 40): # 0 to 39
            if i == 0:
                loadInstance('kroA200')
            elif i == 4:
                loadInstance('gr202')
            elif i == 8:
                loadInstance('pr226')
            elif i == 12:
                loadInstance('pr264')
            elif i == 16:
                loadInstance('pr299')
            elif i == 20:
                loadInstance('lin318')
            elif i == 24:
                loadInstance('pr439')
            elif i == 28:
                loadInstance('pcb442')
            elif i == 32:
                loadInstance('d493')
            elif i == 36:
                loadInstance('d657')
            if i % 4 == 0:
                k = 5
            elif i % 4 == 1:
                k = 10
            elif i % 4 == 2:
                k = 20
            elif i % 4 == 3:
                k = 40
            if algorithm == 'CDS_app':
                CDS(seed, repetitions, "app")
            elif algorithm == 'CDS+_app':
                CDSP(seed, repetitions, "app")
            elif algorithm == 'CDS_h':
                CDS(seed, repetitions, "h")
            elif algorithm == 'CDS+_h':
                CDSP(seed, repetitions, "h")
            elif algorithm == 'CDS_gon':
                CDS(seed, repetitions, "gon")
            elif algorithm == 'CDS+_gon':
                CDSP(seed, repetitions, "gon")
            elif algorithm == 'CDS_n4':
                CDS_n4(seed, repetitions)
            elif algorithm == 'Gon':
                Gon(seed, repetitions)
            elif algorithm == 'Gon+':
                GonP(seed, repetitions)
            elif algorithm == 'Gr':
                Gr(seed, repetitions)
            elif algorithm == 'Gr+':
                GrP(seed, repetitions)
            elif algorithm == 'Scr':
                Scr()
            elif algorithm == "HS":
                HS(seed, repetitions)
    elif library == 'u1060' or library == 'u1817':
        for i in range(1, 16): # 1 to 15
            if i == 1:
                loadInstance(library)
            k = i * 10
            if algorithm == 'CDS_app':
                CDS(seed, repetitions, "app")
            elif algorithm == 'CDS+_app':
                CDSP(seed, repetitions, "app")
            elif algorithm == 'CDS_h':
                CDS(seed, repetitions, "h")
            elif algorithm == 'CDS+_h':
                CDSP(seed, repetitions, "h")
            elif algorithm == 'CDS_gon':
                CDS(seed, repetitions, "gon")
            elif algorithm == 'CDS+_gon':
                CDSP(seed, repetitions, "gon")
            elif algorithm == 'Gon':
                Gon(seed, repetitions)
            elif algorithm == 'Gon+':
                GonP(seed, repetitions)
            elif algorithm == 'Gr':
                Gr(seed, repetitions)
            elif algorithm == 'Gr+':
                GrP(seed, repetitions)
            elif algorithm == 'Scr':
                Scr()
            elif algorithm == "HS":
                HS(seed, repetitions)
    elif library == 'pcb3038':
        for i in range(1, 15): # 1 to 14
            if i == 1:
                loadInstance(library)
            if i <= 5:
                k = i * 10
            else:
                k = 100 + ((i - 6) * 50)
            if algorithm == 'CDS_app':
                CDS(seed, repetitions, "app")
            elif algorithm == 'CDS+_app':
                CDSP(seed, repetitions, "app")
            elif algorithm == 'CDS_h':
                CDS(seed, repetitions, "h")
            elif algorithm == 'CDS+_h':
                CDSP(seed, repetitions, "h")
            elif algorithm == 'CDS_gon':
                CDS(seed, repetitions, "gon")
            elif algorithm == 'CDS+_gon':
                CDSP(seed, repetitions, "gon")
            elif algorithm == 'Gon':
                Gon(seed, repetitions)
            elif algorithm == 'Gon+':
                GonP(seed, repetitions)
            elif algorithm == 'Gr':
                Gr(seed, repetitions)
            elif algorithm == 'Gr+':
                GrP(seed, repetitions)
            elif algorithm == 'Scr':
                Scr()
            elif algorithm == "HS":
                HS(seed, repetitions)
    f.close()
################################ BEGINNING OF THE CODE ################################################################


def CDS(seed, repetitions, version):
    global prob, best_known_size, distance, f, C, gon_sol, n, m, k, ordered_sizes, card
    list = gon()
    gon_sol = list[1]
    gon_sol_size = list[0]
    seed = int(seed)
    repetitions = int(repetitions)
    upper = 0
    lower = 0
    mid = 0
    for h in range(seed, seed + repetitions):
        prob = 1
        #best_known_size = float("inf")
        best_known_size = list[0]
        distance = []
        random.seed(h)
        # Initializing the binary search
        upper = len(ordered_sizes) - 1
        lower = 0
        #mid = math.floor(lower + ((upper - lower)/2))
        mid = math.ceil(lower + ((upper - lower)/2))
        not_done = True
        while not_done:
            # Computing the mid value
            mid = math.ceil(lower + ((upper - lower)/2))
            mid_value = ordered_sizes[int(mid)]
            #print("mid_value: " + repr(mid_value))
            # Computing the cardinality of every vertex over the pruned input graph
            cardinality_size(mid_value)
            # Executing the Critical Dominating Set algorithm
            ds = dominating_set_1(ordered_sizes[int(mid)])
            size = ds[0]
            # If the new solution is better than the previous best one, substitute them
            if size <= best_known_size:
                C = ds[1]
                best_sol = []
                for i in range(0, k):
                    best_sol.append(ds[1][i])
            if size <= best_known_size:
                best_known_size = size
            # This condition is met when the binary search finishes
            if mid == upper:
                not_done = False
            # Determine where to move on the binary search
### Heuristic option ##########################
            if version == "h":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                    lower = mid
### 3-approximated option ##########################
            elif version == "app":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                    if size > 3 * mid_value:
                        lower = mid
                    else:
                        upper = mid
### 2-approximated option ##########################
            elif version == "gon":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                #if not gonDom2W(mid_value):
                    if 2 * mid_value < gon_sol_size:
                        lower = mid
                    else:
                        upper = mid
        #Print the best size found
        #print(repr(best_known_size) + "   " + repr(mid_value))
        print(repr(best_known_size))
        #f.write(repr(best_known_size) + "   " + repr(mid_value) + '\n')
        f.write(repr(best_known_size) + '\n')

def CDSP(seed, repetitions, version):
    global prob, best_known_size, distance, f, C, gon_sol, n, m, k, ordered_sizes, card
    list = gon()
    gon_sol = list[1]
    gon_sol_size = list[0]
    seed = int(seed)
    repetitions = int(repetitions)
    upper = 0
    lower = 0
    mid = 0
    for h in range(seed, seed + repetitions):
        prob = 1
        best_known_size = list[0]
        #best_known_size = float("inf")
        distance = []
        random.seed(h)
        # Initializing the binary search
        upper = len(ordered_sizes) - 1
        lower = 0
        #mid = math.floor(lower + ((upper - lower)/2))
        mid = math.ceil(lower + ((upper - lower)/2))
        not_done = True
        while not_done:
            # Computing the mid value
            mid = math.ceil(lower + ((upper - lower)/2))
            mid_value = ordered_sizes[int(mid)]
            for m in range(0, n):
                # Computing the cardinality of every vertex over the pruned input graph
                cardinality_size(mid_value)
                # Executing the Critical Dominating Set algorithm n times
                ds = dominating_set_2(ordered_sizes[int(mid)], m)
                size = ds[0]
                # If the new solution is better than the previous best one, substitute them
                if size <= best_known_size:
                    C = ds[1]
                if size <= best_known_size:
                    best_known_size = size
            # If the new solution is better than the previous best one, substitute them
            if size <= best_known_size:
                C = ds[1]
                best_sol = []
                for i in range(0, k):
                    best_sol.append(ds[1][i])
            if size <= best_known_size:
                best_known_size = size
            # This condition is met when the binary search finishes
            if mid == upper:
                not_done = False
            # Determine where to move on the binary search
### Heuristic option ##########################
            if version == "h":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                    lower = mid
### 3-approximated option ##########################
            elif version == "app":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                    if size > 3 * mid_value:
                        lower = mid
                    else:
                        upper = mid
### 2-approximated option ##########################
            elif version == "gon":
                if best_known_size <= mid_value:
                    upper = mid
                else:
                #if not gonDom2W(mid_value):
                    if 2 * mid_value < gon_sol_size:
                        lower = mid
                    else:
                        upper = mid
                #if not gonDom2W(mid_value):
                #    lower = mid
                #else:
                #    upper = mid
        #Print the best size found
        #print(repr(best_known_size) + "   " + repr(mid_value))
        print(repr(best_known_size))
        #f.write(repr(best_known_size) + "   " + repr(mid_value) + '\n')
        f.write(repr(best_known_size) + '\n')

def CDS_n4(seed, repetitions):
    global prob, best_known_size, distance, f, C, gon_sol, n, m, k, ordered_sizes, card
    seed = int(seed)
    repetitions = int(repetitions)
    for h in range(seed, seed + repetitions):
        prob = 1
        best_known_size = float("inf")
        #best_known_size = list[0]
        distance = []
        random.seed(h)
        for r in ordered_sizes:
        #while not_done:
            # Computing the cardinality of every vertex over the pruned input graph
            cardinality_size(r)
            # Executing the Critical Dominating Set algorithm
            ds = dominating_set_1(r)
            size = ds[0]
            # If the new solution is better than the previous best one, substitute them
            if size <= best_known_size:
                C = ds[1]
                best_sol = []
                for i in range(0, k):
                    best_sol.append(ds[1][i])
            if size <= best_known_size:
                best_known_size = size
        #Print the best size found
        print(repr(best_known_size))
        f.write(repr(best_known_size) + '\n')

def HS(seed, repetitions):
    global prob, best_known_size, distance, f, C, n, m, k, ordered_sizes, card
    seed = int(seed)
    repetitions = int(repetitions)
    upper = 0
    lower = 0
    mid = 0
    for h in range(seed, seed + repetitions):
        prob = 1
        best_known_size = float("inf")
        distance = []
        random.seed(h)
        # Initializing the binary search
        upper = len(ordered_sizes) - 1
        lower = 0
        #mid = math.floor(lower + ((upper - lower)/2))
        mid = math.ceil(lower + ((upper - lower)/2))
        not_done = True
        while not_done:
            # Computing the mid value
            mid = math.ceil(lower + ((upper - lower)/2))
            mid_value = ordered_sizes[int(mid)]
            # Executing the Critical Dominating Set algorithm
            ds = hs_algorithm(ordered_sizes[int(mid)])
            # This condition is met when the binary search finishes
            if mid == upper:
                not_done = False
            if len(ds[1]) <= k:
                size = ds[0]
                # If the new solution is better than the previous best one, substitute them
                if size <= best_known_size:
                    C = ds[1]
                if size <= best_known_size:
                    best_known_size = size
                upper = mid
            else:
                lower = mid
                #if not gonDom2W(mid_value):
                #    lower = mid
                #else:
                #    upper = mid
        #Print the best size found
        print(best_known_size)
        f.write(repr(best_known_size) + '\n')


def Scr():
    global best_known_size, f, n, k, ordered_sizes, card
    best_known_size = float("inf")
    for b in range(0, len(ordered_sizes)):
        CovCnt = []
        Score = []
        D = []
        cardinality_size(ordered_sizes[b])
        for i in range(0, n):
            CovCnt.append(card[i])
            Score.append(card[i])
        for i in range(0, n):
            min_score = float("inf")
            node_min_score = 0
            for j in range(0, n):
                if Score[j] < min_score:
                    min_score = Score[j]
                    node_min_score = j
            x_exists = False
            for j in range(0, n):
                if matrix[node_min_score][j] <= ordered_sizes[b]:
                    if CovCnt[j] == 1:
                        x_exists = True
            if x_exists:
                D.append(node_min_score)
                for j in range(0, n):
                    if matrix[node_min_score][j] <= ordered_sizes[b]:
                        CovCnt[j] = 0
            else:
                for j in range(0, n):
                    if matrix[node_min_score][j] <= ordered_sizes[b]:
                        if CovCnt[j] > 0:
                            CovCnt[j] = CovCnt[j] - 1
                            Score[j] = Score[j] + 1
            Score[node_min_score] = float("inf")
        if len(D) <= k:
            scr_size = scrSize(D)
            if scr_size <= best_known_size:
                best_known_size = scr_size
    print(best_known_size)
    f.write(repr(best_known_size) + '\n')

def scrSize(sol):
    max_dist = 0
    for i in range(0, n):
        min_dist = float("inf")
        for j in range(0, len(sol)):
            if matrix[i][sol[j]] <= min_dist:
                min_dist = matrix[i][sol[j]]
        if min_dist > max_dist:
            max_dist = min_dist
    return max_dist


def Gon(seed, repetitions):
    global best_known_size, distance, f, C, n, k
    seed = int(seed)
    repetitions = int(repetitions)
    for h in range(seed, seed + repetitions):
        best_known_size = float("inf")
        distance = []
        random.seed(h)
        C = []
        C.append(random.randint(0, n-1))
        for i in range(0, n):
            distance.append(float("inf"))
        for i in range(0, n):
            if matrix[i][C[0]] < distance[i]:
                distance[i] = matrix[i][C[0]]
        for i in range(1, k):
            max_dist = 0
            max_dist_node = 0
            for j in range(0, n):
                if distance[j] > max_dist:
                    max_dist = distance[j]
                    max_dist_node = j
            C.append(max_dist_node)
            for j in range(0, n):
                if matrix[j][C[i]] < distance[j]:
                    distance[j] = matrix[j][C[i]]
        max_dist = 0
        for i in range(0, n):
            if distance[i] > max_dist:
                max_dist = distance[i]
        print(max_dist)
        f.write(repr(max_dist) + '\n')

def GonP(seed, repetitions):
    global best_known_size, distance, f, C, n, k
    seed = int(seed)
    repetitions = int(repetitions)
    for h in range(seed, seed + repetitions):
        best_known_size = float("inf")
        for b in range(0, n):
            distance = []
            random.seed(h)
            C = []
            C.append(b)
            for i in range(0, n):
                distance.append(float("inf"))
            for i in range(0, n):
                if matrix[i][C[0]] < distance[i]:
                    distance[i] = matrix[i][C[0]]
            for i in range(1, k):
                max_dist = 0
                max_dist_node = 0
                for j in range(0, n):
                    if distance[j] > max_dist:
                        max_dist = distance[j]
                        max_dist_node = j
                C.append(max_dist_node)
                for j in range(0, n):
                    if matrix[j][C[i]] < distance[j]:
                        distance[j] = matrix[j][C[i]]
            max_dist = 0
            for i in range(0, n):
                if distance[i] > max_dist:
                    max_dist = distance[i]
            #print(max_dist)
            if max_dist < best_known_size:
                best_known_size = max_dist
        print(best_known_size)
        f.write(repr(best_known_size) + '\n')

def Gr(seed, repetitions):
    global best_known_size, distance, f, C, n, k
    seed = int(seed)
    repetitions = int(repetitions)
    for h in range(seed, seed + repetitions):
        distance = []
        for i in range(0, n):
            distance.append(float("inf"))
        random.seed(h)
        C = []
        for m in range(0, k):
            min_dist = float("inf")
            for i in range(0, n):
                max_dist = 0
                for j in range(0, n):
                    if matrix[i][j] < distance[j]:
                        if matrix[i][j] > max_dist:
                            max_dist = matrix[i][j]
                    else:
                        if distance[j] > max_dist:
                            max_dist = distance[j]
                if max_dist < min_dist:
                    min_dist = max_dist
                    c = i
            if m == 0:
                C.append(random.randint(0, n-1))
            else:
                C.append(c)
            for i in range(0, n):
                if matrix[i][C[m]] < distance[i]:
                    distance[i] = matrix[i][C[m]]
        max_dist = 0
        for m in range(0, n):
            if distance[m] > max_dist:
                max_dist = distance[m]
        print(max_dist)
        f.write(repr(max_dist) + '\n')

def GrP(seed, repetitions):
    global best_known_size, distance, f, C, n, k
    seed = int(seed)
    repetitions = int(repetitions)
    for h in range(seed, seed + repetitions):
        best_known_size = float("inf")
        for b in range(0, n):
            C = []
            distance = []
            for i in range(0, n):
                distance.append(float("inf"))
            random.seed(h)
            for m in range(0, k):
                min_dist = float("inf")
                for i in range(0, n):
                    max_dist = 0
                    for j in range(0, n):
                        if matrix[i][j] < distance[j]:
                            if matrix[i][j] > max_dist:
                                max_dist = matrix[i][j]
                        else:
                            if distance[j] > max_dist:
                                max_dist = distance[j]
                    if max_dist < min_dist:
                        min_dist = max_dist
                        c = i
                if m == 0:
                    C.append(b)
                else:
                    C.append(c)
                for i in range(0, n):
                    if matrix[i][C[m]] < distance[i]:
                        distance[i] = matrix[i][C[m]]
            max_dist = 0
            for m in range(0, n):
                if distance[m] > max_dist:
                    max_dist = distance[m]
            if max_dist < best_known_size:
                best_known_size = max_dist
            #print(max_dist)
        print(best_known_size)
        f.write(repr(best_known_size) + '\n')


def checkArguments(alg, lib, seed, rep, out):
    if alg != "CDS_h" and alg != 'CDS+_h' and alg != 'Gon' and alg != 'Gon+' and alg != 'HS' and alg != 'Scr' and alg != 'Gr' \
        and alg != 'Gr+' and alg != "CDS_app" and alg != 'CDS+_app' and alg != "CDS_gon" and alg != 'CDS+_gon' and alg != 'CDS_n4':
        return False
    if lib != 'ORLib' and lib != 'smallTSPLib' and lib != 'u1060' and lib != 'u1817' and lib != 'pcb3038':
        return False
    try:
        value = int(seed)
        value = int(rep)
    except ValueError:
        return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print ("Wrong number of arguments")
        print ("{algorithm(CDS_h,CDS_app,CDS+_h,CDS+_app,CDS_n4,Gon,Gon+,Gr,Gr+,HS,Scr} {library(ORLib,smallTSPLib,u1060,u1817,pcb3038} {seed} {repetitionsByInstance} " \
              "{outputFile}")
        sys.exit()
    algorithm = sys.argv[1]
    library = sys.argv[2]
    seed = sys.argv[3]
    repetitions = sys.argv[4]
    outputfile = sys.argv[5]
    # global variables
    n = 0
    m = 0
    k = 0
    matrix = []
    ordered_sizes = []
    best_known_size = float("inf")
    distance = []
    f = 0
    C = []
    gon_sol = []
    card = []
    # Run the algorithm
    if checkArguments(algorithm, library, seed, repetitions, outputfile):
        run(algorithm, library, seed, repetitions, outputfile)
    else:
        print("Check the arguments")
