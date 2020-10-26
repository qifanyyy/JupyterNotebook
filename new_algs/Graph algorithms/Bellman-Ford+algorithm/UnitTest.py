from GraphAPI import Graph
from Dijkstra import Dijkstra
from Bell_Ford import Bellman_Ford

import networkx as nx
import random 
import time
import matplotlib.pyplot as plt
import numpy as np
import timeit


'''UnitTest for Dijkstra and Bellmand_Ford'''
class UnitTest(object): 

    '''randomly generate directed graph with networkx and use my graphAPI to replicate the graph
        if negative is True, we want to perform the size of 10 experiment of negative edges
        else, we perform the size of 100 experiment of correctness and performance'''
    def __init__(self, n, m, negative = False, generate = False):
        lowerbound = 0  #lower bound of weight
        size = 100      #sample size
        
        if generate:
            self.n = random.randint(0, 100)
            self.m = random.randint(0, 100)
        else:
            #for performance test
            self.n = n      #number of nodes
            self.m = m      #number of edges
        if negative: 
            #expand range of weight to negative numbers
            lowerbound = -100
            size = 10

        #graphs created by networks
        self.test_list =[]

        for i in range(10):
            #randomly generate directed graphs 
            G = nx.gnm_random_graph(self.n, self.m, directed = True)
            for u, v in G.edges:
                #add edges weights with range (lowerbound, 100)
                G[u][v]['weight'] = random.uniform(lowerbound, 100)
            self.test_list.append(G)

        #replicated graphs created by my graphAPI 
        self.compare_list = []

        for test in self.test_list:
            g = Graph()             #create my own graph
            for u, v in test.edges:
                # add node and weighted edge wiht my API
                g.addNode(u)
                g.addNode(v)
                g.addWeightedEdge(u, v, test[u][v]['weight'])
            self.compare_list.append(g)

   
    '''testing for correctness'''
    def correctness(self):
        #initialize the boolean value for testing Dijkstra's correctness 
        boolean = True 
        print "testing for correctness of Dijkstra..."
        #looping through graphs from my graphs and graphs by networkx
        for answer, my_graph in zip(self.test_list, self.compare_list):
            # if the graph has no nodes, break, automatically true
            if len(answer.nodes) >0:
                #pick the smallest id to be source
                source = min(answer.nodes())
                #run networkx's dijkstra
                length, path = nx.single_source_dijkstra(answer, source , weight = 'weight')
                #run my dijkstra
                my_solution = Dijkstra(my_graph)
                dist, path = my_solution.solver(source) 
                
                #getting rid of all the node that cannot be reached by the source
                for k, v in dist.items():
                    if v == float("inf"):
                        del dist[k] 

                #testing for correctness
                boolean = boolean and dist == length


        if boolean:
            print "Dijkstra test passed"
        else: 
            print "No"

        #initialize the boolean value for testing BF's correctness 
        boolean = True 
        print "testing for correctness of BF algorithm ..."
        #looping through graphs from my graphs and graphs by networkx
        for answer, my_graph in zip(self.test_list, self.compare_list):
            # if the graph has no nodes, break, automatically true
            if len(answer.nodes) >0:
                #pick the smallest id to be source
                source = min(answer.nodes())
                #run networkx's Bellman_ford
                length= nx.single_source_bellman_ford_path_length(answer, source , weight = 'weight')
                #run my Bellman_ford
                my_solution = Bellman_Ford(my_graph)
                dist, path = my_solution.solver(source) 
                
                #getting rid of all the node that cannot be reached by the source
                for k, v in dist.items():
                    if v == float("inf"):
                        del dist[k] 
                
                #correctness
                boolean = boolean and dist == length

        if boolean:
            print "Bellman_Ford test passed"
        else: 
            print "No"

    def negative(self):
        print "test for negative cycle"

        '''test for correctness'''
        self.count = 0
        for answer, my_graph in zip(self.test_list, self.compare_list):
            # if the graph has no nodes, break, automatically the same result
            if len(answer.nodes) >0:
                #run my Dijkstra
                source = min(answer.nodes())
                d_solution = Dijkstra(my_graph)
                d_dist, path = d_solution.solver(source) 

                #run my Bellman_Ford
                b_solution = Bellman_Ford(my_graph) 
                b_dist, path = b_solution.solver(source)

                # if the results are different, increment count
                if d_dist != b_dist:
                    self.count+=1


    def performance(self, dijkstra = False, bellman_Ford = False, own = False):
        #test performance between my dijskra and networks'
        if dijkstra:
            self.answer_time = 0
            self.my_time =0
            for answer, my_graph in zip(self.test_list, self.compare_list):
                # if the graph has no nodes, break, automatically true
                if len(answer.nodes) >0:
                    #measure running time for networkx' 
                    source = min(answer.nodes)
                    start = timeit.default_timer()
                    length, path = nx.single_source_dijkstra(answer, source , weight = 'weight')
                    self.answer_time += timeit.default_timer()- start 

                    #measure running time for my dijkstra
                    my_start = time.time()
                    d_solution = Dijkstra(my_graph)
                    d_dist, path = d_solution.solver(source) 
                    self.my_time += time.time() - my_start

         #test performance between my Bellman_ford and networks'
        if bellman_Ford:
            self.answer_time = 0
            self.my_time =0
            for answer, my_graph in zip(self.test_list, self.compare_list):
                # if the graph has no nodes, break, automatically true
                if len(answer.nodes) >0:
                    #measure running time for networkx'
                    source = min(answer.nodes)
                    start = timeit.default_timer()
                    length= nx.single_source_bellman_ford_path_length(answer, source , weight = 'weight')
                    self.answer_time += timeit.default_timer() - start 

                    #measure running time for my Bellman_Ford
                    my_start = time.time()
                    d_solution = Bellman_Ford(my_graph)
                    dist, path = d_solution.solver(source) 
                    self.my_time += time.time() - my_start

         #test performance between my Bellman_ford and my Dijskra
        if own:
            self.d_time =0
            self.b_time =0
            for answer, my_graph in zip(self.test_list, self.compare_list):
                # if the graph has no nodes, break, automatically true
                if len(answer.nodes) >0:
                    #measure running time for my Dijkstra
                    source = min(answer.nodes)
                    start = time.time()
                    d_solution = Dijkstra(my_graph)
                    d_dist, path = d_solution.solver(source) 
                    self.d_time += time.time() - start 

                    #measure running time for my BellmanFord
                    my_start = time.time()
                    d_solution = Bellman_Ford(my_graph)
                    dist, path = d_solution.solver(source) 
                    self.b_time += time.time() - my_start




if __name__ == "__main__":

    
    '''testing for correctness'''
    '''print 'test passsed' when our implementation is correct'''
    test = UnitTest(100, 100, generate= True)
    test.correctness()

    '''testing for negative cycle'''
    '''print "Graph has negative cycle when one graph has negative cycle"'''
    testNegative = UnitTest(100, 100, negative = True, generate= True)
    testNegative.negative()
    '''print number of cases that the Dijkstsra is different from BellmanFord'''
    print str(testNegative.count) + "/10"


    '''experiment with running time'''

    '''running Time between my Dijkstra and networkx' dijkstra in executing 100 graphs'''
    my_d_time = []
    nx_d_time = []
    #number of node range (1, 1000, 20)
    #number of edge = number of node
    for n in range(1, 1000, 20):
        test = UnitTest(n, n)
        test.performance(dijkstra = True)
        my_d_time.append(test.my_time)
        nx_d_time.append(test.answer_time)

    
    '''running Time between my BellmanFord and networkx' Bellman_Ford in executing 100 graphs'''
    my_b_time = []
    nx_b_time = []
    #number of node range (1, 1000, 20)
    #number of edge = number of node
    for n in range(1, 1000, 20):
        test = UnitTest(n, n)
        test.performance(bellman_Ford = True)
        my_b_time.append(test.my_time)
        nx_b_time.append(test.answer_time)



    # evenly sampled time at 1000ms intervals
    axis  = range(1, 1000, 20)

    # yellow: my Dijkstra; blue: my Bellman_ford; red: nx's Dijkstra; green: nx's bellmanFord
    plt.plot(axis, my_d_time, 'r-', label = 'My Dijsktra') 
    plt.plot(axis, my_b_time, 'b-', label = 'My Bellman_Ford')
    plt.plot(axis, nx_d_time, 'c-', label = 'Networkx Dijsktra')
    plt.plot(axis, nx_b_time, 'g-', label = 'Networkx Bellman_Ford')
    plt.legend(loc='upper left')
    plt.xlabel('BellmanFord')
    plt.ylabel('running time of executing 100 graphs (second)')
    plt.savefig('self-compared')
    plt.show()





