from math import sqrt
from random import choice
import sys

class Vertex:
    next_id = 0

    def __init__(self, name):
        self.id = Vertex.next_id
        Vertex.next_id += 1

        self.name = name

        self.neighbours = []

        self.color = None

        self.saturation = 0

    def get_degree(self):
        return len(self.neighbours)

    def __lt__(self, other):
        return self.get_degree() < other.get_degree()

    def __str__(self):
        return self.name + " | degree: " + str(self.get_degree()) + " | saturation: " + str(self.saturation) + " | color: " + str(self.color) 


class Graph:

    def __init__(self, vertex_list):
        self.vertex_list = vertex_list

    def get_statistics(self):
        ordered_vertexes = sorted(self.vertex_list)

        min_degree = ordered_vertexes[0].get_degree()
        max_degree = ordered_vertexes[-1].get_degree()

        degree_list = [vertex.get_degree() for vertex in ordered_vertexes]

        medium_degree = sum(degree_list) / len(degree_list)

        sd_degree = sqrt(sum([(degree - medium_degree)**2 for degree in degree_list]) / len(degree_list))

        return min_degree, max_degree, medium_degree, sd_degree


    @staticmethod
    def add_edges(v, u):
        if v not in u.neighbours:
            v.neighbours.append(u)
            u.neighbours.append(v)

class Color:
    next_id = 0
    color_names = ["Amarelo", "Azul", "Vermelho", "Verde", "Roxo", "Laranja", "Marrom", "Ocre", "Prata", "Preto", "Branco", "Coral", "Rosa", "Anil"] 

    def __init__(self):
        self.id = Color.next_id
        Color.next_id += 1

        self.name = Color.color_names[self.id]
        self.count = 0

    def __lt__(self, other):
        return self.count < other.count

    def __str__(self):
        return "[" + str(self.id) + " | count: " + str(self.count) + "]"

def Dsatur(g):
    colors = []

    for v in g.vertex_list:
        v.color = None

    random_v = get_next_dsatur_vertex(g) #choice(g.vertex_list) # talvez mudar pra pegar o de maior grau

    paint_vertex(random_v, colors)

    for u in random_v.neighbours:
        if u.color == None:
            u.saturation += 1

    new_v = get_next_dsatur_vertex(g)

    while (new_v != None):
        paint_vertex(new_v, colors)

        for u in new_v.neighbours:
            if u.color == None:
                u.saturation += 1

        new_v = get_next_dsatur_vertex(g)

    return colors
    

def paint_vertex(v, color_list):
    #print("Painting", str(v.name), "!")
    ordered_colors = sorted(color_list)

    neighbours_colors = [u.color for u in v.neighbours if u.color != None]

    # loop varre todas as cores, procurando uma que nao esteja nos vizinhos
    #print("Neighbours: ", list(map(lambda x: x.name, v.neighbours)))
    #print("Neighbours colors: ", list(map(lambda x: x.id, neighbours_colors)))
    #print("Ordered colors: ", list(map(lambda c: c.id, ordered_colors)))

    # if len(ordered_colors) > 3:
    #     print("Count 1, count 2, n:", ordered_colors[0], ordered_colors[1], ordered_colors[2], ordered_colors[3])

    for color in ordered_colors:
        #print("Checking color", color.id)
        if color not in neighbours_colors:
            v.color = color
            color.count += 1
            #print("Color", str(color.id), "!")
            return

    # criar cor nova
    new_color = Color()
    v.color = new_color
    new_color.count += 1

    #print("Color", str(new_color.id), "!")

    color_list.append(new_color)


def get_next_dsatur_vertex(g):
    unpainted_vertexes = [v for v in g.vertex_list if v.color == None]

    if len(unpainted_vertexes) == 0:
        return None

    unpainted_vertexes.sort(key = lambda x: x.saturation)

    max_saturation = unpainted_vertexes[-1]

    same_saturation_vertexes = [x for x in unpainted_vertexes if x.saturation == max_saturation.saturation]

    if len(same_saturation_vertexes) > 1:
        same_saturation_vertexes.sort()

        max_degree = same_saturation_vertexes[-1]

        same_degree_vertexes = [x for x in same_saturation_vertexes if x.get_degree() == max_degree.get_degree()]

        if len(same_degree_vertexes) > 1:
            same_degree_vertexes.sort(key = lambda x: x.id)

            same_degree_vertexes[0]
            return same_degree_vertexes[0]

        else:
            return max_degree
    else:
        return max_saturation

def print_vertex_list(v_list):
    print(list(map(lambda x: str(x), v_list)))

g = Graph([])

if len(sys.argv) != 2:
    print("Inicializar de maneira correta. Qual arquivo?")
    exit(1)
    
filename = sys.argv[1]

f = open(filename, "r") 

lines = f.readlines()

for line in lines:
    line_tokens = line.split(",")

    token = line_tokens[0].replace(" ", "")
    token = token.replace("\n", "")
    if len(token) == 0:
        continue

    if token not in map(lambda v: v.name, g.vertex_list):
        v = Vertex(token)
        g.vertex_list.append(v)
    else:
        v = list(filter(lambda v: v.name == token, g.vertex_list))[0]

    for u in line_tokens[1:]:

        token = u.replace(" ", "")
        token = token.replace("\n", "")
        if len(token) == 0:
            continue

        if token not in map(lambda u: u.name, g.vertex_list):
            u = Vertex(token)
            g.vertex_list.append(u)
        else:
            u = list(filter(lambda u: u.name == token, g.vertex_list))[0]

        Graph.add_edges(v, u)

f.close()


min_degree, max_degree, medium_degree, sd_degree = g.get_statistics()

print("\nmin_degree: " + str(min_degree) + "\nmax_degree: " +  str(max_degree) + "\nmedium_degree: " + str(medium_degree) + "\nsd_degree: " + str(sd_degree))

#print_vertex_list(g.vertex_list)
#print(g.vertex_list[0])

colors = Dsatur(g)

print("Total colors: ", len(colors))
print("Edges: ", sum([x.get_degree() for x in g.vertex_list])/2)
print("Vertexes: ", len(g.vertex_list), "\n")  
print_vertex_list(g.vertex_list)

f = open("saida.csv", "w")

for v in g.vertex_list:
    row = v.name + "," + v.color.name + "\n"
    f.write(row)

f = open("resultados.csv", "w")

row = "n° Vertexes: " + str(len(g.vertex_list)) + ",n° Edges: " + str(sum([x.get_degree() for x in g.vertex_list])/2) + ",Min_Degree: " + str(min_degree) + ",Max_Degree: " + str(max_degree) + ",Medium_Degree: " + str(medium_degree) + ",Sd_Degree: " + str(sd_degree) + ",n° Colors: " + str(len(colors))
f.write(row)

f.close()
