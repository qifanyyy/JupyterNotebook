from WGraphClass import *
from tkinter import *
root = Tk()

w = Canvas(root, width=600, height=400)
w.pack()

widgetlist = []

g1 = Dgraph()

coords = []
vertices_save = {}
alphab = [i for i in range(50)]

def createcoor(event):
    coords.append((event.x, event.y))

    if len(coords) == 1:
        btn = Button(root, text=alphab[0], bg='white', command=lambda j=alphab[0]: clickbutton(j))
        btn.place(x=coords[0][0], y=coords[0][1])
        widgetlist.append(btn)
        vertices_save[alphab[0]] = (coords[0][0], coords[0][1])
        g1.addnode(alphab[0])
        del alphab[0]

    if len(coords) == 1:
        del coords[0]

w.bind("<Button-1>", createcoor)

entry3 = Entry(root)
entry3.pack(side=RIGHT)
label3 = Label(root, text='Distance entry')
label3.pack(side=RIGHT)

connecter = []
distsT = {}
linescolor = {}

def clickbutton(a):
    connecter.append(a)
    if len(connecter) == 2:
        g1.addarrow((connecter[0], connecter[1]), int(entry3.get()))
        x1 = vertices_save[connecter[0]][0]
        y1 = vertices_save[connecter[0]][1]
        x2 = vertices_save[connecter[1]][0]
        y2 = vertices_save[connecter[1]][1]
        linescolor[(connecter[0], connecter[1])] = (x1, y1, x2, y2)
        w.create_line(x1, y1, x2, y2)
        distsT[(connecter[0], connecter[1])] = Label(root, text='{}'.format(g1.dists[(connecter[0], connecter[1])]))
        distsT[(connecter[0], connecter[1])].place(x=(x1 + x2)/2,y=(y1 + y2)/2+10)
        del connecter[0]
        del connecter[0]

def prims(graph):
    begin = graph.closest_neighb(graph.nodes[0])[0]
    tree = []
    if (begin,graph.nodes[0]) in graph.arrows:
        tree = [(begin,graph.nodes[0])]
    else:
        tree = [(graph.nodes[0],begin)]
    while len(tree) < len(graph.nodes)-1:
        least = 10e3
        new_edge = None
        for i in graph.get_edges(tree):
            if graph.dists[i] < least:
                least = graph.dists[i]
                if i in graph.arrows:
                    new_edge = i
                else:
                    new_edge = (i[1],i[0])
        tree.append(new_edge)
    print(tree)
    for k in tree:
        w.create_line(linescolor[k][0],linescolor[k][1],linescolor[k][2],linescolor[k][3],fill='green')

def exec_prims():
    prims(g1)

prims_Btn = Button(root, text='Execute Prims Algorithm', command=exec_prims)
prims_Btn.pack(side= LEFT)

root.mainloop()