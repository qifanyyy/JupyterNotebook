import tempfile, shlex, subprocess
import numpy as np


class MatrixGraph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.reset_color_and_distance()

    def reset_color_and_distance(self):
        self.color = ["white" for node in range(len(self.matrix))]
        self.distance = [None for node in range(len(self.matrix))]

    def display(self, filename):
        with tempfile.NamedTemporaryFile(delete=False) as tmpf:
            tmpf.write("graph BFS {\nnode [fontname=\"Arial\"];\n")
            for node in range(len(self.matrix)):
                label = str(self.distance[node]) if self.distance[node] else "*"
                tmpf.write("node%d [label=\"%s\" style=filled fillcolor=%s];\n" % (node, label, self.color[node]))
            for (x, y), value in np.ndenumerate(self.matrix):
                if value and x>=y:
                    tmpf.write("node%d -- node%d;\n" % (x,y))
            tmpf.write("}")
        cmd =  "dot -Tpng -o %s %s" % (filename, tmpf.name)
        args = shlex.split(cmd)
        subprocess.Popen(args)
        return

    def breadth_first_search(self, index, filenamebase="test"):
        self.reset_color_and_distance()
        self.distance[index] = 0
        queue = [index]
        count_display = 0
        while queue:
            node = queue.pop(0)
            self.color[node] = "green"
            self.display(filenamebase + str(count_display) + ".png")
            count_display += 1
            for i,value in enumerate(self.matrix[node]):
                if value and self.color[i] == "white":
                    self.color[i] = "grey"
                    self.distance[i] = self.distance[node] + 1
                    queue.append(i)
                    self.display(filenamebase + str(count_display) + ".png")
                    count_display += 1
            self.color[node] = "red"
            self.display(filenamebase + str(count_display) + ".png")
            count_display += 1
        return


class ListNode:
    def __init__(self, num, adjacency_list=[]):
        self.id = num
        self.adjacency = adjacency_list
        self.distance = None
        self.color = "white"

class ListGraph:
    def __init__(self, matrix):
        self.nodes = [ListNode(i) for i in range(len(matrix))]
        for i,line in enumerate(matrix):
            adjacency_list = []
            for j, value in enumerate(line):
                if value:
                    adjacency_list.append(self.nodes[j])
            self.nodes[i].adjacency = adjacency_list
        self.reset_color_and_distance()

    def reset_color_and_distance(self):
        for node in self.nodes:
            node.distance = None
            node.color = "white"

    def display(self, filename):
        with tempfile.NamedTemporaryFile(delete=False) as tmpf:
            tmpf.write("graph BST {\nnode [fontname=\"Arial\"];\n")
            for node in self.nodes:
                label = str(node.distance) if node.distance else "*"
                tmpf.write("node%d [label=\"%s\" style=filled fillcolor=%s];\n" % (node.id, label, node.color))
                for neighbor in node.adjacency:
                  if neighbor.id > node.id:
                        tmpf.write("node%d -- node%d;\n" % (node.id,neighbor.id))
            tmpf.write("}")
        cmd =  "dot -Tpng -o %s %s" % (filename, tmpf.name)
        args = shlex.split(cmd)
        subprocess.Popen(args)
        return

    def breadth_first_search(self, index, filenamebase="testlist"):
        self.reset_color_and_distance()
        root = self.nodes[index]
        root.distance = 0
        queue = [root]
        count_display = 0
        while queue:
            node = queue.pop(0)
            node.color = "green"
            self.display(filenamebase + str(count_display) + ".png")
            count_display += 1
            for neighbor in node.adjacency:
                if neighbor.color == "white":
                    neighbor.color = "grey"
                    neighbor.distance = node.distance + 1
                    queue.append(neighbor)
                    self.display(filenamebase + str(count_display) + ".png")
                    count_display += 1
            node.color = "red"
            self.display(filenamebase + str(count_display) + ".png")
            count_display += 1
        return


if __name__=='__main__':
    example_matrix = np.zeros(shape=(8, 8))
    example_matrix[0][1] = 1
    example_matrix[1][0] = 1
    example_matrix[0][4] = 1
    example_matrix[4][0] = 1
    example_matrix[5][1] = 1
    example_matrix[1][5] = 1
    example_matrix[2][5] = 1
    example_matrix[5][2] = 1
    example_matrix[5][6] = 1
    example_matrix[6][5] = 1
    example_matrix[2][3] = 1
    example_matrix[3][2] = 1
    example_matrix[2][6] = 1
    example_matrix[6][2] = 1
    example_matrix[3][6] = 1
    example_matrix[6][3] = 1
    example_matrix[3][7] = 1
    example_matrix[7][3] = 1
    example_matrix[6][7] = 1
    example_matrix[7][6] = 1

    g = MatrixGraph(example_matrix)
    g.breadth_first_search(3)

    h = ListGraph(example_matrix)
    h.breadth_first_search(3)