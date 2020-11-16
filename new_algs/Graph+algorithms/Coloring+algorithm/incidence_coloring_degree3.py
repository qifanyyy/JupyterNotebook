from sage.all import *
from sage.graphs.connectivity import connected_components_subgraphs
import itertools


def incidence_coloring(G, hex_colors=False):
    r"""
    Find incidence coloring of a graph of maximum degree 3.
    
    INPUT:
    
    - ``G``         -- a graph; all vertices of degree 3 or less
    
    - ``hex_colors`` -- bool (default: ``False``); if set to ``True``, 
                        returned coloring uses hexadecimal colors (from rainbow),
                        otherwise the color set is {1,...,5}
    """
    G._scream_if_not_simple()
    _scream_if_not_subcubic(G)

    G_coloring_inversed = _ic_max_degree_3(G)
    
    G_coloring = _inverse_coloring(G_coloring_inversed, {1, 2, 3, 4, 5})

    if hex_colors:
        return _to_hex_colors(G_coloring)
    else:
        return G_coloring

def _ic_max_degree_3(G):
    r"""
    Find inversed incidence coloring of a graph of maximum degree 3.
    
    INPUT:
    
    - ``G``         -- a graph; all vertices of degree 3 or less
    """
    _scream_if_not_subcubic(G)
    
    # embbed G into 3-regular
    G_3, extra_edges = _find_cubic_supergraph(G)

    # find IC of 3-regular graph
    G_coloring_inversed = dict()
    for C in connected_components_subgraphs(G_3):
        G_coloring_inversed.update(__ic_3regular(C))

    # get coloring of G from coloring of G_3
    for u, v in extra_edges:
        del G_coloring_inversed[(u, v)]
        del G_coloring_inversed[(v, u)]
    
    return G_coloring_inversed

def __ic_3regular(G):
    r"""
    Find inversed incidence coloring of 3-regular graph.
    
    INPUT:
    - ``G`` -- a graph; all vertices of degree 3
    """
    B = G.bridges(labels=False)
    G_B = G.copy()
    if B:
        G_B.delete_edges(B)
    # 'K' is set of not single point components G_B
    # 'D' is set of single point components G_B
    K = []
    D = []
    components = G_B.connected_components()
    for s in components:
        (K if len(s) > 1 else D).append(tuple(s))

    N = Graph()  # N is graph having components of G_B as vertices
    # egdes have the original edge (from B) as label
    N.add_vertices(K)
    N.add_vertices(D)
    for u, v in B:
        cs = [c for c in itertools.chain(K, D) if (u in c or v in c)]
        # uv is bridge, so cs contains exactly 2 vertices of N
        N.add_edge(cs[0], cs[1], (u, v))
    G_coloring = dict()

    for C, original_edge in _dfs_with_edge_label(N, N.vertices()[0]):
        C_completed = _add_incident_edges(list(C), B)
        C_completed_coloring = __ic_completed_component(G, C_completed)
        if not G_coloring:
            G_coloring = C_completed_coloring
            continue
        # merge C_completed_coloring to G_coloring via original_edge which is common to them:
        u, v = original_edge
        color_permutation = {
            C_completed_coloring[(u, v)]: G_coloring[(u, v)], 
            C_completed_coloring[(v, u)]: G_coloring[(v, u)]
        }
        _complete_permutation(color_permutation, {1,2,3,4,5})
        C_completed_coloring_recolored = _transform_inversed_coloring(C_completed_coloring, color_permutation)
        del C_completed_coloring_recolored[(u, v)]
        del C_completed_coloring_recolored[(v, u)]
        G_coloring.update(C_completed_coloring_recolored)

    return G_coloring


def __ic_completed_component(G, C):
    r"""
    Find inveresed incidence coloring of subgraph of G induced by C.
    C is completion of a component of cubic G with removed bridges.
    Vertices of the subgraph are supposed to have degree 1 or 3.
    
    INPUT:
    
    - ``G`` -- a graph
    
    - ``C`` -- a subset of vertices of G
    """
    H = G.subgraph(vertices=C, immutable=False, algorithm="add")
    # add Omega's
    degree_1 = [v for v in H.vertices() if H.degree(v) == 1]
    added_edges = []
    for pair in _pair_elements(degree_1):
        u = pair[0]
        v = pair[1]
        p1 = H.add_vertex()
        p2 = H.add_vertex()
        omega = [(u, p1), (u, p2), (v, p1), (v, p2), (p1, p2)]
        H.add_edges(omega)
        added_edges.extend(omega)
    # now vertices of H are of degree 3 and H is 2 connected

    # find coloring from Proposition 4
    C_star_coloring = __ic_2regular_1factor(H)
    for u, v in added_edges:  # delete omegas
        del C_star_coloring[(u, v)]
        del C_star_coloring[(v, u)]
    return C_star_coloring


def __ic_2regular_1factor(G):
    r"""
    Find incidence coloring of graph G such that G = C + F, 
    where C is 2-regular and F is 1-factor,
    and G has no more than 1 vertex of degree 1.
    
    INPUT:
    
    - ``G`` -- a graph, such that G = C + F, where C is 2-regular and F is 1-factor,
               and G has no more than 1 vertex of degree 1.
    """
    F = [(u,v) for u,v,_ in G.matching()]
    C = G.copy()
    C.delete_edges(F)
    if C.connected_components_number() == 1:
        #use Shiu's algorithm:
        cycle = _cyclic_connected_component_containing_vertex(C, C.vertices()[0])
        G_coloring = __ic_3regular_hamiltonian(G,cycle,F)
        return G_coloring
    # else: use Maydanski's algorithm:

    M = Graph()  # M is cycle connection multigraph,
    # vertices are lists of vertices of the cycle (sorted according to cycle),
    # edges has as labels the original edges from F
    for e in F:
        C_i = C.connected_component_containing_vertex(e[0], sort=True)
        C_j = C.connected_component_containing_vertex(e[1], sort=True)
        if C_i != C_j:
            M.add_edge(tuple(C_i), tuple(C_j), e)
        else:
            M.add_vertex(tuple(C_i))

    M_spanning_tree = M.min_spanning_tree()
    T = M.subgraph(edges=M_spanning_tree)

    G_coloring = {}
    dependent_pairs = []  # "special vertices"
    processed_vertices_T = set()  # TODO: this might be optimised - it is only to found 'parent' vertex in DFS
    T_root = [v for v in T.vertices() if len(v) > 1][0]  # root must be non-single point component of C
    for C_i in T.depth_first_search(T_root):
        # color C_i and join it to G_Coloring
        processed_vertices_T.add(C_i)
        is_single_point = len(C_i) == 1
        C_i_coloring = dict()

        if not is_single_point:
            cycle = _cyclic_connected_component_containing_vertex(C, C_i[0])
            p = len(cycle)
            connected_vertices = [cycle.index(v) for e in T.edges(C_i) for v in e[2] if v in C_i]
            connected_vertices.sort()
            starting = __find_starting_vertex(connected_vertices, p)
            _rotate_list(cycle, connected_vertices, starting)
            C_i_coloring = __default_cycle_coloring_inversed(cycle)
            # if's - complete C_i_coloring
            if len(connected_vertices) >= 2 and connected_vertices[1] == 1:  # x_1 is a connection vertex
                C_i_coloring[(cycle[1], cycle[0])] = 5
                C_i_coloring[(cycle[0], cycle[1])] = 4
                next_already_processed = True
            else:
                C_i_coloring[(cycle[0], cycle[p - 1])] = 5
                C_i_coloring[(cycle[0], cycle[1])] = 4
                dependent_pairs.append((cycle[1], cycle[-1]))
                next_already_processed = False
            for k in range(1, len(connected_vertices)):
                if next_already_processed:  # current x_j was involved in previous iteration
                    next_already_processed = False
                    continue
                j = connected_vertices[k]
                if j + 1 == connected_vertices[(k + 1) % len(connected_vertices)] and (j + 1) % len(C_i) != 0:  # x_j+1 is a connection vertex and is not x_0
                    C_i_coloring[(cycle[(j + 1)%len(cycle)], cycle[j])] = 5
                    C_i_coloring[(cycle[j], cycle[(j + 1)%len(cycle)])] = 4
                    next_already_processed = True
                else:
                    C_i_coloring[(cycle[j], cycle[(j + 1)%len(cycle)])] = 5
                    
        # merge C_i_coloring to G_coloring
        if not G_coloring:  # G_coloring is empty
            G_coloring.update(C_i_coloring)
            continue
        
        parent = (processed_vertices_T.intersection(T.neighbors(C_i))).pop()
        connection_edge = T.edge_label(C_i, parent)
        # set u,w such that uw is connection_edge and w is vertex of C_i
        if connection_edge[0] in C_i:
            w = connection_edge[0]
            u = connection_edge[1]
        else:
            w = connection_edge[1]
            u = connection_edge[0]

        # colors for permutation:
        u_colors = __find_colors(u, C.neighbors(u), G_coloring)
        G_coloring.update({(u, w): u_colors['a'], (w, u): u_colors['b']})  # coloring of incidences of connection_edge
        if is_single_point:
            continue  # C_i was proccesed
        w_colors = __find_colors(w, C.neighbors(w), C_i_coloring)
        permutation_alpha = {
            w_colors['a']: u_colors['b'],
            w_colors['b']: u_colors['a'],
            w_colors['c']: u_colors['c'],
            4: 4,
            5: 5
        }
        alpha_C_i_coloring = _transform_inversed_coloring(C_i_coloring, permutation_alpha)
        G_coloring.update(alpha_C_i_coloring)
    # end for C_i in T

    # add remaining edges of F incidence with special vertex
    special_vertices = {v for pair in dependent_pairs for v in pair}  # flattened dependent_pairs

    while bool(special_vertices):  # is not empty
        b_1 = __find_starting_special(special_vertices, F)
        b_i = b_1
        edges_sequence = []
        while True:
            a_i = _get_another(b_i, dependent_pairs)
            special_vertices.discard(a_i)
            b_i1 = _get_another(a_i, F)
            edges_sequence.append((a_i, b_i1))
            if (b_i1 in special_vertices):
                special_vertices.discard(b_i1)
                if b_i1 is b_1:
                    break
                # else: proceed
            else:
                edges_sequence.append((_get_another(b_1,F), b_1))
                special_vertices.discard(b_1)
                break

        for a_k, b_k1 in edges_sequence:
            # adding incidences of F
            G_coloring[(a_k, b_k1)] = 5
            G_coloring[(b_k1, a_k)] = 4

            # recoloring:
            for v in C.neighbors(a_k):
                if G_coloring[(v, a_k)] == 5:
                    G_coloring[(v, a_k)] = 4
            for v in C.neighbors(b_k1):
                if G_coloring[(v, b_k1)] == 4:
                    G_coloring[(v, b_k1)] = 5

    # add remaining edges of F
    remaining_edges = [(e[0], e[1]) for e in F if (e[0], e[1]) not in G_coloring]
    for u, v in remaining_edges:
        G_coloring[(u, v)] = 4
        G_coloring[(v, u)] = 5

        for w in C.neighbors(v):
            if G_coloring[(w, v)] == 5:
                G_coloring[(w, v)] = 4

        for w in C.neighbors(u):
            if G_coloring[(w, u)] == 4:
                G_coloring[(w, u)] = 5

    return G_coloring

def __ic_3regular_hamiltonian(G,C,F):
    r"""
    Find incidence coloring of 3-regular hamiltonian graph ``G`` 
    which was decomposed into a cycle ``C`` and a perfected matching ``F``.
    
    INPUTS:
    - ``C`` -- a list; ``C[i]````C[i+1]`` and ``C[p-1]````C[0]`` are edges
    - ``F`` -- a list of pairs of elements of ``C``; each pair is an edge of the matching
    
    ALGORITHM:
    W. C. Shiu et al.: On incidence coloring for some cubic graphs
    """
    def ic_edges_with_45(E):
        """
        Color both incidences of edges in ``E`` with colors ``4`` and ``5``.
        """
        coloring = dict()
        for u,v in E:
            coloring[(u,v)] = 4
            coloring[(v,u)] = 5
        return coloring    
    
    def find_starting(cycle, F):
        """
        Return ``i`` (index of vertex in cycle) such that 
        vertices matched by ``F`` to ``cycle[i]`` and ``cycle[i+1]`` are not adjacent.
        Return ``None`` if no such ``i`` exists.
        """
        p = len(cycle)
        for i in range(0,p):
            a = _get_another(cycle[i],F)
            b = _get_another(cycle[(i+1)%p],F)
            i_a = cycle.index(a)
            i_b = cycle.index(b)
            if not ((abs(i_a - i_b) == 1) or (i_a == 0 and i_b == p-1) or (i_b == 0 and i_a == p-1)):
                return i
        # else:
        return None
    
    def set_colors_matching_edge(vertex,color_v_mv,color_mv_v):
        _set_colors_edge(coloring,vertex,_get_another(vertex,F),color_v_mv,color_mv_v)
    
    p = len(C)
    
    if p % 3 == 0:
        # Case 1
        coloring = __default_cycle_coloring_inversed(C)
        coloring.update(ic_edges_with_45(F))
        return coloring
    
    #else - Cases 2,3:
    
    # find start:
    i = find_starting(C,F)
    # rotate C such that original C[i] is C[1] (if i was found), and C[0] == C[p], C[p+1]==C[1]:
    if i is not None:
        _rotate_list(C,[],i+1)
    C.insert(0,C[-1])
    C.append(C[1])
    
    # color C:
    color_permutation = { 1: 2, 2: 1, 3: 3} # mapping Maydanski's default cycle coloring to Shiu's cycle coloring
    coloring = _transform_inversed_coloring(__default_cycle_coloring_inversed(C), color_permutation)
    _set_colors_edge(coloring,C[p],C[1],4,5)
    
    if i is not None:
        # Subcases 1
        s = C.index(_get_another(C[1],F))
        r = C.index(_get_another(C[p],F))
        
        if p % 3 == 1:
            # Case 2.1
            if r % 3 == 0:
                coloring[(C[r],C[r-1])] = 4
                x_h = _get_another(C[r-1],F)
                _set_colors_edge(coloring,C[r-1],x_h,5,4)
            if r % 3 == 1:
                coloring[(C[r],C[r+1])] = 4
                x_i = _get_another(C[r+1],F)
                _set_colors_edge(coloring,C[r+1],x_i,5,4)
            if s % 3 == 1:
                coloring[(C[s],C[s-1])] = 5
                x_k = _get_another(C[s-1],F)
                _set_colors_edge(coloring,C[s-1],x_k,4,5)
            if s % 3 == 2:
                coloring[(C[s],C[s+1])] = 5
                x_j = _get_another(C[s+1],F)
                _set_colors_edge(coloring,C[s+1],x_j,4,5)
            _set_colors_edge(coloring,C[p],C[r],1,5)
            _set_colors_edge(coloring,C[1],C[s],3,4)
            #end Case 2.1
        elif p % 3 == 2:
            # Case 3.1
            if r % 3 == 1:
                coloring[(C[r],C[r-1])] = 4
            if r % 3 == 2:
                coloring[(C[r],C[r+1])] = 4
            if s % 3 == 1:
                coloring[(C[s],C[s-1])] = 5
            if s % 3 == 2:
                coloring[(C[s],C[s+1])] = 5
            
            if (s == r - 2 and s % 3 == 2) or (r == s -2 and r % 3 == 2):
                x_rs = C[(r+s)/2] # vertex between x_r and x_s
                m = C.index(_get_another(x_rs,F)) # index of vertex connected with x_rs
                coloring[(x_rs,C[m])] = 3
                for d in {-1,1}: # check both neighbours of C[m]
                    if coloring[(C[m],C[m+d])] == 3:
                        # select 4 or 5 not used to color incidences from C[m+d]:
                        colors = {4,5}
                        for v in G.neighbors(C[m+d]):
                            colors.discard(coloring.get((C[m+d],v)))
                        availible = colors.pop()
                        coloring[(C[m],C[m+d])] = availible
                        coloring[(C[m],x_rs)] = (5 if availible==4 else 4)
                        matched_to_md = _get_another(C[m+d],F)
                        if (C[m+d],matched_to_md) not in coloring:
                            # color that incidence, because it cannot be colored with (4,5) ot (5,4) arbitrary
                            coloring[(C[m+d], matched_to_md)] = (5 if availible==4 else 4)
                            coloring[(matched_to_md, C[m+d])] = availible
                if (C[m],x_rs) not in coloring:
                    coloring[(C[m],x_rs)] = 4 # both 4 and 5 should be fine
            else:
                if r % 3 == 1:
                    set_colors_matching_edge(C[r-1],5,4)
                if r % 3 == 2:
                    set_colors_matching_edge(C[r+1],5,4)
                if s % 3 == 1:
                    set_colors_matching_edge(C[s-1],4,5)
                if s % 3 == 2:
                    set_colors_matching_edge(C[s+1],4,5)
            _set_colors_edge(coloring,C[p],C[r],3,5)
            _set_colors_edge(coloring,C[1],C[s],3,4)
            #end Case 3.1
        #end Subcases 1
    else:
        # Subcases 2 - each vertex of C is matched to its antipodal vertex
        n = p / 2
        
        if p % 3 == 1:
            # Case 2.1
            _set_colors_edge(coloring,C[1],C[n+1],3,4)
            _set_colors_edge(coloring,C[n],C[2*n],5,1)
        
        elif p % 3 == 2:
            # Case 3.1
            coloring[(C[n+1],C[n+2])] = 5
            coloring[(C[n],C[n-1])] = 4
            _set_colors_edge(coloring,C[2],C[n+2],5,4)
            _set_colors_edge(coloring,C[n-1],C[2*n-1],4,5)
            _set_colors_edge(coloring,C[p],C[r],3,5)
            _set_colors_edge(coloring,C[1],C[s],3,4)
        #end Subcases 2
        
    remaining_chords = [e for e in F if e not in coloring]  
    coloring.update(ic_edges_with_45(remaining_chords))
    return coloring

    
def __find_starting_special(special_vertices, F):
    for b in special_vertices:
        if not (_get_another(b, F) in special_vertices):
            return b
    # else
    return next(iter(special_vertices))  # arbitrary special vertex


def __find_colors(vertex, neighbors, coloring):
    r"""
    Returns colors {'a':_,'b':_,'c':_} from {1,2,3} for given vertex according to Lemma 5.
    """
    a = {1, 2, 3}
    for v in neighbors:
        a.discard(coloring[(vertex, v)])
        a.discard(coloring[(v, vertex)])
    a = a.pop()

    b = {1, 2, 3}
    b.discard(a)
    for v in neighbors:
        b.discard(coloring[(vertex, v)])
    b = b.pop()

    c = {1, 2, 3}
    c.discard(a)
    c.discard(b)
    c = c.pop()
    return {'a': a, 'b': b, 'c': c}


def __find_starting_vertex(cycle_indices, n):
    r"""
    Returns first i from cycle_indices such that i+1 % n is in cycle_indices as well.
    If no such i exists, returns cycle_indices[0].
    
    INPUT:
    - ``cycle_indices`` -- sorted list of numbers from [0,...,n-1]
    - ``n``             -- lenght of the cycle
    """
    for j in range(-1, len(cycle_indices) - 1):
        if (cycle_indices[j] + 1) % n == cycle_indices[j + 1]:
            return cycle_indices[j]
    return cycle_indices[0]


def __default_cycle_coloring_inversed(cycle):
    r"""
    Returns inverse (i.e. dict from incidence to color) default incidence cycle coloring of given cycle.
    Colors are {1,2,3}
    Returned coloring might not be proper incidence coloring - possibly problem on {x_0,x_n}
    
    INPUT:
    
    - ``cycle`` -- list of vertices such that (cycle[i],cycle[i+1]) is edge, cycle[0] == "cycle[length]"
    """
    colors_t = {
        0: 1,
        1: 2,
        2: 3
    }
    colors_f = {
        0: 3,
        1: 1,
        2: 2
    }
    coloring = {}
    p = len(cycle)
    for i in range(0, p):
        coloring[(cycle[i], cycle[(i + 1) % p])] = colors_t[i % 3]
        coloring[(cycle[(i + 1) % p], cycle[i])] = colors_f[i % 3]
    return coloring


def _complete_permutation(partial_permutation, aset):
    r"""
    Find permutation (returned as dict that maps elements of ``aset`` to elements of ``aset``)
    which pereserves mapping defined by ``partial_permutation``.
    
    INPUTS:
    - ``aset``                -- a set;
    - ``partial_permutation`` -- a dict; maps some elements of ``aset`` to unique elements of ``aset``
    
    EXAMPLES::
    
        sage: P = _find_permutation({1,2,3,4,5},{2: 4, 4: 3})
        sage: print(P)
        {1: 1, 2: 4, 3: 2, 4: 3, 5: 5}
    """
    # find elements not defined by partial_permutation
    set_keys = aset.difference(partial_permutation.keys())
    set_values = aset.difference(partial_permutation.values())
    if len(set_keys) != len(set_values) or len(set_keys) != len(aset) - len(partial_permutation):
        raise ValueError("'partial_permutation' is invalid")
    # map common elements as identity
    common = set_keys.intersection(set_values)
    partial_permutation.update({c: c for c in common})
    # map remaining elements arbitrary
    set_keys.difference_update(common)
    set_values.difference_update(common)
    while set_keys:
        k = set_keys.pop()
        v = set_values.pop()
        partial_permutation[k] = v
    return partial_permutation


def _cyclic_connected_component_containing_vertex(G, vertex):
    r"""
    Returns list of vertices of connected component ( = cycle) of 2-regular graph `G` which contains the `vertex`.
    The list is sorted according to the cycle (i.e. (x_n,x_0) and (x_i,x_i+1) are edges).

    INPUT:

    - ``G`` -- a 2-regular graph
    - ``vertex`` -- a vertex of `G`
    """
    return list(G.depth_first_search(vertex))


def _rotate_list(alist, indices, k):
    r"""
    Rotates `alist` so that original `alist[k]` is now `alist[0]`.
    Also correctly updates `indices`.

    INPUT:
    - ``alist`` -- a list
    - ``indices`` -- subset of indices of elements in the list.
    - ``k`` -- lenght of first part which will be moved
    """
    n = len(alist)
    a = alist[:k]
    del alist[:k]
    alist.extend(a)
    ind_a = []
    for i in indices:
        if (i >= k): break
        ind_a.append(i + n - k)
    ind_b = []
    for i in range(len(ind_a), len(indices)):
        ind_b.append(indices[i] - k)
    del indices[:]
    indices.extend(ind_b)
    indices.extend(ind_a)


def _get_another(element, pairs):
    r"""
    Returns element that forms a pair with given `element`.
    Returns `None` if none of the `pairs` contains `element`.

    INPUTS:
    - ``element`` -- element of a tuple from `pairs`
    - ``pairs`` -- iterable of binary tuple; list of unordered pairs
    """
    for pair in pairs:
        if element == pair[0]:
            return pair[1]
        if element == pair[1]:
            return pair[0]
    return None


def _inverse_coloring(inversed_coloring, colors):
    r"""
    Transform inversed coloring (maps each object to its color) to coloring (maps each color to list of objects).
    
    INPUTS:
    
    - ``inversed_coloring``  -- a dict; map objects to colors
    
    - ``colors``             -- iterable; set of colors which are used in ``inversed_coloring``
    """
    coloring = {}
    for c in colors:
        coloring[c] = []
    for incidence, color in inversed_coloring.items():
        coloring[color].append(incidence)
    return coloring


def _transform_inversed_coloring(coloring, mapping):
    r"""
    Change colors according to mapping.
    I.e. For {k1: v1, k2: v2, ...} returns {k1: f(v1), k2: f(v2),...} where f(x) == mapping[x].

    INPUT:
    - ``coloring`` -- dict; maps objects to colors
    - ``mapping``  -- dict; maps original colors to new colors
    """
    return {i: mapping[c] for i, c in coloring.items()}


def _set_colors_edge(coloring,u,v,color_uv, color_vu):
    r"""
    Set colors to a pair of incidences along the edge uv.
    
    INPUT:
    - ``coloring``  -- dict; maps incidences (ordered pair of vertices) to colors
    - ``u``, ``v``  -- vertices
    - ``color_uv``  -- color of incidence (u,uv)
    - ``color_vu``  -- color of incidence (v,uv)
    """
    coloring[(u,v)] = color_uv
    coloring[(v,u)] = color_vu
    
    
def _to_hex_colors(coloring):
    r"""
    Transforms coloring which uses an arbitrary set of colors to coloring that uses hexadecimal colors.
    
    INPUTS:
    -- ``coloring`` -- dict; mapping of colors to list of objects.
    """

    n = len(coloring)
    hex_colors = rainbow(n)
    return {hex_colors.pop(): v for k, v in coloring.items()}


def _find_cubic_supergraph(G):
    r"""
    Find cubic (3-regular) graph H such that G is subgraph of H.
    Returns a tuple (H,F) where F are extra edges in H, i.e. F = E(H)\E(G)

    INPUT:
    - ``G`` -- a graph; all vertices of degree 3 or less
    """
    G._scream_if_not_simple()
    _scream_if_not_subcubic(G)

    H = G.copy()
    F = []
    v_low_degree = {v for v in G.vertices() if G.degree(v) < 3}

    for d in range(0, 3):
        L = H.complement().subgraph(v_low_degree)
        M = [(u, v) for u, v, _ in L.matching()]
        F.extend(M)
        H.add_edges(M)
        for e in M:
            for v in e:
                if H.degree(v) == 3:
                    v_low_degree.discard(v)

    for v in v_low_degree:
        for i in range(H.degree(v), 3):
            # add 3-regular graph to vertex v
            vs = [H.add_vertex() for i in range(0, 5)]
            es = [(vs[i], vs[(i + 1) % 5]) for i in range(0, 5)]
            es.extend([(vs[1], vs[3]), (vs[2], vs[4]), (v, vs[0])])
            H.add_edges(es)
            F.extend(es)
    return (H, F)


def _scream_if_not_subcubic(G):
    r"""
    Raise ``ValueError`` if degree of any vertex of ``G`` is more than 3.
    
    INPUT:
    - ``G`` -- a graph
    """
    if max(G.degree_iterator()) > 3:
        raise ValueError("only graphs of maximum degree 3 are supported")


def _add_incident_edges(H, B):
    r"""
    Complete graph induced by H with respect to B,
    i.e. add to H all vertices of edges from B which are incident
    to a vertex of H

    INPUT:

    - ``H`` -- a set of vertices

    - ``B`` -- a set of edges
    """
    us = {u for u, v in B if ((u not in H) and (v in H))}
    vs = {v for u, v in B if ((u in H) and (v not in H))}
    us_vs = us.union(vs)
    if us_vs:
        H.extend(us_vs)
    return H


def _pair_elements(elements):
    r"""
    Return an iterable of pairs of elements (each element is used only once).
    If number of elements is odd, one is unused returned.
    Order of returned pairs and elements should be considered as random.

    - ``elements`` -- an iterable
    """
    it = iter(elements)
    stop = False
    while True:
        a = next(it)
        b = next(it)
        yield (a, b)


def _dfs_with_edge_label(G, start):
    r"""
    Return an iterator over the pair (vertex,label) in a depth-first ordering
    where the label is label of edge connecting vertex with its parent in DFS-tree.
    Label is ``None`` for the start.

    INPUT:
    - ``start`` -- vertex from which to start the traversal
    """
    seen = set()
    stack = [(start, None)]

    while stack:
        v, l = stack.pop()
        if v not in seen:
            yield (v, l)
            seen.add(v)
            for w in G.neighbors(v):
                if w not in seen:
                    stack.append((w, G.edge_label(v, w)))

def _check_is_proper_incidence_coloring(coloring):
    r"""
    Checks whether ``coloring`` does not contain a pair of adjacent incidences colorod by same color.
    
    INPUT:
    - ``coloring`` -- a dict; incidence coloring of a graph; mapping of colors to lists of incidences
    """
    for color_class in coloring.values():
        badly_colored = [((u,v),(w,y)) for u,v in color_class for w,y in color_class if v == w]
        if badly_colored:
            print (badly_colored)
            return false
    return true