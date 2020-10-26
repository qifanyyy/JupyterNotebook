""" Graph utility functions. """
"""
    Graphs are adjacency lists with vertices numbered from 0..n-1
    each element in the list indexed at u is a pair (v,c) denoting edge from
    u to v with capacity c
"""
import graphviz
import sys
import matplotlib.image as mpimg

# Helper function to set the graph styles
styles = {
    'graph': {
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'fontsize': '30',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
        'shape' : 'doublecircle',
    },
    'edges': {
        'color': 'white',
        'arrowhead': 'open',
        'arrowsize':'2.5',
        'fontname': 'Helvetica',
        'fontsize': '30',
        'fontcolor': 'white',
    }
}

styles2 = {
    'graph': {
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'fontsize': '20',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
        'shape' : 'doublecircle',
        'fixedsize' : 'true',
        'width' : '0.5',
        'height' : '0.5'
    },
    'edges': {
        'color': 'white',
        'arrowhead': 'open',
        'arrowsize':'.5',
        'fontname': 'Helvetica',
        'fontsize': '20',
        'fontcolor': 'white',
    }
}

def input_graph(input_file=sys.stdin):
    """ read graph from file.
    n = number of vertices
    m = number of edges
    input format
    n m
    u v c (m times)

    line u v c refers to edge from u to v with capacity c

    returns graph, vertices, edges
    """
    n, m = map(int, input_file.readline().split())
    graph = [[] for _ in range(n)]
    for i in range(m):
        u, v, c = map(int, input_file.readline().split())
        graph[u].append((v, c))

    # modified to return edges also
    return graph, n, m


def display_graph(graph, filename="graphviz_output", highlight_path=None, capacities=None,
                  source=0, sink=None,size_graph = 'l'):

    """ simply displays a graph using graphviz.
    renders to filename.png
    """

# TODO simplify all these functions into one function or use a dictionary


    def label(edge, weight, capacities):
        if capacities is not None:
            return str(weight) + ' / ' + str(capacities[edge])
        else:
            return str(weight)

    # Blue if max capacity,white if edge is not present
    # Red if it is part of the path
    def color_dot(edge, weight, capacities):
        if capacities is not None:
            if capacities[edge] == 0 :
                return '#444444'#333333'
            elif capacities[edge] == weight :
                return 'red'
        else:
            if weight==0:
                return '#444444'#333333'

        return 'white'

    def style_dot(edge,weight,capacities):
        if capacities is not None:
            if capacities[edge] == 0 :
                return 'dashed'
            elif capacities[edge] == weight :
                return 'solid'
        else:
            if weight==0:
                return 'solid'

        return 'solid'
    def font_dot(edge,weight,capacities):
        if capacities is None:
            if weight==0 :
                return '#333333'
            else:
                return 'white'
        else:
            if capacities[edge]==0:
                return '#333333'
            else:
                return 'white'

    def apply_styles(graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )
        return graph



    dot = graphviz.Digraph(comment="max flow graph", format='png', engine='neato')

#     dot.attr('node', shape='doublecircle')

    if size_graph == 'l':
        dot.body.append('size= "12,6"')
    else:
        dot.body.append('size= "5,2.2"')
    dot.body.append('rankdir="LR"')
    dot.body.append('ratio="fill"')
    dot.body.append('overlap ="true"')
    dot.body.append('margin=0')

#     assume source and sink are 0 and n-1

    n = len(graph)
    for i in map(str, range(1, n - 1)):
        dot.node(i)

    if sink is None:
        sink = n - 1

    dot.node(str(source), fillcolor='#FF9900')
    dot.node(str(sink), fillcolor='#FF9900')

    if highlight_path:
        path_edges = zip(highlight_path, highlight_path[1:])

    for i in range(n):
        for j, c in graph[i]:
            if highlight_path and (i, j) in path_edges:
                print 'got path edge', (i, j)
                dot.edge(str(i), str(j), label=label((i, j), c, capacities), color='#FF9900', fontcolor = font_dot((i,j),c,capacities))
            else:
                dot.edge(str(i), str(j), label=label((i, j), c, capacities), color=color_dot((i,j),c,capacities), fontcolor = font_dot((i,j),c,capacities),style = style_dot((i,j),c,capacities))

    if size_graph == 'l':
        dot = apply_styles(dot, styles)
    else:
        dot = apply_styles(dot, styles2)
    dot.render(filename)


def graph_image(graph, highlight_path=None, capacities=None, source=0, sink=None):
    """
        Convert graph to image and returns the image
    """
    filename = "_graph_image_"
    display_graph(graph, filename=filename,
                  highlight_path=highlight_path, capacities=capacities,source = source,sink = sink)
    return mpimg.imread(filename + '.png')
