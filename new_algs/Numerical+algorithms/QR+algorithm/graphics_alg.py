import matplotlib.pyplot as plt
import numpy as np

# use two global list in order to have easy access of them
report_match_some_columns = list()
report_AIC = list()
average_time = list()
report_missmatch_columns = list()

n_list = 4

y_colors = ["green", "red", "gold", "deepskyblue"]


def get_data(filepath):
    # function to get GA computed data in order to show it on graphics

    global report_match_some_columns
    global report_AIC
    global average_time
    global report_missmatch_columns

    try:
        fd = open(filepath, 'r')
        line = fd.readline()
        cnt = 0
        while line:
            values = line.split(",")

            report_match_some_columns.append(float(values[0]))
            report_AIC.append(float(values[1]))
            average_time.append(float(values[2]))
            report_missmatch_columns.append(float(values[3]))

            line = fd.readline()

            # save number of instances
            cnt += 1
    finally:
        fd.close()

    return cnt


# function to get GA computed data in order to show it on graphics
def get_data_tuning(filepath):

    global report_match_some_columns
    global report_AIC
    global average_time
    global report_missmatch_columns

    try:
        fd = open(filepath, 'r')
        line = fd.readline()
        cnt = 0
        while line:
            values = line.split(",")

            report_match_some_columns.append(float(values[0]))
            report_AIC.append(float(values[1]))
            average_time.append(float(values[2]))
            report_missmatch_columns.append(float(values[3]))

            line = fd.readline()

            # save number of instances
            cnt += 1
    finally:
        fd.close()

    return cnt


def get_graphic():

    ########################################
    # scatter the data

    global y_colors

    data = list()

    for i in range(n_list):
        temp_list = []
        temp_list.extend([report_match_some_columns[i], report_missmatch_columns[i], report_AIC[i], average_time[i]])
        data.append(temp_list)

    dim = len(data)

    w = 0.75
    dimw = w / dim

    fig, ax = plt.subplots()
    x = np.arange(len(data))
    x_names = ["GA", "HC", "SA", "GA_BB"]
    y_label = ["Columns match", "Columns missmatch", "AIC error", "Time execution(s)"]
    for i in range(len(data[0])):
        y = [d[i] for d in data]
        b = ax.bar(x + i * dimw, y, dimw, bottom=0.001, label=y_label[i], color=y_colors[i])

    plt.setp(ax, xticks=x + dimw / 2, xticklabels=x_names)

    ax.legend(fancybox=True, framealpha=0.5, loc='upper right')
    ax.set_title('Comparing the performance of heuristic algorithms')

    fig.tight_layout()
    plt.grid(True)

    # plt.show()
    plt.savefig('./output_graphics/generated_images/comparing_alg/Img.png')


def get_graphic2():

    ########################################
    # scatter the data

    data = list()

    for i in range(n_list):
        temp_list = []
        temp_list.extend([report_match_some_columns[i], report_AIC[i]])
        data.append(temp_list)

    width = 0.35

    ax = plt.subplot(2, 1, 1)
    x = np.arange(len(data))
    x_names = ["GA", "HC", "SA", "GA_BB"]
    y_label = ["Columns match", "AIC error"]
    y_colors = ["deepskyblue", "orangered"]

    for i in range(len(data[0])):
        y = [d[i] for d in data]
        b = ax.bar(x + i * width, y, width, bottom=0.001, label=y_label[i], color=y_colors[i])

    plt.setp(ax, xticks=x + width / 2, xticklabels=x_names)

    ax.legend(fancybox=True, framealpha=0.5, loc='upper right')
    ax.set_title('Comparing the performance of heuristic algorithms')

    data = average_time.copy()

    ax2 = plt.subplot(2, 1, 2)
    x2_names = ["GA", "HC", "SA", "GA_BB"]
    y_label = ["Time execution(s)"]

    ax2.plot(x2_names, data, label=y_label[0], color="green")

    ax2.legend(fancybox=True, framealpha=0.5, loc='upper right')

    # plt.show()
    plt.savefig('./output_graphics/generated_images/comparing_alg/Img.png')


def get_graphic3():

    ########################################
    # scatter the data

    global y_colors

    data = list()

    for i in range(n_list):
        temp_list = []
        temp_list.extend([report_match_some_columns[i], report_missmatch_columns[i], report_AIC[i], average_time[i]])
        data.append(temp_list)

    dim = len(data)

    w = 0.75
    dimw = w / dim

    ax = plt.subplot(2, 1, 1)
    x = np.arange(len(data))
    x_names = ["GA", "HC", "SA", "GA_BB"]
    y_label = ["Columns match", "Columns missmatch", "AIC error", "Time execution(s)"]
    for i in range(len(data[0])):
        y = [d[i] for d in data]
        b = ax.bar(x + i * dimw, y, dimw, bottom=0.001, label=y_label[i], color=y_colors[i])

    plt.setp(ax, xticks=x + dimw / 2, xticklabels=x_names)
    plt.title("Comparing the performance of heuristic algorithms")

    ax.legend(fancybox=True, framealpha=0.5, loc='upper right')
    plt.grid(True)

    ax3 = plt.subplot(2, 1, 2)
    for i in range(len(data[0])):
        y = [d[i] for d in data]
        b = ax3.bar(x + i * dimw, y, dimw, bottom=0.001, label=y_label[i], color=y_colors[i])

    plt.setp(ax3, xticks=x + dimw / 2, xticklabels=x_names)

    ax3.set(ylim=(0.0, 1.1))
    ax3.set_title('Zoomed in', fontsize=8)

    plt.grid(True)

    # plt.show()
    plt.savefig('./output_graphics/generated_images/comparing_alg/Img.png')


def get_graphic_tuning(alg):

    ########################################
    # scatter the data
    fig, ax = plt.subplots()

    n_config = len(report_match_some_columns)
    x = np.arange(n_config)

    lines = plt.plot(x, report_match_some_columns, x, report_missmatch_columns, x, report_AIC, x, average_time)
    plt.setp(lines[0], linewidth=4, color=y_colors[0])
    plt.setp(lines[1], linewidth=3, color=y_colors[1])
    plt.setp(lines[2], linewidth=2, color=y_colors[2])
    plt.setp(lines[3], linewidth=1, color=y_colors[3])

    plt.legend(("Columns match", "Columns missmatch", "AIC error", "Time execution(s)"),
               fancybox=True, framealpha=0.5, loc='upper right', fontsize='x-small')
    ax.set_title('Comparing the performance of ' + alg)

    plt.grid(True)

    # fig.tight_layout()

    # plt.show()
    plt.savefig('./output_graphics/generated_images/tunning/difRandomColumns/Img.png')


def execute():
    n = get_data("./output_individuals/Out_Algorithms.csv")

    if n:
        if max(average_time) > 1:
            get_graphic3()
        else:
            get_graphic()
    else:
        print("Empty data, graphic picture could not be created")


def execute_tuning(alg):
    n = get_data_tuning("./output_individuals/Out_Algorithms_Tuning.csv")

    if n:
        get_graphic_tuning(alg)
    else:
        print("Empty data, graphic picture could not be created")