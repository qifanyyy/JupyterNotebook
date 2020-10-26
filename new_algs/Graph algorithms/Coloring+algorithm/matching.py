'''
This module is not finished yet. The main purpose is to realize the Edmonds' matching algorithm.

Feel free to ignore it for now, as I don't use it in other modules.
'''
def Edmonds_Matching(vertices, edges, matching):
    # edge are reprensented as (a, b) where a is smaller than b
    if type(vertices) != set:
        return False
    if type(edges) != set:
        return False
    if type(matching) != set:
        return False
    if not matching.issubset(edges):
        return False

    # initialization
    # method wide global variables
    max_vertex_id = 0
    V_set = {} # v_id -> Vertex object
    E_set = {} # (a, b) -> Edge object
    unsaturated_vertex_set = set()
    root  = 0 # root vertex id
    # S contain root and vertices reached from saturated edges
    # T contain vertices reached from unsaturated edges
    unmarked_S = set()
    marked_S = set()
    T = set()

    def get_length(v):
        # v is vertex id
        length = 0
        while v != root:
            length = length + 1
            v = V_set[v].father  # father is the vertex id
        return length

    def set_cycle_father(x, y):
        if x > y:
            x, y = y, x
        if E_set[(x,y)].matched:
            V_set[x].saturated_father = y
            V_set[y].saturated_father = x
        else:
            V_set[x].unsaturated_father = y
            V_set[y].unsaturated_father = x
        

    def contract_blossom(x, y):
        # get the length
        len_x = get_length(x)
        len_y = get_length(y)
        if len_x > len_y:
            len_x, len_y = len_y, len_x
            x, y = y, x

        px = x
        py = y
        max_vertex_id = max_vertex_id + 1
        new_id = max_vertex_id
        supervertex = Vertex(new_id, True)
        supervertex.vertices = set()
        V_set[new_id] = supervertex
        
        set_cycle_father(x, y)

        for i in range(0,len_y - len_x, 1):
            supervertex.vertices.add(py)
            set_cycle_father(py, V_set[py].father)
            py = V_set[py].father

        while True:
            if py == px:
                supervertex.vertices.add(py)
                if py != root:
                    V_set[new_id].father = V_set[py].father
                else:
                    root = new_id
                break
            else:
                include_vertices.add(py)
                include_vertices.add(px)
                set_cycle_father(px, V_set[px].father)
                set_cycle_father(py, V_set[py].father)
                py = V_set[py].father
                px = V_set[px].father
        
        def mark_contracted_and_notify_neighbor(v_id):
            V_set[v_id].contracted = True
            for neighbor in V_set[v_id].neighbor_vertices:
                if neighbor.id not in supervertex.vertices:
                    V_set[neighbor].neighbor_vertices.remove(V_set[v_id])
                    V_set[neighbor].neighbor_vertices.add(V_set[new_id])
                    supervertex.neighbor_vertices.add(neighbor)
            for neighbor in V_set[v_id].neighbor_edges:
                if neighbor.other_vertex_id(v_id) not in supervertex.vertices:
                    neighbor.replace_vertex_id(v_id, new_id)
                    supervertex.neighbor_edges.add(neighbor)

        for v_i in supervertex.vertices:
            mark_contracted_and_notify_neighbor(v_i)

        unmarked_S.difference_update(supervertex.vertices)
        marked_S.difference_update(supervertex.vertices)
        T.difference_update(supervertex.vertices)
        unmarked_S.add(new_id)

        return supervertex

    def set_fathership(v_id, blossom):
    	if hasattr(blossom, 'father'):
    		pass
    	else:
    		index = root


    def find_M_augmenting_path(blossom, v_id):
    	path = list()
    	temp = [blossom.id, v_id]
    	temp.sort()
    	edge = E_set[tuple(temp)]
    	for v in blossom.vertices:
    		if edge in v.neighbor_edges:
    			V_set[v_id].father = v
    			while 


    def clear_blossom(blossom):
    	#blossom = V_set[blossom_id]
        blossom_id = blossom.id    
    	for v_id in blossom.vertices:
    		V_set[v_id].contracted = blossom.contracted
            for neighbor in V_set[v_id].neighbor_vertices:
                if neighbor.id not in supervertex.vertices:
                    neighbor.neighbor_vertices.remove(blossom)
                    neighbor.neighbor_vertices.add(V_set[v_id])
                    
            for neighbor in V_set[v_id].neighbor_edges:
                if neighbor.has_vertex_id(blossom_id):
                    neighbor.replace_vertex_id(blossom_id, v_id)
        del V_set[blossom_id]
    
    def clear_father_relationship():
    	for v in V_set:
    		if hasattr(V_set[v], 'father'):
    			del V_set[v].father
    		if hasattr(V_set[v], 'unsaturated_father'):
    			del V_set[v].unsaturated_father
    		if hasattr(V_set[v], 'saturated_father'):
    			del V_set[v].saturated_father


    def start_from(u_id):
        # initialization
        # S --  u and vertices reached along saturated edge
        # T --  vertices reached along unsaturated edge
        unmarked_S = {u_id}
        marked_S = set()
        T = set()
        while True:
            if len(unmarked_S) == 0:
                break ######################
            v_id = unmarked_S.pop()

            finished = False
            while not finished:
                for y in V_set[v_id].neighbor_vertices:
                    if y.id in T:
                        continue
                    if y.is_saturated == False:
                        # find an M-augmenting path
                        # code here
                        '''first, second = y, V_set[v_id]
                        temp = [y.id, v_id]
                        temp.sort()
                        M_path = set()'''
                        
                        p = find_M_augmenting_path(y, V_set[v_id])
                        for e in p:
                        	if e.matched == True:
                        		e.matched == False
                        	else:
                        		e.matched = True
                        
                        # recover the blossom
                        for v in V_set:
                        	if V_set[v].is_super:
                        		clear_blossom(V_set[v])
                        clear_father_relationship()
                        return
                    elif (y.id in unmarked_S) or (y.id in marked_S):
                        # a blossom is found
                        new_id = contract_blossom(v_id, y.id)
                        v_id = new_id
                        break
                    else:
                        for n_e in y.neighbor_edges:
                            if n_e.matched == True:
                                T.add(y.id)
                                y.father = v_id
                                w = n_e.other_vertex_id(y.id)
                                unmarked_S.add(w)
                                V_set[w].father = y
                                break
                #finished = True
                marked_S.add(v)


    # main()
    max_vertex_id = max(vertices)

    V_set = {} # v_id -> Vertex object
    for v in vertices:
        V_set[v] = Vertex(v)

    E_set = {} # (a, b) -> Edge object
    for e in edges: # e = (a, b)
        E_set[e] = Edge(e[0], e[1])
        V_set[e[0]].neighbor_edges.add(E_set[e])
        V_set[e[1]].neighbor_edges.add(E_set[e])
        V_set[e[0]].neighbor_vertices.add(V_set[e[1]])
        V_set[e[1]].neighbor_vertices.add(V_set[e[0]])

    for e in matching:
        E_set[e].matched = True
        
    unsaturated_vertex_set = set() # set of v_id
    for v in vertices:
        if V_set[v].is_saturated == False:
            unsaturated_vertex_set.add(v) 

    while True:
        if len(unsaturated_vertex_set) == 0:
            return E_set
        u_id = unsaturated_vertex_set.pop()
        start_from(u_id)



class Edge(object):
    def __init__(self, a, b, matched = False):
        self.endpoints = {a, b}
        self.matched = matched
        
        def other_vertex_id(self, v_id):
            tmp = self.endpoints - {v_id}
            if len(tmp) == 2:
                return None
            else:
                return tmp.pop()

        def has_vertex_id(self, v_id):
        	return v_id in self.endpoints

        def replace_vertex_id(self, old_v, new_v):
            assert old_v in self.endpoints
            self.endpoints.remove(old_v)
            self.endpoints.add(new_v)


class Vertex(object):
    def __init__(self, v_id, supervertex = False):
        self.id = v_id
        self.is_super = supervertex
        self.contracted = False
        self.neighbor_edges = set() # set of Edge object
        self.neighbor_vertices = set() # set of Vertex object

        @property
        def is_saturated(self):
            for e in self.neighbor_edges:
                if e.matched == True:
                    return True
            return False
