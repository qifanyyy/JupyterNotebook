"""Testing pbnt. Run this before anything else to get pbnt to work!"""
import sys
if('pbnt/combined' not in sys.path):
    sys.path.append('pbnt/combined')
from exampleinference import inferenceExample

inferenceExample()
# Should output:
# ('The marginal probability of sprinkler=false:', 0.80102921)
#('The marginal probability of wetgrass=false | cloudy=False, rain=True:', 0.055)

'''
WRITE YOUR CODE BELOW. DO NOT CHANGE ANY FUNCTION HEADERS FROM THE NOTEBOOK.
'''
from Node import BayesNode
from Graph import BayesNet
def make_power_plant_net():
    """Create a Bayes Net representation of the above power plant problem. 
    Use the following as the name attribute: "alarm","faulty alarm", "gauge","faulty gauge", "temperature". (for the tests to work.)
    """
    nodes = []
    # TODO: finish this function
    A_node = BayesNode(0, 2, name="alarm")
    Fa_node = BayesNode(1, 2, name="faulty alarm")
    G_node = BayesNode(2, 2, name="gauge")
    Fg_node = BayesNode(3, 2, name="faulty gauge")
    T_node = BayesNode(4, 2, name="temperature")
    
    A_node.add_parent(Fa_node)
    Fa_node.add_child(A_node)
    
    A_node.add_parent(G_node)
    G_node.add_child(A_node)
    
    G_node.add_parent(Fg_node)
    Fg_node.add_child(G_node)
    
    G_node.add_parent(T_node)
    T_node.add_child(G_node)
    
    Fg_node.add_parent(T_node)
    T_node.add_child(Fg_node)
    
    nodes = [A_node, Fa_node, G_node, Fg_node, T_node]
    
    return BayesNet(nodes)

def is_polytree():
    """Multiple choice  question about polytrees."""
    
    # TODO: make a choice!
    choice = 'c'
    answers = {
        'a' : 'Yes, because it can be decomposed into multiple sub-trees.',
        'b' : 'Yes, because its underlying undirected graph is a tree.',
        'c' : 'No, because its underlying undirected graph is not a tree.',
        'd' : 'No, because it cannot be decomposed into multiple sub-trees.'
    }
    return answers[choice]

from numpy import zeros, float32
import Distribution
from Distribution import DiscreteDistribution, ConditionalDiscreteDistribution
def set_probability(bayes_net):
    """Set probability distribution for each node in the power plant system."""
    
    A_node = bayes_net.get_node_by_name("alarm")
    F_A_node = bayes_net.get_node_by_name("faulty alarm")
    G_node = bayes_net.get_node_by_name("gauge")
    F_G_node = bayes_net.get_node_by_name("faulty gauge")
    T_node = bayes_net.get_node_by_name("temperature")
    nodes = [A_node, F_A_node, G_node, F_G_node, T_node]
    # TODO: set the probability distribution for each node
    # 1. Gauge Probability Distribution
    # T | Fg | P(G | T, Fg)
    # F | F  | 0.05
    # F | T  | 0.8
    # T | F  | 0.95
    # T | T  | 0.2
    dist = zeros([T_node.size(), F_G_node.size(), G_node.size()], dtype=float32)
    dist[0,0,:] = [0.95, 0.05]
    dist[0,1,:] = [0.2, 0.8]
    dist[1,0,:] = [0.05, 0.95]
    dist[1,1,:] = [0.8, 0.2]
    G_distribution = ConditionalDiscreteDistribution(nodes=[T_node, F_G_node, G_node],
                                                     table=dist)
    G_node.set_dist(G_distribution)
    # 2. Faulty Alarm Probability Distribution
    # P(Fa) = 0.15
    Fa_distribution = DiscreteDistribution(F_A_node)
    index = Fa_distribution.generate_index([], [])
    Fa_distribution[index] = [0.85, 0.15]
    F_A_node.set_dist(Fa_distribution)
    # 3. Actual Temperature Probability Distribution
    # P(T) = 0.2
    T_distribution = DiscreteDistribution(T_node)
    index = T_distribution.generate_index([],[])
    T_distribution[index] = [0.8, 0.2]
    T_node.set_dist(T_distribution)
    # 4. Faulty Gauge Probability Distribution
    # T | P(Fg | T)
    # F | 0.05
    # T | 0.8
    dist = zeros([T_node.size(), F_G_node.size()], dtype=float32)
    dist[0, :] = [.95,0.05]
    dist[1, :] = [0.2,0.8]
    Fg_distribution = ConditionalDiscreteDistribution(nodes=[T_node, F_G_node], table=dist)
    F_G_node.set_dist(Fg_distribution)
    # 5. Alarm Probability Distribution
    # Fa | G | P(A | Fa, G)
    # F  | F | 0.1
    # F  | T | 0.9
    # T  | F | 0.45
    # T  | T | 0.55
    dist = zeros([F_A_node.size(), G_node.size(), A_node.size()], dtype=float32)
    dist[0,0,:] = [0.9, 0.1]
    dist[0,1,:] = [0.1, 0.9]
    dist[1,0,:] = [0.55, 0.45]
    dist[1,1,:] = [0.45, 0.55]
    A_distribution = ConditionalDiscreteDistribution(nodes=[F_A_node, G_node, A_node],
                                                    table=dist)
    A_node.set_dist(A_distribution)
    
    return bayes_net

from Inference import JunctionTreeEngine
def get_alarm_prob(bayes_net, alarm_rings):
    """Calculate the marginal 
    probability of the alarm 
    ringing (T/F) in the 
    power plant system."""
    # TODO: finish this function
    A_node = bayes_net.get_node_by_name('alarm')
    engine = JunctionTreeEngine(bayes_net)
    Q = engine.marginal(A_node)[0]
    index = Q.generate_index([alarm_rings], range(Q.nDims))
    alarm_prob = Q[index]
    return alarm_prob

def get_gauge_prob(bayes_net, gauge_hot):
    """Calculate the marginal
    probability of the gauge 
    showing hot (T/F) in the 
    power plant system."""
    # TOOD: finish this function
    G_node = bayes_net.get_node_by_name('gauge')
    engine = JunctionTreeEngine(bayes_net)
    Q = engine.marginal(G_node)[0]
    index = Q.generate_index([gauge_hot], range(Q.nDims))
    gauge_prob = Q[index]
    return gauge_prob

def get_temperature_prob(bayes_net,temp_hot):
    """Calculate the probability of the 
    temperature being hot (T/F) in the
    power plant system, given that the
    alarm sounds and neither the gauge
    nor alarm is faulty."""
    # TODO: finish this function
    A_node = bayes_net.get_node_by_name('alarm')
    Fg_node = bayes_net.get_node_by_name('faulty gauge')
    Fa_node = bayes_net.get_node_by_name('faulty alarm')
    T_node = bayes_net.get_node_by_name('temperature')
    engine = JunctionTreeEngine(bayes_net)
    engine.evidence[A_node] = True
    engine.evidence[Fg_node] = False
    engine.evidence[Fa_node] = False
    Q = engine.marginal(T_node)[0]
    index = Q.generate_index([temp_hot], range(Q.nDims))
    temp_prob = Q[index]
    return temp_prob

def get_game_network():
    """Create a Bayes Net representation of the game problem.
    Name the nodes as "A","B","C","AvB","BvC" and "CvA".  """
    nodes = []
    # TODO: fill this out
    A_node = BayesNode(0, 4, name='A')
    B_node = BayesNode(1, 4, name='B')
    C_node = BayesNode(2, 4, name='C')
    AvB_node = BayesNode(3, 3, name='AvB')
    BvC_node = BayesNode(4, 3, name='BvC')
    CvA_node = BayesNode(5, 3, name='CvA')
    # Match A v B
    AvB_node.add_parent(A_node)
    AvB_node.add_parent(B_node)
    A_node.add_child(AvB_node)
    B_node.add_child(AvB_node)
    # Match B v C
    BvC_node.add_parent(B_node)
    BvC_node.add_parent(C_node)
    B_node.add_child(BvC_node)
    C_node.add_child(BvC_node)
    # Match C v A
    CvA_node.add_parent(C_node)
    CvA_node.add_parent(A_node)
    C_node.add_child(CvA_node)
    A_node.add_child(CvA_node)
    
    nodes = [A_node, B_node, C_node, AvB_node, BvC_node, CvA_node]
    
    prior_skill_dist = [0.15, 0.45, 0.3, 0.1]
    
    A_skill_dist = DiscreteDistribution(A_node)
    index = A_skill_dist.generate_index([], [])
    A_skill_dist[index] = prior_skill_dist
    A_node.set_dist(A_skill_dist)
    
    B_skill_dist = DiscreteDistribution(B_node)
    index = B_skill_dist.generate_index([], [])
    B_skill_dist[index] = prior_skill_dist
    B_node.set_dist(B_skill_dist)
    
    C_skill_dist = DiscreteDistribution(C_node)
    index = C_skill_dist.generate_index([], [])
    C_skill_dist[index] = prior_skill_dist
    C_node.set_dist(C_skill_dist)
    # Match Prob Distribution
    # P(T1vT2 | T1, T2)
    # T1 | T2 | T1   | T2   | Tie
    # 0  | 0  | 0.1  | 0.1  | 0.8
    # 0  | 1  | 0.2  | 0.6  | 0.2
    # 0  | 2  | 0.15 | 0.75 | 0.1
    # 0  | 3  | 0.05 | 0.9  | 0.05
    # 1  | 0  | 0.6  | 0.2  | 0.2
    # 1  | 1  | 0.1  | 0.1  | 0.8
    # 1  | 2  | 0.2  | 0.6  | 0.2
    # 1  | 3  | 0.15 | 0.75 | 0.1
    # 2  | 0  | 0.75 | 0.15 | 0.1
    # 2  | 1  | 0.6  | 0.2  | 0.2
    # 2  | 2  | 0.1  | 0.1  | 0.8
    # 2  | 3  | 0.2  | 0.6  | 0.2
    # 3  | 0  | 0.9  | 0.05 | 0.05
    # 3  | 1  | 0.75 | 0.15 | 0.1
    # 3  | 2  | 0.6  | 0.2  | 0.2
    # 3  | 3  | 0.1  | 0.1  | 0.8
    match_dist = zeros([A_node.size(), B_node.size(), AvB_node.size()], dtype=float32)
    match_dist[0, 0,:] = [0.1, 0.1, 0.8]
    match_dist[0, 1,:] = [0.2, 0.6, 0.2]
    match_dist[0, 2,:] = [0.15, 0.75, 0.1]
    match_dist[0, 3,:] = [0.05, 0.9, 0.05]
    match_dist[1, 0,:] = [0.6, 0.2, 0.2]
    match_dist[1, 1,:] = [0.1, 0.1, 0.8]
    match_dist[1, 2,:] = [0.2, 0.6, 0.2]
    match_dist[1, 3,:] = [0.15, 0.75, 0.1]
    match_dist[2, 0,:] = [0.75, 0.15, 0.1]
    match_dist[2, 1,:] = [0.6, 0.2, 0.2]
    match_dist[2, 2,:] = [0.1, 0.1, 0.8]
    match_dist[2, 3,:] = [0.2, 0.6, 0.2]
    match_dist[3, 0,:] = [0.9, 0.05, 0.05]
    match_dist[3, 1,:] = [0.75, 0.15, 0.1]
    match_dist[3, 2,:] = [0.6, 0.2, 0.2]
    match_dist[3, 3,:] = [0.1, 0.1, 0.8]
                                             
    AvB_distribution = ConditionalDiscreteDistribution(nodes=[A_node, B_node, AvB_node],
                                                    table=match_dist)
    AvB_node.set_dist(AvB_distribution)
    
    BvC_distribution = ConditionalDiscreteDistribution(nodes=[B_node, C_node, BvC_node],
                                                      table=match_dist)
    BvC_node.set_dist(BvC_distribution)
    
    CvA_distribution = ConditionalDiscreteDistribution(nodes=[C_node, A_node, CvA_node],
                                                      table=match_dist)
    CvA_node.set_dist(CvA_distribution)
                        
    return BayesNet(nodes)

from Inference import EnumerationEngine
def calculate_posterior(games_net):
    """Calculate the posterior distribution of the BvC match given that A won against B and tied C. 
    Return a list of probabilities corresponding to win, loss and tie likelihood."""
    posterior = [0,0,0]
    # TODO: finish this function
    BvC_node = games_net.get_node_by_name('BvC')
    AvB_node = games_net.get_node_by_name('AvB')
    CvA_node = games_net.get_node_by_name('CvA')
    engine = EnumerationEngine(games_net)
    engine.evidence[AvB_node] = 0
    engine.evidence[CvA_node] = 2
    Q = engine.marginal(BvC_node)[0]
    posterior = Q.table
    return posterior.tolist()

import random
import numpy as np
def Gibbs_sampler(games_net, initial_value, number_of_teams=5, evidence=None):
    """Complete a single iteration of the Gibbs sampling algorithm 
    given a Bayesian network and an initial state value. 
    
    initial_value is a list of length 10 where: 
    index 0-4: represent skills of teams T1, .. ,T5 (values lie in [0,3] inclusive)
    index 5-9: represent results of matches T1vT2,...,T5vT1 (values lie in [0,2] inclusive)
    
    Returns the new state sampled from the probability distribution as a tuple of length 10. 
    Return the sample as a tuple.
    
    You will need the evidence variable for part 2d, for now there is None. 
    You can implement this any way you want (i.e as a list/tuple of evidence indices) 
    """
    A= games_net.get_node_by_name("A")      
    AvB= games_net.get_node_by_name("AvB")
    match_table = AvB.dist.table
    team_table = A.dist.table
    # TODO: finish this function
    # Generate uniform random state if initial_value is omitted
    if initial_value is None or len(initial_value) == 0:
        if initial_value is None:
            initial_value = []
        for i in range(2*number_of_teams):
            if i < number_of_teams:
                initial_value.append(random.randint(0, 3))
            else:
                initial_value.append(random.randint(0, 2))
    # Choose non evidence variable at random 
    index = random.randint(0, 2*number_of_teams - 1)
    while not evidence is None and index in evidence:
        index = random.randint(0, 2*number_of_teams - 1)
    # Sample choosen variable
    if index < number_of_teams:
        value = np.random.choice([0, 1, 2, 3], p=team_table)
        initial_value[index] = np.asscalar(value)
    else:
        p_result = match_table[initial_value[index - number_of_teams], 
                               initial_value[(index + 1 - number_of_teams) % number_of_teams]]
        value = np.random.choice([0, 1, 2], p=p_result)
        initial_value[index] = np.asscalar(value)
    sample = tuple(initial_value)
    return sample

def converge_count_Gibbs(bayes_net, initial_state, match_results, number_of_teams=5):
    """Calculate number of iterations for Gibbs sampling to converge to a stationary distribution. 
    And return the likelihoods for the last match. """
    prob_win = 0.0
    prob_loss = 0.0
    prob_tie = 0.0
    posterior = [prob_win,prob_loss,prob_tie]
    # TODO: finish this function
    N = 100000
    delta = 0.0001
    # Indicies of evidence variables
    evidence = (5, 6, 7, 8)
    match1 = 5
    match2 = 6
    match3 = 7
    match4 = 8
    match5 = 9
    win = 0
    loss = 1
    tie = 2
    outcome_count = {win: 0, loss: 0, tie: 0}
    burn_in = 1000
    nth_sample = 5
    min_count = 200
    # Initialize initial state if necessary
    if initial_state is None or len(initial_state) == 0:
        if initial_state is None:
            initial_state = []
        for i in range(0, number_of_teams):
            initial_state.append(0)
        initial_state = initial_state + match_results
        for i in range(len(initial_state), 2*number_of_teams):
            initial_state.append(0)
    else:
        initial_state[match1] = match_results[match1 - number_of_teams]
        initial_state[match2] = match_results[match2 - number_of_teams]
        initial_state[match3] = match_results[match3 - number_of_teams]
        initial_state[match4] = match_results[match4 - number_of_teams]
    # Collect nth samples after burn in
    for count in range(1, N + 1):
        sample = Gibbs_sampler(bayes_net,
                               initial_state,
                               number_of_teams,
                               evidence)
        if count > burn_in and count % nth_sample == 0:
            outcome_count[sample[match5]] += 1
            total_samples = float(outcome_count[win] + outcome_count[loss] + outcome_count[tie])
            prob_win =  outcome_count[win] / total_samples
            prob_loss = outcome_count[loss] / total_samples
            prob_tie = outcome_count[tie] / total_samples
            expected_outcome_diff = [abs(prob_win - posterior[win]),
                                     abs(prob_loss - posterior[loss]),
                                     abs(prob_tie - posterior[tie])]
            if count > min_count + burn_in \
                and sum(expected_outcome_diff) < delta:
                return count, [prob_win, prob_loss, prob_tie]
            posterior = [prob_win, prob_loss, prob_tie]
        initial_state = list(sample)
    return count, posterior

def complexity_question():
    # TODO: write an expression for complexity
    complexity = 'O(4^n)'
    return complexity

def MH_sampler(games_net, initial_value, n=5, evidence=None):
    """Complete a single iteration of the MH sampling algorithm given a Bayesian network and an initial state value. 
    initial_value is a list of length 10 where: 
    index 0-4: represent skills of teams T1, .. ,T5 (values lie in [0,3] inclusive)
    index 5-9: represent results of matches T1vT2,...,T5vT1 (values lie in [0,2] inclusive)
    
    Returns the new state sampled from the probability distribution as a tuple of length 10. 
    """
    A= games_net.get_node_by_name("A")      
    AvB= games_net.get_node_by_name("AvB")
    match_table = AvB.dist.table
    team_table = A.dist.table    
    # TODO: finish this function
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    AvB = 5
    BvC = 6
    CvD = 7
    DvE = 8
    EvA = 9
    # Generate uniform random state if initial_value is omitted
    if initial_value is None or len(initial_value) == 0:
        if initial_value is None:
            initial_value = []
        for i in range(2*n):
            if i < n:
                initial_value.append(random.randint(0, 3))
            else:
                initial_value.append(random.randint(0, 2))
    sample = tuple(initial_value)
    # Generate candidate sample
    candidate = []
    for i in range(2*n):
        if not evidence is None and i in evidence:
            candidate.append(initial_value[i])
        else:
            if i < n:
                candidate.append(random.randint(0,3))
            else:
                candidate.append(random.randint(0,2))
        
    alpha = random.uniform(0,1)
    # Calculate Probabilities
    p_current = match_table[initial_value[E], initial_value[A], initial_value[EvA]] \
        * match_table[initial_value[D], initial_value[E], initial_value[DvE]] \
        * match_table[initial_value[C], initial_value[D], initial_value[CvD]] \
        * match_table[initial_value[B], initial_value[C], initial_value[BvC]] \
        * match_table[initial_value[A], initial_value[B], initial_value[AvB]] \
        * team_table[initial_value[E]] \
        * team_table[initial_value[D]] \
        * team_table[initial_value[C]] \
        * team_table[initial_value[B]] \
        * team_table[initial_value[A]]
    p_candidate = match_table[candidate[E], candidate[A], candidate[EvA]] \
        * match_table[candidate[D], candidate[E], candidate[DvE]] \
        * match_table[candidate[C], candidate[D], candidate[CvD]] \
        * match_table[candidate[B], candidate[C], candidate[BvC]] \
        * match_table[candidate[A], candidate[B], candidate[AvB]] \
        * team_table[candidate[E]] \
        * team_table[candidate[D]] \
        * team_table[candidate[C]] \
        * team_table[candidate[B]] \
        * team_table[candidate[A]] 
    # Accept/Reject Candidate
    if alpha < p_candidate/p_current:
        sample = tuple(candidate)
    return sample

def converge_count_MH(bayes_net, initial_state, match_results, number_of_teams=5):
    """Calculate number of iterations for MH sampling to converge to any stationary distribution. 
    And return the likelihoods for the last match. """
    count=0
    prob_win = 0.0
    prob_loss = 0.0
    prob_tie = 0.0
    posterior = [prob_win,prob_loss,prob_tie]
    # TODO: finish this function
    N = 100000
    delta = 0.0001
    # Indicies of evidence variables
    evidence = (5, 6, 7, 8)
    match1 = 5
    match2 = 6
    match3 = 7
    match4 = 8
    match5 = 9
    win = 0
    loss = 1
    tie = 2
    outcome_count = {win: 0, loss: 0, tie: 0}
    burn_in = 1000
    nth_sample = 5
    min_count = 200
    # Initialize initial state if necessary
    if initial_state is None or len(initial_state) == 0:
        if initial_state is None:
            initial_state = []
        for i in range(0, number_of_teams):
            initial_state.append(0)
        initial_state = initial_state + match_results
        for i in range(len(initial_state), 2*number_of_teams):
            initial_state.append(0)
    else:
        initial_state[match1] = match_results[match1 - number_of_teams]
        initial_state[match2] = match_results[match2 - number_of_teams]
        initial_state[match3] = match_results[match3 - number_of_teams]
        initial_state[match4] = match_results[match4 - number_of_teams]
    # Collect nth samples after burn in
    for count in range(1, N + 1):
        sample = MH_sampler(bayes_net,
                               initial_state,
                               number_of_teams,
                               evidence)
        if count > burn_in and count % nth_sample == 0:
            outcome_count[sample[match5]] += 1
            total_samples = float(outcome_count[win] + outcome_count[loss] + outcome_count[tie])
            prob_win =  outcome_count[win] / total_samples
            prob_loss = outcome_count[loss] / total_samples
            prob_tie = outcome_count[tie] / total_samples
            expected_outcome_diff = [abs(prob_win - posterior[win]),
                                     abs(prob_loss - posterior[loss]),
                                     abs(prob_tie - posterior[tie])]
            if count > min_count + burn_in \
                and sum(expected_outcome_diff) < delta:
                return count, [prob_win, prob_loss, prob_tie]
            posterior = [prob_win, prob_loss, prob_tie]
        initial_state = list(sample)
    return count,posterior

def compare_sampling(bayes_net,initial_state, match_results, n):
    """Compare Gibbs and Metropolis-Hastings sampling by calculating how long it takes for each method to converge 
    to the provided posterior."""
    Gibbs_count = 0
    MH_count = 0
    # TODO: finish this function
    Gibbs_count, Gibbs_posterior = converge_count_Gibbs(game_net, initial_state, match_results, number_of_teams=5)
    
    MH_count, MH_posterior = converge_count_MH(game_net, initial_state, match_results, n)
    
    return Gibbs_count, MH_count

def sampling_question():
    """Question about sampling performance."""
    # TODO: assign value to choice and factor
    n = 5
    game_net = get_game_network()
    initial_state = [0 for i in range(0,2*n)]
    match_results = [0,0,1,1]
    Gibbs_count, MH_count = compare_sampling(game_net, initial_state, match_results, n)
    choice = 0
    print (Gibbs_count, MH_count)
    if MH_count < Gibbs_count:
        choice = 1
    options = ['Gibbs','Metropolis-Hastings']
    factor = float(Gibbs_count) / float(MH_count)
    return options[choice], factor