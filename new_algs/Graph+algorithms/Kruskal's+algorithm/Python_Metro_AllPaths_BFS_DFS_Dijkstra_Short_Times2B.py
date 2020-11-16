#===============
##### PROJECT : 1) implement Graph of [station_names]
# -vertices = station_index, station_names
# -edges = [station_I1, station_I2, distance]
#           2) Find a possible l_path (not necessarily the shortest): Breadth-First-Search or Depth-First search
# NB : distances are not used here - though declared a member of class Graph
### At first I simplify the pb by taking only IDs
#===============

#================
##### ALGO:
# Transform the Metromap data into (vertices, edges) into a directed Graph
# I = dict_Connect <class AdjacencyList> ={k=root:val=[pair of adjacent nodes]}
# O = dict_ = {list[path(source, dest)]}
# METHOD : version of BFS for cycled graph since Metro has looping lines
# to prevent infinite loops
# NB : no need of a Graph class in my code
# ResultFile = MetroPossiblePaths.txt 
#================

#================
##### DATA :
## INPUT :
#RAW level : metro.complet.txt BLOCK1:Vertices[nodenumber, station_name] & BLOCK2:[N1,N2]
#NB : a 'station_name' may have several Nodes associated with
#INTERMEDIATE1 : listVertices[[N1, name1],[N2,name1], [N3, name2], ... ]
#INTERMEDIATE2 : dictData {k=NodeNmb:val=[N]}
## DATA REPRESENTATION
#GRAPH : {k:[NodeNmb (string), station_name (string)]:val=[Ni, Nj]}
#================

#================
#### GLOBAL VARIABLES :
#    l_Station list of station IDs and names
#    l_Connect list of station IDs and adjacent node 
#    dict_Stations dict of ID and station_name
#    dict_Connects dict of ID and list of adjacent nodes
#### LOCAL VARIABLES of bfs_paths_cycle fcn:
#    l_queue = queue <list> of paths
#    l_path = 1st l_path dequeued from queue
#    s_current_neighbour self-explanatory
#    l_new_path = local in loop over neighbours to be appended with s_current_neighbour if not in path
#### FUNCTIONS :
#    bfs_paths_cycle(dict_Connects, s_source, s_dest)

#### Badr version : http://stackoverflow.com/questions/28343513/depth-first-search-in-python-including-cycles
#Uses Queue lib

#================

#================
# TO DO STILL for Metro project:
# other GraphTraversal Algo
# and Performance assesment
# Which Algo is more efficient here?
#================

#================
############################ CODE ###########################
#================
import numpy as np
import matplotlib as mlp
import string
import codecs #to hande utf8 encoding issue
import sys

'-------------------------------------------------------'
'----------- DATA READING FROM 1 ASCII FILE ------------'
'-------------------------------------------------------'

#STEP1: Data reading --> vertices, edges -->l_Station=[ [stationnID,stationName],... ]<class 'list'>
#                                        -->l_Connect=[ [nodeID,adjacentNode N],... ]   
#========
lDataNodes=[]
l_Station=[]
l_Connect=[]
l_ConnecTimes=[] ##N1, N2, connectionTime

bFlagVertex=0
bFlagEdge=0

#with codecs.open('Metro_complet.txt', 'r',encoding='utf8') as fp:
with codecs.open('Metro_complet.txt', 'r') as fp:
    for i, line in enumerate(fp.readlines()):
        line_split = line.split()
        if 'Vertices' in line:
            bFlagVertex = 1
            continue  #go next line on for
        if 'Edges' in line:
            bFlagVertex = 0
            bFlagEdge = 1
            continue
            #process Vertices
        if bFlagVertex == 1:
            station_id = int(line_split[0])           #int
            station_name = ' '.join(line.split()[1:]) #1 string 'Chatelet les Halles' par ex 
            l_Station.append([station_id,station_name])
        if bFlagEdge == 1:
            #l_Connect.append([int(line_split[0]), int(line_split[1])])
            l_Connect.append([line_split[0], line_split[1]])
            l_ConnecTimes.append([line_split[0], line_split[1], line_split[2]])

print(l_Station[0:5])  #OK here
#[[0, 'Abbesses'], [1, 'Alexandre Dumas'], [2, 'Alma Marceau'], [3, 'Alésia'], [4, 'Anatole France']]
print(l_Connect[0:10])
#[[0, 238], [0, 159], [1, 12], [1, 235]]
print(l_ConnecTimes[0:10])  ##OK
##sys.exit()

#=======
#STEP2: change Data structure into Dictionnary to be used for #graph processing
#=======
#lDataNodes <list> --> dictInput <dictionary> (|--> graph type to process) 

'--------Build dict_Stations ------'
dict_Stations = {}
for item in l_Station:
    key = int(item[0]) #ok
    dict_Stations[key] = item[1]
print('dic_stations',dict_Stations) #OK
###sys.exit()

'--------Build dict_Connects for BFS, DFS and Shortest------'
dict_Connects = {}
for item in l_Connect:
    key = "/".join(item[:-1])
    dict_Connects.setdefault(key, []).append(item[-1])
print(dict_Connects)

#----- transform : dict(k:[values]) into dict(k:set([values])) : set type needed for dfs_paths and bfs_paths ------
dict_Connects = {k:set(v) for k,v in dict_Connects.items()}


'--------Build dict_Connects for DIJKSTRA (positive edge weights)------'
'--------to find the closest path between source and destination-------'
dict_ConnecTimes = {}
for item in l_ConnecTimes:
    key = "/".join(item[:-2]) #should not be int!!!!
    if item[-1]=='120.0':
        item[-1]='120'
    l_temp = list((item[-2],item[-1]))
    dict_ConnecTimes.setdefault(key, []).append(l_temp)
print('dict_ConnecTimes',dict_ConnecTimes)
###dict_ConnecTimes {'93': [['19', '33'], ['97', '45'], ['94', '120']],
## '28': [['29', '79']], '232': [['209', '54'], ['348', '46'], ['231', '120']], 
## '145': [['54', '51'], ['373', '55']], '231': [['368', '40'], 
##['106', '29'], ['232', '120']],...]
##sys.exit()


'--------------------------------------------------------------------------'
'-------- For the metro project, BFS turns out to be faster than DFS ------'
'--------------------------------------------------------------------------'
'--- add condition to avoid cycling inf loop -----'
'--- bi-directional unweighted graph : time unused'
def bfs_paths_yield(graph, start, goal):
    queue = [(start, [start])]
    #print('type(queue)',type(queue))
    #print('queue',queue)
    while queue:
        gcount=0
        (vertex, path) = queue.pop(0)
        #print('vertex',vertex)
        #print('path',path)
        for next in graph[vertex] - set(path):
            #07-oct 
            if (next in queue) or (next in path):
                gcount+=1
                break
            #print('next',next)
            elif (next == goal):
                #print('goal',goal)
                yield path + [next]
                print(path + [next])
            else:
                queue.append((next, path + [next]))
    ##return path

'---------  Shortest path for Bfs -------'
def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths_yield(graph, start, goal))
    except StopIteration:
        return None


#-------------------------------------------------
#----------------- DFS for Metro -----------------
#-------------------------------------------------
#--- add condition to avoid cycling inf loop -----
#--- bi-directional unweighted graph : time unused
#--- code from Eddmann --------------------------

'---------  Paths searching with DFS and generator next ----'
def dfs_paths(graph, start, goal):
    i_dfs_counter = 0
    limit=100
    i_len_lim=20
    stack = [(start, [start])]
    while stack and i_dfs_counter<limit:
        i_dfs_len = 0
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                i_dfs_counter+=1
                yield path + [next]
                print(path + [next])
            if (next in path) or i_dfs_len>i_len_lim:
                break
            else:
                i_dfs_len+=1
                stack.append((next, path + [next]))


'---------  Paths searching with DFS recursive ----'
def dfs_paths_recursive(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        print(path)
        yield path
    for next in graph[start] - set(path):
        if next in path:
            break
        else:
            yield from dfs_paths_recursive(graph, next, goal, path + [next])


'---------  Shortest path for Dfs -------'
def shortest_path_dfs(graph, start, goal):
    try:
##        return next(dfs_paths_recursive(graph, start, goal,None))
        return next(dfs_paths(graph, start, goal))
    except StopIteration:
        return None    


'-------- DIJKSTRA : Weighted graph with Times --> dict_ConnecTimes ----------'
def dijkstra(graph,start,target):
    print('in dijkstra')
    inf = 0
    for u in graph: 
##        print('first loop dijkstra')
##        print('graph[u]',graph[u]) #set
##        print('len graph u',len(graph[u]))
##        for v ,w in graph[u]:
##        for v,w in list(graph[u]):
##        l_temp = list(graph[u])
        l_temp = graph[u]      
##        print('l_temp',l_temp)
        for ii in range(len(l_temp)):
            v = l_temp[ii][0]
            w = l_temp[ii][1]
##            print('second loop dijkstra')
##            print('v',v)
##            print('w',int(w))
##            sys.exit()
            inf = inf + int(w)
##            print('inf',inf)
##            sys.exit()
    dist = dict([(u,inf) for u in graph])
##    print(dist,'dist')
##    sys.exit()
    prev = dict([(u,None) for u in graph])
    q = graph.keys()
    dist[start] = 0
    #helper function
    def x(v):
        return dist[v]

    print('q',q)
    ##sys.exit()
    while q != []:
        u = min(q, key=x)
        q.remove(u)
        for v,w in graph[u]:
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    #way
    trav = []
    temp = target
    while temp != start:
        trav.append(prev[temp])
        temp = prev[temp]
    trav.reverse()
    trav.append(target)
    print('Dijkstra',trav)
    print('Dijkstra dist',dist[target])
    return trav,dist[target]  # if we want to use another example .join(map(str, trav)),dist[target]


#---------------------------------------
#----------------- RUN -----------------
#---------------------------------------

#------- PRINT 30 FIRST ALL PATHS -----
dict_graphMetro = dict_Connects
s_station_A='1'#'100'#'122'#'1'#'150'#'100'#'122'#slower run with these 2 '122#-to-'323'
s_station_B='165'#'345'#'323'#'165'#'345'#'165'#'323'


#'BFS' ok runs takes a while for 
s_method = 'DJK'#'BFS'

'[1]------- BFS based path finding -------'
if (s_method == 'BFS'):
    try :
        print('30 First Paths from ',s_station_A, ' to ', s_station_B, ': \n')
        BFS_paths = list(bfs_paths_yield(dict_graphMetro,s_station_A,s_station_B))  ## applied on LinkedList dict_Connects
        print(BFS_paths) 
    except :
        e = sys.exc_info()[0]
    
'[2]------- DFS based path finding -------'
if (s_method == 'DFS'):
    try:
##      print('paths generated by dfs',list(dfs_paths(dict_graphMetro, s_station_A, s_station_B)))
        print('paths generated by dfs',list(dfs_paths_recursive(dict_graphMetro, s_station_A, s_station_B, None)))
    except :
        e = sys.exc_info()[0]

'[3]------- DJK based path finding : use dict_Dijkstra !!! -------'
if (s_method == 'DJK'):
    try:
        print('paths generated by djk',list(dijkstra(dict_ConnecTimes, s_station_A, s_station_B )))
    except :
        e = sys.exc_info()[0]


#[4]------- PRINT SHORTEST PATH FROM BFS ------
try:
    print('shortest_path BFS',shortest_path(dict_graphMetro, s_station_A, s_station_B))  ##OK
    #------- GIVE STATION NAMES ASSOCIATEED TO NODES OF SORTEST ------
    for i in list(shortest_path(dict_graphMetro, s_station_A, s_station_B)):
        print('stationID',i,' ', dict_Stations[int(i)],'\n')      ##OK
except :
    e = sys.exc_info()[0]


#[6]------- PRINT SHORTEST PATH FROM DFS ------
## Not working properly for DFS here    
try:
    print('shortest_path DFS',shortest_path_dfs(dict_graphMetro, s_station_A, s_station_B))
except :
    e = sys.exc_info()[0]
    
sys.exit()

#### PRINT Id : Station_name list of 1ST SHORTEST PATH ####
##list_ID_Names_shortest = list([ list_ShortestPath[i], list_Stations[list_ShortestPath[i] ] for i in range(i_shortest_path_len))
##print()   

#////////// RESULTS : /////////
"""
----- 30 First Paths from  150  to  345 :
['150', '57', '55', '127', '109', '50', '77', '356', '227', '228', '255', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '356', '227', '228', '255', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '356', '227', '173', '67', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '68', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '70', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '177', '176', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '78', '175', '176', '281', '69', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '356', '227', '173', '67', '68', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '356', '227', '173', '67', '69', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '356', '227', '173', '67', '70', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '79', '177', '176', '281', '69', '71', '254', '345']
['150', '57', '56', '55', '127', '109', '50', '77', '78', '175', '176', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '228', '282', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '68', '70', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '68', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '69', '68', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '69', '70', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '70', '68', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '70', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '177', '176', '281', '69', '68', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '177', '176', '281', '69', '70', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '177', '176', '281', '69', '67', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '177', '175', '176', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '79', '78', '175', '176', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '78', '79', '177', '176', '281', '69', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '78', '175', '176', '281', '69', '68', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '78', '175', '176', '281', '69', '70', '71', '254', '345']
['150', '57', '55', '127', '109', '50', '77', '78', '175', '176', '281', '69', '67', '71', '254', '345']
    
SHORTEST PATH(S)
shortest_path n° 1 from  150  to  345 :  ['150', '57', '55', '127', '109', '50', '77', '356', '227', '228', '255', '71', '254', '345']
shortest_path n° 2 from  150  to  345 :  ['150', '57', '55', '127', '109', '50', '77', '356', '227', '173', '67', '71', '254', '345']

-------- 30 First Paths from  1  to  165 :
['1', '12', '213', '212', '295', '119', '120', '69', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '68', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '67', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '71', '70', '165']
['1', '12', '213', '214', '212', '295', '119', '120', '69', '70', '165']
['1', '12', '213', '215', '212', '295', '119', '120', '69', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '68', '67', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '68', '71', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '67', '68', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '67', '71', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '71', '68', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '71', '67', '70', '165']
['1', '12', '213', '212', '295', '119', '16', '331', '135', '67', '70', '165']
['1', '12', '213', '214', '212', '295', '119', '120', '69', '68', '70', '165']
['1', '12', '213', '214', '212', '295', '119', '120', '69', '67', '70', '165']
['1', '12', '213', '214', '212', '295', '119', '120', '69', '71', '70', '165']
['1', '12', '213', '214', '215', '212', '295', '119', '120', '69', '70', '165']
['1', '12', '213', '215', '212', '295', '119', '120', '69', '68', '70', '165']
['1', '12', '213', '215', '212', '295', '119', '120', '69', '67', '70', '165']
['1', '12', '213', '215', '212', '295', '119', '120', '69', '71', '70', '165']
['1', '12', '213', '215', '214', '212', '295', '119', '120', '69', '70', '165']
['1', '235', '284', '285', '305', '229', '312', '350', '8', '309', '310', '375', '165']
['1', '235', '284', '285', '305', '229', '312', '314', '343', '342', '310', '375', '165']
['1', '235', '284', '285', '305', '229', '312', '315', '344', '342', '310', '375', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '68', '67', '71', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '68', '71', '67', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '67', '68', '71', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '67', '71', '68', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '71', '68', '67', '70', '165']
['1', '12', '213', '212', '295', '119', '120', '69', '71', '67', '68', '70', '165']

-------
shortest_path n° 1 from  1  to  165 :  ['1', '12', '213', '212', '295', '119', '120', '69', '70', '165']
shortest_path n° 1 from  100  to  345 :  ['100', '99', '358', '346', '174', '221', '74', '195', '47', '148', '149', '345']
stationID 100   Duroc

stationID 99   Duroc

stationID 358   Vaneau

stationID 346   Sèvres Babylone

stationID 174   Mabillon

stationID 221   Odéon

stationID 222   Odéon

stationID 330   Saint-Michel

stationID 73   Cité

stationID 70   Châtelet

stationID 71   Châtelet

stationID 254   Pont-Marie

stationID 345   Sully Morland
"""
#Please see Result_AllPathsBFS_Metro_07oct2016.txt
