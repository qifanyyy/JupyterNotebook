from pulp import *
import numpy as np
import numpy.random as rd
import queue

n = 10
s,t = 0, n-1

def rand_graph():
    G = [[rd.randint(0,3) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i==j:
                G[i][j] = 0
            else:
                G[i][j] = G[j][i]
    return G

def is_connected(G):
    visited = [False]*n
    q = queue.Queue()
    q.put(0)
    while(not q.empty()):
        v = q.get()
        if (not visited[v]):
            visited[v]=True
            for j in range(n):
                if G[v][j] > 0 and not visited[j]:
                    q.put(j)
    for b in visited:
        if b == 0:
            return False
    return True

def rand_connected_graph():
    G = rand_graph()
    while(not is_connected(G)):
        G = rand_graph()
    return G

def read_problem():
    myfile = open("temp.txt", "r")
    problem = myfile.readlines()
    n = int(problem[0])
    s = int(problem[1])
    t = int(problem[2])
    G = [[int(s) for s in problem[i].split(',')[:-1]] for i in range(3, n+3)]
    myfile.close()
    return n, s, t, G

n, s, t, G = read_problem()
'''
print("G= ", G)
print("s,t = ", s,t)
print("")
'''

def make_sets():
    edges = set()
    flow_v = set()
    flow_t = set()
    for i in range(n):
        for j in range(i+1, n):
            if (G[i][j]>0):
                edges.add((i,j))
                flow_t.add((i,j))
                flow_t.add((j,i))
                for v in range(n):
                    if v != s and v != t:
                        flow_v.add((v,i,j))
                        flow_v.add((v,j,i))
    return edges, flow_v, flow_t

def delta_plus(v):
    res = set()
    for a in range(n):
        if G[v][a] > 0:
            res.add((v,a))
    return res

def delta_minus(v):
    res = set()
    for a in range(n):
        if G[a][v] > 0:
            res.add((a,v))
    return res

edges, flow_v, flow_t = make_sets()

prob = LpProblem("Path-TSP", LpMinimize)

x = pulp.LpVariable.dicts('x', edges)
f_t = pulp.LpVariable.dicts('f_t', flow_t)
f_v = pulp.LpVariable.dicts('f_v', flow_v)

def make_weighted_x(X):
    return [x[(i,j)]*G[i][j] for (i,j) in edges]

prob += lpSum(make_weighted_x(x))

for (v,i,j) in flow_v:
    prob += f_v[(v,i,j)] >= 0
    if j < i:
        prob += f_v[(v,i,j)] <= x[(j,i)]
    else:
        prob += f_v[(v,i,j)] <= x[(i,j)]

for (i,j) in edges:
    prob += f_t[(i,j)] >= 0
    prob += f_t[(j,i)] >= 0
    prob += f_t[(i,j)] <= x[(i,j)]
    prob += f_t[(j,i)] <= x[(i,j)]
#    prob += x[(i,j)] <= 1

for v in range(n):
    if v != s and v != t:
        for u in range(n):
            if u != v and u != s and u != t:
                sortant = lpSum([f_v[(v,i,j)] for (i,j) in delta_plus(u)])
                entrant = lpSum([f_v[(v,i,j)] for (i,j) in delta_minus(u)])
                prob += sortant == entrant

for v in range(n):
    if v != s and v != t:
        sortant = lpSum([f_v[(v,i,j)] for (i,j) in delta_plus(v)])
        entrant = lpSum([f_v[(v,i,j)] for (i,j) in delta_minus(v)])
        prob += sortant == entrant + 2

        sortant = lpSum([f_v[(v,i,j)] for (i,j) in delta_plus(s).union(delta_plus(t))])
        entrant = lpSum([f_v[(v,i,j)] for (i,j) in delta_minus(s).union(delta_minus(t))])
        prob += sortant == entrant - 2

        sortant = lpSum([f_t[a] for a in delta_plus(v)])
        entrant = lpSum([f_t[a] for a in delta_minus(v)])
        prob += sortant == entrant


sortant = lpSum([f_t[a] for a in delta_plus(t)])
entrant = lpSum([f_t[a] for a in delta_minus(t)])
prob += sortant == entrant + 1

sortant = lpSum([f_t[a] for a in delta_plus(s)])
entrant = lpSum([f_t[a] for a in delta_minus(s)])
prob += sortant == entrant - 1

#print(prob)

prob.solve(pulp.COIN_CMD(options=['primalSimplex']))
print("Status:", LpStatus[prob.status], value(lpSum(x)))

def from_name_to_edge(name):
    i = 0;
    while name[i] != "(":
        i+=1
    i+=1
    u = ""
    while name[i] != ",":
        u+=name[i]
        i+=1
    v = ""
    i+=2
    while name[i] != ")":
        v+=name[i]
        i+=1
    return int(u), int(v)

def from_variables_to_graph(variables):
    G = [[0 for _ in range(n)] for _ in range(n)]
    for v in variables:
        if v.name[0] == "x":
            i, j = from_name_to_edge(v.name)
            G[i][j] = v.varValue
            G[j][i] = v.varValue
    return G

def store_graph(G):
    f = open("temp.txt", "w")
    for l in G:
        for c in l:
            f.write(str(c)+"\n")
    f.close()

store_graph(from_variables_to_graph(prob.variables()))
