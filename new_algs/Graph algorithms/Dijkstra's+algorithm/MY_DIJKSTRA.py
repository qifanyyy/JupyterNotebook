
# coding: utf-8

# In[3]:

x =[123,245,367,409,511]

y = [211,612,321,499,211]

for i,v in enumerate(x):
    
    z[v] = y[i]        
    
print (z)


a = {}
key = "somekey"
a[key] = []
a[key].append(1)
a[key].append(2)
print (a)



# In[4]:

import heapq

adj = {'c': [('b', 0.32), ('e', 0.17), ('f', 0.91)],
         'g': [('d', 0.17), ('e', 0.27), ('h', 0.92)],
         'i': [('e', 1.98), ('f', 0.13), ('h', 0.22)],
         'f': [('c', 0.91), ('e', 0.33), ('i', 0.13)],
         'h': [('e', 0.18), ('g', 0.92), ('i', 0.22)],
         'd': [('a', 0.72), ('e', 0.29), ('g', 0.17)],
         'a': [('b', 0.95), ('d', 0.72), ('e', 1.75)],
         'e': [('a', 1.75), ('b', 0.82), ('c', 0.17), ('d', 0.29), ('f', 0.33), ('g', 0.27), ('h', 0.18), ('i', 1.98)],
         'b': [('a', 0.95), ('c', 0.32), ('e', 0.82)]}
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
    
    #INF = ((1<<63) - 1)//2
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = { x:x for x in graph } 
    #cost_so_far = { x:INF for x in adj }
    cost_so_far = {}
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current_node = frontier.get()
        
        if current_node == goal:
            break
        
        for next_node in graph[current_node]:
            #print(next_node)
            n_id = next_node[0]
            n_dist = next_node[1]
            
            new_cost = cost_so_far[current_node] + n_dist
            
            if n_id not in cost_so_far or new_cost < cost_so_far[n_id]:
                cost_so_far[n_id] = new_cost
                priority = new_cost
                frontier.put(n_id, priority)
                came_from[n_id] = current_node
    
    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    
    return came_from#, cost_so_far


def reconstruct_path(came_from, start, goal):
    current_node = goal
    path = [current_node]
    while current_node != start:
        current_node = came_from[current_node]
        path.append(current_node)
    #path.append(start) # optional
    path.reverse() # optional
    return path

    
f=dijkstra_search(adj, 'a', 'g') 
y =reconstruct_path(f, 'a', 'g')
print(y)





#def main():
  
#     dijkstra_search(graph(), '', '169')
 


# In[5]:

import heapq
import pandas as pd
adj = {'c': [('b', 0.32), ('e', 0.17), ('f', 0.91)],
         'g': [('d', 0.17), ('e', 0.27), ('h', 0.92)],
         'i': [('e', 1.98), ('f', 0.13), ('h', 0.22)],
         'f': [('c', 0.91), ('e', 0.33), ('i', 0.13)],
         'h': [('e', 0.18), ('g', 0.92), ('i', 0.22)],
         'd': [('a', 0.72), ('e', 0.29), ('g', 0.17)],
         'a': [('b', 0.95), ('d', 0.72), ('e', 1.75)],
         'e': [('a', 1.75), ('b', 0.82), ('c', 0.17), ('d', 0.29), ('f', 0.33), ('g', 0.27), ('h', 0.18), ('i', 1.98)],
         'b': [('a', 0.95), ('c', 0.32), ('e', 0.82)]}

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(adj, start, goal):
    #INF = ((1<<63) - 1)//2
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = { x:x for x in adj } 
    #cost_so_far = { x:INF for x in adj }
    cost_so_far = {}
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current_node = frontier.get()
        
        if current_node == goal:
            break
        
        for next_node in adj[current_node]:
            #print(next_node)
            n_id = next_node[0]
            n_dist = next_node[1]
            
            new_cost = cost_so_far[current_node] + n_dist
            
            if n_id not in cost_so_far or new_cost < cost_so_far[n_id]:
                cost_so_far[n_id] = new_cost
                priority = new_cost
                frontier.put(n_id, priority)
                came_from[n_id] = current_node
   
    
    return came_from#, cost_so_far


def reconstruct_path(came_from, start, goal):
    current_node = goal
    path = [current_node]
    while current_node != start:
        current_node = came_from[current_node]
        path.append(current_node)
    #path.append(start) # optional
    path.reverse() # optional
    return path
    
#dijkstra_search(adj, 'a', 'i')
reconstruct_path(dijkstra_search(adj, 'a', 'c'), 'a', 'c')

nodes = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEFILE_DOPENODES.csv')
roads = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEROAD_DOPENODE.csv')

a = list(roads.IN)
#print('------------------------------------------------------------------------------------------------')
b = list(roads.OUT)

distance = list(roads.DISTANCE)

#box=[]
box2=[]

#for i,v in enumerate(a):
 #   w =([v, distance[i]])
  #  box.append(w)
    
#print (box)

for i,v in enumerate(a):
    
    #if v[0] == a[i]:
    box2.append([v,b[i],distance[i]])
    
#print(box2)

#box3 =box2
#box3.sort()
#print(box3)



empty = {}
empty[165]=[]
for i in box2:
    
    
    if i[0]==165:
        
        empty[165].append(i[1:])
        
print(empty)      

h ={a[i]:[] for i in a}




# In[6]:

empty2 = {i:[] for i in a}

#print(empty2)
#print(box2)
for i,v in enumerate(box2):
  
    if v[0]==a[i]:
        
        empty2[a[i]].append(v[1:])
        
for i in empty[165]:
    
    print(i)


# In[8]:

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
h = (s[171])
print(h)

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
        print('Current Node:',current_node)
        
    
        mileage += cost_so_far[current_node]

        print("Mileage:",mileage)

        
        if current_node == goal or cost_so_far[goal]<mileage:
            print('GOAL CAMEE FROM',came_from[goal],mileage, current_node)
            print('CURRENT NODDEEEEEEEEEE:',current_node)
            print('GOAL MILEAGE and COST:', goal_miles,cost_so_far[goal])
            break
        
        for next_node in graph[current_node]:
            try:
                print('GCN:',graph[current_node])
                print('Next node:',next_node)
                n_id = next_node[0]
                #if n_id not in graph.keys():
                    #print(not in)
                print('CURRENT COST:',cost_so_far[current_node])
                print('NEXT NODE COST:',cost_so_far[n_id])
                print('node id: ', n_id)
                n_dist = next_node[1]

                new_cost = cost_so_far[current_node] + n_dist

                #if n_id not in cost_so_far or 
                if new_cost < cost_so_far[n_id]:

                    print('new cost: ',new_cost)
                    cost_so_far[n_id] = new_cost
                    print('cost so far',cost_so_far[n_id])
                    priority = new_cost
                    frontier.put(n_id, priority)
                    came_from[n_id] = current_node
                    
                if n_id == goal:
                    
                    goal_miles = mileage
                    print('GOAL MILEAGE:', goal_miles)
                    
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

  


# In[9]:

#print(s[951])
#print(s.keys())

#Shortest path: [356, 357, 358, 377, 378, 393, 394, 444, 445, 452, 456, 565, 566, 568, 827, 829, 834, 835, 839, 841, 860, 861, 865, 866, 874, 914, 917, 918, 923, 924]
if 924 not in s.keys():
    print("not in ")


# In[54]:

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
        
        if start not in graph.keys():
            
            print('There is no path from %s, to %s' % (start,goal))
            break
        
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
    

    if cost_so_far[goal] == INF:

        print(('There is no path from %s, to %s') % (start,goal))
        return 0
        

    else:
        return came_from
        
    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    #print(cost_so_far)
    #, cost_so_far
    


def reconstruct_path(came_from, start, goal):
    
    if came_from == 0:
        return 0
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

def letsgo(start,goal):

    came_from=dijkstra_search(s, start, goal)
    
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
    
    print(path)
    return(path)
    

#y =reconstruct_path(f, 356, 924)

d= letsgo('a','i')



# In[48]:

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
                        print('GOAL CAME FROM',came_from[current_node],mileage)
                        print('CURRENT NODDEEEEEEEEEE:',current_node)
                        break

                     pass

    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    #print(cost_so_far)
    return came_from#, cost_so_far

def letsgo(start,goal):

    came_from=dijkstra_search(s, start, goal)
    
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
    
    print(path)
    return(path)
    

y =reconstruct_path(f, 356, 924)

y = letsgo(356,924)
print(y)


# In[43]:

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
                        print('GOAL CAME FROM',came_from[current_node],mileage)
                        print('CURRENT NODDEEEEEEEEEE:',current_node)
                        break

                     pass

    #if dist[target]==INF:
     #   stdout.write("There is no path between " + source + " and " + target)
    #print(cost_so_far)
    return came_from#, cost_so_far

def letsgo(start,goal):

    came_from=dijkstra_search(s, start, goal)
    
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
    
    print(path)
    return(path)
    

#y =reconstruct_path(f, 356, 924)

#y = letsgo(165,924)
#print(y)


# In[42]:

import sys 
from functools import total_ordering

class Vertex:
    def __init__(self, node):
        self.id = node 
        self.adjacent = {} 
        
        # Set distance to infinity for all nodes 
        self.distance = float(99999999)
        
        # Mark all nodes unvisited 
        self.visited = False 
        
        # Predecessor 
        self.previous = None 
    
    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight 
    
    def get_connections(self):
        return self.adjacent.keys() 
    
    def get_id(self):
        return self.id 
    
    def get_weight(self, neighbor):
        return self.adjacent[neighbor] 
    
    def set_distance(self, dist):
        self.distance = float(dist)
    
    def get_distance(self): 
        return self.distance 
    
    def set_previous(self, prev): 
        self.previous = prev 
    
    def set_visited(self): 
        self.visited = True 
    
    def __str__(self): 
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent]) 
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.distance == other.distance
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance
        return NotImplemented
    
    def __hash__(self):
        return id(self)

class Graph:
    def __init__(self): 
        self.vert_dict = {} 
        self.num_vertices = 0
    
    def __iter__(self): 
        return iter(self.vert_dict.values()) 
    
    def add_vertex(self, node): 
        self.num_vertices = self.num_vertices + 1 
        new_vertex = Vertex(node) 
        self.vert_dict[node] = new_vertex 
        return new_vertex 
    
    def get_vertex(self, n): 
        if n in self.vert_dict: 
            return self.vert_dict[n] 
        else: 
            return None 
    
    def add_edge(self, frm, to, cost = 0): 
        if frm not in self.vert_dict: 
            self.add_vertex(frm) 
        if to not in self.vert_dict: 
            self.add_vertex(to) 
        
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost) 
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost) 
    
    def get_vertices(self): 
        return self.vert_dict.keys() 
    
    def set_previous(self, current): 
        self.previous = current 
    
    def get_previous(self, current): 
        return self.previous 
    
def shortest(v, path): 
    # Make shortest path from v.previous 
    if v.previous: 
        path.append(v.previous.get_id()) 
        shortest(v.previous, path) 
    return 
    
import heapq 
    
def dijkstra(aGraph, start, target): 
    #print('''Dijkstra's shortest path''') 
    # Set the distance for the start node to zero 
    start.set_distance(0) 
        
    # Put tuple pair into the priority queue 
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)
        
    while len(unvisited_queue): 
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue) 
        current = uv[1] 
        current.set_visited() 
            
        # For next in v.adjacent: 
        for next in current.adjacent: 
            # If visited, skip 
            if next.visited: 
                continue 
            new_dist = float(current.get_distance() + current.get_weight(next))
        
            
            if new_dist < next.get_distance(): 
                next.set_distance(new_dist) 
                next.set_previous(current)
                """
                # Prints iterations of the search that update path
                print('updated : current = %s next = %s new_dist = %s' \
                      %(current.get_id(), next.get_id(), next.get_distance()))
                
            else:
                
                # Prints iterations of the search that don't update path
                print('not updated : current = %s next = %s new_dist = %s' \
                      %(current.get_id(), next.get_id(), next.get_distance()))
                """
                    
        # Rebuild heap 
        # 1. Pop every item 
        while len(unvisited_queue): 
            heapq.heappop(unvisited_queue) 
        # 2. Put all vertices not visited into the queue 
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited] 
        heapq.heapify(unvisited_queue)

import pandas as pd
        
if __name__ == '__main__': 
        
    network = Graph()
    
    """
    Import nodes df
    Nodes csv should have node number column labeled as 'NODE'
    """
    nodes = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEFILE_DOPENODES.csv')
    
    # Iteratively add nodes to network
    for node in nodes.index:
        #print(nodes['NODE'][node])
        network.add_vertex(nodes['NODE'][node])
        
    """   
    Import roads df
    Roads csv should have road start column labeled 'IN', road end column labeled
    'OUT', and road distance column labeled 'DISTANCE'
    """
    roads = pd.read_csv(r'C:\Users\591943\Desktop\Python scripts\DOPEROAD_DOPENODE.csv')
    #print(roads['IN'])
    # Iteratively add roads to network as edges
    for j in roads.index:
        network.add_edge(roads['IN'][j], roads['OUT'][j], float(roads['DISTANCE'][j]))
        
    """
    # Prints graph data (node pairings and distances)
    print('Graph data:')
    for v in network: 
        for w in v.get_connections(): 
            vid = v.get_id() 
            wid = w.get_id() 
            print ('( %s , %s, %3d)' % ( vid, wid, v.get_weight(w)))
    """
    
    # Define starting vertex as currentNode
    currentNode = 356
    start = network.get_vertex(currentNode)
    # Define target vertex as exitNode
    exitNode = 924
    target = network.get_vertex(exitNode)
    
    # Run the dijkstra function
    dijkstra(network, start, target) 
    
    # Define and report the shortest path
    path = [target.get_id()]
    shortest(target, path)
    shortest_path = path[::-1]
    
    print('Shortest path: %s' %(shortest_path))




