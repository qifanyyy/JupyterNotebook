import subprocess
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import sys
import time
fig, ax = plt.subplots(figsize=(10,8))
G = nx.DiGraph()
#os.chdir(r"C:\Users\ASuS\Desktop\discrete math proj\algo repo\Bellman-Ford-algorithm-animation\Bellman-Ford\src")
def execute(Commands):
    commands=[]
    commands.extend(["java","Main"])
    commands.extend(Commands)
    Algorithm = subprocess.Popen(commands, stdout = subprocess.PIPE)
    resultList = []
    for line in Algorithm.stdout:
        if(line=='\n'):
            continue
        decode = line[:-2]
        resultList.append(decode.decode())
    return resultList



commands = []


Nodes = input("Enter Number of Nodes : ")
Edges = input("Enter Number of Edges : ")
commands.extend([Nodes,Edges])
print("Enter Nodes Name")

#add node to graph
for i in range(int(Nodes)):
    NodeName = input()
    commands.append(NodeName)
    G.add_node(NodeName,distance=0)

pos = nx.spring_layout(G)


print("Enter edges and sperate with space")
print("FromNodes-ToNodes-Weight")

#get edges from user and put into graph and commands
for i in range(int(Edges)):
    line = input()
    FromNodes,ToNodes,Weight = line.split()
    G.add_edge(FromNodes,ToNodes,weight=Weight)
    commands.extend([FromNodes,ToNodes,Weight])


OutPut = execute(commands)
print(execute(commands))

#extract edge labels
edge_labels = dict([((u,v),d['weight'])
             for u,v,d in G.edges(data=True)])
print(edge_labels)
#extract nodes label
Nodes_label = []
for node in G.nodes():
    Nodes_label.append(str(node))


#list for checking nodes
Visited_Nodes = []
Current_Nodes = []
Unvisited_Nodes = list(G.nodes()).copy()

#list for checking edges
Visited_Edges = []
Current_Edges = []
Unvisited_Edges = list(G.edges()).copy()


#function for period
def period():
    global Visited_Edges
    global Visited_Nodes
    global Unvisited_Edges
    global Unvisited_Nodes
    global Current_Edges
    global Current_Nodes
    Visited_Nodes = []
    Current_Nodes = []
    Unvisited_Nodes = list(G.nodes()).copy()
    Visited_Edges = []
    Current_Edges = []
    Unvisited_Edges = list(G.edges()).copy()

def render_distance():
    global pos
    for i in range(len(G.nodes())):
        x,y = pos[list(G.nodes())[i]]
        plt.text(x,y+0.105,str(G.nodes[list(G.nodes())[i]]['distance']), bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')



#function for render on page
count = 0
period_count=1
period_title = "Period : "+str(period_count)
def render(i):
    global count
    global period_count
    global period_title
    global Visited_Edges
    global Visited_Nodes
    global Unvisited_Edges
    global Unvisited_Nodes
    global Current_Edges
    global Current_Nodes
    global edge_labels
    ax.clear()
    if count==len(OutPut):
        stop_animation()
        count=0
        period()
        print("done")
        sys.exit()


    if "Node" in OutPut[count]:
        if(len(Current_Nodes) != 0 and OutPut[count][4:] in Visited_Nodes):
            period()
            period_count += 1
            period_title = "Period : "+str(period_count)
        if(len(Current_Nodes) != 0):
            Visited_Nodes.append(Current_Nodes[0])
        Current_Nodes.clear()
        Current_Nodes.append(OutPut[count][4:])
        Unvisited_Nodes.remove(OutPut[count][4:])

        #delete previous edge from current edge
        if(len(Current_Edges)!=0):
            Visited_Edges.append(Current_Edges[0])
        Current_Edges.clear()


    elif "Edge" in OutPut[count]:
        split_list = OutPut[count][4:].split(",")
        Unvisited_Edges.remove(tuple("".join(split_list)))
        if(len(Current_Edges)!=0):
            Visited_Edges.append(Current_Edges[0])
        Current_Edges.clear()
        Current_Edges.append(tuple("".join(split_list)))

    elif "Distance" in OutPut[count]:
        split_list =  OutPut[count][8:].split(",")
        G.nodes[split_list[0]]['distance']=split_list[1]


    elif "Final" in OutPut[count]:
        period()
        Unvisited_Edges = []
        Unvisited_Nodes = []
        edge_labels = {}
        while(True):
            if count==len(OutPut):
                break
            split_list = OutPut[count][6:].split(",")
            #sf
            Visited_Nodes.append(split_list[0])
            for i in range(len(split_list)-1):
                Visited_Nodes.append(split_list[i+1])
                Edge = [split_list[i],split_list[i+1]]
                if tuple("".join(Edge)) in edge_labels:
                    continue
                edge_labels.__setitem__(tuple("".join(Edge)),G[split_list[i]][split_list[i+1]]['weight'])
                Visited_Edges.append(tuple("".join(Edge)))
                Edge = []
            count += 1
        period_title = "Final Path"
        print(Visited_Edges)
        stop_animation()


    count +=1

    ax.set_title(period_title,fontdict={'fontsize': 18, 'fontweight': 'medium'})



    nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels,font_color='red')
    nx.draw_networkx_labels(G, pos=pos, labels=dict(zip(Nodes_label,Nodes_label)),  font_color="white", ax=ax)


    nx.draw_networkx_edges(G,pos=pos,edgelist=Visited_Edges,ax=ax,edge_color="black")
    nx.draw_networkx_edges(G,pos=pos,edgelist=Current_Edges,ax=ax,edge_color="violet")
    nx.draw_networkx_edges(G,pos=pos,edgelist=Unvisited_Edges,ax=ax,edge_color="gray")


    nx.draw_networkx_nodes(G, pos=pos, nodelist=Visited_Nodes, node_color="green",  ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=Current_Nodes, node_color="blue",  ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=Unvisited_Nodes, node_color="red",  ax=ax)
    render_distance()



ani = matplotlib.animation.FuncAnimation(fig, render,interval=1000,repeat=True)
def stop_animation():
    ani.event_source.stop()
#ani.save('myAnimation.gif', writer='imagemagick', fps=1)
#stop animation

plt.show()
