from tkinter import *

import matplotlib

from main import work
from util.params import Params
from util.util import *

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def nope():
    print("nope nopety nope!")


def randomize_nodes():
    no_nodes = int(node_count_entry.get())
    nodes = get_random_points(no_nodes)
    string = ''
    for point in nodes:
        string += str(point.x) + ' ' + str(point.y)
        string += '\n'
    node_list_entry.delete(1.0, "end")
    node_list_entry.insert("end", string)


def randomize_edge():
    no_nodes = int(node_count_entry.get())
    no_edges = int(edge_count_entry.get())
    edges = get_random_edges(no_nodes, no_edges)
    string = ''
    for edge in edges:
        string += str(edge.start) + ' ' + str(edge.end)
        string += '\n'
    edge_list_entry.delete(1.0, "end")
    edge_list_entry.insert("end", string)


def run_genetic():
    nodes = []
    nodes_string = node_list_entry.get(1.0, "end")
    for node_string in nodes_string.split("\n"):
        if node_string == '':
            continue
        nodes.append(Point(int(node_string.split()[0]), int(node_string.split()[1])))

    edges = []
    edges_string = edge_list_entry.get(1.0, "end")
    for edge_string in edges_string.split("\n"):
        if edge_string == '':
            continue
        start, end = edge_string.split()[0], edge_string.split()[1]
        start, end = int(start), int(end)
        edges.append(Edge(start, end))

    print(nodes, edges)
    work(nodes, edges)


root = Tk()
root.attributes("-fullscreen", True)
"""MENU"""
menu = Menu(root)
root.config(menu=menu)

mutation_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Mutation", menu=mutation_menu)
mutation_menu.add_command(label="Swapping Mutation", command=Params.set_mutation_function("Swapping Mutation"))
mutation_menu.add_command(label="Mutation 1", command=Params.set_mutation_function("1"))
mutation_menu.add_command(label="Mutation 2", command=Params.set_mutation_function("2"))
mutation_menu.add_command(label="Mutation 3", command=Params.set_mutation_function("3"))
mutation_menu.add_command(label="Mutation 4", command=Params.set_mutation_function("4"))
mutation_menu.add_separator()
mutation_menu.add_command(label="No mutation", command=Params.set_mutation_function("None"))

crossover_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Crossover", menu=crossover_menu)
crossover_menu.add_command(label="Standard half Crossover", command=Params.set_crossover_function("Standard"))
crossover_menu.add_command(label="Jumbled half Crossover", command=Params.set_crossover_function("Jumbled"))
crossover_menu.add_separator()
crossover_menu.add_command(label="No Crossover", command=Params.set_crossover_function("None"))

"""INPUT BOX"""
left_frame = Frame(root, width=50)
left_frame.pack(side=LEFT, fill='both')
input_label = Label(left_frame, text="INPUT", font="Helvetica 44 bold underline")
input_label.pack(side=TOP)
node_label = Label(left_frame, text="NODE", font="Helvetica 24")
node_label.pack(side=TOP, pady=(20, 10))

node_entry_frame = Frame(left_frame)
node_entry_frame.pack(side=TOP, fill=X)
node_count_label = Label(node_entry_frame, text="count")
node_count_entry = Entry(node_entry_frame)
node_count_label.pack(side=LEFT, padx=20)
node_count_entry.pack(side=LEFT)
node_randomize_button = Button(node_entry_frame, text='Randomize!', command=randomize_nodes)
node_randomize_button.pack(side=RIGHT, padx=(50, 20))
node_list_entry = Text(left_frame, height=10, width=20)
node_list_entry.pack(side=TOP, pady=25, padx=50)

border_line = Frame(left_frame, height=1, width=250, bg="black")
border_line.pack(padx=5)

edge_label = Label(left_frame, text="EDGE", font="Helvetica 24")
edge_label.pack(side=TOP, pady=(20, 10))

edge_entry_frame = Frame(left_frame)
edge_entry_frame.pack(side=TOP, fill=X)
edge_count_label = Label(edge_entry_frame, text="count")
edge_count_entry = Entry(edge_entry_frame)
edge_count_label.pack(side=LEFT, padx=20)
edge_count_entry.pack(side=LEFT)

edge_randomize_button = Button(edge_entry_frame, text='Randomize!', command=randomize_edge)
edge_randomize_button.pack(side=RIGHT, padx=(50, 20))
edge_list_entry = Text(left_frame, height=10, width=20)
edge_list_entry.pack(side=TOP, pady=25, padx=50)

run_button = Button(left_frame, text="RUN IT!", bg="light blue", command=run_genetic)
run_button.pack(side=BOTTOM, pady=(10, 20))

border_line_1 = Frame(root, width=1, bg="black")
border_line_1.pack(fill=Y, pady=5, side=LEFT)

non_input_frame = Frame(root)
non_input_frame.pack(side=LEFT, fill='both', expand='yes')

"""BOTTOM FRAME"""
bottom_frame = Frame(non_input_frame, height=300)
bottom_frame.pack(side=BOTTOM, fill=X, pady=20)
settings_label = Label(bottom_frame, text="SETTINGS")


def get_settings(entries):
    entries[0].insert(0, Params.initial_population_size)
    entries[1].insert(0, Params.crossover_parents)
    entries[2].insert(0, Params.mutation_parents)
    entries[3].insert(0, Params.random_count)
    entries[4].insert(0, Params.propogation_count)
    entries[5].insert(0, Params.stop_genetic_after_count)
    entries[6].insert(0, Params.display_delay)
    print(Params.initial_population_size)
    print(Params.crossover_parents)
    print(Params.mutation_parents)
    print(Params.random_count)
    print(Params.propogation_count)
    print(Params.stop_genetic_after_count)
    print(Params.display_delay)


def save_settings():
    Params.initial_population_size = int(entries[0].get())
    Params.crossover_parents = int(entries[1].get())
    Params.mutation_parents = int(entries[2].get())
    Params.random_count = int(entries[3].get())
    Params.propogation_count = int(entries[4].get())
    Params.stop_genetic_after_count = int(entries[5].get())
    Params.display_delay = int(entries[6].get())
    Params.show_plot = bool(entries[7].get())
    print(Params.initial_population_size)
    print(Params.crossover_parents)
    print(Params.mutation_parents)
    print(Params.random_count)
    print(Params.propogation_count)
    print(Params.stop_genetic_after_count)
    print(Params.display_delay)
    print(Params.show_plot)


entries = []

save_settings_button = Button(bottom_frame, text='SAVE', command=save_settings)
bottom_left_frame = Frame(bottom_frame)
bottom_right_frame = Frame(bottom_frame)
settings_label.grid(row=0, columnspan=2)
save_settings_button.grid(row=2, columnspan=2, pady=20)
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_rowconfigure(1, weight=1)

bottom_left_frame.grid(row=1, column=0)

variables = ['initial_size', 'parents_crossover', 'parents_mutate', 'parents_random', 'top_n_parents', 'stop_after',
             'display_delay']

for i in range(4):
    label = Label(bottom_left_frame, text=variables[i])
    entry = Entry(bottom_left_frame)
    label.grid(row=i, columnspan=2, sticky=E, pady=5)
    entry.grid(row=i, column=2)
    entries.append(entry)

bottom_right_frame.grid(row=1, column=1)

for i in range(4, len(variables)):
    label = Label(bottom_right_frame, text=variables[i])
    entry = Entry(bottom_right_frame)
    label.grid(row=i, columnspan=2, sticky=E, pady=5)
    entry.grid(row=i, column=2)
    entries.append(entry)

var = IntVar()
entries.append(var)
get_settings(entries)
display_checkbox = Checkbutton(bottom_right_frame, text='show plot', variable=var)
var.set(1)
display_checkbox.grid(row=len(variables), columnspan=3, pady=5)

"""TOP FRAME - GRAPH FRAME"""
top_frame = Frame(non_input_frame, bg='green')
top_frame.pack(fill=BOTH, side=BOTTOM, pady=50, padx=100)

f = Figure(figsize=(10, 10), dpi=100)
a = f.add_subplot(111)

canvas = FigureCanvasTkAgg(f, top_frame)
canvas.show()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
Params.subplot = a
Params.canvas = canvas
Params.root = top_frame

root.mainloop()
