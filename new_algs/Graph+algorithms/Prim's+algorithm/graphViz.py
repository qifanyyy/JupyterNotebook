#----------------------------------------------------Headers------------------------------------------------------
import random, pylab, ast
import time
import tkinter
from networkx.algorithms import tree
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
font9="-family {Courier New} -size 12"
shell=None
import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

G=nx.DiGraph()
pos = nx.spring_layout(G)
graph={}
rand = random.randint(1, 5)
label2 = None
fixed_positions = {1:(0,0),2:(-1,2)}#dict with two of the positions set
fixed_nodes = fixed_positions.keys()
#----------------------------------------------------Globals-------------------------------------------------------

root = tk.Tk()
'''This class configures and populates the rootlevel window.
    root is the rootlevel containing window.'''
_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9' # X11 color: 'gray85'
_ana1color = '#d9d9d9' # X11 color: 'gray85'
_ana2color = '#ececec' # Closest X11 color: 'gray92'
font11 = "-family {Lucida Console} -size 12"
font12 = "-family {Segoe UI} -size 12 -weight bold"
font14 = "-family {MS UI Gothic} -size 11 -weight bold"
font15 = "-family {MS PGothic} -size 14 -weight bold"
font16 = "-family {Segoe UI} -size 12 -weight bold"
font17 = "-family {Lucida Sans Unicode} -size 13 -weight bold "  \
    "-underline 1"
font23 = "-family {Arial} -size 14"
font24 = "-family {Segoe UI} -size 14"
font27 = "-family {Arial} -size 12"
font9 = "-family {Segoe UI} -size 9"
style = ttk.Style()
style.configure('.',background=_bgcolor)
style.configure('.',foreground=_fgcolor)
style.configure('.',font="TkDefaultFont")
style.map('.',background=
    [('selected', _compcolor), ('active',_ana2color)])

#----------------------------------------------------GUI Begins-----------------------------------------------
root.geometry("850x727")
root.minsize(120, 1)
root.maxsize(1372, 893)
root.resizable(1, 1)
root.title("New Toplevel")
root.configure(background="#000000")
root.configure(highlightbackground="#000000")
root.configure(highlightcolor="black")

Graph = tk.Canvas(root)
Graph.place(relx=0.0, rely=0.457, relheight=0.543, relwidth=0.698)
Graph.configure(background="#000000")
Graph.configure(borderwidth="2")
Graph.configure(highlightbackground="#00ff00")
Graph.configure(highlightcolor="black")
Graph.configure(insertbackground="black")
Graph.configure(relief="ridge")
Graph.configure(selectbackground="#c4c4c4")
Graph.configure(selectforeground="black")

menubar = tk.Menu(root,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
root.configure(menu = menubar)

Canvas1 = tk.Canvas(root)
Canvas1.place(relx=0.702, rely=0.0, relheight=0.999, relwidth=0.294)

Canvas1.configure(background="#000000")
Canvas1.configure(borderwidth="2")
Canvas1.configure(highlightbackground="#00ff00")
Canvas1.configure(highlightcolor="#00ff00")
Canvas1.configure(insertbackground="black")
Canvas1.configure(relief="ridge")
Canvas1.configure(selectbackground="#00ff00")
Canvas1.configure(selectforeground="black")

Entry1 = tk.Entry(Canvas1)
Entry1.place(relx=0.596, rely=0.124,height=20, relwidth=0.336)
Entry1.configure(background="white")
Entry1.configure(disabledforeground="#a3a3a3")
Entry1.configure(font="TkFixedFont")
Entry1.configure(foreground="#000000")
Entry1.configure(insertbackground="black")

Entry2 = tk.Entry(Canvas1)
Entry2.place(relx=0.596, rely=0.167,height=20, relwidth=0.336)
Entry2.configure(background="white")
Entry2.configure(disabledforeground="#a3a3a3")
Entry2.configure(font="TkFixedFont")
Entry2.configure(foreground="#000000")
Entry2.configure(insertbackground="black")

default_text = True
# v=tk.StringVar(root, value='default text')
Entry3 = tk.Entry(root)
Entry3.place(relx=0.0, rely=0.106, relheight=0.268, relwidth=0.695)
Entry3.configure(background="#000000")
Entry3.configure(borderwidth="2")
Entry3.configure(font=font27)
Entry3.configure(foreground="#80ff00")
Entry3.configure(highlightbackground="#80ff00")
Entry3.configure(highlightcolor="#008000")
Entry3.configure(highlightthickness="2")
Entry3.configure(insertbackground="#00ff00")
Entry3.configure(selectbackground="#00ff00")
Entry3.configure(selectforeground="black")
Entry3.insert(0,"Enter Here, the Graph Adjacency List in the format mentioned above...")
def delete_text(event):
    global default_text
    if default_text:
        Entry3.delete(0, tk.END)
        default_text = False
Entry3.bind("<Button-1>", delete_text)

Label5 = tk.Label(root)
Label5.place(relx=0.012, rely=0.385, height=41, width=404)
Label5.configure(activebackground="#000000")
Label5.configure(activeforeground="white")
Label5.configure(activeforeground="#ff0000")
Label5.configure(background="#000000")
Label5.configure(disabledforeground="#a3a3a3")
Label5.configure(font=font14)
Label5.configure(foreground="#ff0000")
Label5.configure(justify='left')
Label5.configure(text='''''')

Label3_5 = tk.Label(Canvas1)
Label3_5.place(relx=0.037, rely=0.821, height=20, width=147)
Label3_5.configure(activebackground="#f9f9f9")
Label3_5.configure(activeforeground="black")
Label3_5.configure(background="#000000")
Label3_5.configure(disabledforeground="#a3a3a3")
Label3_5.configure(font="-family {MS UI Gothic} -size 11 -weight bold")
Label3_5.configure(foreground="#80ff00")
Label3_5.configure(highlightbackground="#d9d9d9")
Label3_5.configure(highlightcolor="black")
Label3_5.configure(text='''Start Node:''')

Label3_6 = tk.Label(Canvas1)
Label3_6.place(relx=0.037, rely=0.865, height=20, width=147)
Label3_6.configure(activebackground="#f9f9f9")
Label3_6.configure(activeforeground="black")
Label3_6.configure(background="#000000")
Label3_6.configure(disabledforeground="#a3a3a3")
Label3_6.configure(font="-family {MS UI Gothic} -size 11 -weight bold")
Label3_6.configure(foreground="#80ff00")
Label3_6.configure(highlightbackground="#d9d9d9")
Label3_6.configure(highlightcolor="black")
Label3_6.configure(text='''End Node:''')

Entry1_7 = tk.Entry(Canvas1)
Entry1_7.place(relx=0.595, rely=0.821,height=20, relwidth=0.312)
Entry1_7.configure(background="white")
Entry1_7.configure(disabledforeground="#a3a3a3")
Entry1_7.configure(font="TkFixedFont")
Entry1_7.configure(foreground="#000000")
Entry1_7.configure(highlightbackground="#d9d9d9")
Entry1_7.configure(highlightcolor="black")
Entry1_7.configure(insertbackground="black")
Entry1_7.configure(selectbackground="#c4c4c4")
Entry1_7.configure(selectforeground="black")

Entry1_8 = tk.Entry(Canvas1)
Entry1_8.place(relx=0.595, rely=0.865,height=20, relwidth=0.312)
Entry1_8.configure(background="white")
Entry1_8.configure(disabledforeground="#a3a3a3")
Entry1_8.configure(font="TkFixedFont")
Entry1_8.configure(foreground="#000000")
Entry1_8.configure(highlightbackground="#d9d9d9")
Entry1_8.configure(highlightcolor="black")
Entry1_8.configure(insertbackground="black")
Entry1_8.configure(selectbackground="#c4c4c4")
Entry1_8.configure(selectforeground="black")


fig = Figure()
ax = plt.subplot()
ax.set_title('Visualization Area', fontsize=10)

    #Adding the Graph into the TK window

visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
# visuals.draw()

toolbar = NavigationToolbar2Tk(visuals, Graph)
toolbar.update()
button = tkinter.Button(master=Graph, text="Quit", command=Graph.quit)
button.pack(side=tkinter.BOTTOM)
visuals.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#-----------------------------------------Functions-----------------------------------------------
def main():
    root.destroy()
    import main
def Terminus():
    Entry3.delete(0, tk.END)  #Reseting the Entry3
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    visuals.get_tk_widget().pack_forget()       #Reseting the Canvas
    button.pack_forget()
    toolbar.pack_forget()
    Label5.configure(text='''''')

def CreateGraph():
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos, graph
    wlgraph={}
    for (u, v) in (G.adj).items():
        wlgraph[u]=[]
    for (u, v) in (G.adj).items():
        for val2 in v.keys():
            wlgraph[u].append(val2)
    graph=wlgraph
        

def Genisis1():
    #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos
    visuals.get_tk_widget().pack_forget()
    button.pack_forget()
    toolbar.pack_forget()
    pylab.ion()
    Label5.configure(text='''''')
    #---------------------------------------------Graph Generation backend----------------------------------------------------
    #Adding the Graph into the TK window
    nos = Entry1.get()        #No. of Nodes
    # n=int(nos)
    nts= Entry2.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nos)==0:
        nos=0
    if len(nts)==0:  
        nts=0
    n=int(nos)
    m=random.randint(0,n+1)
    #Random Graph
    G = nx.fast_gnp_random_graph(n, 0.7, seed=None, directed=False)
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = random.randint(0,10)
    for (u, v) in G.edges():
        print(G.edges[u,v]['weight']),
    #Matlab: Drawing Graphs; This is where Visualization begins
    fig = plt.figure( dpi=100)
    ax = plt.subplot(111)
    ax.set_title('Graph Visualization', fontsize=10)
    labels = nx.get_edge_attributes(G,'weight')
    # #Fixing the position static for the Graph
    #This line draws it on Canvas(Shows the result on canvas)
    pos = nx.spring_layout(G)
    nx.draw(G,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    plt.axis('off')
    print(G.edges())
    CreateGraph()
    #Adding the Graph into the TK window
    visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    visuals.draw()
    button = tkinter.Button(master=Graph, text="Quit", command=Graph.quit)
    button.pack(side=tkinter.BOTTOM)
    visuals.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def Genisis2():
    #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos
    visuals.get_tk_widget().pack_forget()
    button.pack_forget()
    toolbar.pack_forget()
    pylab.ion()
    Label5.configure(text='''''')
    #-------------------------------------------Graph Based on the Input Given------------------------------------------------
    graph= ast.literal_eval(str(Entry3.get()))
    print((graph))
    try:
        G=nx.DiGraph(graph)
    except:
        Label5.configure(text='''Make sure the format is correct and please try again...''')
    fig = plt.figure( dpi=100)
    ax = plt.subplot(111)
    ax.set_title('Graph Visualization', fontsize=10)
    labels = nx.get_edge_attributes(G,'weight')
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    nx.draw(G,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    plt.axis('off')
    print(G.edges())
    CreateGraph()
    #Adding the Graph into the TK window
    visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    visuals.draw()
    button = tkinter.Button(master=Graph, text="Quit", command=Graph.quit)
    button.pack(side=tkinter.BOTTOM)
    visuals.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
def DFS():
     # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos
    print(graph)
    visited=[]
    stack=list(graph.keys())
    # stack.append((graph.keys())[0])
    dfslist=[]
    nts= Entry2.get()                           #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=int(list(G.nodes())[-1])

    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    while(len(visited)!=len(graph)):
        popped_item=stack.pop()
        if((popped_item) not in visited):     #Pop element
            visited.append(popped_item)    #processing
            dfslist.append(popped_item)  
        for i in graph[popped_item]:     #Add all the popped neighbours in the stack
            if(i not in visited):
                stack.append(i)
    print(nts)
    print(dfslist)
    x=[]
    j=0
    txt=""
    nx.draw_networkx_nodes(G, pos, nodelist=[list(graph.keys())[0]], node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    for i in (dfslist):
        j=j+1
        x.append(i)       
        plt.title('DFS Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if str(i)==str(nts):
            nx.draw_networkx_nodes(G, pos, nodelist=[i], node_size=400, node_color='red', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
            break
        plt.pause(1)
    txt=str(x)
    dfs=plt.text(0.5,-0.1, "DFS Order: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def BFS():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos, graph
    txt=""
    nts= Entry2.get()     #No. to search
    print("Inside BFs")
    print(graph,G.nodes())
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=int(list(G.nodes())[-1])
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[]
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    j=0
    for i in (list(G.nodes())):
        j=j+1
        x.append(i)       
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        # visuals.after(1000)
        print("Getting Inside")
        if str(i)==str(nts):
            nx.draw_networkx_nodes(G, pos, nodelist=[i], node_size=400, node_color='red', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
            break
        plt.pause(1)
        # plt.clf()
        # plt.show()
    txt=str(x)
    bfs=plt.text(0.5,-0.1, "BFS Order: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph


def Shortest_Path():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos, graph
    startnode=Entry1_7.get()
    endnode=Entry1_8.get()
    #This will deal with empty Entry inputs
    if len(startnode)==0:  
        startnode=int(list(G.nodes())[-1])
    #This will deal with empty Entry inputs
    if len(endnode)==0:  
        endnode=int(list(G.nodes())[-1])
    p=nx.shortest_path(G)
    print(p)
    path=list(p[int(startnode)][int(endnode)])
    print("PAth="+str(path))
    x=[]
    txt=""
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    labels = nx.get_edge_attributes(G,'weight')
    j=0
    for i in path:
        j=j+1
        x.append(i)       
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        # visuals.after(1000)
        print("Getting Inside")
        if str(i)==str(endnode):
            nx.draw_networkx_nodes(G, pos, nodelist=[i], node_size=400, node_color='red', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
            break
        plt.pause(1)
        # plt.clf()
        # plt.show()
    txt=str(x)
    sp=plt.text(0.5,-0.1, "Shortest Path: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph


def Prims():
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos, graph
    mst = tree.minimum_spanning_edges(G, algorithm='prim', data=False)
    edgelist = list(mst)
    print(edgelist)
    Label5.configure(text=edgelist)
    j=0
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    for i in edgelist:
        plt.title('Iteration {}'.format(j))
        j=j+1
        nx.draw_networkx_edges(G, pos,
                       edgelist=[i],
                       width=8, alpha=0.5, edge_color='r')
        print("Getting Inside")
        plt.pause(1)
        # plt.clf()
        # plt.show()
    prims=plt.text(0.5,-0.1, "Prims Edges Order: "+str(edgelist), size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def Kruskals():
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, pos, graph
    mst = tree.minimum_spanning_edges(G, algorithm='kruskal', data=False)
    edgelist = list(mst)
    print(edgelist)
    Label5.configure(text=edgelist)
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G ,pos, edge_labels=labels)
    j=0
    for i in edgelist:
        plt.title('Iteration {}'.format(j))
        j=j+1
        nx.draw_networkx_edges(G, pos,
                       edgelist=[i],
                       width=8, alpha=0.5, edge_color='r')
        print("Getting Inside")
        plt.pause(1)
        # plt.clf()
        # plt.show()
    kruskals=plt.text(0.5,-0.1, "Kruskal's Edges Order: "+str(edgelist), size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def FindBoundaries():
    return
    

#--------------------------------------Might Add this in Future-----------------------------------
# combobox = tk.StringVar()
# TCombobox1 = ttk.Combobox(Canvas1)
# TCombobox1.place(relx=0.08, rely=0.291, relheight=0.029
#         , relwidth=0.868)
# value_list = ['Custom Graph ','Random Graph','Peterson Graph','Tetrahedral','Icosahedron','Octahedron','Binomial Graph',]
# TCombobox1.configure(values=value_list)
# TCombobox1.configure(font=font9)
# TCombobox1.configure(textvariable=combobox)
# TCombobox1.configure(foreground="#00ff00")
# TCombobox1.configure(background="#000000")
# TCombobox1.configure(takefocus="")
# TCombobox1.configure(cursor="fleur")

Button4 = tk.Button(root)
Button4.place(relx=0.494, rely=0.385, height=44, width=167)
Button4.configure(activebackground="#000000")
Button4.configure(activeforeground="white")
Button4.configure(activeforeground="#008000")
Button4.configure(background="#000000")
Button4.configure(disabledforeground="#a3a3a3")
Button4.configure(font=font12)
Button4.configure(foreground="#008000")
Button4.configure(highlightbackground="#d9d9d9")
Button4.configure(highlightcolor="black")
Button4.configure(highlightthickness="2")
Button4.configure(pady="0")
Button4.configure(command=Genisis2)
Button4.configure(text='''Create Custom Graph''')

Button1 = tk.Button(Canvas1)
Button1.place(relx=0.108, rely=0.028, height=64, width=197)
Button1.configure(activebackground="#ececec")
Button1.configure(activeforeground="#000000")
Button1.configure(background="#000000")
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(font=font15)
Button1.configure(foreground="#c0c0c0")
Button1.configure(highlightbackground="#ffffff")
Button1.configure(highlightcolor="black")
Button1.configure(highlightthickness="2")
Button1.configure(pady="0")
Button1.configure(command=main)
Button1.configure(text='''⌂ Back to Home''')

Button1_1 = tk.Button(Canvas1)
Button1_1.place(relx=0.08, rely=0.346, height=64, width=217)
Button1_1.configure(activebackground="#000000")
Button1_1.configure(activeforeground="white")
Button1_1.configure(activeforeground="#ff0000")
Button1_1.configure(background="#000000")
Button1_1.configure(disabledforeground="#ff0000")
Button1_1.configure(font=font23)
Button1_1.configure(foreground="#ff0000")
Button1_1.configure(highlightbackground="#ff0000")
Button1_1.configure(highlightcolor="#ff0000")
Button1_1.configure(highlightthickness="2")
Button1_1.configure(pady="0")
Button1_1.configure(command=BFS)
Button1_1.configure(text='''Breadth First Search''')

Button1_2 = tk.Button(Canvas1)
Button1_2.place(relx=0.08, rely=0.456, height=64, width=217)
Button1_2.configure(activebackground="#000000")
Button1_2.configure(activeforeground="white")
Button1_2.configure(activeforeground="#ff8040")
Button1_2.configure(background="#000000")
Button1_2.configure(disabledforeground="#a3a3a3")
Button1_2.configure(font=font23)
Button1_2.configure(foreground="#ff8040")
Button1_2.configure(highlightbackground="#d9d9d9")
Button1_2.configure(highlightcolor="black")
Button1_2.configure(pady="0")
Button1_2.configure(command=DFS)
Button1_2.configure(text='''Depth First Search''')

Button1_3 = tk.Button(Canvas1)
Button1_3.place(relx=0.08, rely=0.567, height=64, width=217)
Button1_3.configure(activebackground="#000000")
Button1_3.configure(activeforeground="white")
Button1_3.configure(activeforeground="#ffff00")
Button1_3.configure(background="#000000")
Button1_3.configure(disabledforeground="#a3a3a3")
Button1_3.configure(font=font24)
Button1_3.configure(foreground="#ffff00")
Button1_3.configure(highlightbackground="#d9d9d9")
Button1_3.configure(highlightcolor="black")
Button1_3.configure(pady="0")
Button1_3.configure(command=Prims)
Button1_3.configure(text='''Prim's MST Algorithm''')

Button1_4 = tk.Button(Canvas1)
Button1_4.place(relx=0.08, rely=0.678, height=64, width=217)
Button1_4.configure(activebackground="#000000")
Button1_4.configure(activeforeground="white")
Button1_4.configure(activeforeground="#008000")
Button1_4.configure(background="#000000")
Button1_4.configure(disabledforeground="#a3a3a3")
Button1_4.configure(font=font24)
Button1_4.configure(foreground="#008000")
Button1_4.configure(highlightbackground="#d9d9d9")
Button1_4.configure(highlightcolor="black")
Button1_4.configure(pady="0")
Button1_4.configure(command=Kruskals)
Button1_4.configure(text='''Kruskal's MST Algorithm''')

Button1_5 = tk.Button(Canvas1)
Button1_5.place(relx=0.082, rely=0.924, height=44, width=217)
Button1_5.configure(activebackground="#000000")
Button1_5.configure(activeforeground="white")
Button1_5.configure(activeforeground="#0000ff")
Button1_5.configure(background="#000000")
Button1_5.configure(disabledforeground="#a3a3a3")
Button1_5.configure(font="-family {Segoe UI} -size 14")
Button1_5.configure(foreground="#0000ff")
Button1_5.configure(highlightbackground="#d9d9d9")
Button1_5.configure(highlightcolor="black")
Button1_5.configure(pady="0")
Button1_5.configure(command=Shortest_Path)
Button1_5.configure(text='''Shortest Path Algorithm''')

Label3 = tk.Label(Canvas1)
Label3.place(relx=0.04, rely=0.124, height=21, width=137)
Label3.configure(background="#000000")
Label3.configure(disabledforeground="#a3a3a3")
Label3.configure(font=font14)
Label3.configure(foreground="#80ff00")
Label3.configure(text='''Number of Nodes:''')

Label4 = tk.Label(Canvas1)
Label4.place(relx=0.08, rely=0.167, height=21, width=130)
Label4.configure(background="#000000")
Label4.configure(disabledforeground="#a3a3a3")
Label4.configure(font=font14)
Label4.configure(foreground="#80ff00")
Label4.configure(text='''Node to Search:''')


Button2 = tk.Button(Canvas1)
Button2.place(relx=0.12, rely=0.25, height=34, width=88)
Button2.configure(activebackground="#80ff80")
Button2.configure(activeforeground="#008000")
Button2.configure(background="#000000")
Button2.configure(disabledforeground="#a3a3a3")
Button2.configure(font=font16)
Button2.configure(foreground="#008000")
Button2.configure(highlightbackground="#00ff00")
Button2.configure(highlightcolor="#000000")
Button2.configure(pady="0")
Button2.configure(command=Genisis1)
Button2.configure(text='''Create''')

Button3 = tk.Button(Canvas1)
Button3.place(relx=0.556, rely=0.25, height=34, width=89)
Button3.configure(activebackground="#80ff00")
Button3.configure(activeforeground="#000000")
Button3.configure(background="#000000")
Button3.configure(disabledforeground="#00ff00")
Button3.configure(font=font16)
Button3.configure(foreground="#008000")
Button3.configure(highlightbackground="#80ff00")
Button3.configure(highlightcolor="#000000")
Button3.configure(pady="0")
Button3.configure(command=Terminus)
Button3.configure(text='''Reset''')

TSeparator1 = ttk.Separator(Canvas1)
TSeparator1.place(relx=0.04, rely=0.332, relwidth=0.92)

TSeparator1_3 = ttk.Separator(Canvas1)
TSeparator1_3.place(relx=0.04, rely=0.207, relwidth=0.92)

Label1 = tk.Label(root)
Label1.place(relx=0.012, rely=0.041, height=22, width=382)
Label1.configure(activebackground="#000040")
Label1.configure(activeforeground="white")
Label1.configure(background="#000000")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(font=font11)
Label1.configure(foreground="#00ff00")
Label1.configure(text='''Please Enter the Graph Adjacency List:''')

Label2 = tk.Label(root)
Label2.place(relx=0.012, rely=0.069, height=21, width=573)
Label2.configure(background="#000000")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(font=font11)
Label2.configure(foreground="#00ff00")
Label2.configure(text='''Format: {val1: {val2: {'weight': w1}}, {val3: {'weight':w2}}, ...}''')

TLabel1 = ttk.Label(root)
TLabel1.place(relx=0.318, rely=0.0, height=29, width=269)
TLabel1.configure(background="#000000")
TLabel1.configure(foreground="#00ff00")
TLabel1.configure(font=font17)
TLabel1.configure(relief="flat")
TLabel1.configure(anchor='w')
TLabel1.configure(justify='left')
TLabel1.configure(text='''ALGORITHMS VISUALIZATION''')

root.mainloop()