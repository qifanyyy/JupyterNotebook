# http://stackoverflow.com/questions/30464163/functional-breadth-first-search

###### Python_Veolia_DFS_YESclean.py  -- 11-oct-2016 09:00LT

#===============
# PROJECT : VEOLIA HYDRONETWORK : cf paper notes provided
#===============

#================
# ALGO:
# Transform the Water_network data into (vertices, edges) into  # an undirected Graph
# Graph Search Method : Depth-First-Search using a stack : from last stacked elt neighbors searching
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
# l_ list of station IDs and names
# l_ list of station IDs and adjacent node

# dict_Both_PandV : dict {Edge_ID:[N1,N2,Edge_ID,Flag]...]}
# dict_Edges_Flags : dict {EDGE_ID:[..[Edge,Flag]..]} adjacency list on edges  ---> used as Input in dfs_path_cycle()

#### LOCAL VARIABLES of bfs_paths_cycle fcn:
# l_stack <list> of llatest Edge visited
# l_path = 
# s_current_neighbour of a EDGE=[E_ID,Flag] format [E_ID,Flag]

#### FUNCTIONS :
# dfs_paths_cycle(dict_Connects, s_source, s_dest)
#================



#============================================================
############################ CODE ##########################
#============================================================

#========
#IMPORTS
#========
import numpy as np
import string
from collections import defaultdict
import matplotlib as mlp
import codecs #to hande utf8 encoding issue
import sys
from fcn_remove_edge_from_dict import remove_edge_from_dict
###from fcn_change_Status_Edge_in_dict import change_Status_Edge_in_dict
import os
from time import time
import psutil # must be installed first or deleted (library for calculating memory allocated in every current implementation)


#---------------------------------------------------------------------
#------------------- TIME MANAGEMENT : INIT TIME ---------------------
#---------------------------------------------------------------------
#calculate memory allocated for every implementation  !!!!need install library psutil-4.3.1 or delete line below with import psutil!!!!
process = psutil.Process(os.getpid())#delete this line if you can't donwload and install library psutil-4.3.1
print('Memory allocated for this implementation :',(process.memory_info().rss),'\n')
'----------------------------------------------------'
#define local variable for running time of algorithm
t0 = time()
print('starting time',t0)
#sys.exit()
'----------------------------------------------------'


#--------------------------------------------------------------
#---------------  DATA READING :FROM ASCII FILE ---------------
#--------------------------------------------------------------

#========
#STEP1: DATA READING --> vertices, edges, Flag
#========
#lDataNodes : list of source,destination nodes 
lDataNodes=[]

##read PIPES
bFlagPipes = False
lPipesList = []
##read VALVES
bFlagValves = False
lValvesList = []

#stackoverfow:python - Read file from and to specific lines of text
with open('Water_network.txt', "r") as fp:
	for i, line in enumerate(fp.readlines()):
		if 'PIPES' in line: 
			bFlagPipes = True
			print ("started at line in PIPES", i)
			continue
		if 'PUMPS' in line:
			print ("end at line", i)
			bFlagPipes = False
			#break
		if 'VALVES' in line: 
			bFlagValves = True
			print ("started at line in VALVES", i)
			continue
		if 'TAGS' in line:
			print ("end at line", i)
			bFlagValves = False
			break
                # process Pipeline 
		if bFlagPipes == True: 
		        #lPipesList.append(line.rstrip())
                        lInter = line.split()[0:3] #[0]=EdgeID, [1]=N1, [2]=N2
                        #print(type(lInter)) <class list>
                        lInter.append('0')         #[3]'0'=FlagPipe
                        #add Flag 'open'
                        lInter.append('open')
                        lPipesList.append(lInter)
		if bFlagValves == True: 
                        lInter = line.split()[0:3] #[0]=EdgeID, [1]=N1, [2]=N2
                        lInter.append('1')
                        lInter.append('open') 
                        lValvesList.append(lInter) #[3]'1'=FlagValve
            		
fp.close()
lPipesList=lPipesList[1:-1]
print("lPipesList")
print(lPipesList[0:20]) #
print(type(lPipesList))
"""
lPipesList
[['14T11b7', '14N353e', '14N353c', '0'], ['14T11b6', '14N35c1', '14N35bc', '0']]
"""
#OK
lValvesList=lValvesList[1:-1]
print("lValvesList")
print(lValvesList[0:20]) #
print(type(lValvesList))
#sys.exit()
#at this point, we have 2 lists of  : 1 for PIPES & 1 for VALVES


#-----------------------------------------------------------------------------------------
#----------------- DATA STRUCTURE = DICT{k=EDGE_ID:V=[...[EDGE,FLAG]...] } ---------------
#-----------------------------------------------------------------------------------------

#=======
#STEP2: change Data structure into dictionnary to be used for #graph processing
#=======
#lPipesList <list> --> dictPipes <dictionary> (|--> graph type to process)
#ADD EDGE_ID IN THE STRUCTURE
dictPipes = {}
for item in lPipesList:
    key = "/".join(item[:-4])  #-1])
    dictPipes.setdefault(key, []).append(item[1])  #Node1
    dictPipes.setdefault(key, []).append(item[2])  #Node2
    dictPipes.setdefault(key, []).append(item[0])  #EdgeID  
    dictPipes.setdefault(key, []).append(item[3])  #Flag
    dictPipes.setdefault(key, []).append(item[4])  #Status
#OK

##### TEST print PIPES dictionary
dictFirstpairs = {k: dictPipes[k] for k in sorted(dictPipes.keys())[:3]}
#print(dictFirstpairs)
#dictFirstpairs=None
#{'14T10': ['14N17ef', '14N17f0', '0'], '14T100': ['14N198e', '14N198f', '0']}

#lValvesList <list> --> dictPipes <dictionary> (|--> graph type to process)
#ADD EDGE_ID IN THE STRUCTURE
dictValves = {}
for item in lValvesList:
    key = "/".join(item[:-4])  #-1])
    dictValves.setdefault(key, []).append(item[1])  #Node1
    dictValves.setdefault(key, []).append(item[2])  #Node2
    dictValves.setdefault(key, []).append(item[0])  #Edge  
    dictValves.setdefault(key, []).append(item[3])  #Flag
    dictValves.setdefault(key, []).append(item[4])  #Status
# TEST print VALVES dictionary : cf verifications_Veolia_code.rtf

#### MERGE 2 dictionaries #####
dict_Both_PandV = dict(dictPipes)
dict_Both_PandV.update(dictValves)
# TEST print VALVES dictionary : cf verifications_Veolia_code.rtf
dictFirstpairs = {k : dict_Both_PandV[k] for k in sorted(dict_Both_PandV.keys())[:3]}
print(dictFirstpairs)
#sys.exit()


#------------------------------------------------------------------------------------------------------------------
#----------- INVERSE MAPPING USING A CONCATENATION OF NODES  Inv_dict_Nodes = {k=concat_Nodes:v=Edge_ID} ----------
#------------------------------------------------------------------------------------------------------------------

def concat_Nodes_ID(Na,Nb):
        return 'N1-'+Na+'-N2-'+Nb

Inv_dict_Temp = defaultdict(list)
for k,v in dict_Both_PandV.items():
        s_Nodes_Edge = concat_Nodes_ID(v[0],v[1]) 
        Inv_dict_Temp[s_Nodes_Edge].append(k)
Inv_dict_Both_PandV = dict(Inv_dict_Temp)
print(Inv_dict_Both_PandV)
##sys.exit() ##OK

#### DICT OF NODES ADJACENCIES
## BE CAREFUL HERE : THIS IS TO BE A NON-DIRECTED GRAPH :
## if N1 N2 in dict, we got to have N1->[[N2, FlagN1N2]...] & N2->[[N1, FlagN1N2]...] in dict_Nodes_Edges_Flags !!!!!! 
#built from dict_Both_PandV = {EdgeID:[Node1,(Node2),Flag]} !! use v[-1] to get Flag and v[-2] for Nod2
dict_Nodes_temp = defaultdict(list)
for k,v in dict_Both_PandV.items():
        dict_Nodes_temp[v[0]].append(v[1:])
        ## SWAP HERE V[0]=N1 and V[1]=N2=key : N2->[[N1, FlagN1N2]...]
        if v[2] != '0' and v[2] !='1': #there is a second node in items() associated to ID_ = k
                dict_Nodes_temp[v[1]].append(list((v[0],v[2],v[3],v[4])))  #v[0]=Node1, v[2]=edgeID, v[3]=Flag, v[4]=Status 
        
dict_Nodes_Edges_Flags = dict(dict_Nodes_temp)
print(dict_Nodes_Edges_Flags)
print('neighbours of NKSDOU04')
print(dict_Nodes_Edges_Flags['NKSDOU04'])
###sys.exit() #looks OK



#------------------------------------------------------------------------------------------------------------
#--------------- BUILD DICT OF EDGES AND FLAGS FOR ADJACENCY ON EDGES TO BE USED IN NEW BFS VERSION ---------
#------------------------------------------------------------------------------------------------------------

dict_Edges_Flags={}
list_EdgeIDs=None
list_EdgeIDs=list(dict_Both_PandV.keys())
print(list_EdgeIDs)
dict_Edges_temp = defaultdict(list)
###### BUILD DICT_EDGES_FLAGS={Edge1:[[Edge2,F2], etc ], Edge2:[[Edge1,F1], etc]} ########
### in order to apply faster BFS
for s_current_edge in list_EdgeIDs:
        Node1 = dict_Both_PandV[s_current_edge][0] #to do also with node2
        Node2 = dict_Both_PandV[s_current_edge][1] 
        #print('s_current_edge',s_current_edge)
        #print('Node1',Node1)
        #get Edges connected to Node1 from dict_NEF
        l_current_E_F = [] #list of pairs [E,F] connected to s_current_edge
        for v in dict_Nodes_Edges_Flags[Node1]:
                if v[1]!=s_current_edge:
                        l_current_E_F.append(list((v[1],v[2],v[3])))
        for v in dict_Nodes_Edges_Flags[Node2]:
                if v[1]!=s_current_edge:
                        l_current_E_F.append(list((v[1],v[2],v[3])))
        #print('l_current_E_F',l_current_E_F)
        #sys.exit()
        dict_Edges_temp[s_current_edge].append(l_current_E_F)
        dict_Edges_temp[s_current_edge] = dict_Edges_temp[s_current_edge][0] # to remove a list level!!!!
        #print('dict_Edges_temp',dict_Edges_temp)
        #sys.exit()'14T105b-2': [['14T105b-1', '0', 'open'], ['14T7d9', '0', 'open']]
        continue
dict_Edges_Flags = dict(dict_Edges_temp)
print('dict_Edges_Flags',dict_Edges_Flags)
##sys.exit() 

"""
s_current_edge 14T552-1
Node1 14N2045
l_current_E_F [['14Ted8', '0'], ['14Ted7-1', '0']]
"""


#-----------------------------------------------------------------------------------
#-------------  GRAPH SEARCH ALGO = DFS --> VALVLES LIST TO TURN OFF ---------------
#-----------------------------------------------------------------------------------

######## WANTED : for any given pipe return the list of VALVE_IDs to close ##########
## We don't want here the list of all paths from source node to 1st Node flag 1 met
#BFS without destination node but stop path(k)->new_path(k+1) iteration if current_neighbour is Valve !
### arg : graph_to_search = dict_Nodes_Edges_Flags
### function bfs_paths_cycle ti be Called twice for each node of Pipe ID
## start = [N1,'1'] or [N2,'1'] node of Pipe

####### cf doc notes_prints_VEOLIA_bfs.rtf #######
####### for prints of intermediate vars in bfs see Python_Veolia_BFS26.py ######
### USE DICT_EDGES_FLAGS  {N1:[[N2,F2],[N5,F5]], etc !!!! ####
#def remove_edge_from_dict(graph_tempo,s_vertex_EDGE):

#-----------------------------------------------------------------------------------
#---------------  CHANGE STATUS FROM 'OPEN' TO 'CLOSE' FOR VISITED EDGDES ----------
#-----------------------------------------------------------------------------------
'---------  Change status of Edge visited ---------'
def change_Status_Edge_in_dict(graph_tempo,s_vertex_EDGE):
    matched_Node = None
    ##graph_tempo[s_vertex_EDGE].remove() #remove full record of key=s_vertex_EDGE
    #del graph_tempo[s_vertex_EDGE]
    for kk,vv in graph_tempo.items():
        #print('vv',vv)  #vv [['14Tf04', '0', 'open'], ['14Tea7-2', '0', 'open']]
        #print('ln(vv)',len(vv))
        #sys.exit()
        for mm in range(len(vv)):
                #print('vv[mm][2]',vv[mm][2])
                #sys.exit()
                if vv[mm][0]==s_vertex_EDGE:
                        l_temp_list = graph_tempo[kk]
                        l_temp_list[mm][2] = 'close'  
                        graph_tempo[kk] = l_temp_list
                        #print('graph_tempo[kk]',graph_tempo[kk]) #['PNEU0001', '1', 'close']] ok
                        #sys.exit()
    # graph_tempo[kk].remove(vv)  #vv=list[Edge,Flag]
    return graph_tempo


'--------- remove edges level (l+1) from identified Valve Edge -------'
def remove_edge_from_dict(graph_tempo,s_vertex_EDGE):
    matched_Node = None
    graph_tempo[s_vertex_EDGE] = None
    ##graph_tempo[s_vertex_EDGE].remove() #remove full record of key=s_vertex_EDGE
    try:
            del graph_tempo[s_vertex_EDGE]
            for kk,vv in graph_tempo.items():
        ##        print('vv',vv)
        ##        print('graph_tempo[kk]',graph_tempo[kk])
        ##        print('s_vertex_EDGE',s_vertex_EDGE)
        ##        sys.exit()
                if vv[0]==s_vertex_EDGE:
                        graph_tempo[kk].remove(vv)  #vv=list[Edge,Flag]
##                        print('graph_tempo[kk]',graph_tempo[kk])
##                        print('s_vertex_EDGE',s_vertex_EDGE)
##                        sys.exit()
    except:
            e = sys.exc_info()[0]
##         print('no edge to remove')
##        ##continue
    return graph_tempo


##def change_Status_Edge_in_dict(graph_tempo,s_vertex_EDGE):  ##Pb : in dfs_paths_cycle it is the same level connected edges that we want to flag as 'close'!! 
##    print(type(graph_tempo[s_vertex_EDGE]))
##    print(graph_tempo[s_vertex_EDGE])  ##list of lists(3uples)
##    l_temp_list=graph_tempo[s_vertex_EDGE]
##    print(l_temp_list)
##    for kk,vv in graph_tempo.items():
##        if vv[0]==s_vertex_EDGE:
##            l_temp_list[2] = 'close'  #vv=list[Edge,Flag]
##    ##sys.exit()        
##    return graph_tempo




#---------------------------------------------------------------------------------------
#---------------------- DFS TO BE PROCESSED FOR EACH INPUT EDGES -----------------------
#---------------------- PUPOSE : ONE TIME RUN TO GET SUB-GRAPH(interconnected edges) ---
#---------------------------------------------------------------------------------------
# in case the METHOD.1 for subgraph extraction from Linked list itself wouldn't work out

def bfs_paths_levels(graph_to_search, start, i_levelMax):
##        #PURPOSE : record edges from source up to level=i_levelMax
##        #1)all all paths at same level ingraph!!
##        #2)record all edges on paths from source=edge0 choosen at center on graph
        
    l_queue = [[start]] #a list of pair(s) [Edge, flag]
    # l_queue = [start]
    list_Paths=[]  # output of this fcn
    i_Max_display = 100
    i_counter = 0
    i_full_counter=0
    l_EDGES_TOCLOSE=[]
    graph_tempo = graph_to_search
    graph_shrink={}
    l_Edge_IDs = []
##    #print('graph_tempo',graph_tempo)
##    #print('printed graph_tempo')
##    ####sys.exit()

    ta= time()
    ta_time = 0 

##    #NB !!!! arg=graph_to_search is actually an adjacencyList of <class dict>
    while l_queue and ta_time<10.:
        i_full_counter+=1
##        # Gets the first l_path in the l_queue
        l_path = l_queue.pop(0)  #dequeue first l_path, not just a node!!
##        # Gets the last item values in the l_path !!
##        # NB : in Metro: it was [-1]-> final Node of path since previous ones were addressed already
##        # NB : in Veolia : catch last 3-uplets (new node) from l_path list and [0]=NodeID from last 3-uplets
        '----- get vertex infos ------'
        b_vertex_STATUS=l_path[-1][2] #3rd elt=STATUS
        b_vertex_FLAG=l_path[-1][1] #3rd elt=FLAG
        s_vertex_EDGE=l_path[-1][0] #2nd elt=EDGE_ID of last elt of path
    
        #dequeued path skip if s_vertex_EDGE in l_VALVEID
##        if s_vertex_EDGE in l_EDGES_TOCLOSE or b_vertex_STATUS=='close' or s_vertex_EDGE in l_Edge_IDs:
        if s_vertex_EDGE in l_EDGES_TOCLOSE or b_vertex_STATUS=='close':
                continue  #dequeue next path in l_queue

        #Test to store l_path in list_Paths and Edge in l_VALVEID
        '------ current vertex is a VALVLE ------'
        if b_vertex_FLAG == '1':
            i_counter +=1
            # The way the code is built makes it returns first the shortest path(s)
            if l_path not in list_Paths:
                    list_Paths.append(l_path)
##                    print('path ending by valve')
##                    print(l_path)
                    l_EDGES_TOCLOSE.append(s_vertex_EDGE)
##                    print('l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)
##                    #sys.exit()
##                    ### to do here : remove records containing "l_path.EdgeID" from dict_Nodes_Edges_Flags
##                    #dict_Nodes_Edges_Flags
##                    # TO REMOVE in dict_N_E_F N1-->[..., [N2,EdgeID,Flag], ...] and viceversa on key=N2 = elagage du graph temporaire
##                    # PB ici : il faut le faire sur un dict temporaire!!
##                    #remove from graph_tempo [N1->[list_of_neighbours[3-uplets]] , N2->[list_of_neighbours[3-uplets]]]
                    graph_tempo=change_Status_Edge_in_dict(graph_tempo,s_vertex_EDGE)
                    graph_shrink=remove_edge_from_dict(graph_tempo, s_vertex_EDGE) #remove key and Edge in values also from dictionary
                    graph_tempo=graph_shrink


        '-----  BLOC2 : loop on level+1 connected nodes from s_Vertex_Node -----'
##            # We check if the current node is already in the visited nodes set in order not to recheck it
##            # Loop on adjacent Nodes#### NEIGHBOURS ### from vertex Node in the graph(dict) (1st arg if this fcn)
##      #key=Edge=vertex_EDGE --> [ [EdgeIDpn, Flag],[Edge, Flag] etc]
        for s_current_neighbour in graph_tempo.get(s_vertex_EDGE,[]):
##                # BFS Algo builts-up several paths in // with an update one-by-one node neighbour if not if path already
##                # and queue them one-after-another

                '------- get current edge infos ------'
                s_current_Edge = s_current_neighbour[0] ## s_current_neighbour is a 3-uple [NodeID, EdgeID, Flag]
                s_current_Flag = s_current_neighbour[1]
                s_current_Status = s_current_neighbour[2]
##                ## extract Edge list from .items in graph_to_search=dict_E_F
##                ## from l_path =[[2uple_1],[2uple_2],...,[2uple_n]]--> [Edges 1 to n]!!!!

                '------- list Edge IDs on current path ----'
                a = l_path
                [l_Edge_IDs.append(a[i][0]) for i in range(len(a))]
##                ##l_Edge_IDs = l_path[:]  ##NB:Flag is l_path[:][1]
##                # this condition avoids inifinite loops : ie Node_neighbour passing by l_path !!
                
                '------ append edge current neighbour in path under condition -----'
                if s_current_Edge not in l_Edge_IDs and s_current_Edge not in l_EDGES_TOCLOSE and s_current_Status!='close':
                        l_new_path = list(l_path) #at each iteration, go back to previous state of l_path = l_path
##                        # after having built-up l_new_path := l_path + s_current_neighbour (if was not in l_path)
                        l_new_path.append(s_current_neighbour) #s_current_neighbour i a 3-uple list
                        l_queue.append(l_new_path)
        '----- time cal ----'
        ta_end= time()
        ta_time += (ta_end-ta)
        ta = ta_end
        ##print ('runtime : ',ta_time)

    '--------  Print final result ------'
    print('---Pile Leakage on ',start[0])
    print('---Number of valves to close:',len(l_EDGES_TOCLOSE))
    print('---l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)
    
    '------ save result ----'    
    return list_Paths 
        


#---------------------------------------------------------------------------------------
#---------------------- DFS TO BE PROCESSED FOR EACH INPUT EDGES -----------------------
#---------------------------------------------------------------------------------------
def dfs_paths_cycle(graph_to_search, start):
    '------ Initialize stack, EDGES_TO_CLOSE list, temporary graph ---'
    l_stack = [(start,[start])] #a list of pair(s) [Edge, flag]
    list_Paths=[]  #stores the path of a Valve = output of this fcn
    i_counter = 0
    i_full_counter=0
    l_EDGES_TOCLOSE=[]
    visited = set()
    graph_tempo = graph_to_search
    graph_shrink={}
    allEdgesMet = []
    i_Nb_neighbors = 0
    '----------------------------------------------------------------'

##    #!!!! oct11th,4:40pm  KEY POINT IN TOPOLOGY OF HYDRONET : if close EdgeN(k+1):Flag=='1' that has joint neighbors Edges(k) w/r Edge0(k-1) then need to pop-out
##    # the other neighbors out of stack and save them in l_EDGES_TOCLOSE !!!!
##    #NB !!!! arg=graph_to_search is actually an adjacencyList of <class dict>
    
    '-------------- Loop over stack until empty !! ------------------'
    while l_stack:
        ##l_stack: contains only final Edge info on each branch and not the full pth each time!
        i_full_counter+=1
        # Gets the last l_path stack
        #KEEP ONLY LAST [EDGE,FLAG] PAIR IN STACK
        (Edge,l_path) = l_stack.pop()  #dequeue first l_path, not just a node!!
        b_FLAG=Edge[1]
        s_EDGE=Edge[0]
        s_STATUS=Edge[2]
        allEdgesMet.append(Edge)
        i_Nb_neighbors=0
##        #print('l_path',l_path)
##        #print('Edge',Edge)
##        #sys.exit()

        '------------------- BLOC.1 current Edge check if Valve if yes process ---------'
        
        '---------- Check the status of current EDGE in regards of visited Valve  ------'
        if (s_EDGE in l_EDGES_TOCLOSE or s_EDGE in visited or s_STATUS=='close'):
##        if ((s_EDGE in l_EDGES_TOCLOSE or s_EDGE in visited) or s_EDGE in allEdgesMet):
##        if (s_EDGE in l_EDGES_TOCLOSE or s_STATUS=='close'):
                continue  #dequeue next path in l_queue

        '---------- Process the following only if currrent Edge labeled as Valve --------'
        #Test to store l_path in list_Paths and Edge in l_VALVEID
        if b_FLAG == '1':
            i_counter +=1
            '------ check if path already registered ------'
            if l_path not in list_Paths:
                    list_Paths.append(l_path)
                    visited.add(s_EDGE)
                    l_EDGES_TOCLOSE.append(s_EDGE)
                    #
                    graph_tempo=change_Status_Edge_in_dict(graph_tempo, s_EDGE) #from 'open' to 'close' on s_EDGE as adjacent edge from a kk=other Edge
                    graph_temp=remove_edge_from_dict(graph_tempo,s_EDGE)
##                    try:
##                            del graph_tempo[s_EDGE] ##cut branch=Edge
##                    except:
##                            continue

##                    #unstack as well related neighbors from same edge!!
##                    print('before for l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)

                    '------- loop for the current valve Edge over the same level neighbors ---------'
                    #### [1]level (k+1) neighbors : s_EDGE --> get children using graph_tempo.get(s_EDGE,[])  and set them to visited!!
                    #### use s_prev_EDGE and not s_EDGE !!
##                    if len(l_path)>3:
##                            print('l_path',l_path)
##                            sys.exit()
                    for s_current_neighbour in graph_tempo.get(s_prev_EDGE,[]):
                            visited.add(s_current_neighbour[0])
                            allEdgesMet.append(s_current_neighbour)
                            i_Nb_neighbors+=1
                            #print('s_current_neighbour',s_current_neighbour)
##                            s_current_neighbour ['SVIBV5', '1', 'open']
##                            s_current_neighbour ['PNEU0001', '1', 'close']  #OK
##                            s_current_neighbour ['14Ta00', '0', 'open']
##                            s_current_neighbour ['14T9f8-1', '0', 'open']
##                            ### in next for
##                            i_Nb_neighbors 4
##                            Edge ['SVIBV5', '1', 'open']
                            

                            #### [2]s_EDGE --> add to visited tracker all same level neighbors calculated in next bloc #####
                    for ii in range(i_Nb_neighbors-1):
                            #print('i_Nb_neighbors',i_Nb_neighbors)

                            '---------- from previous iteration : in BLOC 2 : in stack((same level Edges) as Edge unstacked) --------'
                            (Edge,l_path) = l_stack.pop() #get Edges at same graph_level as s_Edge which neighbors in Bloc2 of dfs_paths_cycle!!
                            #print('Edge',Edge)
                            #sys.exit()
                            #print('in for Edge',Edge,'l_path',l_path)
                            b_FLAG=Edge[1]
                            s_EDGE=Edge[0]
                            s_STATUS=Edge[2]
                            
                            #
                            graph_tempo=change_Status_Edge_in_dict(graph_tempo, s_EDGE) #from 'open' to 'close' on s_EDGE Pipe or Valve
                            graph_tempo=remove_edge_from_dict(graph_tempo,s_EDGE)
##                            ####s_STATUS=Edge[2] #not to be out here for sure cf 14Tdf3 would have only 1 valve to close .
##                            ##also set s_STATUS='close' but in the dict_ itself !!
##                            #print('Edge',Edge)  #Edge ['SVIBV5', '1', 'close'] ok
##                            ##sys.exit()

                            '------------ update allEdgesMet -----------'
                            allEdgesMet.append(Edge)
                            #set all neighbors same level of Valve detected from main neighbors below @ visited
                            #visited.add(s_EDGE) #if put here=>pb
##                            if (s_EDGE in l_EDGES_TOCLOSE or s_EDGE in visited or s_EDGE in allEdgesMet):
                            if (s_EDGE in l_EDGES_TOCLOSE or s_EDGE in visited or s_STATUS=='close'):  ##cas 1: Edge previous Vanne ou 'close'
##                            if (s_EDGE in l_EDGES_TOCLOSE or s_EDGE in visited):
##                            if (s_EDGE in l_EDGES_TOCLOSE or s_STATUS=='close'):
                                    ## il faut tester si s_EDGE still a key of graph_tempo
##                                    try:
##                                            del graph_tempo[s_EDGE] ##cut branch=Edge
##                                    except:
##                                            continue #passe au suivant dans le for
                                    continue

                            '----------- current Edge(k) assessment ---------'
                            if b_FLAG == '1':  ##case vanne not registered yet
                                    if l_path not in list_Paths:
                                            list_Paths.append(l_path)
                                            visited.add(s_EDGE)
                                            l_EDGES_TOCLOSE.append(s_EDGE)
                                            #
                                            graph_tempo=change_Status_Edge_in_dict(graph_tempo, s_EDGE) #from 'open' to 'close' on s_EDGE
                                            graph_tempo=remove_edge_from_dict(graph_tempo,s_EDGE)
##                                            try:
##                                                    del graph_tempo[s_EDGE] ##cut branch=Edge
##                                            except:
##                                                    continue
                            #else:  #cas 3: neighbour(=Edge) is a pipe
                                    #try:
                                    #        del graph_tempo[s_EDGE] ##cut branch=Edge
                                    #except:
                                    #        continue
                                    
                    '---------- print itermediate results and final result ----------'
##                    print('after for l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)       
##                    #if i_counter==5:
##                    #        sys.exit()
##                    #print('path ending by valve')
##                    #print(l_path)
##                    #print('allEdgesMet',allEdgesMet)
##                    print('---Pile Leakage on ',start[0])
##                    print('---Number of valves to close:',len(l_EDGES_TOCLOSE))
##                    print('---l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)
                    continue


        '-------------  BLOC.2 process neighbors = clidren of current Egde unstacked ------------'
         
        i_Nb_neighbors=0
        s_prev_EDGE = s_EDGE
        ##key=Edge=vertex_EDGE --> [ [EdgeIDpn, Flag],[Edge, Flag] etc]
        '------ loop over Neighbours for the unstack Edge(k) ---------'
        for s_current_neighbour in graph_tempo.get(s_EDGE,[]):
                i_Nb_neighbors+=1
                # BFS Algo builts-up several paths in // with an update one-by-one node neighbour if not if path already
                '-------------- current Neighbor Edge infos --------------'
                s_current_Edge = s_current_neighbour[0] ## s_current_neighbour is a 3-uple [NodeID, EdgeID, Flag]
                s_current_Flag = s_current_neighbour[1]
                s_current_Status = s_current_neighbour[2]
                '---------------------------------------------------------'
##                #print('s_current_neighbour',s_current_neighbour)
##                #sys.exit()
##                ### extract Edge list from .items in graph_to_search=dict_E_F
##                ## from l_path =[[2uple_1],[2uple_2],...,[2uple_n]]--> [Edges 1 to n]!!!!
                '------------- read Egde iDs from l_path for checking next ----'
                a = l_path
                l_Edge_IDs = [a[i][0] for i in range(len(a))]
                '--------------------------------------------------------------'
                # this condition avoids inifinite loops : ie Node_neighbour passing by l_path !!
                #if (s_current_Edge not in l_Edge_IDs and s_current_Edge not in l_EDGES_TOCLOSE):
                '------------- stack this Neighbour edge if satisfies the conditions -----'
                if (s_current_Edge not in l_Edge_IDs and s_current_Edge not in l_EDGES_TOCLOSE and s_current_Edge not in visited): #and s_current_Status=='open'):
##                #KEEP ONLY LAST [EDGE,FLAG] PAIR IN l_stack and STORE UNIQUE EDGES TO AllEdgesMet!!!! ---> IT SOLVED THE PENDING PB !!!!!
##                ###if s_current_Edge not in l_EDGES_TOCLOSE:
##                        #l_new_path = list(l_path) #at each iteration, go back to previous state of l_path = l_path
                        l_new_path = []
                        # after having built-up l_new_path := l_path + s_current_neighbour (if was not in l_path)
                        l_new_path.append(s_current_neighbour) #s_current_neighbour i a 3-uple list
                        #!!!! add to l_stack only if not there yet !!!!
                        if s_current_neighbour not in allEdgesMet:
                                l_stack.append((s_current_neighbour,l_new_path))

    '--------  Print final result ------'
    print('---Pile Leakage on ',start[0])
    print('---Number of valves to close:',len(l_EDGES_TOCLOSE))
    print('---l_EDGES_TOCLOSE',l_EDGES_TOCLOSE)

    '---- FREE VARS MEMORY SPACE ----'
    l_EDGES_TOCLOSE = None
    l_new_path = None
    l_path = None
    l_Edge_IDs = None
    l_stack = None
    allEdgesMet = None
    graph_tempo = None
    visited = None
    
    '----- output ------'
    return list_Paths                


#-------------------------------------------------------------
#---------------------- RUNS WITH DFS  -----------------------
#-------------------------------------------------------------

#==========
##DFS based path finding 
#==========
##### with dict_N_E_F
#l_Paths_endValve = bfs_paths_cycle(dict_Nodes_Edges_Flags,['14N17e6','14T42','0'])			   
##### with dict_E_F (no nodes reference in dict) adjacency list of Edges
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T42','0','open'])    #-15oct 8v/6(__runtime3.py version 12-oct 8:00pm) 5 (__runtime version 12-oct 5:30pm) l_EDGES_TOCLOSE ['DD135-04', 'DD135-02', 'DC136-0', 'SDOUQ2', 'V6d703'] ok vs 161 before _runtime.y version
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14Td17-1','0','open']) #8 valves to close still ok
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T6a6','0','open'])   #77
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T533-1','0','open']) #104 (__runtime version 12-oct 5:30pm)
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['V6de73','0'])   #NEED TO STOP IN DFS IF IN VALVES this label is a valve.
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T8d0-2','0','open']) #71 (__runtime version 12-oct 5:30pm) 
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T11b7','0','open'])  #ok-15oct 3v('close' but no 'visited' cond)/ok 3 valves --> pb ! 1 valve... 13oct
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T1198','0','open'])  #161 valves though not in network center --> 77 valves
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14Tdf3','0','open'])   #ok-15oct 2v/ ok 2 valv as expected l_EDGES_TOCLOSE ['V6de62', 'PNEU0003']
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T861','0','open'])    #77 valves (__runtime version 12-oct 5:30pm)
# = dfs_paths_cycle(dict_Edges_Flags,['14T9','0','open'])     #15oct 8v/ 6 l_EDGES_TOCLOSE ['V6d703', 'DD135-04', 'DD135-02', 'DC136-0', 'SDOUQ2', 'SDOUQ1']
##print('l_Paths_endValve',l_Paths_endValve)
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14T47f-2','0','open'])  #126
#l_Paths_endValve = dfs_paths_cycle(dict_Edges_Flags,['14Td79-3','0','open'])  #22
#sys.exit()

'------  BFS results are better : fewer nodes 2-13(still too high) ----'
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T9c7','0','open'], 10) 
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14Tdf3','0','open'], 10)  ##17oct 3v ok ends properly 3v: l_EDGES_TOCLOSE ['PNEU0003', 'V6de62']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T11b7','0','open'],10)  ##17oct 2v ok ends properly 2v: l_EDGES_TOCLOSE ['V6eb68', 'PNEU0004', 'V6eb69']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14Td17-1','0','open'],10)  ##17oct 5v : l_EDGES_TOCLOSE ['DI134-02', 'DI134-01', 'DI134010', 'DI134-07', 'DH134-03']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T42','0','open'],10)     ##17oct 5v : l_EDGES_TOCLOSE ['DI134-02', 'DI134-01', 'DI134010', 'DI134-07', 'DH134-03']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T861','0','open'],10)    ##17oct 13v : l_EDGES_TOCLOSE ['V6eb81', 'V6eb82', 'DH123-04', 'V6eabf', 'V6eb59', 'V6eab6', 'V6eb57', 'V6eb51', 'SPIEV4', 'V6df70', 'V6eab4', 'V6df6f', 'V6eb96', 'V6eab1']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T8d0-2','0','open'],10)  ##17 oct 10v l_EDGES_TOCLOSE ['V6eb33', 'V6eacb', 'V6ead8', 'DI127-14', 'DH127-11', 'V6eb5f', 'V6eb5e', 'DH0201', 'DI127-11', 'V6eaaa']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T533-1','0','open'],10)   ##17oct 9v l_EDGES_TOCLOSE ['V6e321', 'V6e324', 'V6e326', 'V6e33f', 'V6e31e', 'V6e317', 'DE130-02', 'V6e33e', 'V6e377']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T9','0','open'],10)   ##17oct 9v l_EDGES_TOCLOSE ['SDOUQ2', 'SDOUQ1', 'DD135-02', 'DD135-04', 'V6d703', 'DD133-02', 'DC136-0', 'V6d769', 'DE132-04']
#l_Paths_endValve = bfs_paths_levels(dict_Edges_Flags,['14T3a4','0','open'],10) 
#sys.exit()


'---------------- RESULTS: ------'
##-------- BFS -----------
##---Pile Leakage on  14Td55
##---Number of valves to close: 10

##---Pile Leakage on  14T1cd
##---Number of valves to close: 15

##---Pile Leakage on  14T106a-1
##---Number of valves to close: 23

##---Pile Leakage on  14T107b-1
##---Number of valves to close: 18
##---l_EDGES_TOCLOSE ['V6eacb', 'V6eb33', 'V6ead8', 'V6eb5f', 'V6eb5e', 'DH0201', 'V6eaaa', 'DI127-14',
##                    'DH127-11', 'DI127-11', 'DG124-03', 'DG125-03', 'DF126-02', 'V6dce2', 'V6ead9', 'V6eb38', 'DG122-04', 'DF126-05']


##-------- DFS -----------
## 17 oct avec dfs // but dfs quite unstable and give high values often
##---Pile Leakage on  14T9
##---Number of valves to close: 4
##---l_EDGES_TOCLOSE ['DD135-04', 'DD135-02', 'DC136-0', 'SDOUQ1']

## If 'visited' condition is off
##---Pile Leakage on  14T42
##---Number of valves to close: 8 
##---l_EDGES_TOCLOSE ['DD135-04', 'DC136-0', 'V6d769', 'DD133-02', 'V6d703', 'DD135-02', 'SDOUQ2', 'SDOUQ1']

##---Pile Leakage on  14Td17-1
##---Number of valves to close: 8
##---l_EDGES_TOCLOSE ['DH134-03', 'DI134010', 'DI134-07', 'DI134-01', 'DI134-02', 'DG134-04', 'DG134-01', 'DG134-06']

##---Pile Leakage on  14T11b7
##---Number of valves to close: 3
##---l_EDGES_TOCLOSE ['V6eb69', 'V6eb68', 'PNEU0004']

##---Pile Leakage on  14Tdf3
##---Number of valves to close: 2
##---l_EDGES_TOCLOSE ['V6de62', 'PNEU0003']

##---Pile Leakage on  14T9
##---Number of valves to close: 8
##---l_EDGES_TOCLOSE ['DD135-02', 'V6d769', 'DD133-02', 'V6d703', 'DD135-04', 'DC136-0', 'SDOUQ2', 'SDOUQ1']

##---Pile Leakage on  14T1198  :  FAILS
##---Number of valves to close: 79
##---l_EDGES_TOCLOSE

#Please see VEOLIA_overview_Results_11oct2016am.rtf

'--------------------------------------------------------------------'
'----------- RUNETIME ASSESSMENT from dict n first elets ------------'
'--------------------------------------------------------------------'
#
#Running time test Algorithm BFS with n = Step (100,300,500,700,900,1100) , Delete comments if you want tot test the running time with output of Linear Graphic

'----------------------------------------------------'

ta= time()
#
#VARIABLE HERE IS I_SIZE_CUT_NETWORK to be = 100,200,300,400,500,1000,4000 first Pipes --> associated Rt
#Edges_to_close = dfs_paths_cycle(dict_Edges_Flags,['14T42','0','open'])

list_keys = list(dict_Edges_Flags.keys())
##print('type list keys',type(list_keys))
##print('keys',list_keys)
##sys.exit()
NbNodes=5
i_counter=0
for lk in list_keys[:NbNodes]:
        i_counter +=1
        graph_new_Temp = dict_Edges_Flags
        data_set = dict_Edges_Flags.get(lk,[])
        Edges_to_close = bfs_paths_levels(graph_new_Temp,[lk,'0','open'],10)
        Edges_to_close = None
        graph_new_Temp = None
        print('lk',lk)
        print('type lk',type(lk))

ta_end= time()
ta_time= (ta_end-ta)
print('--- Nb Nodes: ', NbNodes)
print ('runtime : ',ta_time)

'----------------------------------------------------'

