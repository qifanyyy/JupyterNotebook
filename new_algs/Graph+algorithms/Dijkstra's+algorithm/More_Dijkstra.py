
# coding: utf-8

# In[1]:

import heapq
import pandas as pd

#def graph():

nodes = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEFILE_DOPENODES.csv')
roads = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEROAD_DOPENODE.csv')

a = list(roads.IN)
b = list(roads.OUT)
distance = list(roads.DISTANCE)


box=[]

for i,j in enumerate(a):


    box.append([j,b[i],distance[i]])

case = {i:[] for i in a}

for i,v in enumerate(box):

    if v[0]==a[i]:

        case[a[i]].append(v[1:])

    #return(case)

adj = {'c': [('b', 0.32), ('e', 0.17), ('f', 0.91)],
         'g': [('d', 0.17), ('e', 0.27), ('h', 0.92)],
         'i': [('e', 1.98), ('f', 0.13), ('h', 0.22)],
         'f': [('c', 0.91), ('e', 0.33), ('i', 0.13)],
         'h': [('e', 0.18), ('g', 0.92), ('i', 0.22)],
         'd': [('a', 0.72), ('e', 0.29), ('g', 0.17)],
         'a': [('b', 0.95), ('d', 0.72), ('e', 1.75)],
         'e': [('a', 1.75), ('b', 0.82), ('c', 0.17), ('d', 0.29), ('f', 0.33), ('g', 0.27), ('h', 0.18), ('i', 1.98)],
         'b': [('a', 0.95), ('c', 0.32), ('e', 0.82)]}
s = adj

#print(s)
#h = (s[171])
#print(h)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):

    #print(graph[173])

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
        #print(frontier.elements)
        current_node = frontier.get()
        #print('Current Node:',current_node)


        mileage += cost_so_far[current_node]

        #print("Mileage:",mileage)


        if current_node == goal or cost_so_far[goal]<mileage:
            print('GOAL CAME FROM: ',came_from[goal],', Goal Cost: ',cost_so_far[goal],', Dijkstra Mileage: ',mileage, sep= '')
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
                        print('GOAL CAME FROM',came_from[current_node],mileage)
                        print('CURRENT NODDEEEEEEEEEE:',current_node)
                        break

                     pass

    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    #print(cost_so_far)
    return came_from#, cost_so_far

#def letsgo(start,goal):

#came_from=dijkstra_search(s, start, goal)

def reconstruct_path(came_from, start, goal):
    current_node = goal
    path = [current_node]
    while current_node != start:
        current_node = came_from[current_node]
        path.append(current_node)
    #path.append(start) # optional
    path.reverse() # optional
    #print([goal])
    return path

    #print(path)
    #return path
    

f=dijkstra_search(s, 'a', 'i') 
y =reconstruct_path(f, 'a', 'i')
print(y)


# In[15]:

import heapq
import pandas as pd

#def graph():

nodes = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEFILE_DOPENODES.csv')
roads = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEROAD_DOPENODE.csv')

a = list(roads.IN)
b = list(roads.OUT)
distance = list(roads.DISTANCE)


box=[]

for i,j in enumerate(a):


    box.append([j,b[i],distance[i]])

case = {i:[] for i in a}

for i,v in enumerate(box):

    if v[0]==a[i]:

        case[a[i]].append(v[1:])
    
    #return(case)


s = case

#print(s)
#h = (s[171])
#print(h)

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):
    
    #print(graph[173])
    
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
        #print(frontier.elements)
        current_node = frontier.get()
        #print('Current Node:',current_node)
        
    
        mileage += cost_so_far[current_node]

        #print("Mileage:",mileage)

        
        if current_node == goal or cost_so_far[goal]<mileage:
            print('GOAL CAME FROM: ',came_from[goal],', Goal Cost: ',cost_so_far[goal],', Dijkstra Mileage: ',mileage, sep= '')
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
                        print('GOAL CAME FROMMM',came_from[current_node],mileage)
                        print('CURRENT NODDEEEEEEEEEE:',current_node)
                        print('GOAL MILEAGE:', goal_miles)
                        break

                     pass
    
    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    #print(cost_so_far)
    return came_from#, cost_so_far


def reconstruct_path(came_from, start, goal):
    current_node = goal
    path = [current_node]
    while current_node != start:
        current_node = came_from[current_node]
        path.append(current_node)
    #path.append(start) # optional
    path.reverse() # optional
    #print([goal])
    return path

    
f=dijkstra_search(s, 356, 924) 
y =reconstruct_path(f, 356, 924)
print(y)

  


# In[ ]:



