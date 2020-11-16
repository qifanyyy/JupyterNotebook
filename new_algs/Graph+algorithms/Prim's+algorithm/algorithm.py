from random import randint as rand
import math
import svgwrite
import shutil
import os


class Graph:

    # Makes a graph with quadratic matrix (n x n)
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    # Prints info about MST and prints circle and rectangle view of MST
    def printMST(self, info):
        for n in range(len(info)):
            print(info[n][0], '\t', info[n][1])
# Start of making svd
# Circle-graph
            dwg = svgwrite.Drawing('static\pics\step' + str(n + 1) + '.svg', size=("1024px", "960px"))
            dwg.add(dwg.rect(insert=(30, 30),
                             size=("770px", "670px"),
                             stroke_width="1",
                             stroke="black",
                             fill="rgb(212,212,212)"))
            self.paintGridCirc(dwg)
            for j in range(0, n+1):
                self.paintConnectionCircle(dwg, info[j][0][0], info[j][0][1], drawWeight=True, weight=info[j][1])
            dwg.save()

# Rectangle graph
            dwg = svgwrite.Drawing('static\pics\step' + str(n+1) + '_rect.svg', size=("1024px", "960px"))
            dwg.add(dwg.rect(insert=(30, 30),
                             size=("770px", "670px"),
                             stroke_width="1",
                             stroke="black",
                             fill="rgb(212,212,212)"))
            self.paintGridRect(dwg)
            for j in range(n+1):
                self.paintConnectionRect(dwg, info[j][0][0], info[j][0][1], drawWeight=True, weight=info[j][1])
                self.paintConnectionRect(dwg, info[j][0][1], info[j][0][0], drawWeight=True, weight=info[j][1])
            dwg.save()
# Circle final
        dwg = svgwrite.Drawing('static\pics\graphCircle_final.svg', size=("1024px", "960px"))
        dwg.add(dwg.rect(insert=(30, 30),
                         size=("770px", "670px"),
                         stroke_width="1",
                         stroke="black",
                         fill="rgb(212,212,212)"))
        self.paintGridCirc(dwg)
        for i in range(self.V):
            for j in range(self.V):
                self.paintConnectionCircle(dwg, i, j, color="120,120,120", weight=self.graph[i][j])
        for j in range(0, len(info)):
            self.paintConnectionCircle(dwg, info[j][0][0], info[j][0][1], color="255,0,0", weight=info[j][1])
        dwg.save()
# Rectangle final
        dwg = svgwrite.Drawing('static\pics\graphRect_final.svg', size=("1024px", "960px"))
        dwg.add(dwg.rect(insert=(30, 30),
                         size=("770px", "670px"),
                         stroke_width="1",
                         stroke="black",
                         fill="rgb(212,212,212)"))

        self.paintGridRect(dwg)
        for i in range(self.V):
            for j in range(self.V):
                self.paintConnectionRect(dwg, i, j, color="120,120,120", weight=self.graph[i][j])
        for j in range(0, len(info)):
            self.paintConnectionRect(dwg, info[j][0][0], info[j][0][1], color="255,0,0", weight=info[j][1])
        dwg.save()

    # Shows the graph in a matrix view
    def showGraph(self):
        print(end='  ')
        for i in range(self.V):
            print(i, end=' ')
        print()
        for i in range(self.V):
            print(i, end=' ')
            for j in range(self.V):
                print(self.graph[i][j], end=' ')
            print()

    # Draws a grid and verticles for a rectangle version
    def paintGridRect(self, dwg, color="25,25,112"):
            # GRID
            dwg.add(
                dwg.line(start=(200, 300), end=(200 + 80 * 6, 300), style="stroke:rgb(160,160,160);stroke-width:1.5"))
            dwg.add(
                dwg.line(start=(200, 340), end=(200 + 80 * 6, 340), style="stroke:rgb(160,160,160);stroke-width:1.5"))
            for i in range(7):
                dwg.add(dwg.line(start=(200 + 80 * i, 300), end=(200 + 80 * i, 340),
                                 style="stroke:rgb(160,160,160);stroke-width:1.5"))
            if self.V > 6:
                dwg.add(dwg.line(start=(200, 400), end=(200 + 80 * 6, 400),
                                 style="stroke:rgb(160,160,160);stroke-width:1.5"))
                dwg.add(dwg.line(start=(200, 440), end=(200 + 80 * 6, 440),
                                 style="stroke:rgb(160,160,160);stroke-width:1.5"))
                for i in range(7):
                    dwg.add(dwg.line(start=(200 + 80 * i, 400), end=(200 + 80 * i, 440),
                                     style="stroke:rgb(160,160,160);stroke-width:1.5"))
                if self.V > 12:
                    dwg.add(dwg.line(start=(200, 500), end=(200 + 80 * 6, 500),
                                     style="stroke:rgb(160,160,160);stroke-width:1.5"))
                    dwg.add(dwg.line(start=(200, 540), end=(200 + 80 * 6, 540),
                                     style="stroke:rgb(160,160,160);stroke-width:1.5"))
                    for i in range(7):
                        dwg.add(dwg.line(start=(200 + 80 * i, 500), end=(200 + 80 * i, 540),
                                         style="stroke:rgb(160,160,160);stroke-width:1.5"))
            # END GRID, START VERTEX
            for i in range(self.V):
                dwg.add(dwg.circle(center=(240 + 80 * (i % 6), 320 + 100 * (i // 6)), r=18, fill="rgb(" + color + ")"))
                dwg.add(dwg.text(i, insert=(204 + 80 * (i % 6), 328 + 100 * (i // 6)),
                                 style="font-size:13;font-family:Comic Sans MS, Arial"))
            dwg.save()

    # Draws a grid and verticles for a circle version
    def paintGridCirc(self, dwg, color="25,25,112"):
        R = 250
        for i in range(self.V):
            x_center = 400 + R * math.sin(i * 2 * math.pi / self.V)
            y_center = 350 + R * math.cos(i * 2 * math.pi / self.V)
            dwg.add(dwg.circle(center=(x_center, y_center), r=14, fill="rgb(" + color + ")"))
            dwg.add(dwg.text(i, insert=(x_center + 13 - 3 * i * math.cos(2 * math.pi / (i + 1)),
                                        y_center + 15 - 7 * i * math.sin(2 * math.pi / (i + 1)))))
        dwg.save()

    # Draws a connect-line between 2 verticles for circle version
    def paintConnectionCircle(self, dwg, i, j, color="138,43,226", drawWeight=False, weight=0):
        if weight > 0:
            R = 250
            dwg.add(dwg.line(start=(400 + R * math.sin(i * 2 * math.pi / self.V),
                                    350 + R * math.cos(i * 2 * math.pi / self.V)),
                             end=(400 + R * math.sin(j * 2 * math.pi / self.V),
                                  350 + R * math.cos(j * 2 * math.pi / self.V)),
                             style="stroke:rgb(" + color + "); stroke-width:1.25"))
            if drawWeight:
                dwg.add(dwg.text(weight,
                                 insert=(400 + (R * math.sin(i * 2 * math.pi / self.V) +
                                                R * math.sin(j * 2 * math.pi / self.V)) / 2,
                                         335 + (R * math.cos(i * 2 * math.pi / self.V) +
                                                R * math.cos(j * 2 * math.pi / self.V)) / 2),
                                 fill="rgb(" + color + ")",
                                 style="font-size:17;font-family:Comic Sans MS, Arial"))
            dwg.save()

    # Draws a connect-line between 2 verticles for rect version
    def paintConnectionRect(self, dwg, i, j, color="138,43,226", drawWeight=False, weight=0):
        if weight > 0:
            if self.graph[i][j] > 0:
                if i < 6 and j < 6:  # CASE 1
                    dwg.add(dwg.path(d="M " + str(240 + 80 * i) + " 300 q "
                                       + str((j - i) * 80 / 2) + " -65 "
                                       + str((j - i) * 80) + " 0",
                                     style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                    if drawWeight:
                        dwg.add(dwg.text(weight, insert=(((240+80*i)+240+80*j)/2, 258), fill="rgb(" + color + ")",
                                         style="font-size:14;font-family:Comic Sans MS, Arial"))
                elif i < 6 and 6 <= j <= 11:  # CASE 2
                    dwg.add(dwg.path(d="M " + str(240 + 80 * i) + " 340 C "
                                       + str(240 + 80 * i) + " 365 "
                                       + str(240 + 80 * (j % 6)) + " 385 "
                                       + str(240 + (j % 6) * 80) + " 400",
                                     style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                    if drawWeight:
                        dwg.add(dwg.text(weight, insert=(((240+80*i)+240+80*(j%6)+18)/2, 368), fill="rgb(" + color + ")",
                                         style="font-size:14;font-family:Comic Sans MS, Arial"))
                elif i < 6 and 12 <= j <= 17:  # CASE 3
                    if (j % 6) > i:
                        dwg.add(dwg.path(d="M " + str(240 + 80 * i) + " 340 C "
                                           + str(240 + 80 * i + 40) + " 385 "
                                           + str(240 + 80 * i + 40) + " 440 "
                                           + str(240 + 80 * i + 40) + " 465 "
                                           + "S " + str(240 + 80 * (j % 6)) + " 485 "
                                           + str(240 + 80 * (j % 6)) + " 500 ",
                                         style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                        if drawWeight:
                            dwg.add(dwg.text(weight, insert=(((240 + 80 * (i%6) + 5), 465)),
                                             fill="rgb(" + color + ")",
                                             style="font-size:14;font-family:Comic Sans MS, Arial"))
                    else:
                        dwg.add(dwg.path(d="M " + str(240 + 80 * i) + " 340 C "
                                           + str(240 + 80 * i - 40) + " 385 "
                                           + str(240 + 80 * i - 40) + " 440 "
                                           + str(240 + 80 * i - 40) + " 465 "
                                           + "S " + str(240 + 80 * (j % 6)) + " 485 "
                                           + str(240 + 80 * (j % 6)) + " 500 ",
                                         style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                        if drawWeight:
                            dwg.add(dwg.text(weight, insert=(((240 + 80 * (i%6) - 18), 465)),
                                             fill="rgb(" + color + ")",
                                             style="font-size:14;font-family:Comic Sans MS, Arial"))
                elif 6 <= i <= 11 and 12 <= j <= 17:  # CASE 4
                    dwg.add(dwg.path(d="M " + str(240 + 80 * (i % 6)) + " 440 C "
                                       + str(240 + 80 * (i % 6)) + " 465 "
                                       + str(240 + 80 * (j % 6)) + " 485 "
                                       + str(240 + (j % 6) * 80) + " 500",
                                     style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                    if drawWeight:
                        dwg.add(dwg.text(weight, insert=(((240+80*(i%6))+240+80*(j%6)-10)/2, 463), fill="rgb(" + color + ")",
                                         style="font-size:14;font-family:Comic Sans MS, Arial"))
                elif 6 <= i <= 11 and 6 <= j <= 11:  # CASE 5
                    dwg.add(dwg.path(d="M " + str(240 + 80 * (i % 6)) + " 440 q "
                                       + str((j - i) * 80 / 2) + " 65 "
                                       + str((j - i) * 80) + " 0",
                                     style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                    if drawWeight:
                        dwg.add(dwg.text(weight, insert=(((240+80*(i%6))+240+80*(j%6))/2, 470), fill="rgb(" + color + ")",
                                         style="font-size:14;font-family:Comic Sans MS, Arial"))
                elif 12 <= i <= 17 and 12 <= j <= 17:  # CASE 6
                    dwg.add(dwg.path(d="M " + str(240 + 80 * (i % 6)) + " 540 q "
                                       + str((j - i) * 80 / 2) + " 65 "
                                       + str((j - i) * 80) + " 0",
                                     style="stroke:rgb(" + color + "); stroke-width:1.25; fill:none"))
                    if drawWeight:
                        dwg.add(dwg.text(weight, insert=(((240+80*(i%6))+240+80*(j%6))/2, 600), fill="rgb(" + color + ")",
                                         style="font-size:14;font-family:Comic Sans MS, Arial"))

            dwg.save()

    # Creates an svg file of the graph
    def graphToSVG(self):
# Circle-graph
        dwg = svgwrite.Drawing('static\pics\graph.svg', size=("1024px", "960px"))
        dwg.add(dwg.rect(insert=(30, 30),
                                   size = ("770px", "670px"),
                                   stroke_width = "1",
                                   stroke = "black",
                                   fill = "rgb(212,212,212)"))
        self.paintGridCirc(dwg)
        for i in range(self.V):
            randColor = str(rand(50, 255))+", "+str(rand(50, 255))+", "+str(rand(50, 255))
            for j in range(self.V):
                self.paintConnectionCircle(dwg, i, j, color=randColor, weight=self.graph[i][j])
        dwg.save()

        dwg = svgwrite.Drawing('static\pics\graph_rect.svg', size=("1024px", "960px"))
        dwg.add(dwg.rect(insert=(30, 30),
                         size=("770px", "670px"),
                         stroke_width="1",
                         stroke="black",
                         fill="rgb(212,212,212)"))

        self.paintGridRect(dwg)
# Connection drawing
        for i in range(self.V):
            randColor = str(rand(0, 200)) + ", " + str(rand(0, 200)) + ", " + str(rand(0, 200))
            for j in range(self.V):
                self.paintConnectionRect(dwg, i, j, randColor, weight=self.graph[i][j])
# Rectangular grid graphs
        dwg = svgwrite.Drawing('static\pics\graph_rect.svg', size=("1024px", "960px"))
        dwg.add(dwg.rect(insert=(30, 30),
                         size=("770px", "670px"),
                         stroke_width="1",
                         stroke="black",
                         fill="rgb(212,212,212)"))

        self.paintGridRect(dwg)
# Connection drawing
        for i in range(self.V):
            randColor = str(rand(0, 200)) + ", " + str(rand(0, 200)) + ", " + str(rand(0, 200))
            for j in range(self.V):
                self.paintConnectionRect(dwg, i, j, randColor, weight=self.graph[i][j])
        dwg.save()

    # A utility function to find the vertex with minimum distance value not in the set of visited vertex
    def minKey(self, key, mstSet):
        min = 999999
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
        try:
            return min_index
        except:
            return False

    # Runs Prim's algorithm for MST
    def primMST(self):
        # Key values used to pick minimum weight edge in cut
        info = []
        key = [9999999] * self.V  # max values of weights
        parent = [None] * self.V
        key[0] = 0  # the first vertex to start tree building
        mstSet = [False] * self.V  # list of visited vertices
        parent[0] = -1
        for index in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and not mstSet[v] and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u
            if index >= 1:
                info.append([[parent[u], u], key[u]])
        tree_existing = True  # checks if there is no such a tree
        for i in info:
            if not i[0][1]:
                tree_existing = False
                break
        if tree_existing:
            self.printMST(info)  # prints the resulted MST
        else:
            print('No such a tree')


# Generates a random undirected graph with determined size and return a matrix view of it (n x n)
def generateGraph(size, a, b):
    graph = [[-1000 for column in range(size)] for row in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j and graph[i][j] == -1000:
                randNum = rand(a, b)
                graph[i][j] = randNum
                graph[j][i] = randNum
    for i in range(size):
        for j in range(size):
            if graph[i][j] <= 0:
                graph[i][j] = 0
    return graph


def runAlg(size, a, b):
    if os.path.exists('static\pics'):
        shutil.rmtree('static\pics')
    if not os.path.exists('static\pics'):
        os.makedirs('static\pics')
    g = Graph(size)
    g.graph = generateGraph(size, a, b)
    g.primMST()
    g.showGraph()
    g.graphToSVG()

