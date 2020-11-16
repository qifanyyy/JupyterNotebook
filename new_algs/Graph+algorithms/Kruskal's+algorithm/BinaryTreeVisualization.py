import random, pylab, ast
import time
import zoinks
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
font9="-family {Courier New} -size 12"
shell=None
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
#-----------------------------------------------------------------Globals-------------------------------------------------------
G=nx.Graph()
tree={}
rand = random.randint(1, 5)
label2 = None
fixed_positions = {1:(0,0),2:(-1,2)}#dict with two of the positions set
fixed_nodes = fixed_positions.keys()


#Graph is the canvas areana
#G is the graph

#Matlab: Drawing Graphs; This is where Visualization begins
root = tk.Tk()
Graph = tk.Canvas(root)
Graph.place(relx=0.0, rely=0.269, relheight=0.731, relwidth=0.71)
Graph.configure(background="#000000")
Graph.configure(cursor="arrow")
Graph.configure(highlightbackground="#0e7709")
Graph.configure(highlightcolor="#646464")
Graph.configure(insertbackground="black")
Graph.configure(relief="ridge")
Graph.configure(selectbackground="#188b07")
Graph.configure(selectforeground="black")

Entry1 = tk.Entry(root)
Entry1.place(relx=0.425, rely=0.063,height=40, relwidth=0.275)
Entry1.configure(background="#535353")
Entry1.configure(disabledbackground="#f0f0f0f0f0f0")
Entry1.configure(disabledforeground="#a3a3a3")
Entry1.configure(font="-family {Courier New} -size 12")
Entry1.configure(foreground="#000000")
Entry1.configure(highlightbackground="#d9d9d9")
Entry1.configure(highlightcolor="black")
Entry1.configure(insertbackground="black")
Entry1.configure(selectbackground="#c4c4c4")
Entry1.configure(selectforeground="black")

Entry1_7 = tk.Entry(root)
Entry1_7.place(relx=0.425, rely=0.127,height=40, relwidth=0.275)
Entry1_7.configure(background="#535353")
Entry1_7.configure(disabledbackground="#f0f0f0f0f0f0")
Entry1_7.configure(disabledforeground="#a3a3a3")
Entry1_7.configure(font="-family {Courier New} -size 12")
Entry1_7.configure(foreground="#000000")
Entry1_7.configure(highlightbackground="#d9d9d9")
Entry1_7.configure(highlightcolor="black")
Entry1_7.configure(insertbackground="black")
Entry1_7.configure(selectbackground="#c4c4c4")
Entry1_7.configure(selectforeground="black")

fig = Figure()
ax = plt.subplot()
ax.set_title('Complete Binary Tree', fontsize=10)

    #Adding the Graph into the TK window

visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
# visuals.draw()

toolbar = NavigationToolbar2Tk(visuals, Graph)
toolbar.update()
button = tk.Button(master=Graph, text="Quit", command=Graph.quit)
button.pack(side=tk.BOTTOM)
visuals.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


#----------------------------------------------------Functions-----------------------------------------------------------------
def mainmenu():
    root.destroy()
    import main

def Creation():
    #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, tree
    visuals.get_tk_widget().pack_forget()
    button.pack_forget()
    toolbar.pack_forget()
    pylab.ion()
    #---------------------------------------------Graph Generation backend----------------------------------------------------
    #Adding the Graph into the TK window
    nos = Entry1.get()        #No. of Nodes
    # n=int(nos)
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nos)==0:
        nos=0
    if len(nts)==0:  
        nts=0
    n=int(nos)
    # viz.num_of_nodes=n
    tree={}
    j=2
    for i in range(1,n+1):
        tree[i]=[]
    for i in range(1,n+1):
        if j<=n:
            tree[i].append(j)
            if j+1<=n:
                tree[i].append(j+1)
            j=j+2
    #------------------------------------------------------Creating a new Tree--------------------------------------------------            
    G=nx.Graph()
    print(tree)
    #Generating the Tree G created using the backend list into the tree
    for i,j in tree.items():
            for k in j:
                G.add_edge(i,k)   


    #Matlab: Drawing Graphs; This is where Visualization begins
    fig = plt.figure( dpi=100)
    ax = plt.subplot(111)
    ax.set_title('Complete Binary Tree', fontsize=10)

    # #Fixing the position static for the Graph
    #This line draws it on Canvas(Shows the result on canvas)
    pos = zoinks.hierarchy_pos(G,1)
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    
    #Adding the Graph into the TK window
    visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    visuals.draw()
    button = tk.Button(master=Graph, text="Quit", command=Graph.quit)
    button.pack(side=tk.BOTTOM)
    visuals.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def inorder():
    
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    pos = zoinks.hierarchy_pos(G,1)
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(tree.keys())[-1]
    txt=""
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[]
    j=0
    for i in (list(G.nodes())):
        x.append(i)       
        j=j+1
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if str(i)==str(nts):
            break
        plt.pause(0.7)
    # plt.figtext(str(x))
    txt=str(x)
    ino=plt.text(0.5,-0.1, "In-Order Traversal: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def preorder():
    
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    pos = zoinks.hierarchy_pos(G,1)    
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(tree.keys())[-1]
    txt=""
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[]
    j=0
    for i in (list(nx.dfs_preorder_nodes(G,1))):
        x.append(i)       
        j=j+1
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if str(i)==str(nts):
            break
        plt.pause(0.7)
    txt=str(x)
    pre=plt.text(0.5,-0.1, "Pre-Order Traversal: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def postorder():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    pos = zoinks.hierarchy_pos(G,1)
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(tree.keys())[-1]
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[]
    txt=""
    j=0
    for i in (list(nx.dfs_postorder_nodes(G,1))):
        x.append(i)       
        j=j+1
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if str(i)==str(nts):
            break
        plt.pause(0.7)
    txt=str(x)
    pos=plt.text(0.5,-0.1, "Post-Order Traversal: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph
    
def DFS():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions, tree
    pos = zoinks.hierarchy_pos(G,1)
    graph = tree
    visited=[]
    stack=list(graph.keys())
    stack.append(1)
    dfslist=[]
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(tree.keys())[-1]

    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')

    while(len(visited)!=len(graph)):
        popped_item=stack.pop()
        if((popped_item) not in visited):     #Pop element
            visited.append(popped_item)    #processing
            dfslist.append(popped_item)  
        for i in graph[popped_item]:     #Add all the popped neighbours in the stack
            if(i not in visited):
                stack.append(i)
    print(nts)
    x=[]
    j=0
    txt=""
    for i in (dfslist):
        j=j+1
        x.append(i)       
        plt.title('DFS Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if str(i)==str(nts):
            break
        plt.pause(0.7)
    txt=str(x)
    dfs=plt.text(0.5,-0.1, "DFS Order: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def BFS():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    pos = zoinks.hierarchy_pos(G,1)
    txt=""
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(tree.keys())[-1]
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[]
    j=0
    for i in (list(G.nodes())):
        x.append(i)       
        j=j+1
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=x, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        # visuals.after(1000)
        if str(i)==str(nts):
            break
        plt.pause(0.7)
        # plt.clf()
        # plt.show()
    txt=str(x)
    bfs=plt.text(0.5,-0.1, "BFS Order: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

def levelorder():
    # #--------------------------------------DELETING/Getting rid of any previous graph-----------------------------------------
    global Graph, visuals, button, toolbar, G, fixed_nodes,fixed_positions
    pos = zoinks.hierarchy_pos(G,1)
    txt=""
    nts= Entry1_7.get()     #No. to search
    #This will deal with empty Entry inputs
    if len(nts)==0:  
        nts=list(G.nodes())[-1]
    nx.draw(G ,pos, fixed=None, with_labels=True, node_size=800, node_color='skyblue', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
    x=[2**i for i in range(20)] #Exponential split: No. of elements per level
    print(x)
    y=list(G.nodes()) #The nodelist
    lot=[]   #Resultant level wise split list
    treelist=list(G.nodes())
    for i in range(len(x)):
        try:
            lot.append(y[x[i]-1:x[i+1]-1])
        except IndexError as error:
            # Output expected IndexErrors.
            break
    lot = [ele for ele in lot if ele != []] 
    j=0
    for i in (lot):   
        j=j+1
        plt.title('Iteration {}'.format(j))
        nx.draw_networkx_nodes(G, pos, nodelist=i, node_size=400, node_color='yellow', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
        if int(nts) in i:
            nx.draw_networkx_nodes(G, pos, nodelist=[int(nts)], node_size=400, node_color='red', node_shape="s", alpha=0.5, linewidths=10, font_size=8, font_weight='bold')
            break
        plt.pause(0.7)
        # plt.clf()
        plt.show()
    txt=str(lot)
    bfs=plt.text(0.5,-0.1, "Level Wise Traversal: "+txt, size=12, ha="center", transform=ax.transAxes)   #Shows the Caption below the graph

#Reset/Erase the Graph
def Destruction():
    global Graph, fig, ax, visuals, button, toolbar
    visuals.get_tk_widget().pack_forget()
    button.pack_forget()
    toolbar.pack_forget()
    fig = Figure()
    ax = plt.subplot(111)
    ax.set_title('Complete Binary Tree', fontsize=10)
    visuals = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    # visuals.draw()

    toolbar = NavigationToolbar2Tk(visuals, Graph)
    toolbar.update()
    button = tk.Button(master=Graph, text="Quit", command=Graph.quit)
    button.pack(side=tk.BOTTOM)
    visuals.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
w = None
num_of_nodes=0

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9' # X11 color: 'gray85'
_ana1color = '#d9d9d9' # X11 color: 'gray85'
_ana2color = '#ececec' # Closest X11 color: 'gray92'
font9 = "-family {System} -size 12 -weight bold"
style = ttk.Style()
style.configure('.',background=_bgcolor)
style.configure('.',foreground=_fgcolor)
style.configure('.',font="TkDefaultFont")
style.map('.',background=
    [('selected', _compcolor), ('active',_ana2color)])

root.geometry("777x631")
root.minsize(120, 1)
root.maxsize(1372, 893)
root.resizable(1, 1)
root.title("New Toplevel")
root.configure(background="#000000")
root.configure(highlightbackground="#d9d9d9")
root.configure(highlightcolor="#000000")

Canvas2 = tk.Canvas(root)
Canvas2.place(relx=1.308, rely=0.098, relheight=0.96
        , relwidth=0.278)
Canvas2.configure(background="#020202")
Canvas2.configure(cursor="arrow")
Canvas2.configure(highlightbackground="#095b06")
Canvas2.configure(highlightcolor="black")
Canvas2.configure(insertbackground="black")
Canvas2.configure(relief="ridge")
Canvas2.configure(selectbackground="#037414")
Canvas2.configure(selectforeground="black")

TSeparator1 = ttk.Separator(Canvas2)
TSeparator1.place(relx=0.046, rely=0.145, relwidth=0.884)

TSeparator1_1 = ttk.Separator(Canvas2)
TSeparator1_1.place(relx=0.046, rely=0.248, relwidth=0.884)

Canvas2_3 = tk.Canvas(Canvas2)
Canvas2_3.place(relx=-2.116, rely=-0.068, relheight=1.691
        , relwidth=1.75)
Canvas2_3.configure(background="#020202")
Canvas2_3.configure(cursor="arrow")
Canvas2_3.configure(highlightbackground="#095b06")
Canvas2_3.configure(highlightcolor="black")
Canvas2_3.configure(insertbackground="black")
Canvas2_3.configure(relief="ridge")
Canvas2_3.configure(selectbackground="#037414")
Canvas2_3.configure(selectforeground="black")

TSeparator1_4 = ttk.Separator(Canvas2_3)
TSeparator1_4.place(relx=0.048, rely=0.145, relwidth=0.884)

TSeparator1_2 = ttk.Separator(Canvas2_3)
TSeparator1_2.place(relx=0.048, rely=0.248, relwidth=0.884)

Label1 = tk.Label(root)
Label1.place(relx=0.245, rely=0.0, height=30, width=366)
Label1.configure(activebackground="#444444")
Label1.configure(activeforeground="white")
Label1.configure(activeforeground="black")
Label1.configure(background="#000000")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(font="-family {Sitka Small} -size 14")
Label1.configure(foreground="#008000")
Label1.configure(highlightbackground="#494949")
Label1.configure(highlightcolor="#ffffff")
Label1.configure(text='''Binary Tree Algorithm Visualization''')

Buttons = tk.Canvas(root)
Buttons.place(relx=0.721, rely=0.016, relheight=0.976
        , relwidth=0.278)
Buttons.configure(background="#020202")
Buttons.configure(cursor="arrow")
Buttons.configure(highlightbackground="#095b06")
Buttons.configure(highlightcolor="black")
Buttons.configure(insertbackground="black")
Buttons.configure(relief="ridge")
Buttons.configure(selectbackground="#037414")
Buttons.configure(selectforeground="black")
Buttons.configure(takefocus="0")

TSeparator1_2 = ttk.Separator(Buttons)
TSeparator1_2.place(relx=0.046, rely=0.144, relwidth=0.884)
TSeparator1_2.configure(takefocus="0")

TSeparator1_3 = ttk.Separator(Buttons)
TSeparator1_3.place(relx=0.051, rely=0.282, relwidth=0.884)
TSeparator1_3.configure(takefocus="0")

Canvas2_4 = tk.Canvas(Buttons)
Canvas2_4.place(relx=2.639, rely=0.502, relheight=1.0
        , relwidth=1.005)
Canvas2_4.configure(background="#020202")
Canvas2_4.configure(cursor="arrow")
Canvas2_4.configure(highlightbackground="#095b06")
Canvas2_4.configure(highlightcolor="black")
Canvas2_4.configure(insertbackground="black")
Canvas2_4.configure(relief="ridge")
Canvas2_4.configure(selectbackground="#037414")
Canvas2_4.configure(selectforeground="black")
Canvas2_4.configure(takefocus="0")

TSeparator1_5 = ttk.Separator(Canvas2_4)
TSeparator1_5.place(relx=0.046, rely=0.144, relwidth=0.885)
TSeparator1_5.configure(takefocus="0")

TSeparator1_3 = ttk.Separator(Canvas2_4)
TSeparator1_3.place(relx=0.046, rely=0.248, relwidth=0.885)
TSeparator1_3.configure(takefocus="0")

Canvas2_5 = tk.Canvas(Canvas2_4)
Canvas2_5.place(relx=2.631, rely=0.502, relheight=1.0, relwidth=1.0)

Canvas2_5.configure(background="#020202")
Canvas2_5.configure(cursor="arrow")
Canvas2_5.configure(highlightbackground="#095b06")
Canvas2_5.configure(highlightcolor="black")
Canvas2_5.configure(insertbackground="black")
Canvas2_5.configure(relief="ridge")
Canvas2_5.configure(selectbackground="#037414")
Canvas2_5.configure(selectforeground="black")
Canvas2_5.configure(takefocus="0")

TSeparator1_6 = ttk.Separator(Canvas2_5)
TSeparator1_6.place(relx=0.046, rely=0.144, relwidth=0.885)
TSeparator1_6.configure(takefocus="0")

TSeparator1_5 = ttk.Separator(Canvas2_5)
TSeparator1_5.place(relx=0.046, rely=0.248, relwidth=0.885)
TSeparator1_5.configure(takefocus="0")

Button1 = tk.Button(Buttons)
Button1.place(relx=0.046, rely=0.42, height=60, width=197)
Button1.configure(activebackground="#000000")
Button1.configure(activeforeground="white")
Button1.configure(activeforeground="#21edf8")
Button1.configure(background="#000000")
# Button1.configure(command=self.play)
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(font="-family {Segoe UI} -size 14")
Button1.configure(foreground="#00ffff")
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="#000000")
Button1.configure(pady="0")
Button1.configure(takefocus="0")
Button1.configure(text='''❷Pre-Order Traversal''')
Button1.configure(command=preorder)

Button2 = tk.Button(Buttons)
Button2.place(relx=0.046, rely=0.54, height=60, width=197)
Button2.configure(activebackground="#ececec")
Button2.configure(activeforeground="#000000")
Button2.configure(background="#000000")
Button2.configure(command=postorder)
Button2.configure(disabledforeground="#a3a3a3")
Button2.configure(font="-family {Segoe UI} -size 14")
Button2.configure(foreground="#00ff40")
Button2.configure(highlightbackground="#d9d9d9")
Button2.configure(highlightcolor="black")
Button2.configure(pady="0")
Button2.configure(takefocus="0")
Button2.configure(text='''➌Post Order Traversal''')

Button3 = tk.Button(Buttons)
Button3.place(relx=0.046, rely=0.66, height=60, width=197)
Button3.configure(activebackground="#ececec")
Button3.configure(activeforeground="#000000")
Button3.configure(background="#030303")
Button3.configure(command=BFS)
Button3.configure(disabledforeground="#a3a3a3")
Button3.configure(font="-family {Segoe UI} -size 14")
Button3.configure(foreground="#ffff00")
Button3.configure(highlightbackground="#d9d9d9")
Button3.configure(highlightcolor="black")
Button3.configure(pady="0")
Button3.configure(takefocus="0")
Button3.configure(text='''➍Breadth First Search''')

Button4 = tk.Button(Buttons)
Button4.place(relx=0.046, rely=0.78, height=60, width=197)
Button4.configure(activebackground="#ececec")
Button4.configure(activeforeground="#000000")
Button4.configure(background="#070707")
Button4.configure(command=DFS)
Button4.configure(disabledforeground="#a3a3a3")
Button4.configure(font="-family {Segoe UI} -size 14")
Button4.configure(foreground="#ff00ff")
Button4.configure(highlightbackground="#d9d9d9")
Button4.configure(highlightcolor="black")
Button4.configure(pady="0")
Button4.configure(takefocus="0")
Button4.configure(text='''➎Depth First Search''')

Button41 = tk.Button(Buttons)
Button41.place(relx=0.046, rely=0.899, height=60, width=197)
Button41.configure(activebackground="#ececec")
Button41.configure(activeforeground="#000000")
Button41.configure(background="#070707")
Button41.configure(command=levelorder)
Button41.configure(disabledforeground="#a3a3a3")
Button41.configure(font="-family {Segoe UI} -size 14")
Button41.configure(foreground="orange")
Button41.configure(highlightbackground="#d9d9d9")
Button41.configure(highlightcolor="black")
Button41.configure(pady="0")
Button41.configure(takefocus="0")
Button41.configure(text='''➏Level Order Search''')

Button5 = tk.Button(Buttons)
Button5.place(relx=0.046, rely=0.3, height=60, width=197)
Button5.configure(activebackground="#ececec")
Button5.configure(activeforeground="#000000")
Button5.configure(background="#020202")
Button5.configure(command=inorder)
Button5.configure(disabledforeground="#a3a3a3")
Button5.configure(font="-family {Segoe UI} -size 14")
Button5.configure(foreground="#ff0000")
Button5.configure(highlightbackground="#d9d9d9")
Button5.configure(highlightcolor="black")
Button5.configure(pady="0")
Button5.configure(takefocus="0")
Button5.configure(text='''❶ In-order Traversal''')

Button5_11 = tk.Button(Buttons)
Button5_11.place(relx=0.046, rely=0.1, height=70, width=197)
Button5_11.configure(activebackground="#ececec")
Button5_11.configure(activeforeground="#000000")
Button5_11.configure(background="black")
Button5_11.configure(command=mainmenu)
Button5_11.configure(disabledforeground="#a3a3a3")
Button5_11.configure(font="-family {Segoe UI} -size 14")
Button5_11.configure(foreground="white")
Button5_11.configure(highlightbackground="#d9d9d9")
Button5_11.configure(highlightcolor="black")
Button5_11.configure(pady="0")
Button5_11.configure(takefocus="0")
Button5_11.configure(text='''⌂ Back to Home''')

Label2 = tk.Label(root)
Label2.place(relx=-0.013, rely=0.063, height=41, width=305)
Label2.configure(activebackground="#030303")
Label2.configure(activeforeground="white")
Label2.configure(activeforeground="black")
Label2.configure(background="#000000")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(font="-family {System} -size 12 -weight bold")
Label2.configure(foreground="#00ff00")
Label2.configure(highlightbackground="#000000")
Label2.configure(highlightcolor="black")
Label2.configure(text='''Please enter the number of nodes :''')

Label2_6 = tk.Label(root)
Label2_6.place(relx=0.0, rely=0.127, height=41, width=326)
Label2_6.configure(activebackground="#030303")
Label2_6.configure(activeforeground="white")
Label2_6.configure(activeforeground="black")
Label2_6.configure(background="#000000")
Label2_6.configure(disabledforeground="#a3a3a3")
Label2_6.configure(font="-family {System} -size 12 -weight bold")
Label2_6.configure(foreground="#00ff00")
Label2_6.configure(highlightbackground="#000000")
Label2_6.configure(highlightcolor="black")
Label2_6.configure(text='''Please enter the number to be searched:''')

Button6_7 = tk.Button(root)
Button6_7.place(relx=0.309, rely=0.206, height=34, width=147)
Button6_7.configure(activebackground="#000000")
Button6_7.configure(activeforeground="white")
Button6_7.configure(activeforeground="#00ff00")
Button6_7.configure(background="#070707")
Button6_7.configure(disabledforeground="#a3a3a3")
Button6_7.configure(font="-family {System} -size 12 -weight bold")
Button6_7.configure(foreground="#00ff00")
Button6_7.configure(highlightbackground="#d9d9d9")
Button6_7.configure(highlightcolor="black")
Button6_7.configure(pady="0")
Button6_7.configure(text='''Reset''')
Button6_7.configure(command=Destruction)       #Calling the function to create the graph

# sdf=input()   

Button6 = tk.Button(root)
Button6.place(relx=0.515, rely=0.206, height=34, width=147)
Button6.configure(activebackground="#000000")
Button6.configure(activeforeground="white")
Button6.configure(activeforeground="#00ff00")
Button6.configure(background="#070707")
Button6.configure(disabledforeground="#a3a3a3")
Button6.configure(font=font9)
Button6.configure(foreground="#00ff00")
Button6.configure(highlightbackground="#d9d9d9")
Button6.configure(highlightcolor="black")
Button6.configure(pady="0")
Button6.configure(text='''Create''')
Button6.configure(command=Creation)       #Calling the function to create the graph

root.mainloop()

