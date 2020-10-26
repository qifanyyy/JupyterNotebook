# Created By Parth Dani
# Date 24/05/2020

import sys
import os

VERTICES = []
GRAPH = []
VISITED = []
REVERSE = []
RESULT_SCC = []
COMPONENT = []


def reading_file():
    line_counter = 0
    valid_lines = []
    path_of_file = "test_data_implementation_1.txt"
    if not os.path.isfile(path_of_file):
        sys.exit("Files doesnt exists")
    file = open(path_of_file, "r")
    read_lines = file.readlines()
    for line in read_lines:
        if not line.isspace():
            valid_lines.append(line)
    file.close()
    file = open(path_of_file, "w")
    file.write("".join(valid_lines))
    file.close()
    file = open(path_of_file)
    for line in file:
        line = line[:-1]
        if len(line.split(",")) == 2 or len(line.split(",")) == 3:
            add_edges_and_vertices(line.split(",")[0], line.split(",")[1], line_counter)
            line_counter += 1


def add_edges_and_vertices(edge1, edge2, counter):
    GRAPH.append(edge1)
    GRAPH[counter] += ":"
    GRAPH[counter] += edge2
    if edge1 not in VERTICES:
        VERTICES.append(edge1)
    if edge2 not in VERTICES:
        VERTICES.append(edge2)


def create_graph_matrix(vertex, transposed):
    newMatrix = [["."] * (len(vertex) + 1) for i in range(len(vertex) + 1)]
    for column in range(len(vertex) + 1):
        for row in range(len(vertex) + 1):
            if column == 0:
                if row == 0:
                    newMatrix[column][row] = "-"
                else:
                    newMatrix[column][row] = vertex[row - 1]
            else:
                if row == 0:
                    newMatrix[column][row] = vertex[column - 1]
                else:
                    newMatrix[column][row] = "-"

    for i in range(len(vertex) + 1):
        for j in range(len(vertex) + 1):
            for k in range(len(GRAPH)):
                if (newMatrix[i][0] == GRAPH[k].split(":")[0]) and (newMatrix[0][j] == GRAPH[k].split(":")[1]):
                    if transposed == 0:
                        newMatrix[i][j] = "E"
                    else:
                        newMatrix[j][i] = "E"
    return newMatrix


def depth_first_search(yAxis, matrix):
    if not matrix[yAxis][0] in VISITED:
        VISITED.append(matrix[yAxis][0])
    RESULT_SCC.append(matrix[yAxis][0])
    for xAxis in range(1, len(VERTICES) + 1):
        if matrix[yAxis][xAxis] == "E" and not matrix[xAxis][0] in VISITED:
            depth_first_search(xAxis, matrix)
    REVERSE.append(matrix[yAxis][0])
    COMPONENT.append(matrix[yAxis][0])
    return


if __name__ == '__main__':
    reading_file()
    graph_matrix = create_graph_matrix(VERTICES, 0)
    for row in graph_matrix:
        print(row)
    for v in range(1, len(VERTICES)):
        if VERTICES[v] not in VISITED:
            depth_first_search(v + 1, graph_matrix)
    REVERSE = REVERSE[::-1]
    graph_matrix = create_graph_matrix(REVERSE, 1)
    RESULT_SCC = []
    VISITED = []
    print("Strongly connected components are :")
    for v in range(len(REVERSE)):
        if RESULT_SCC.count(REVERSE[v]) == 0:
            COMPONENT = []
            depth_first_search(v + 1, graph_matrix)
            print(COMPONENT)
