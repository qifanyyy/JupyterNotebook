import operator
from typing import Optional, Tuple, Union

from .data_structures import PriorityQueue, UnionFind
from .graph import Graph
from .type_constants import Edges, Number, T


INF = float('inf')


def find_cycle_edges(vertex: T, g: Graph, visited: list, parent: Optional[T] = None) -> Tuple[Optional[Edges], bool]:
    if vertex in visited:
        return [], False
    
    visited.append(vertex)
    for v, w in g.vertex_neighbours(vertex):
        if v == parent:
            continue
        edges, finished = find_cycle_edges(v, g, visited, vertex)
        if edges is None:
            continue
        if finished:
            return edges, True
        edges.append(((vertex, v), w))
        
        # check if the current vertex marks the end of the cycle            
        if vertex == edges[0][0][1]:
            finished = True
        return edges, finished

    return None, False

def dijkstra_mst(g: Graph, verbose: int = 0) -> Graph:
    mst = Graph()
    trace = []
    visited = set()
    
    for (u, v), w in g.edges():
        if verbose > 0:
            print(f'edge {(u, v), w} added to the tree')
        mst.add_edge((u, v), w)
        trace.append(((u, v), w))

        if u in visited and v in visited:
            cycle_edges, _ = find_cycle_edges(u, mst, visited=[])
            if cycle_edges:
                max_edge, max_w = max(cycle_edges, key=operator.itemgetter(1))
                mst.remove_edge(max_edge, max_w)
                max_u, max_v = max_edge
                if ((max_u, max_v), max_w) in trace:
                    trace.remove(((max_u, max_v), max_w))
                else:
                    trace.remove(((max_v, max_u), max_w))
                if verbose > 0:
                    print(f'edge {max_edge, max_w} removed from the tree (edge with maximum weight within cycle)')

        visited.add(u)
        visited.add(v)

    mst._trace = trace
    return mst


def kruskal_mst(g: Graph, verbose: int = 0) -> Graph:
    queue = PriorityQueue()
    uf = UnionFind()
    trace = []

    for (u, v), w in g.edges():
        queue.put((w, (u, v)))
        uf.add(u)
        uf.add(v)
    
    mst = Graph()
    edge_num, mst_edge_num = 0, len(g.vertices()) - 1
    while edge_num < mst_edge_num:
        w, (u, v) = queue.get()

        if uf.find(u) == uf.find(v):
            if verbose > 1:
                print(f'edge {(u, v), w} rejected (forms cycle)')
            continue
        
        if verbose > 0:
            print(f'edge {(u, v), w} added to the tree')

        mst.add_edge((u, v), w)
        uf.union(u, v)
        trace.append(((u, v), w))
        edge_num += 1

    mst._trace = trace
    return mst


def prim_mst(g: Graph, verbose: int = 0) -> Graph:
    vertices = g.vertices()
    vcost = dict.fromkeys(g.vertices(), INF)
    vparent = {}

    mst = Graph()
    trace = []
    while vertices:
        u = min(vertices, key=vcost.get)

        mst.add_vertex(u)
        if u in vparent:
            if verbose > 0:
                print(f'edge {vparent[u], vcost[u]} added to the tree')
            mst.add_edge(vparent[u], vcost[u])
            trace.append((vparent[u], vcost[u]))
       
        vertices.remove(u)
       
        for v, w in g.vertex_neighbours(u):
            if v in vertices and w < vcost[v]:
                vcost[v] = w
                vparent[v] = (u, v)
                if verbose > 1:
                    print(f'edge {vparent[v]} weight updated to {vcost[v]}')
    
    mst._trace = trace
    return mst