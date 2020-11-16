import datetime
import math
import pickle
import random
import sys
from copy import deepcopy

import networkx as nx
import numpy as np
import statsmodels.api as statModels
from scipy import stats
from sklearn import linear_model
from linetimer import CodeTimer


ALLOWABLE_EMBEDDING_DISTANCE_ERROR = 0.00001 #often the cap on the number of dimensions will be reached before this
print("ALLOWABLE_EMBEDDING_DISTANCE_ERROR = ",ALLOWABLE_EMBEDDING_DISTANCE_ERROR)
RATIO_NUM_NON_PIVOTS = 0.0
print("currently RATIO_NUM_NON_PIVOTS = ",RATIO_NUM_NON_PIVOTS)

EPSILON_PATH_LEN_DIFFERENCE = 1.0
MULTIPLE_OF_PIVOT_SET_FOR_NUM_NON_PIVOTS = 1
USE_WEIGHTED_LEAST_SQUARES = False
PIVOTS_ONLY_CONSTRAINT_WEIGHT = 1.0
SINGLE_PIVOTS_ONLY_CONSTRAINT_WEIGHT = 1.0 #ONLY VALID if USE_WEIGHTED_LEAST_SQUARES = True
NO_PIVOTS_CONSTRAINT_WEIGHT = 1.0
MIN_ADDITIONAL_NODES = 10

TRUE_AVG_DIST_IN_POT_FUNC = False
#NOTE so this is an interesting switch to try. When true, the pot function is
# just about learning the true difference between average and directed distance. In this
# the error from average distance is not carried over to be compensated in the pot func.
# In some cases, this works well, when average embedding is mediocre and only makes the
# pot func more convoluted. In some cases it is better to have the pot func correct errors.
# NOTE: for well structured graphs, with clusters, hierarchy, and clear pivot points, I think using true avg dist helps.


#========================================================================
def nCr(n,r):
    """
    :summary: Taken from https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
    :param n:
    :param r:
    :return:
    """
    f = math.factorial
    return f(n) / f(r) / f(n-r)

#========================================================================

def get_poly_terms(num_terms,poly_degree):
    """

    :param num_terms:
    :param poly_degree:
    :param bias: This was added to compute the result for models other than the WLS model from stats library.
    :return:
    """
    terms = []
    term_options_stack = []
    for _ in range(poly_degree): # cannot do [x]*poly_degree. For whatever reason, that links the elements together
        term_options_stack.append(list(range(num_terms)))
    current_term = [-1]*poly_degree #-1 is a place holder, will be replaced by 0,1,2...poly_degree-1, representing each of the terms
    current_degree = poly_degree-1
    #---quick function for local use
    def check_cases_left_in_stack(stack):
        for single_term_cases in stack:
            if len(single_term_cases) > 0:
                return True
        return False
    #---end local function num_cases_in_stack
    while check_cases_left_in_stack(term_options_stack):
        if len(term_options_stack[current_degree]) == 0:
            #this will only happen for stacks other than the highest degree. If it was the highest degree stack, we would
            #have exited the while loop
            #Refill the stack and go back up a level
            term_options_stack[current_degree] = list(range(num_terms))
            current_degree += 1
        #end if
        else:
            current_term[current_degree] = term_options_stack[current_degree][0]
            del term_options_stack[current_degree][0]
            current_degree -= 1
            if current_degree == -1:
                terms.append(deepcopy(current_term))
                current_degree += 1 #stay in the last level/degree until it is empty
                #when it is empty, the first if check in the while loop will refill it and move up a level.
            #end if
        #end else
    #end while
    return tuple(terms)

    #end while loop
#========================================================================


def compute_NRMSD_distortion(in_graph, inv_graph, poly_terms, resultant_weights, vertex_embedding_dict,
                             bias = 0.0, ratio_of_points = 0.2, num_points = -1, num_samples_per_point=100):
    """
    :param set_vertex_pair_and_weight:
    :param poly_terms:
    :param resultant_weights:
    :return:
    """
    accumulated_meanSq_error = 0.0
    accumulated_graph_distance = 0.0
    embed_only_accumulated_meanSq_error = 0.0
    distance_errors = []
    all_vertices_set = set(in_graph.nodes())  # index per vertex is fixed and is a mapping between vertex and idx
    num_vertices = len(all_vertices_set)
    num_sampled_vertices = num_points
    if num_points == -1:
        num_sampled_vertices = int(ratio_of_points * num_vertices)
    vertices_for_nrmsd = random.sample(all_vertices_set,num_sampled_vertices)
    num_cases_count = num_sampled_vertices*num_samples_per_point # no div by 2, because bidirectional so n*(n-1) cases
    count = 0
    for vertex_1 in vertices_for_nrmsd:
        short_path_tree = nx.single_source_dijkstra_path_length(in_graph, vertex_1, weight="weight")
        inv_short_path_tree = nx.single_source_dijkstra_path_length(inv_graph, vertex_1, weight="weight")
        vertices_sampled = random.sample(list(short_path_tree.keys()),num_samples_per_point)
        # sorted_vertices = sorted(list(short_path_tree.items()),key = lambda x:x[1],reverse=True)
        # vertices_sampled = [x[0] for x in sorted_vertices[:num_samples_per_point+1]]
        for vertex_2 in vertices_sampled:
            if vertex_1 == vertex_2:
                continue
            count += 1
            #we have two pivots, get their embeddings
            v1_embedding = vertex_embedding_dict[vertex_1]
            v2_embedding = vertex_embedding_dict[vertex_2]
            #now get the values of each term, eg: x1x2 term would be dimension1*dimension2
            constraint_vector_as_list = []
            inv_constaint_vector = []
            for single_term in poly_terms:
                constr_single_term_value_a = 1.0  # will be multiplied by other terms.
                constr_single_term_value_b = 1.0  # will be multiplied by other terms.
                for single_dim in single_term:
                    constr_single_term_value_a *= v1_embedding[single_dim]
                    constr_single_term_value_b *= v2_embedding[single_dim]
                # end for through the dimensions of a term
                constraint_vector_as_list.append(constr_single_term_value_b - constr_single_term_value_a)
                inv_constaint_vector.append(constr_single_term_value_a - constr_single_term_value_b)
            #end for through the terms of the potential field polynomial function
            output = np.sum(np.array([1.0]+constraint_vector_as_list) * resultant_weights) + bias
            output2 = np.sum(np.array([1.0]+inv_constaint_vector) * resultant_weights) + bias
            # output = np.sum(np.array( constraint_vector_as_list) * resultant_weights) + bias
            # output2 = np.sum(np.array( inv_constaint_vector) * resultant_weights) + bias

            
            distance_1 = short_path_tree[vertex_2]
            distance_2 = inv_short_path_tree[vertex_2]
            delta_1 = distance_1 - (output+ np.linalg.norm(np.array(vertex_embedding_dict[vertex_1]) - np.array(vertex_embedding_dict[vertex_2])))
            delta_2 = distance_2 - ( output2 + np.linalg.norm(np.array(vertex_embedding_dict[vertex_1]) - np.array(vertex_embedding_dict[vertex_2])))
            distance_errors += [abs(delta_1),abs(delta_2)]
            accumulated_meanSq_error += (delta_1)**2
            accumulated_meanSq_error += (delta_2)**2
            embed_only_accumulated_meanSq_error += (distance_1 - np.linalg.norm(np.array(vertex_embedding_dict[vertex_1]) - np.array(vertex_embedding_dict[vertex_2])))**2
            embed_only_accumulated_meanSq_error += (distance_2 - np.linalg.norm(np.array(vertex_embedding_dict[vertex_1]) - np.array(vertex_embedding_dict[vertex_2])))**2
            accumulated_graph_distance += distance_1
            accumulated_graph_distance += distance_2

        #end inner for
    #end outer for
    #end for loop through vertex pair and weight

    rms_error = math.sqrt(accumulated_meanSq_error/num_cases_count)
    normalization_denominator = accumulated_graph_distance/num_cases_count
    nrmsd_result = rms_error/normalization_denominator
    print("For embedding AND pot function")
    print(nrmsd_result ," is the nrmsd for ", num_sampled_vertices, " points")
    #------
    rms_error = math.sqrt(embed_only_accumulated_meanSq_error / num_cases_count)
    nrmsd_result = rms_error/normalization_denominator
    print("For embedding only")
    print(nrmsd_result, " is the nrmsd for ", num_sampled_vertices, " points")


# ========================================================================
def main_fastmap_dirGraph_embedder(in_graph, max_dimensions, embedding_distance_error, degree_potFunc): # todo allow config distance_type = 2
    """
    :summary: embeds average distance in max-1 dimensions (default L2 distance),
            and the last dimension has the  potential difference which captures the directed distance
    :param in_graph:
    :param max_dimensions:
    :param embedding_distance_error: The allowance or error margin at which we can stop adding dimensions
    :return:
    """
    pivot_search_attempts = 20 #"C" in the pseudocode
    inverted_graph = in_graph.reverse(copy=True)

    all_vertices_tuple = tuple(in_graph.nodes())#index per vertex is fixed and is a mapping between vertex and idx
    all_vertices_set = set(all_vertices_tuple)
    num_vertices = len(all_vertices_tuple)
    shortest_path_SOURCE_dict = {}
    shortest_path_DEST_dict = {}
    vertex_embedding_dict = {}
    pivot_pairs = []
    average_toFro_dict = {}
    
    #---NOW first initialize the embeddings to empty list

    for single_v in all_vertices_set:
        vertex_embedding_dict[single_v] = []

    DEBUG_NUM_KEYS_IN_VERTEX_EMB_DICT = len(list(vertex_embedding_dict.keys()))

    #---then add embeddings
    for dim_idx in range(1,max_dimensions+1):
        vertex_a = random.choice(all_vertices_tuple)
        vertex_b = random.choice(all_vertices_tuple)
        for t in range(pivot_search_attempts): #this is a quick-dirty method to find largest dist. otherwise O(n^2)
            embedding_a = np.array(vertex_embedding_dict[vertex_a])
            shortest_paths_SOURCE_vertexA = nx.single_source_dijkstra_path_length(in_graph,vertex_a,weight="weight")
            shortest_path_SOURCE_dict[vertex_a] = shortest_paths_SOURCE_vertexA
            shortest_paths_DEST_vertexA = nx.single_source_dijkstra_path_length(inverted_graph,vertex_a,weight="weight")
            shortest_path_DEST_dict[vertex_a] = shortest_paths_DEST_vertexA
            reachable_nodes = all_vertices_set
            average_toFro_dict[vertex_a] = dict(zip(reachable_nodes,\
                                            [(shortest_path_SOURCE_dict[vertex_a][x] + shortest_path_DEST_dict[vertex_a][x])/2 for x in reachable_nodes] ) )
            list_distDiff = []
            remainder_vertices = list(all_vertices_set.difference(set([vertex_a])))
            for vertex_i in remainder_vertices:
                embedding_i = np.array(vertex_embedding_dict[vertex_i])
                distAvgSq_ai = average_toFro_dict[vertex_a][vertex_i]**2
                distSqDiff_ai = distAvgSq_ai - np.sum(np.square(embedding_i - embedding_a))
                list_distDiff.append(distSqDiff_ai)
            #end for loop through vertices
            index_max = list_distDiff.index(max(list_distDiff))
            vertex_max = remainder_vertices[index_max]
            if vertex_max == vertex_b: #the furthest vertex_i was vertex_b, so we reached a local max
                
                embedding_a = np.array(vertex_embedding_dict[vertex_a])
                embedding_b = np.array(vertex_embedding_dict[vertex_b])
                # ---compute the avg to fro and shortest paths for vertex b
                shortest_paths_SOURCE_vertexB = nx.single_source_dijkstra_path_length(in_graph, vertex_b, weight="weight")
                shortest_path_SOURCE_dict[vertex_b] = shortest_paths_SOURCE_vertexB
                shortest_paths_DEST_vertexB = nx.single_source_dijkstra_path_length(inverted_graph, vertex_b,
                                                                                  weight="weight")
                shortest_path_DEST_dict[vertex_b] = shortest_paths_DEST_vertexB
                reachable_nodes_A = all_vertices_set
                average_toFro_dict[vertex_a] = dict(zip(reachable_nodes_A, \
                                                        [(shortest_path_SOURCE_dict[vertex_a][x] +
                                                          shortest_path_DEST_dict[vertex_a][x]) / 2 for x in
                                                         reachable_nodes_A]))
                reachable_nodes_B = all_vertices_set
                average_toFro_dict[vertex_b] = dict(zip(reachable_nodes_B, \
                                                        [(shortest_path_SOURCE_dict[vertex_b][x] +
                                                          shortest_path_DEST_dict[vertex_b][x]) / 2 for x in
                                                         reachable_nodes_B]))
                # ---determine if the distance between a-b is appreciable enough to deserve another dimension
                distAvgSq_ab = average_toFro_dict[vertex_a][vertex_b] ** 2
                distSqDiff_ab = distAvgSq_ab - np.sum(
                    np.square(embedding_b - embedding_a))  # order does not matter, it is for to-fro distance
                try:
                    
                    dist_left_ab = math.sqrt(distSqDiff_ab)
                    break  # if we succeeded break out of the for loop through pivot search attempts
                except:
                    vertex_a = random.choice(all_vertices_tuple)
                    vertex_b = random.choice(all_vertices_tuple)
                    continue #back to the start of the for loop !!
                #end except
            #end if vertex_max == vertex_b
            #otherwise update vertex a and b and continue
            vertex_b = vertex_a
            vertex_a = vertex_max
            if t == pivot_search_attempts-1: #zero indexed
                print("PIVOT SEARCH ATTEMPTS MAXED OUT  t == pivot_search_attempts-1")
        #end for loop through pivot search attempts
        #---
        
        embedding_a = np.array(vertex_embedding_dict[vertex_a])
        embedding_b = np.array(vertex_embedding_dict[vertex_b])
        # ---compute the avg to fro and shortest paths for vertex b
        shortest_paths_SOURCE_vertexA = nx.single_source_dijkstra_path_length(in_graph, vertex_a, weight="weight")
        shortest_path_SOURCE_dict[vertex_a] = shortest_paths_SOURCE_vertexA
        shortest_paths_DEST_vertexA = nx.single_source_dijkstra_path_length(inverted_graph, vertex_a, weight="weight")
        shortest_path_DEST_dict[vertex_a] = shortest_paths_DEST_vertexA
        shortest_paths_SOURCE_vertexB = nx.single_source_dijkstra_path_length(in_graph, vertex_b, weight="weight")
        shortest_path_SOURCE_dict[vertex_b] = shortest_paths_SOURCE_vertexB
        shortest_paths_DEST_vertexB = nx.single_source_dijkstra_path_length(inverted_graph, vertex_b,
                                                                          weight="weight")
        shortest_path_DEST_dict[vertex_b] = shortest_paths_DEST_vertexB
        reachable_nodes_A = all_vertices_set
        average_toFro_dict[vertex_a] = dict(zip(reachable_nodes_A, \
                                                [(shortest_path_SOURCE_dict[vertex_a][x] +
                                                  shortest_path_DEST_dict[vertex_a][x]) / 2 for x in
                                                 reachable_nodes_A]))
        reachable_nodes_B = all_vertices_set
        average_toFro_dict[vertex_b] = dict(zip(reachable_nodes_B, \
                                                [(shortest_path_SOURCE_dict[vertex_b][x] +
                                                  shortest_path_DEST_dict[vertex_b][x]) / 2 for x in
                                                 reachable_nodes_B]))

        #-----------------------
        # ---determine if the distance between a-b is appreciable enough to deserve another dimension
        distAvgSq_ab = average_toFro_dict[vertex_a][vertex_b] ** 2
        distSqDiff_ab = distAvgSq_ab - np.sum(
            np.square(embedding_b - embedding_a))  # order does not matter, it is for to-fro distance
        if distSqDiff_ab < EPSILON_PATH_LEN_DIFFERENCE:
            distSqDiff_ab = 0 + EPSILON_PATH_LEN_DIFFERENCE
        try:
            dist_left_ab = math.sqrt(distSqDiff_ab)
        except:
            dim_idx = dim_idx-1 #oh man this is terrible code. Do this better
            continue  # GOES BACK TO START OF FOR LOOP, this dimension is skipped.
        #--compute new embedding dimension here

        if  dist_left_ab < embedding_distance_error:
            break #out of the for loop through dimensions
        pivot_pairs.append((vertex_a,vertex_b)) #if there is more "distance" to embed, then add to the pivot pairs and continue
        #---else
        for vertex_i in all_vertices_set:

            embedding_i = np.array(vertex_embedding_dict[vertex_i])

            distAvgSq_ai = average_toFro_dict[vertex_a][vertex_i]**2

            try:
                distSqDiff_ai = distAvgSq_ai - np.sum(np.square(embedding_i - embedding_a))
                if distSqDiff_ai < 0:
                    distSqDiff_ai = 0
                distAvgSq_ib = average_toFro_dict[vertex_b][vertex_i]**2 #yes b-i rather than i-b. It is the same for avg to-fro distance
                distSqDiff_ib = distAvgSq_ib - np.sum(np.square(embedding_b - embedding_i))
                if distSqDiff_ib < 0:
                    distSqDiff_ib = 0
            except:
                print(embedding_a.shape)
                print(embedding_i.shape)
                print(embedding_b.shape)
                exit(1)

            denominator_term = math.sqrt(distSqDiff_ab)
            new_embedding_value = (distSqDiff_ai + distSqDiff_ab - distSqDiff_ib)/ (2*denominator_term)
            vertex_embedding_dict[vertex_i].append(new_embedding_value)
        #end for loop through updating dumensions
    #end for loop through dimensions
    #---now we compute the potential field coefficients by solving a weighted set of constraints
    pivot_vertices = set()
    for single_pivot_pair in pivot_pairs:
        pivot_vertices.add(single_pivot_pair[0])
        pivot_vertices.add(single_pivot_pair[1])
    num_pivots = len(pivot_vertices)
    num_constraints = num_pivots * (num_pivots-1)
    #note that the num constraints is not |vertices| * |vertices-1|. We only check the distance between the pivot vertices, and distance between the pivot and non-pivots
    num_dimensions = len(pivot_pairs)
    print("num pivots = ", num_pivots)
    print("num dimensions = ", num_dimensions)
    print("pot func degree = ", degree_potFunc)

    # --- lets determine the terms of the polynomial and a mapping of term to index
    poly_terms = []
    
    num_terms = 0
    for currrent_term_degree in range(1,degree_potFunc+1):
        tmp = get_poly_terms(num_dimensions,currrent_term_degree)
        num_terms += len(tmp)
        poly_terms += tmp

    
    min_additional_nodes_set = set()
    additional_constraints_needed = 0
    if num_constraints < num_terms + 2*MIN_ADDITIONAL_NODES*num_pivots: # why"x2" because one constraint for each direction.
        additional_constraints_needed = num_terms - num_constraints +  2*MIN_ADDITIONAL_NODES*num_pivots
        # pivots*extra = additional. because we only want the constraints to be pivot to non-pivot, not between non-pivots
        #Below we "/2" since a->b != b->a, and +1 since we round up to have enough constraints for a fully constrained system
        addition_node_number = int(additional_constraints_needed/(num_pivots-1))+MIN_ADDITIONAL_NODES #the constraints are pivots * (second set). second set has pivots too, which we already counted
        non_pivot_vertices_set = all_vertices_set.difference(pivot_vertices)  # so we dont repick pivots
        min_additional_nodes_set = set(random.sample(non_pivot_vertices_set, addition_node_number))

    # --- now build the constraints

    constraint_list = []
    set_vertex_pair_and_weight = set()
    seen_pairs = set()
    # build the constraints
    # for vertex_1 in pivot_vertices:
    chosen_non_pivot_vertices_set = all_vertices_set.difference(pivot_vertices)
    #if you want only pivots and bare min to fully constrain the OLS
    chosen_non_pivot_vertices_set = set(random.sample(chosen_non_pivot_vertices_set, int(len(chosen_non_pivot_vertices_set) * RATIO_NUM_NON_PIVOTS)))
    if len(chosen_non_pivot_vertices_set) > int(additional_constraints_needed/(num_pivots-1))+MIN_ADDITIONAL_NODES:
        second_vertex_set = chosen_non_pivot_vertices_set.union(pivot_vertices)
    else:
        second_vertex_set = min_additional_nodes_set.union(pivot_vertices)

    for vertex_1 in pivot_vertices: #second_vertex_set if you want only random nodes in the constraints
        for vertex_2 in second_vertex_set: #so we get pivot pairs and pivot-non pivot
            if vertex_1 == vertex_2:
                continue #select another pivot
            #end if
            curr_case = tuple(sorted([vertex_1,vertex_2]))
            if curr_case in seen_pairs:
                continue
            #end if
            seen_pairs.add(curr_case)
            if vertex_1 in pivot_vertices and vertex_2 in pivot_vertices:
                set_vertex_pair_and_weight.add((vertex_1, vertex_2, PIVOTS_ONLY_CONSTRAINT_WEIGHT))
                #the vertex 2 -> vertex 1 case will happen auto in the later code below that computes the constraints
            elif vertex_1 in pivot_vertices or vertex_2 in pivot_vertices:
                set_vertex_pair_and_weight.add((vertex_1, vertex_2, SINGLE_PIVOTS_ONLY_CONSTRAINT_WEIGHT))
            else:
                set_vertex_pair_and_weight.add((vertex_1, vertex_2, NO_PIVOTS_CONSTRAINT_WEIGHT))
                # the vertex 2 -> vertex 1 case will happen auto in the later code below that computes the constraints
        #end inner for through pivots
    #end outer for through pivots

    
    list_vertex_pair_and_weight = list(set_vertex_pair_and_weight)
    num_list_vertex_pair_and_weight = len(list_vertex_pair_and_weight)
    for vertex_pair_and_weight_idx in range(num_list_vertex_pair_and_weight):
        if vertex_pair_and_weight_idx % 1000 == 0:
            print("idx for constraint processing = ", vertex_pair_and_weight_idx, " / ",
                  num_list_vertex_pair_and_weight)
        vertex_pair_and_weight = list_vertex_pair_and_weight[vertex_pair_and_weight_idx]
        vertex_1 = vertex_pair_and_weight[0]
        vertex_2 = vertex_pair_and_weight[1]
        weight = vertex_pair_and_weight[2]
        #we have two pivots, get their embeddings
        v1_embedding = vertex_embedding_dict[vertex_1]
        v2_embedding = vertex_embedding_dict[vertex_2]
        #now get the values of each term, eg: x1x2 term would be dimension1*dimension2
        constraint_vector_as_list = []
        inv_constaint_vector = []
        #TODO NOTE IMPORTANT CHANGE
        #need to fill in the terms as sep
        for single_term in poly_terms:
            constr_single_term_value_a = 1.0 #will be multiplied by other terms.
            constr_single_term_value_b = 1.0  # will be multiplied by other terms.
            for single_dim in single_term:
                constr_single_term_value_a *= v1_embedding[single_dim]
                constr_single_term_value_b *= v2_embedding[single_dim]
            #end for through the dimensions of a term
            constraint_vector_as_list.append(constr_single_term_value_b - constr_single_term_value_a)
            inv_constaint_vector.append(constr_single_term_value_a - constr_single_term_value_b)
        #end for through the terms of the potential field polynomial function

        
        avg_distance = np.linalg.norm(np.array(vertex_embedding_dict[vertex_1]) - np.array(vertex_embedding_dict[vertex_2]))
        if TRUE_AVG_DIST_IN_POT_FUNC:
            avg_distance = average_toFro_dict[vertex_1][vertex_2]
        #now add the two constraints , one for each direction

        try:
            constraint_list.append(
                (constraint_vector_as_list,shortest_path_SOURCE_dict[vertex_1][vertex_2]-avg_distance,weight))
        except KeyError: # in case we computed it in the shortest_path_SOURCE_dict only
                        # we do not do full computation of shortest paths to keep the linearity
                        # NOTE the order of vertices is FLIPPED for the FROM dict to get the same info.
            if vertex_2 in shortest_path_DEST_dict.keys():
                constraint_list.append(
                    (constraint_vector_as_list,shortest_path_DEST_dict[vertex_2][vertex_1]-avg_distance,weight))
            else:
                shortest_paths_SOURCE_vertexA = nx.single_source_dijkstra_path_length(in_graph, vertex_1,
                                                                                      weight="weight")
                shortest_path_SOURCE_dict[vertex_1] = shortest_paths_SOURCE_vertexA
                shortest_paths_DEST_vertexA = nx.single_source_dijkstra_path_length(inverted_graph, vertex_1,
                                                                                    weight="weight")
                shortest_path_DEST_dict[vertex_1] = shortest_paths_DEST_vertexA
                constraint_list.append(
                    (constraint_vector_as_list,shortest_path_SOURCE_dict[vertex_1][vertex_2]-avg_distance,weight))

        try:
            constraint_list.append(
                (inv_constaint_vector,shortest_path_SOURCE_dict[vertex_2][vertex_1]-avg_distance,weight))
        except KeyError:
            constraint_list.append(
                (inv_constaint_vector,shortest_path_DEST_dict[vertex_1][vertex_2]-avg_distance,weight))

    #end for loop through vertex_pair_and_weight
    #------
    #now organize the constraints, and weights into matrices and vectors for the weighted least squares function call
    constraint_matrix = np.array([x[0] for x in constraint_list])
    constraint_targets = np.array([x[1] for x in constraint_list])
    constraint_weights = np.array([x[2] for x in constraint_list])
    constraint_matrix = statModels.add_constant(constraint_matrix) #inserts a column of 1s that represents the bias !!
    bias= 0

    
    if USE_WEIGHTED_LEAST_SQUARES:
        wls_model = statModels.WLS(constraint_targets, constraint_matrix,
                                   weights=constraint_weights)  # use the error as the weight
        
        # wls_model = statModels.WLS(constraint_targets,constraint_matrix, weights=np.abs(constraint_targets))
        results = wls_model.fit()
        resultant_weights = results.params
    else:
        # lin_model = linear_model.LinearRegression(fit_intercept=False).fit(constraint_matrix, constraint_targets)
        # lin_model = linear_model.Ridge().fit(constraint_matrix, constraint_targets)
        lin_model = linear_model.Lasso(fit_intercept=False).fit(constraint_matrix, constraint_targets)
        #https://stats.stackexchange.com/questions/76518/what-is-the-time-complexity-of-lasso-regression
        # lin_model = linear_model.ElasticNet().fit(constraint_matrix, constraint_targets)
        print("Linear model (non weighted) score =" , lin_model.score(constraint_matrix, constraint_targets))
        resultant_weights = lin_model.coef_
        bias = lin_model.intercept_

    print("TESTING")
    print("COMPUTING METRICS")

    inverted_graph = in_graph.reverse(copy=True)
    compute_NRMSD_distortion(in_graph, inverted_graph, poly_terms, resultant_weights, vertex_embedding_dict, bias,
                             ratio_of_points=0.001, num_points=50, num_samples_per_point=600)

    print("num dimensions used = ", num_dimensions)
    print("max degree of potential func = ", degree_potFunc)
    #--------
    return (vertex_embedding_dict,poly_terms,resultant_weights)

#---END main_fastmap_dirGraph_embedder
#=================================================================
#===================================================================
#===================================================================



if __name__ == "__main__":

    print("Remember to pickle(save) vertex_embed_dict,poly_terms,poly_weight for use in downstream tasks")
    print("These objects are produced at the end of this code")
    in_graph = None
    source_graph_files = []#add the locations of the graphs you wish to run. files are pickle files of the networkx directed graph object
    # source_graph_files += ["./GraphFolder/TOPOL_DIR_EDITED_hrt201n.p"]
    # source_graph_files += ["./GraphFolder/TOPOL_DIR_EDITED_maze512-32-0.p"]
    # source_graph_files += ["./GraphFolder/TOPOL_DIR_EDITED_random512-40-0.p"]
    source_graph_files += ["./GraphFolder/TOPOL_DIR_EDITED_Boston_2_256.p"]
    # source_graph_files += ["./GraphFolder/POLYNOMIAL_DIR_EDITED_Boston_2_256.p"]
    # source_graph_files += ["./GraphFolder/POLYNOMIAL_DIR_EDITED_hrt201n.p"]

    print("source_files" , source_graph_files)
    list_dimensions = [2, 5, 8, 11, 15, 20, 30]
    potFunc_options = [2]

    print("list_dimensions ", list_dimensions)
    print("potFunc_options = ", potFunc_options)


    for source_graph_file in source_graph_files:
        date_time_str = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        date_time_str = date_time_str.replace(" ", "_")
        date_time_str = date_time_str.replace("/", "_")
        date_time_str = date_time_str.replace(",", "_")
        date_time_str = date_time_str.replace(":", "_")
        output_file_name = 'D-fastmap_output_results' + source_graph_file.replace("./GraphFolder/","").replace(".p","") +"_" + date_time_str
        print("date and time:", date_time_str)
        sys.stdout = open(output_file_name + '.txt', 'w')
        with open(source_graph_file, "rb") as src: # 0.076 vs 0.307 (w 15 dim, and 0.25 of the non-pivots, pot func degree 2)
            in_graph = pickle.load(src)
        print("date and time:", date_time_str)
        print(len(in_graph.nodes()))
        print(len(in_graph.edges()))
        print("source_graph_file", source_graph_file)
        print("list_dimensions ", list_dimensions)
        print("potFunc_options = ", potFunc_options)
        # todo NOTE do not make modifications on this, use the MODIFIED FILE



        for max_dimensions in list_dimensions:
            for degree_potFunc in potFunc_options:
                embedding_distance_error = ALLOWABLE_EMBEDDING_DISTANCE_ERROR
                with CodeTimer():
                    (vertex_embed_dict,poly_terms,poly_weight) = \
                        main_fastmap_dirGraph_embedder(in_graph,max_dimensions, embedding_distance_error, degree_potFunc)
                sys.stdout.flush()
        #end for loop
        sys.stdout.flush()


