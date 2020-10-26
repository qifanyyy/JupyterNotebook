# -*- coding: utf-8 -*-
import numpy as np 
import networkx as nx

def initialization(grid):
    """This function takes in the 2-D grid given as input and returns an initial graph.
    Example
    -------

    grid = [(1,2),(3,4),(5,6)]
    initial_graph = initialization(grid)

    Parameters
    ----------

    grid : list of tuples
        the input list of tuples 

    Output
    ------

    graph : M x M numpy array (M is the number of tuples in grid)
        a weighted adjacency matrix for the graph generated from the list of tuples"""

    grid = np.asarray(grid)
    graph = np.zeros((len(grid),len(grid)))

    for i in range(0,len(grid),1):
        for j in range(0,len(grid),1):
            graph[i,j] = np.sqrt((grid[i,0] - grid[j,0])**2 + (grid[i,1]-grid[j,1])**2) #Euclidean distance between two points
    return graph

def connected(i,rand_i,rand_j):
    """This function tests whether a given graph will still be connected if the proposed replacement is made. The proposed 
    replacement represents changing the position at rand_i,rand_j to 0 if it is non-0 and changing it to non-0 if it is 0.

    Example
    -------
    i = [[0,1,1],[1,0,0],[1,0,0]]
    proposed_index_1_change = 1
    proposed_index_2_change = 2
    connected(i,proposed_index_1_change,proposed_index_2_change)

    Parameters
    ----------

    i : M x M numpy array (where M is the number of tuples in the initial grid)
    rand_i : int
        index 1 value
    rand_j : int
        index 2 value

    Output
    ------
    truth_value : boolean
        whether the proposed graph would be connected or not"""

    graph = list(i)
    graph = np.asarray(graph)

    #testing to see if the proposed position change is 0 or not 0 and setting it to the opposite of what it currently is
    if graph[rand_i,rand_j] == 0:
        graph[rand_i,rand_j] = 1
        graph[rand_j,rand_i] = 1
    elif graph[rand_i,rand_j] != 0:
        graph[rand_i,rand_j] = 0
        graph[rand_j,rand_i] = 0

    #using networkx's is_connected feature to discern connectedness
    graph = nx.from_numpy_matrix(graph)
    return(nx.is_connected(graph))

def q(i,grid):
    """This function returns a candidate state given the state that the Markov chain is currently in. 

    Example
    -------
    grid = [(1,2),(2,3),(4,5)]
    i = [[0,4,6],[2,0,9],[7,5,0]]
    candidate = q(i)
    print(candidate)


    Parameters
    ----------
    i : M x M array
        The current state of the Markov distribution (a gonnected graph).
    grid : M x 2 array
        x and y distance values for the vertices in the initial Markov state.

    Returns
    -------
    candidate : array
        candidate is the candidate state based on the decision calculus intrinsic to q."""

    grid = np.array(grid)
    candidate = list(i)
    candidate = np.asarray(candidate)
    rand_i = np.random.randint(len(i))
    rand_j = np.random.randint(len(i))

    #following while loop ensures that the candidate graph is connected and does not contain self-loops
    while rand_i == rand_j or connected(candidate,rand_i,rand_j) == False:
        rand_i = np.random.randint(len(i))
        rand_j = np.random.randint(len(i))
        
    #generating candidate graph by replacing index rand_i,rand_j 
    if candidate[rand_i,rand_j] != 0:
        candidate[rand_i,rand_j] = 0
        candidate[rand_j,rand_i] = 0

        
    elif candidate[rand_j,rand_i] == 0:
        weight_i_j = np.sqrt((grid[rand_i,0] - grid[rand_j,0])**2 + (grid[rand_i,1]-grid[rand_j,1])**2)
        candidate[rand_i,rand_j] = weight_i_j
        candidate[rand_j,rand_i] = weight_i_j

    return candidate


def theta(i,r=1):
    """This function calculates the value of theta for the given state. Theta is a function defined in the problem statement.

    Example
    -------

    i = [[1,0],[0,1]]
    weights = [[1,2],[3,4]]
    value = theta(i,weights)

    Parameters
    ----------

    i : MxM array
        This is the current state represented in an MxM adjacency matrix.

    grid : Mx2 list of tuples
        This is the list of x and y values in Cartesian space for the given index/label (i.e. the individual column headers in the 'i array.')

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    Output
    ------

    value : integer
        This is the theta value for the given state."""

    i = np.array(i)
    total_weight = np.sum(i)
    graph = nx.from_numpy_matrix(i)
    partial_weight = 0
    for v in range(0,len(i),1):
        path = nx.shortest_path(graph,0,v)
        # path is a set of nodes inclusive of end pts. Thus, len(path)-1 = number of edges in our path of interest.
        for node in range(0,len(path)-1,1):
            partial_weight += i[path[node],path[node+1]]
    return(r * total_weight + partial_weight)

def probability(i,j,T=1,r=1):
    """This function computes the probability that the candidate state will be selected.

    Example
    -------

    i = [[1,0],[0,1]]
    j = [[0,1],[1,0]]
    prob = probability(i,j)

    Parameters
    ----------

    i : MxM array
      This is the current graph represented by its adjacency matrix.

    j : MxM array
      This is the candidate graph represented by its adjacency matrix.

    T : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    Output
    ------

    prob : float
      This is the probability that the candidate graph is selected. It takes values on [0,1]."""

    #collecting different variables in probability calculation
    theta_i = theta(i,r)
    theta_j = theta(j,r)
    number_of_potential_edges = len(i) * (len(i) - 1) / 2
    cut_edges_i = cut_edges(i)
    cut_edges_j = cut_edges(j)
    
    #calculating q(j|i) and q(i|j)
    q_j_given_i = 1/(number_of_potential_edges - cut_edges_i)
    q_i_given_j = 1/(number_of_potential_edges - cut_edges_j)
    
    #calculating relative value of pi_j / pi_i
    eq_distrib_ratio = np.exp(-(theta_j - theta_i)/T)
    
    #calculating alpha using Metropolis-Hastings criteria
    
    alpha_proposed = eq_distrib_ratio * q_i_given_j / q_j_given_i
    
    if alpha_proposed >= 1:
        alpha = 1.0
    
    if alpha_proposed < 1:
        alpha = alpha_proposed
    return alpha


def cut_edges(i):
    '''This function counts the number of edges that if removed (set equal to 0) would cause the graph to be disconnected.

    Example
    -------

    i = [[0,1],[1,0]]
    cut_edges(i)

    Parameters
    ----------

    i : M x M numpy array (where M is the number of tuples in the initial grid)

    Output
    ------

    cut_edges : int
        number of such edges as described earlier in the docstring.'''

    #creating a numpy_matrix we can play around with w/o affecting our original
    i = np.array(i)
    prax_graph = list(i)
    prax_graph = np.array(prax_graph)
    
    #next section iterates over every edge in the graph, sets it to 0, and calculates the number of connected components
    #this will tell us whether a given edge is a cut edge
    
    cut_edges = 0
    for val_i in range(0,len(i),1):
        for val_j in range(0,len(i),1):
            prax_graph[val_i,val_j] = 0
            prax_graph[val_j,val_i] = 0 
            nx_graph = nx.from_numpy_matrix(prax_graph)
            if nx.number_connected_components(nx_graph) != 1:
                cut_edges += 1
            prax_graph[val_i,val_j] = i[val_i,val_j]
            prax_graph[val_j,val_i] = i[val_j,val_i]
            
    return cut_edges/2 # o/w we will double count number of cut edges


def next_state(i,j,probability):
    """ This function returns the next state using functions already defined.

    Example
    -------
    
    i = [[0,1,1],[1,0,0],[1,0,0]]
    j = [[0,1,1],[1,0,1],[1,1,0]]

    state = next_state(i,j,.4)

    Parameters
    ----------

    i : M x M numpy array (where M is the number of tuples in the initial grid)
      the current state

    j : M x M numpy array
      the candidate state

    probability : float
      the probability that state j is selected

    Output 
    ------

    state : M x M numpy array 
      the state chosen"""

    #using a random number generator to generate a random number.
    u = np.random.uniform(0.0,1.0)
    
    #calculating new state based on Metropolis-Hastings algorithm specifications:
    if u > probability: 
        new_state = i
    elif u <= probability:
        new_state = j
        
    return new_state

def expected_connect_to_0(grid,N,T=1,r=1):
    """ This function returns the arithmetic mean number of edges that are connected to the 0 node given an input grid. This should 
    approximate the expected number of edges of this type quite well if N is large.
    Example
    -------

    grid = [(12,17),(13,19),(34,69),(34,12)]
    number_edges = MCMC.expected_connect_to_0(grid,1000)

    Parameters
    ----------

    grid : list of tuples
      the x and y coordinates of all the different nodes in the graph. The 1st entry should be the all-important "0" node, while
      the rest of them can be in any arbitrary order.

    N : int
        the number of iterations desired.

    T : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    Output
    ------
    
    number_edges : float
    The expected number of edges that connect to the 0 node."""

    import numpy as np
    initial_graph = initialization(grid)
    new_state = initial_graph
    number_edges = 0


    for i in range(N):
        #generating next graph
        candidate_graph = q(new_state,grid)
        switching_likelihood = probability(new_state,candidate_graph,T,r)
        new_state = next_state(new_state,candidate_graph,switching_likelihood)

        #computing number connections to 0
        for i in range(len(new_state)):
            if new_state[0,i] != 0: 
                number_edges += 1

    #computing average
    return number_edges / N

def expected_number_edges(grid,N,T=1,r=1):
    """ This function returns the arithmetic mean number of edges in the graph. This should 
    approximate the expected number of edges of this type quite well if N is large.
    Example
    -------

    grid = [(12,17),(13,19),(34,69),(34,12)]
    number_edges = MCMC.expected_number_edges(grid,1000)

    Parameters
    ----------

    grid : list of tuples
      the x and y coordinates of all the different nodes in the graph. The 1st entry should be the all-important "0" node, while
      the rest of them can be in any arbitrary order.

    N : int
        the number of iterations desired.

    T : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.


    Output
    ------
    
    number_edges : float
    The expected number of edges in a graph."""

    import numpy as np
    initial_graph = initialization(grid)
    new_state = initial_graph
    number_edges = 0


    for i in range(N):
        #generating next graph
        candidate_graph = q(new_state,grid)
        switching_likelihood = probability(new_state,candidate_graph,T,r)
        new_state = next_state(new_state,candidate_graph,switching_likelihood)

        #computing number connections to 0
        for i in range(len(new_state)):
            for j in range(len(new_state)):
                if new_state[i,j] != 0: 
                    number_edges += 1

    #computing average
    return number_edges / ( 2 * N )

def expected_furthest_from_0(grid,N,T=1,r=1):
    """This function returns the arithmetic mean number of edges between the 0 node and the node that is the furthest from 0. 
    This should approximate the actual expected number of edges in this path as N gets large.

    Example
    -------

    grid = [(12,17),(13,19),(34,69),(34,12)]
    number_edges = MCMC.expected_furthest_from_0(grid,1000)

    Parameters
    ----------

    grid : list of tuples
        the x and y coordinates of all the different nodes in the graph. The 1st entry should be the all-important "0" node, while
        the rest of them can be in any arbitrary order.

    N : int
        the number of iterations desired.

    T : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    Output
    ------

    number_edges : float
    The expected number of edges in the shortest path between 0 and the vertex furthest from 0."""

    import numpy as np
    initial_graph = initialization(grid)
    new_state = initial_graph
    number_edges = 0

    #calculating and storing longest "shortest path" from 0
    overall_path = 0
    nx_graph = nx.from_numpy_matrix(new_state)
    for node in range(len(initial_graph)):
        path =  len(nx.shortest_path(nx_graph,0,node))
        if path > overall_path:
            overall_path = path

    #recall this is an edge path, and networkx returns a node path, so we subtract one to get the number of edges
    overall_path = overall_path - 1


    for i in range(N):
        #generating next graph
        candidate_graph = q(new_state,grid)
        switching_likelihood = probability(new_state,candidate_graph,T,r)
        new_state = next_state(new_state,candidate_graph,switching_likelihood)

        #computing shortest paths from 0 to each node and selecting the largest of them
        nx_graph = nx.from_numpy_matrix(new_state)
        largest_path = 0
        for node in range(len(candidate_graph)):
            path = len(nx.shortest_path(nx_graph,0,node))
            if path > largest_path:
                largest_path = path 

        #adding the largest path's edge length to the overall total
        overall_path += largest_path - 1

    return overall_path / N

def most_likely_graphs(grid,percentage,N,T=1,r=1):
    """This function returns the most likely graphs ordered from most to least. The amount of returned graphs depends on the input percentage.
    Example
    -------

    grid = [(12,17),(13,19),(34,69),(34,12)]
    graphs = MCMC.most_likely_graphs(grid,.01,1000)

    Parameters
    ----------

    grid : list of tuples
      the x and y coordinates of all the different nodes in the graph. The 1st entry should be the all-important "0" node, while
      the rest of them can be in any arbitrary order.

    percentage : float
        the percentage of different graphs travelled that you would like returned. e.g. .01 returns the 1% of most likely graphs.

    N : int
        the number of iterations desired.

    T : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    r : float (optional)
        adjustable parameter to improve specificity of intrinsic probability distribution.

    Output
    ------

    graphs : list
        a list of most likely graphs ordered from most to least likely (of the top given percentage of course). Each graph is
        itself a list."""

    initial_graph = initialization(grid)
    new_state = initial_graph
    graphs = []
    counter = []


    for i in range(N):
        #generating next graph
        candidate_graph = q(new_state,grid)
        switching_likelihood = probability(new_state,candidate_graph,T,r)
        new_state = next_state(new_state,candidate_graph,switching_likelihood)

        #check if the graph is already in the list. if not, append it to the list
        identical_graph_found = False
        for graph in range(len(graphs)):

            if np.allclose(graphs[graph],new_state) == True: 
                counter[graph] += 1
                identical_graph_found = True

        if identical_graph_found == False:
            graphs.append(new_state)
            counter.append(1)

    #calculating number of graphs to return
    uniques = len(counter)
    returned = int(uniques * percentage)
    if returned == 0:
        returned = 1 

    #sorting by counter value and selecting the correct graphs
    #source for zipping: http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
    graph_and_counter = zip(counter,graphs)
    likely_graphs = [graph for counter, graph in sorted(graph_and_counter,reverse = True, key = lambda count: count[0])]    
    return likely_graphs[:returned]
        








    

















