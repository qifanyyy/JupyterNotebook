from incidence_coloring_degree3 import _ic_max_degree_3, _inverse_coloring, _to_hex_colors, _check_is_proper_incidence_coloring
from collections import deque
from sage.all import *


def incidence_coloring(G, hex_colors=False):
    r"""
    Find incidence coloring of a graph of maximum degree 4.
    
    INPUT:
    
    - ``G``         -- a graph; all vertices of degree 4 or less
    
    - ``hex_colors`` -- bool (default: ``False``); if set to ``True``, 
                        returned coloring uses hexadecimal colors (from rainbow),
                        otherwise the color set is {1,...,7}
    """
    
    G._scream_if_not_simple()
    _scream_if_not_subquartic(G)
    
    if max(G.degree_iterator()) < 4:
        G_coloring = _inverse_coloring(_ic_max_degree_3(G), {1,2,3,4,5})
    else:
        G_coloring = _inverse_coloring(_ic_max_degree_4(G), {1,2,3,4,5,6,7})
    
    if hex_colors:
        return _to_hex_colors(G_coloring)
    else:
        return G_coloring
    
def _ic_max_degree_4(G): 
    r"""
    Find inversed incidence coloring of a graph of maximum degree 4.
    
    INPUT:
    
    - ``G``         -- a graph; all vertices of degree 4 or less
    """
    M = [frozenset({e[0],e[1]}) for e in G.matching()] #red edges, undirected
    M_vertices = {v for e in M for v in e} #red
    A = {v for v in G.vertices() if G.degree(v)==4}.difference(M_vertices) #black vertices
    is_red_black_edge = lambda e : (e[0] in M_vertices and e[1] in A) or (e[0] in A and e[1] in M_vertices)
    red_black = G.subgraph(edge_property = is_red_black_edge)
    B = [frozenset({e[0],e[1]}) for e in red_black.matching()] #black edges, undirected

    #is_not_in_M_nor_B = lambda e: not (e  in M or e in B)
    C = G.subgraph(edge_property = lambda e: not __is_in_M_or_B(e,M,B)) #blue edges
    C_inversed_coloring_complete = _ic_max_degree_3(C)
    
    if(A):
        #step 1
        C_inversed_coloring = __recolor(G, C, C_inversed_coloring_complete, A, B)
    else:
        C_inversed_coloring = C_inversed_coloring_complete
        
    #step 2
    #color remaining incidences
    F = __build_uncolored_graph(G, C_inversed_coloring)
    
    F_coloring = _inverse_coloring(F.bipartite_color(), {0,1}) #uses colors {0,1}
    
    #inverse and merge colorings:
    C_coloring = _inverse_coloring(C_inversed_coloring, {1,2,3,4,5})
    C_coloring[6] = F_coloring[0]
    C_coloring[7] = F_coloring[1]
    
    return C_coloring
    
def __build_uncolored_graph(G, coloring):
    r"""
    Creates graph that has uncolored incidences of G as vertices and
    two incidences makes an edge iff they are adjacent.
    
    INPUT:
    - ``G``        -- a graph
    - ``coloring`` -- a dict; partial inversed incidence coloring of G (maps incidences to colors)
    """
    F = Graph()
    for e in G.edges():
        u = e[0]
        v = e[1]
        if (u,v) not in coloring:
            F.add_vertex((u,v))
        if (v,u) not in coloring:
            F.add_vertex((v,u))
    
    for i in F.vertices():
        for j in F.vertices():
            if __are_adjacent(i,j):
                F.add_edge(i,j)
    return F
    
    
def __are_adjacent(i,j):
    r"""
    Returns whether incidences ``i`` and ``j`` are adjacent.
    
    INPPUT:
    - ``i``  -- a binary tuple; an incidence represented as ordered tuple of vertices
    - ``j``  -- a binary tuple; an incidence represented as ordered tuple of vertices
    """
    i1,i2 = i
    j1,j2 = j
    return i1 == j2 or i2==j1 or (i1 == j1 and i2 != j2)

def __is_in_M_or_B(e,M,B):
    r"""
    Returns whether edge ``e`` is contained in at least one of ``M`` and ``B``.
    
    INPUT:
    - ``e`` -- a tuple; undirected edge represented as tuple ``(v1,v2,label)``
    - ``B`` -- an enumerable of binary frozensets; list of undirected edges represented as frozensets ``{v1,v2}``- 
    - ``M`` -- an enumerable of binary frozensets; list of undirected edges represented as frozensets ``{v1,v2}``
    """
    e_undirected = frozenset({e[0],e[1]})
    return (e_undirected in M or e_undirected in B)

def __direct_black_edges(black_vertices,black_edges):
    r"""
    Returns list of ``black_edges`` directed such that its terminal vertex is in ``black_vertices``.
    
    INPUT:
    - ``black_vertices`` -- an enumarable
    -- ``black_edges``   -- an enumerable of binary sets, one vertex of each set is in ``black_vertices``
    """
    directed = list()
    for u,v in black_edges:
        if u in black_vertices:
            directed.append((v,u))
        else:
            directed.append((u,v))
    return directed
    
def __recolor(G,blue_graph, blue_coloring, black_vertices, black_edges):
    r"""
    Returns partial inversed incidence coloring of G
    created according to Step 1 of the algorithm.
    
    INPUTS:
    - ``G``   -- a graph;
    - ``blue_graph`` -- a graph; subcubic subgraph of G
    - ``blue_coloring`` -- a dict; inversed incidence coloring of ``blue_graph``
    - ``black_edges`` -- a list; matching in G between black and red vertices
    """
    
    chains = []
    uncolored_black_edges = __direct_black_edges(black_vertices, black_edges)
    coloring = copy(blue_coloring)
    
    while(uncolored_black_edges):
    
        black_edges_to_prolong = {e for e in uncolored_black_edges if e[0] == chains[-1][-1]} if chains else list()
        if(black_edges_to_prolong):
            next_black_edge = black_edges_to_prolong.pop()
            uncolored_black_edges.remove(next_black_edge)
        else:
            next_black_edge = uncolored_black_edges.pop()
            chains.append(list(next_black_edge)) #start new chain

        
        v_macron,v = next_black_edge
        chains_starts = frozenset([c[0] for c in chains])
        
        is_case_b, x, v_prime = __choose_color(G,v_macron,v, coloring, blue_graph, chains_starts)
        coloring[v_macron,v] = x
        chains[-1].append(v)

        if is_case_b:
            del coloring[v,v_prime]
            #continue with respect to v_prime

            if v_prime not in chains_starts and v_prime not in chains[-1]:
                #case (a)
                chains[-1].append(v_prime)
                
            elif v_prime in chains_starts:
                #case (b)
                index_chain_starting_with_v_prime = {i for i in range(0,len(chains)) if chains[i][0] == v_prime}[0]
                #conacatenate chains[-1] and chain_starting_with_v_prime
                chains[index_chain_starting_with_v_prime] = chains[index_chain_starting_with_v_prime] + chains[-1]
                del chains[-1]
            else:
                #case (c) - v_prime is internal vertex of chain[-1] (=> loop) => recoloring
                index_v_prime = chains[-1].index(v_prime) # != 0 nor last
                u = chains[index_v_prime - 1]
                w = chains[index_v_prime + 1]
                
                a = C_coloring[u, v_prime]
                b = coloring[v_prime,w]
                c = coloring[v_prime,v]
                d = coloring[v_prime, u]
                e = (frozenset({1,2,3,4,5}).difference({a,b,c,d})).pop()
                
                coloring[w, v_prime] = b
                a_or_e_in_s0_w = frozenset({a,e}).difference(__spectrum0(G,w,coloring))
                if(a_or_e_in_s0_w):
                    coloring[v_prime,w] = a_or_e_in_s0_w.pop()
                else:
                    coloring[v_prime,w] = d
                    coloring[v_prime,u] = a
                
                #split chains[-1]:
                #chains[-1] == start..u-v_prime-w..v_macron-v
                index_w = index_v_prime + 1
                tail = chains[-1][index_w:]
                del chains[-1][index_w:]
                tail.append(v_prime)
                chains.append(tail)
    return coloring
    
def __choose_color(G,v_macron,v,coloring,G_blue, chains_starts):
    r"""
    Chooses color ``x`` from ``{1,2,3,4,5}`` such that conditions R1 and R2 are satisfied.
    
    """
    available_colors = {1,2,3,4,5} #all blue colors
    
    #R1
    available_colors.difference_update(__spectrum(G,v_macron,coloring))
            
    #R2
    s0 = __spectrum0(G,v,coloring)
    case_a = available_colors.difference(s0)
    if(case_a):
        return (False, case_a.pop(), None)
    else:
        #find color fulfiling case (b):
        for x in available_colors:
            for w in G_blue.neighbors(v):
                if(coloring[v,w]==x and w not in chains_starts):
                    return (True, x,w)
        
        
    
def __spectrum(G,v,coloring):
    r"""
    Returns set of colors that are used to coloring incidences of edges 
    incident with ``v`` in ``coloring``.
    
    INPUTS:
    - ``G``        -- a graph;
    - ``v``        -- a vertex of ``G``
    - ``coloring`` -- a dict;partial inversed incidence coloring of ``G``
    """
    s0 = __spectrum0(G,v,coloring)
    s1 = __spectrum1(G,v,coloring)
    return s0.union(s1)
    
def __spectrum0(G,v,coloring):
    r"""
    Returns set of all colors that are used to color incidences ``(v,uv)`` in ``coloring``.
    
    INPUTS:
    - ``G``        -- a graph;
    - ``v``        -- a vertex of ``G``
    - ``coloring`` -- a dict;partial inversed incidence coloring of ``G``
    """
    spectrum = set()
    for u in G.neighbors(v):
        if((v,u) in coloring):
            spectrum.add(coloring[v,u])
    return spectrum

def __spectrum1(G,v,coloring):
    r"""
    Returns set of all colors that are used to color incidences ``(u,uv)`` in ``coloring``.
    
    INPUTS:
    - ``G``        -- a graph;
    - ``v``        -- a vertex of ``G``
    - ``coloring`` -- a dict;partial inversed incidence coloring of ``G``
    """
    spectrum = set()
    for u in G.neighbors(v):
        if((u,v) in coloring):
            spectrum.add(coloring[u,v])
    return spectrum


def _scream_if_not_subquartic(G):
    r"""
    Raise ``ValueError`` if degree of any vertex of ``G`` is more than 4.
    
    INPUT:
    - ``G`` -- a graph
    """
    if max(G.degree_iterator()) > 4:
        raise ValueError("only graphs of maximum degree 3 are supported")
