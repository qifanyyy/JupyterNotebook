
# coding: utf-8

# In[1]:


"""
Samuel Oge 8/2/17

Dijkstra 2.0

Ran For Oroville Data

"""




import heapq
import pandas as pd


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

nodes = pd.read_csv(r'..\Python scripts\DOPEROAD_DOPENODE.csv')
#roads = pd.read_csv(r'..\Python scripts\DOPEROAD_DOPENODE.csv')

a = list(nodes.IN)
b = list(nodes.OUT)
distance = list(nodes.DISTANCE)
    
def shortest_path(start, goal):
    
    def graph():

       

        #print(a)

        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        #print(b)

        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        #print(distance)

        box=[]

        for i,j in enumerate(a):


            box.append([j,b[i],distance[i]])

        case = {i:[] for i in a}

        for i,v in enumerate(box):

            if v[0]==a[i]:

                case[a[i]].append(v[1:])

        return case


    graph_data = graph()
    
    
    #print(s)
    #h = (s[171])
    #print(h)
    
    def dijkstra_search(graph_data,start, goal):

        #print(graph[173])

        graph = graph_data

        INF = ((1<<63) - 1)//2
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = { x:x for x in graph } 
        #print(came_from)
        cost_so_far = { x: INF for x in graph }
        #print(cost_so_far)
        #cost_so_far = {}
        cost_so_far[start] = 0
        cost_so_far[goal] = INF
        mileage = 0

        while not frontier.empty():
            
            if start == goal:
                cost_so_far[goal] = 0
                return (start, cost_so_far[goal] )

            if start not in graph.keys():

                #print('There is no path from %s, to %s' % (start,goal))
                break

            #print(frontier.elements)
            current_node = frontier.get()
            #print('Current Node:',current_node)


            mileage += cost_so_far[current_node]

            #print("Mileage:",mileage)


            if current_node == goal or cost_so_far[goal]<mileage:
                #print('GOAL CAME FROM: ',came_from[goal],', Goal Cost: ',cost_so_far[goal],', Dijkstra Mileage: ',mileage, sep= '')
                #print('CURRENT NODDEEEEEEEEEE:',current_node)
                break

            for next_node in graph[current_node]:
                try:
                    #print('GCN:',graph[current_node])
                    #print('Next node:',next_node)
                    n_id = next_node[0]
                    #if n_id not in graph.keys():
                        #print(not in)
                    #print('CURRENT COST:',cost_so_far[current_node])
                    #print('NEXT NODE COST:',cost_so_far[n_id])
                    #print('node id: ', n_id)
                    n_dist = next_node[1]

                    new_cost = cost_so_far[current_node] + n_dist

                    #if n_id not in cost_so_far or 
                    if new_cost < cost_so_far[n_id]:

                        #print('new cost: ',new_cost)
                        cost_so_far[n_id] = new_cost
                        #print('cost so far',cost_so_far[n_id])
                        priority = new_cost
                        frontier.put(n_id, priority)
                        came_from[n_id] = current_node

                    if n_id == goal:

                        goal_miles = mileage
                        #print('GOAL MILEAGE:', goal_miles)

                except:   
                         if (n_id == goal and n_id not in graph.keys()):
                            #print('GOAL CAME FROM',came_from[current_node],mileage)
                            #print('CURRENT NODDEEEEEEEEEE:',current_node)
                            break

                         pass


        if cost_so_far[goal] == INF:

            #print(('There is no path from %s, to %s') % (start,goal))
            return (0,INF)
            

        else:
            return (came_from, cost_so_far[goal])

        #if dist[target]==INF:
         #   stdout.write("There is no path between " + source + " and " + target)
        #print(cost_so_far)
        #, cost_so_far



    dijkstra_result = dijkstra_search(graph_data,start,goal)

    def reconstruct_path(came_from, start, goal):
    
        if came_from == 0:
            return start
        current_node = goal
        path = [current_node]
        while current_node != start:
            current_node = came_from[current_node]
            path.append(current_node)
        #path.append(start) # optional
        path.reverse() # optional
        #print([goal])
        return path

    path_taken = reconstruct_path(dijkstra_result[0], start, goal)
    
    return (path_taken, dijkstra_result[1])

    
#print(shortest_path(924,923))
#print(nodes[nodes['OUT'] == 924])


"""
def find_all_shortest_paths(destination):
    
    pathsDict = {k:[] for k in a}
    distDict = {l:[] for l in a}
    #dest = destination

    for node in nodes.IN.unique():
        pack = {}
        pack2 = {}
        for dest in destination:
            #result =dijkstra_search(s, node, destination) 
            #y =reconstruct_path(f, node, destination)
            #y =print(shortest_path(node,dest)[0])
            y = shortest_path(node,dest)[0]
            pack[dest] = y
            x=shortest_path(node,dest)[1]
            pack2[dest]= x
        pathsDict[node] = pack
        distDict[node] = pack2
            
    #for i in a:

        #for v in pack:

            #print(v)
             #if v[0]==i:
                #print('v:',v[0],'i:',i)
                    #pathsDict[i].append(v) 
            #print(pathDict[k])
             
    return  (distDict,pathsDict)

    
desti = [924, 356, 66, 491]
carton = find_all_shortest_paths(desti)
ALLTHEPATHS = carton[0]
ALLTHEDISTS = carton[1]
di = {i: min(ALLTHEDISTS[i].values()) for i in ALLTHEDISTS}

#print(di)"""


"""df = pd.DataFrame(columns=['NODE','DESTINATION','DISTANCE','PATH'])
for node in ALLTHEPATHS:
    for dest in ALLTHEPATHS[node]:
        df.loc[len(df)]=[node,dest,ALLTHEPATHS[node][dest]]
        
print(df)"""


# In[159]:

df.loc[10]


# In[131]:

pathsDict = {i:[] for i in nodes.IN}
pathsDict[165].append(([165,245,34,5,222],[165,23,4,3,2,1]))
#print (pathsDict)

l = nodes.IN.unique()
#print(l)


# In[139]:

#list(nodes['IN'])


# In[151]:

box=[]

for i,j in enumerate(a):


    box.append([j,b[i],distance[i]])

case = {i:[] for i in a}

for i,v in enumerate(box):

    if v[0]==a[i]:

        case[a[i]].append(v[1:])
        
#case
#box
print(case)


# In[227]:

case = {k:[] for k in a}
    #dest = destination

    for node in nodes.IN.unique():
        pack = []

        for dest in destination:
            #result =dijkstra_search(s, node, destination) 
            #y =reconstruct_path(f, node, destination)
            y = shortest_path(node,dest)
            pack.append(y)
        
        pathsDict[node] = pack
            


# In[230]:

INF = ((1<<63) - 1)/2
INF


# In[327]:

list = {165: {924: 39098.676539200016, 356: 24954.568113370005, 66: 1330.1155189999999, 491: 11261.209781300002}}
min(list[165].values())

list[165].items()




# In[340]:

list ={165: {924: 39098.676539200016, 356: 24954.568113370005, 66: 1330.1155189999999, 491: 11261.209781300002}, 169: {924: 38588.864814600012, 356: 24444.756388770002, 66: 29341.438502469999, 491: 10751.398056700002}}


y = {i: min(list[i].values()) for i in list}


print(list[165].get(924))

"""for i in y.keys():
    print(i)"""
"""for i in list[165].items():
    
    if i[1] == y[165]:

         print (i[0])
"""

#y.values()
#= {distdi.append(min(list[i].values())) for i in list}

#x = {list[i]: v for i,v in enumerate(y)}
#print (y)


# In[258]:

"""
def find_all_shortest_paths(destination):
    
    pathsDict = {k:[] for k in a}
    distDict = {l:[] for l in a}
    #dest = destination

    for node in nodes.IN.unique():
        pack = {}
        pack2 = {}
        for dest in destination:
            #result =dijkstra_search(s, node, destination) 
            #y =reconstruct_path(f, node, destination)
            #y =print(shortest_path(node,dest)[0])
            y = shortest_path(node,dest)[0]
            pack[dest] = y
            x=shortest_path(node,dest)[1]
            pack2[dest]= x
        pathsDict[node] = pack
        distDict[node] = pack2
            
    #for i in a:

        #for v in pack:

            #print(v)
             #if v[0]==i:
                #print('v:',v[0],'i:',i)
                    #pathsDict[i].append(v) 
            #print(pathDict[k])
             
    return  (distDict,pathsDict)

    
desti = [924, 356, 66, 491]
carton = find_all_shortest_paths(desti)
ALLTHEPATHS = carton[0]
ALLTHEDISTS = carton[1]
di = {i: min(ALLTHEDISTS[i].values()) for i in ALLTHEDISTS}

#print(di)"""


"""df = pd.DataFrame(columns=['NODE','DESTINATION','DISTANCE','PATH'])
for node in ALLTHEPATHS:
    for dest in ALLTHEPATHS[node]:
        df.loc[len(df)]=[node,dest,ALLTHEPATHS[node][dest]]
        
print(df)"""

