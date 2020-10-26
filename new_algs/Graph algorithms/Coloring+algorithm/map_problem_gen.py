from graphics import *
from map_data_types import *
import random
import math
import os
import time


def problem_gen(num_vert, win_sz):

    N = num_vert + 4    # Need to add corners for poly generation
    graph = []
    all_edges = []
    polygraph = []

    # Fill the list of points
    margin = 20
    for i in range(0,N-4):
        x_pt = random.randint(margin,win_sz-margin)
        y_pt = random.randint(margin,win_sz-margin)
        next_pt = Point(x_pt, y_pt)
        graph.append(graph_point(next_pt))
        polygraph.append(graph_point(next_pt))

    # Create list of all edges between vertices and store in list
    for i in range(0, N-4):
        edges = []  # Save all edges from each vertex for storage in list
        for j in range(0, N-4):
            if j != i:
                ln = Line(graph[i].pt, graph[j].pt)
                ln.setFill('black')
                ln.setWidth(1)
                edge = graph_edge(ln, graph[i], graph[j], distance(ln))
                edges.append(edge)

        edges.sort(key=lambda x: x.distance)
        graph[i].all_edges = edges

    # Eliminate all crossings in main graph
    elim_crossings(N-4, graph, all_edges)

    graph.insert(0, graph_point(Point(win_sz-1,win_sz-1)))
    graph.insert(0, graph_point(Point(win_sz-1,0)))
    graph.insert(0, graph_point(Point(0, win_sz-1)))
    graph.insert(0, graph_point(Point(0,0)))
    polygraph.insert(0, graph_point(Point(win_sz-1,win_sz-1)))
    polygraph.insert(0, graph_point(Point(win_sz-1,0)))
    polygraph.insert(0, graph_point(Point(0, win_sz-1)))
    polygraph.insert(0, graph_point(Point(0,0)))

    # Create list of all edges between corner nodes and graph
    for i in range(0, 4):
        edges = []  # Save all edges from each vertex for storage in list
        for j in range(0, N):
            if j != i:
                ln = Line(graph[i].pt, graph[j].pt)
                ln.setFill('black')
                ln.setWidth(1)
                edge = graph_edge(ln, graph[i], graph[j], distance(ln))
                edges.append(edge)

        edges.sort(key=lambda x: x.distance)
        graph[i].all_edges = edges

    # Create list of all edges between corner nodes and graph
    for i in range(4, N):
        edges = []  # Save all edges from each vertex for storage in list
        for j in range(0, 4):
            if j != i:
                ln = Line(graph[i].pt, graph[j].pt)
                ln.setFill('black')
                ln.setWidth(1)
                edge = graph_edge(ln, graph[i], graph[j], distance(ln))
                edges.append(edge)

        edges.sort(key=lambda x: x.distance)
        graph[i].all_edges = edges


    # Eliminate all crossings in main graph
    elim_crossings(N, graph, all_edges)

    # Sort edges by angle
    sort_edges_by_angle(N, graph)

    # Construct polygon structure to represent graph
    for i in range(4, len(graph)):

        # Find the vertices of the polygon surrounding each graph vertex
        pt1 = graph[i]
        num_e = len(pt1.edges)
        for j in range(0,num_e):

            # Grab two adjacent edges
            edge2 = pt1.edges[j]
            edge3 = pt1.edges[(j+1) % num_e]
            pt2 = edge2.end_point
            pt3 = edge3.end_point

            # Construct line to midpoint of vertex
            mid_pt = graph_point(edge2.ln.getCenter())
            ln = Line(pt1.pt, mid_pt.pt)
            new_edge = graph_edge(ln, pt1, mid_pt, distance(ln))
            polygraph[i].edges.append(new_edge)

            # Construct triangle and append to poly edge list
            next_triangle = [pt1, pt2, pt3]
            next_center = centroid(next_triangle)
            next_edge = graph_edge(ln, pt1, next_center, distance(ln))
            polygraph[i].edges.append(next_edge)


        # Calculate polygons
        poly_verts = []
        for j in range(0, len(polygraph[i].edges)):
            next_vert = polygraph[i].edges[j].end_point.pt
            poly_verts.append(next_vert)

        # Insert polygons into our graph object
        colors = ["blue","green", "yellow", "orange", "red", "purple"]
        next_poly = Polygon(poly_verts)
        next_poly.setOutline('grey')
        next_poly.setWidth(2)
        graph[i].color = Color.no_color
        graph[i].poly = next_poly

    corners = graph[:4]
    final_graph=graph[4:]

    # Trim off corners and the edges
    for pt in final_graph:
        for edge in pt.edges[:]:
            end_pt = edge.end_point

            if any((end_pt.pt.getX() == corner.pt.getX()) and (end_pt.pt.getY() == corner.pt.getY()) for corner in corners):
                pt.edges.remove(edge)

    # Sort edges by number of connections
    final_graph.sort(key=lambda x: len(x.edges), reverse=True)

    # Precalculate all neighbors
    for pt in final_graph:
        for edge in pt.edges:
            pt.neighbors.append(edge.end_point)

    # Prepare Map object
    map = Map(final_graph)
    for pt in final_graph:
        pt.map = map

    return map

def elim_crossings(N, graph, all_edges):

    # Implement graph constructing algorithm defined in problem statement
    escape = True
    vertex_escape = [False] * N  # All elements must be true to escape loope
    while (escape):


        i = random.randint(0, N - 1)  # Select random point

        edges = graph[i].all_edges  # Select all edges from random point
        num_edges = len(edges)

        # Find next closest point
        for j in range(0, num_edges):

            test_edge = edges[j]

            if test_edge.checked == False:  # Proceed only if we haven't checked this edge
                test_edge.checked = True  # Make sure to inform the program we checked the edge

                # Check that the test edge does not cross any current edges
                if len(all_edges) == 0:
                    graph[i].edges.append(test_edge)
                    all_edges.append(test_edge)
                    break
                else:
                    crosses = False
                    for edge in all_edges:

                        if does_cross(test_edge.ln, edge.ln):
                            crosses = True
                            break

                    if crosses == False:
                        graph[i].edges.append(test_edge)
                        all_edges.append(test_edge)
                        break

            # Escape based on full trips through all FOR loops
            if j == num_edges-1:
                vertex_escape[i] = True

        if all(item == True for item in vertex_escape):
            escape = False

# Check if lines cross by checking if both x and y coordinates simultaneously switch order
# Solution given by http://stackoverflow.com/a/1968345
def does_cross(line1, line2):

    try:
        p0_x = line1.getP1().getX()
        p0_y = line1.getP1().getY()
        p1_x = line1.getP2().getX()
        p1_y = line1.getP2().getY()
        p2_x = line2.getP1().getX()
        p2_y = line2.getP1().getY()
        p3_x = line2.getP2().getX()
        p3_y = line2.getP2().getY()

        # If the two lines are the same, we say that they do not cross
        if(p0_x == p2_x and p0_y == p2_y and p1_x == p3_x and p1_y == p3_y):
            return False

        s1_x = p1_x - p0_x
        s1_y = p1_y - p0_y
        s2_x = p3_x - p2_x
        s2_y = p3_y - p2_y

        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
        t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)


        if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
            if ((i_x == p0_x and i_y == p0_y) or (i_x == p1_x and i_y == p1_y) or (i_x == p2_x and i_y == p2_y) or (i_x == p3_x and i_y == p3_y)):
                return False
            else:
                return True
        else:
            return False

    except ZeroDivisionError:   # If the two lines
        return False

def init_rand(seed=None):
    if seed is None:
        try:
            seed = os.urandom(8)
        except NotImplementedError:
            seed = time.time()
    print('seed: %s' % seed)
    random.seed(seed)


# Compute the Euclidian distance of a line segment
def distance(line1):
    x_dist = line1.getP2().getX() - line1.getP1().getX()
    y_dist = line1.getP2().getY() - line1.getP1().getY()

    return math.sqrt(x_dist * x_dist + y_dist * y_dist)

def centroid(pts):

    X = 0
    Y = 0
    for pt in pts:
        X = X + pt.pt.getX()
        Y = Y + pt.pt.getY()

    X = math.floor(X / len(pts))
    Y = math.floor(Y / len(pts))
    center_pt = Point(X,Y)
    center_pt.setFill('red')
    # center_pt.draw(win)

    return graph_point(center_pt)

def sort_edges_by_angle(N, graph):
    for i in range(0,N):
        for j in range(0, len(graph[i].edges)):
            dx = graph[i].edges[j].end_point.pt.getX() - graph[i].edges[j].start_point.pt.getX()
            dy = graph[i].edges[j].end_point.pt.getY() - graph[i].edges[j].start_point.pt.getY()
            graph[i].edges[j].theta = math.atan2(dy, dx)
            # if (i == 1 and j == 0):  # 4th quadrant needs special treatment
            #     graph[i].edges[j].theta = 2 * math.pi
        graph[i].edges.sort(key=lambda x: x.theta)








