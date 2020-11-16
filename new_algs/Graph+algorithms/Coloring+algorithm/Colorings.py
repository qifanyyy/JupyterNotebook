'''
Colorings

Tests whether or not a given coloring is proper and  determines
whether or not a given graph has chromatic number of at most 3. Also
makes a proper vertex coloring using the greedy algorithm.

@author: Kehlsey Lewis
'''

'''
This has two inputs: one a graph, and the other a
labelling of the vertices. It determines whether or not the labelling is a proper vertex-coloring of the given
graph. 
'''


def is_proper(graph, color):
    
    answer = True;
    
    if graph == {}: #not proper if empty
        answer = False
    
    for node in graph:
        for edge in graph[node]:
            if color[edge] == color[node]: #adjacent vertex cannot have the same color
                answer = False             
    return answer


'''
Takes in a graph as its input, and then returns all possible
vertex-colorings
'''


def three_color(graph):
    
    coloring = {}
    answer = []
    
    
    for node in graph:
        coloring[node] = 1 #sets default color value as 1 for all
    answer.append(dict(coloring)) #turns into dictionary and adds to answer list
      
    i = 0
    loop = len(graph)**3
    
    #loops through list x3 to get all possible combinations
    while i < loop:
        for node in coloring:
            if coloring[node] < 3: #makes sure color can be adjusted
                coloring[node] = coloring[node] + 1 #adds one to existing color
                answer.append(dict(coloring)) #turns coloring into dictionary and adds to answer list

            else: #resets color to 1 if it is >3
                coloring[node] = 1 
        i = i + 1 #adds to counter
    return answer


'''
takes in a graph as its input, and then returns all possible
vertex-colorings. it will return the Boolean value
True if it is, and False if it is not.

'''


def is_three_color(graph):
    answer = True
    
    for node in graph:
        if len(graph[node]) > 2: #can't be a 3 color graph if >2 connecting vertexes
            answer = False

    return answer


'''
Takes in a weighted graph and then determines whether or not the labelling is a proper edge-coloring.
It will return the Boolean value True if it is, and False if it is not.

'''


def is_proper_edge(graph):
    answer = True
    
    if graph == {}: #not proper if empty
        answer = False
    
    for node in graph:
        for edge in graph[node]:  
            for thing in graph[edge[0]]:
                if thing[0] != node and thing[1] == edge[1]: #checks to see if adjacent edge has the same color
                    answer = False #answer is false if edges have same color

    return answer


'''
Takes in two inputs, one a graph and the other an ordering
of the vertices, and returns the proper vertex-coloring produced by the greedy algorithm.

'''


def greedy(graph, order):  
    answer = {} #keeps track of colors assigned
    
    answer[order[0]] = 1 #first vertex assigned a 1
    
    for node in order: #loops through ordered vertexes
         
        answer[node] = 1 #starts vertex with color of 1
        adjacentEdges = [] #makes list to keep track of adjacent edges
         
         
        for edge in graph[node]: #runs through edges listed for node in given graph
            if edge in answer:
                adjacentEdges.append(answer[edge]) #adds adjacent edges to list
        
        if answer[node] in adjacentEdges:
            answer[node] = answer[node] + 1 #if color is already used will add 1
            while answer[node] in adjacentEdges: #keeps adding 1 until color is unique
                answer[node] = answer[node] + 1

    return answer


#print(is_proper_edge({}))
#print(is_three_color({"A" : ["B", "C"], "B" : ["A", "C"], "C" : ["A", "B"]}))
#print(is_three_color({"A" : ["B", "C", "D"], "B" : ["A", "C", "D"], "C" : ["A", "B", "D"], "D" : ["A", "B", "C"]}))
#print(is_proper({"A" : ["B", "C"], "B" : ["A", "C"], "C" : ["A", "B"]}, {"A" : 1, "B" : 2, "C" : 3}))
#print(three_color({"A" : ["B"], "B" : ["A"]}))
#print(greedy({"A" : ["B", "C"], "B" : ["A"], "C" : ["A"]}, ["A", "B", "C"]))
#print(greedy({"A" : ["B"], "B" : ["A", "C"], "C" : ["B", "D"], "D" : ["C"]}, ["A", "D", "B", "C"]))
