import tkinter as tk
from tkinter import ttk

import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as mpl
from graph_colorizer import GraphColorizer

win = tk.Tk()
win.title("Genetic algorithm for graph coloring - Maciej Zamorski")
win.resizable(0, 0)

filename_label = ttk.Label(win, text="Filepath")
filename_label.grid(column=0, row=0)

filename = tk.StringVar()
filename_entry = ttk.Entry(win, width=20, textvariable=filename)
filename_entry.grid(column=0, row=1)
filename_entry.focus()

times_run_label = ttk.Label(win, text="Number of runs")
times_run_label.grid(column=1, row=0)

times_run = tk.IntVar()
times_run_entry = ttk.Entry(win, width=20, textvariable=times_run)
times_run_entry.grid(column=1, row=1)

population_size_label = ttk.Label(win, text="Population size")
population_size_label.grid(column=0, row=2)

population_size = tk.IntVar()
population_size_entry = ttk.Entry(win, width=20, textvariable=population_size)
population_size_entry.grid(column=0, row=3)

max_time_label = ttk.Label(win, text="Generations")
max_time_label.grid(column=1, row=2)

max_time = tk.IntVar()
max_time_entry = ttk.Entry(win, width=20, textvariable=max_time)
max_time_entry.grid(column=1, row=3)

crossing_prob_label = ttk.Label(win, text="Crossover probability")
crossing_prob_label.grid(column=0, row=4)

crossing_prob = tk.IntVar()
crossing_prob_entry = ttk.Entry(win, width=20, textvariable=crossing_prob)
crossing_prob_entry.grid(column=0, row=5)

mutation_prob_label = ttk.Label(win, text="Mutation probability")
mutation_prob_label.grid(column=1, row=4)

mutation_prob = tk.IntVar()
mutation_prob_entry = ttk.Entry(win, width=20, textvariable=mutation_prob)
mutation_prob_entry.grid(column=1, row=5)


def set_params():
    path = "files/" + filename.get()
    params = {
        'N': times_run.get(),
        'T': max_time.get(),
        'population_size': population_size.get(),
        'mutation_probability': mutation_prob.get() / 100,
        'crossover_probability': crossing_prob.get() / 100,
        'max_no_improvements': 100,
    }
    return path, params


def compute_results_stats(results):
    best_results = []
    worst_results = []
    avg_results = []
    for best, worst, avg in results:
        best_results.append(best)
        worst_results.append(worst)
        avg_results.append(avg)
    return best_results, worst_results, avg_results


def plot_results(results, best_results, worst_results, avg_results):
    x = [k for k in range(len(results))]
    line1, = mpl.plot(x, best_results, label='Best result')
    line2, = mpl.plot(x, avg_results, label='Average result')
    line3, = mpl.plot(x, worst_results, label='Worst result')
    mpl.legend([line1, line2, line3], ["Best", "Average", "Worst"])
    mpl.show()


def show_results(results):
    best_results, worst_results, avg_results = compute_results_stats(results)
    plot_results(results, best_results, worst_results, avg_results)


def run():
    path, params = set_params()
    gc = GraphColorizer(path, params)
    results = gc.colorize()
    colors = [result[1] for result in results]
    result = 'Min: {:.2f}, max: {:.2f}, avg: {:.2f}'.format(
        min(colors), max(colors), sum(colors) / len(colors))
    results_label = ttk.Label(win, text=result)
    results_label.grid(column=2, row=1)


def run_stats():
    path, params = set_params()
    gc = GraphColorizer(path, params)
    results = gc.run_statistics()
    show_results(results)


def generation_stats():
    path, params = set_params()
    gc = GraphColorizer(path, params)
    results = gc.generations_statistics()
    show_results(results)

run_button = ttk.Button(win, text="Colorize", command=run)
run_button.grid(column=2, row=0)

stats_iter = ttk.Button(win, text="Single run statistics",
                        command=generation_stats)
stats_iter.grid(column=2, row=2)

stats_button = ttk.Button(win, text="Multiple runs statistics",
                          command=run_stats)
stats_button.grid(column=2, row=4)

win.mainloop()
