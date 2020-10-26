# -*- coding: utf-8 -*-

"""
TITLE: Ford-Fulkerson Algorithm
AUTHORS: Marina Berbel Palomeque & Nieves Montes Gómez
DATE: 20/12/2019
DESCRIPTION: Implementation of the Ford-Fulkerson algorithm to find the 
maximum flow of organic matter between two taxa in an ecological food chain.
The FFA uses BFS to find shortest augmenting paths (Edmonds-Karp algorithm).
"""

#%%
"""
All necessary imports
"""
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import queue as qu
import pandas as pd
import numpy as np
#%%

#%%
"""
Function to plot the initial graph
"""
def plot_initial_graph(G, s, t):
    pos = nx.layout.circular_layout(G, scale=2)
    plt.figure(figsize=(12,12))
    node_sizes = 500
    node_colors=[]
    for node in G:
        if node==s:
            node_colors.append('blue')
        elif node==t:
            node_colors.append('red')
        else:
            node_colors.append('black')
    edge_colors = list(nx.get_edge_attributes(G, 'capacity').values())
    cmap = 'Spectral'
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                                   node_color=node_colors)
    nx.draw_networkx_labels(G, pos, font_size=16, font_color='white', 
                            font_weight='bold')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, 
                                   arrowstyle='->', arrowsize=20, 
                                   edge_color=edge_colors,
                                   edge_cmap=plt.get_cmap(cmap), width=3)
    if (edges):
        pc = mpl.collections.PatchCollection(edges, cmap=plt.get_cmap(cmap))
        pc.set_array(edge_colors)
        plt.colorbar(pc)
    plt.text(3.75, 0, 'Capacity (feeding factor)', horizontalalignment='right',
             verticalalignment='center', rotation=-90)
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()
#%%
    
#%%
"""
Function that computes the residual graph
"""
def residual_graph(G):
    capacities = nx.get_edge_attributes(G, 'capacity')
    flows = nx.get_edge_attributes(G, 'flow')
    resG = nx.MultiDiGraph()
    for node in list(G.nodes):
        resG.add_node(node)
    # residual capacities
    for edge in list(G.edges):
        cap = capacities[edge]
        fl = flows[edge]
        # capacity left in the edge
        if (cap-fl>0):
            resG.add_edge(edge[0], edge[1], capacity=cap-fl)
        # send though it now (flow field has to be updated)
        if (fl>0):
            resG.add_edge(edge[1], edge[0], capacity=fl)
    return resG
#%%
            
#%%
"""
Given an augmenting path in a graph, find its bottleneck, i.e. the minimum
capacity of all edges that make up the path.
"""
def findBottleneck(G, path):
    N = len(path)
    minimum = 5000
    for i in range(N-1):
        new = G[path[i]][path[i+1]][0]['capacity']
        if (new<minimum):
            minimum = new
    return minimum
#%%
    
#%%
"""
Compute the path from source to parent as a list of nodes
"""
def doPath(nodes, parents, s, t):
    path = []
    indexs = nodes.index(s)
    indext = nodes.index(t)
    while (indext!=indexs):
        path.append(nodes[indext])
        indext = parents[indext] 
    path.append(nodes[indext])
    path.reverse()
    return path 
#%%
    
#%%
"""
Find an augmenting path with breadth-first search.
"""
def augmenting_path_BFS(G, s, t):
    found = False; bottleneck = 0; path = []
    N = len(G.nodes)
    nodes = list(G.nodes())
    Q = qu.Queue(maxsize=N)
    visit = [False for x in range(N)]
    parents = [-1 for x in range(N)]
    index = nodes.index(s)
    visit[index] = True
    Q.put(s)
    while(not Q.empty()):
        u = Q.get()
        indexu = nodes.index(u)
        if (u==t):
            found = True
            path = doPath(nodes,parents,s,t) # in order s ---> t
            bottleneck = findBottleneck(G,path)
            break
        else:
            for v in G.neighbors(u):
                index = nodes.index(v)
                if(not visit[index]):
                    visit[index] = True
                    parents[index] = indexu
                    Q.put(v)
    return [found, bottleneck, path]
#%%
    
#%%
"""
Push flow along a path
-> adds to the path found to target the maximum amount of flow that it can 
   handle. Later the flux will be compared to the capacity of each edge, 
   and this will be eliminated if necessary.
"""
def push_flow(G, flow, path):
    N = len(path)
    fatG = G.copy()
    for i in range(N-1):
        fatG[path[i]][path[i+1]][0]['flow']+=flow
    return fatG
#%%

#%%
"""
Data downloaded from: http://konect.uni-koblenz.de/networks/foodweb-baywet
Import the data and name the columns. Round the feed_factor to an integer
and delete edges with feed_factor = 0.
"""
fla = pd.read_csv("foodweb-baywet/out.foodweb-baywet", delimiter=r"\s+", 
                  index_col=False, comment="%", header=None)
fla.columns = ['from', 'to', 'capacity']
fla.capacity = fla.capacity.astype(int)
fla = fla[fla.capacity > 0]

"""
Build directed weighted graph from the data and add 'flow' attribute 
initialized to 0. Build initial residual graph and choose source and target 
nodes.
"""
myG = nx.from_pandas_edgelist(fla, source='from', target='to', 
                              edge_attr=['capacity'], 
                              create_using=nx.MultiDiGraph())
# add atributte that did not exist and set value
nx.set_edge_attributes(myG, 0, 'flow')
#%%

#%%
"""
FORD-FULKERSON
"""
# set source and target nodes
s=1; t=128;
progress = []
progress.append((0, myG))
resG = residual_graph(myG)
aug_path = augmenting_path_BFS(resG, s, t)
count = 0
while (aug_path[0]):
    bottleneck = aug_path[1]
    path = aug_path[2]
    # add bottleneck to flow attribute of corresponding edges
    newG = push_flow(myG, bottleneck, path)
    myG = newG
    progress.append((bottleneck, myG))
    resG = residual_graph(myG)
    aug_path = augmenting_path_BFS(resG, s, t)
    count+=1

print('source:',s)
print('target:',t)
print('iterations done:', count)
tot_flow = 0
for i in range(len(progress)):
    tot_flow+=progress[i][0]
print("total flow transported:", tot_flow)
#%%

#%%
"""
Plot an iteration in the Ford-Fulkerson loop.
"""
def plot_iteration(G, s, t, bottleneck):
    pos = nx.layout.circular_layout(G, scale=2)
    fig, ax = plt.subplots(figsize=(12,12))
    node_sizes = 500
    node_colors=[]
    for node in G:
        if node==s:
            node_colors.append('blue')
        elif node==t:
            node_colors.append('red')
        else:
            node_colors.append('black')
    cmap = 'RdPu'
    capacities = nx.get_edge_attributes(G, 'capacity')
    flows = nx.get_edge_attributes(G, 'flow')
    edge_colors = []
    edge_labels = {}
    edge_alphas = []
    for edge in G.edges:
            if (flows[edge]>0):
                label = str(flows[edge]) + '/' + str(capacities[edge])
                edge_colors.append(flows[edge]/capacities[edge])
                edge_labels.update({edge[:2]:label})
                edge_alphas.append(1)
            else:
                edge_colors.append(0)
                edge_alphas.append(0)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                           node_color=node_colors)
    nx.draw_networkx_labels(G, pos, font_size=16, font_color='white', 
                            font_weight='bold')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, 
                                   arrowstyle='->', arrowsize=20, 
                                   edge_color=edge_colors,
                                   edge_cmap=plt.get_cmap(cmap), width=3)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_weight='bold', font_size=15)
    M = G.number_of_edges()
    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])
    if (edges):
        pc = mpl.collections.PatchCollection(edges, cmap=plt.get_cmap(cmap))
        pc.set_array(edge_colors)
        plt.colorbar(pc)
        pc.set_clim(0, 1.0)
    ax = plt.gca()
    ax.set_axis_off()
    plt.text(-2, 2, 'Flow += ' + str(bottleneck))
    plt.text(3.75, 0, 'Flow/Capacity', horizontalalignment='right',
             verticalalignment='center', rotation=-90)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image
#%%
        
#%%
"""
Make a gif with the evolution of the algorithm.
"""
import imageio
imageio.mimsave('./FF-'+str(s)+'-'+str(t)+'.gif', 
                [plot_iteration(progress[i][1], s, t, progress[i][0]) 
                for i in range(len(progress))], fps=1/1.5)
#%%
    
#%%
"""
Print final flow out of the source and into the target edge-by-edge.
"""
final_flow = nx.get_edge_attributes(myG, 'flow')
in_flow = 0
out_flow = 0

for edge in list(myG.edges):
    if (edge[0]==s):
        print(edge[:2], final_flow[edge])
        out_flow += final_flow[edge]
print('Total out-flow:', out_flow)
print('\n')       
for edge in list(myG.edges):
    if (edge[1]==t):
        print(edge[:2], final_flow[edge])
        in_flow += final_flow[edge]
print('Total in-flow:', in_flow)
#%%