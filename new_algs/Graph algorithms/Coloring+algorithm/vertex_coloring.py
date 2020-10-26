import csv
from matplotlib import pyplot
from edge_coloring import get_color
from random import randint

Y_COORDINATE_DIC = {}


def get_y(v):
    """
    assume v is x_coordiante, method returns its y_coordinate
    :param v: the x coordinate
    :return: the y coordinate
    """
    if v in Y_COORDINATE_DIC.keys():
        return Y_COORDINATE_DIC[v]
    x = randint(0, 10000)
    rnd = randint(x, x + randint(1, 10000))
    Y_COORDINATE_DIC[v] = rnd
    return rnd


def do_normalization(set_of_vertices):
    """
    map vertices to numbers start from 0
    :param set_of_vertices vertices of input graph
    """
    sorted_set = sorted(set_of_vertices)
    c = 1
    table = {}
    for x in sorted_set:
        table[x] = c
        c += 1
    print(table)
    return table


def do_vertex_coloring(input_path1, input_path2):
    """
    draw graph which its vertices are colored , with aid of matplotlib library
    :param input_path1: the path to input of vertex_coloring process of java code
    :param input_path2: the path to output of vertex_coloring process of java code
    :return:
    """
    unsorted_set = set()
    src = []
    dst = []
    colors = {}

    with open(input_path1, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            unsorted_set.add(int(row[0]))
            unsorted_set.add(int(row[1]))

    table = do_normalization(unsorted_set)

    with open(input_path1, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            src.append(table.get(int(row[0])))
            dst.append(table.get(int(row[1])))

    print(src)
    print(dst)
    with open(input_path2, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            colors[int(row[0])] = int(row[1])

    for i in range(0, len(src)):
        x = src[i]
        y = get_y(x)
        a = dst[i]
        b = get_y(a)

        d1 = [x, a]

        d2 = [y, b]

        pyplot.plot(d1, d2, '#000000', markersize=50)

    for i in range(0, len(src)):
        x = src[i]
        y = get_y(x)
        a = dst[i]
        b = get_y(a)
        pyplot.scatter(x, y, c=get_color(colors[x]), marker='o')
        pyplot.annotate(x, (x, y), size=10)
        pyplot.scatter(a, b, c=get_color(colors[a]), marker='o')
        pyplot.annotate(a, (a, b), size=10)

    pyplot.show()

    print('sources')
    print(src)
    print('destinations')
    print(dst)
    print('colors')
    print(colors)
