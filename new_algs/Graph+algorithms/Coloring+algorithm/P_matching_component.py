import random
from common.storage import failed_graph_DB

class MatchingComponent(object):
    """
        Perfect matching for cubic graph.
    """

    def edge_coloring_by_perfect_matching(self):
        if not self.perfect_matching():
            return False

        vlist = self.graph.vid_list
        
        while len(vlist) > 0:
            v = random.choice(vlist)
            cycle = list()
            cycle.append(v)
            vlist.remove(v)
            color, alt_color = 1, 2
            while True:
                e_nbr = self.graph.neighbor_eid_list(v)
                edge = None
                for e in e_nbr:
                    temp = self.graph.get_edge(e)
                    if temp.color == 0 and temp.get_another_vertex(v) not in cycle:
                        edge = temp
                        break
                if edge != None:
                    edge.color = color
                    color, alt_color = alt_color, color
                    v = edge.get_another_vertex(v)
                    cycle.append(v)
                    vlist.remove(v)
                else:
                    temp = self.graph.get_edge_by_endpoints(v, cycle[0], 0)
                    if len(cycle) % 2 == 0:
                        temp.color = color
                    else:
                        self.graph.set_color(temp.id, v, color)
                        self.graph.set_color(temp.id, cycle[0], alt_color)
                    break
    
        return True                    

    def perfect_matching(self):
        if not self.check_if_base_graph():
            edge = self.graph.random_pick_a_edge()
            x = edge.get_endpoints()
            self.main_logic_for_perfect_matching(x)
        else:
            self.color_base_graph()

        return self.check_if_perfect_matching()
        
    def main_logic_for_perfect_matching(self, nonmatchingEdge):
        '''
        1. The underlaying graph is bridgeless cubic graph (no loop,
            multiple-edge possible).
        2. This method try to find a perfect matching on this graph.
        3. And "nonmatchingEdge"(may be simple edge) is not supposed
            to be in the matching.
        '''
        if not self.check_if_base_graph():
            # find a simple edge incident to nonmathcingEdge
            info = self._find_simple_edge_incident_to_given_edge(nonmatchingEdge)
            if info != None: # the simple edge is found
                temp, v_pos, w_pos = self._one_step_reduction(info)
                (a, b, c, d, v, w) = temp
                #self.graph.validate()##
                self.main_logic_for_perfect_matching((a, c))
                self._one_step_induction(temp, v_pos, w_pos)
                
            else: # the simple edge is not found
                temp, x_pos, t_pos = self._one_step_reduction_when_no_simple_edge(nonmatchingEdge)
                (y, x, t, z) = temp
                #self.graph.validate()###
                self.main_logic_for_perfect_matching((y,z))
                self._one_step_induction_when_no_simple_edge(temp, x_pos, t_pos)

        else:
            self.color_base_graph()
        
    def check_if_perfect_matching(self):
        vlist = []
        for edge in self.graph.edges:
            if edge.color == 3:
                (a, b) = edge.get_endpoints()
                vlist.append(a)
                vlist.append(b)
        #print "vlist: ",vlist
        if len(vlist) != self.graph.num_vertices:
            return False
        
        for vid in self.graph:
            if vid not in vlist:
                return False

        return True

    def check_if_base_graph(self):
        if len(self.graph._vertices) == 2 and len(self.graph._edges) == 3:
            return True
        return False

    def color_base_graph(self):
        if self.check_if_base_graph():
            a = random.randint(0,2)
            index = 0
            for x in self.graph._edges:
                if index == a:
                    self.graph.get_edge(x).color = 3
                else:
                    self.graph.get_edge(x).color = 0
                index = index + 1       
        else:
            print ("It is not base graph yet.")

    def _find_simple_edge_incident_to_given_edge(self, edge):
        (x, y) = edge
        (a, v, w, b) = (-1, -1, -1, -1)
        x_nbr_V = self.graph.neighbor_vid_list(x)
        y_nbr_V = self.graph.neighbor_vid_list(y)
        x_nbr_V.remove(y)
        y_nbr_V.remove(x)

        if x_nbr_V[0] != x_nbr_V[1]:
            if x_nbr_V[0] != y:
                (a, v, w, b) = (y, x, x_nbr_V[0], x_nbr_V[1])
            elif x_nbr_V[1] != y:
                (a, v, w, b) = (y, x, x_nbr_V[1], x_nbr_V[0])
        
        if a == -1: 
            if y_nbr_V[0] != y_nbr_V[1]:
                if y_nbr_V[0] != x:
                    (a, v, w, b) = (x, y, y_nbr_V[0], y_nbr_V[1])
                elif y_nbr_V[1] != x:
                    (a, v, w, b) = (x, y, y_nbr_V[1], y_nbr_V[0])
        
        if a != -1: # the simple edge is found
            assert self.graph.multiplicity(v, w) == 1
            w_nbr_V = self.graph.neighbor_vid_list(w)
            w_nbr_V.remove(v)
            c, d = w_nbr_V[0], w_nbr_V[1]
            return (a, b, c, d, v, w)
        else:
            return None

    def _one_step_reduction(self, info):
        (a, b, c, d, v, w) = info
        #print "(a, b, c, d, v, w): ", info
        #assert self.graph.multiplicity(v, w) == 1
        #try:
        #    assert self.if_connected() == True  
        #except:
        #    failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
        #    assert 0 == 1
        v_position = self.graph.get_position(v)
        w_position = self.graph.get_position(w)

        #print self.graph.to_json()
        #self.graph.validate()

        self.graph.delete_vertex(v)
        self.graph.delete_vertex(w)
        
        done = False
        if a != c and b != d:
            ac_temp = self.graph.add_edge(a, c)
            bd_temp = self.graph.add_edge(b, d)
            
            if len(self.cut_edges()) == 0 and self.if_connected() == True:
                done = True
            else:
                self.graph.remove_edge(ac_temp)
                self.graph.remove_edge(bd_temp)
                
                
        if done == False:
            c, d = d, c
            self.graph.add_edge(a, c)
            self.graph.add_edge(b, d)
            #print "a, b, c, d:",a,b,c,d
            assert len(self.cut_edges()) == 0
            assert self.if_connected() == True
        
        temp = (a, b, c, d, v, w)
        
        return (temp, v_position, w_position)

    def _one_step_induction(self, info, v_pos, w_pos):
        (a, b, c, d, v, w) = info
        edge_ac = self.graph.get_edge_by_endpoints(a, c, 0)
        edge_bd_list = self.graph.get_edges(b, d)
        
        for e in edge_bd_list:
            if e.id != edge_ac.id:
                edge_bd = e
                break

        if edge_bd.color == 3:
            bd_matched = True
        elif edge_bd.color == 0:
            bd_matched = False
        self.graph.remove_edge(edge_ac.id)
        self.graph.remove_edge(edge_bd.id)
        self.graph.add_vertex(v, v_pos)
        self.graph.add_vertex(w, w_pos)
        e_av = self.graph.add_edge(a, v)
        e_bv = self.graph.add_edge(b, v)
        e_vw = self.graph.add_edge(v, w)
        e_cw = self.graph.add_edge(c, w)
        e_dw = self.graph.add_edge(d, w)
        
        self.graph.get_edge(e_av).color = 0
        self.graph.get_edge(e_cw).color = 0
        if bd_matched == True:
            self.graph.get_edge(e_bv).color = 3
            self.graph.get_edge(e_vw).color = 0
            self.graph.get_edge(e_dw).color = 3
        else:
            self.graph.get_edge(e_bv).color = 0
            self.graph.get_edge(e_vw).color = 3
            self.graph.get_edge(e_dw).color = 0

    def _one_step_reduction_when_no_simple_edge(self, edge):
        (x, y) = edge
        if random.random() > 0.5:
            x, y = y, x
        x_nbr_V = self.graph.neighbor_vid_list(x)
        x_nbr_V.remove(y)
        t = x_nbr_V[0]
        temp = self.graph.neighbor_vid_list(t)
        temp.remove(x)
        temp.remove(x)
        z = temp[0]

        x_position = self.graph.get_position(x)
        t_position = self.graph.get_position(t)
        self.graph.delete_vertex(x)
        self.graph.delete_vertex(t)
        try:
            self.graph.add_edge(y, z)
        except:
            print ("yz: ",y,z)
            raise Exception("sadfasdg")
        info = (y, x, t, z)
        assert len(self.cut_edges()) == 0
        return (info, x_position, t_position)
        
    def _one_step_induction_when_no_simple_edge(self, info, x_pos, t_pos):
        (y, x, t, z) = info
        temp = self.graph.get_edge_by_endpoints(y, z, 0)
        self.graph.remove_edge(temp.id)
        self.graph.add_vertex(x, x_pos)
        self.graph.add_vertex(t, t_pos)
        self.graph.add_edge(y, x, 0)
        self.graph.add_edge(t, z, 0)
        self.graph.add_edge(x, t, 3)
        self.graph.add_edge(x, t, 0)


    def cut_edges(self):
        """
        Return the cut-edges of the given graph.
        
        A cut edge, or bridge, is an edge of a graph whose removal increases the number of connected
        components in the graph.

        @rtype:  list
        @return: List of cut-edges.
        """
        if self.check_if_base_graph():
            return []

        pre = {}    # Pre-ordering
        low = {}    # Lowest pre[] reachable from this node going down the spanning tree + one backedge
        spanning_tree = {}
        reply = []
        pre[None] = 0

        for each in self.graph:
            if (each not in pre):
                spanning_tree[each] = None
                self._cut_dfs(spanning_tree, pre, low, reply, each)
        
        return reply

    def if_connected(self):
        visited = {}
        count = 0

        # For 'each' node not found to belong to a connected component, find its connected
        # component.
        for each in self.graph:
            if (each not in visited):
                self._dfs(visited, count, each)
                count = count + 1
        if count == 1:
            return True

        return False

    def _dfs(self, visited, count, node):
        visited[node] = count
        # Explore recursively the connected component
        for each in self.graph[node]:
            if (each not in visited):
                self._dfs(visited, count, each)

    def _cut_dfs(self, spanning_tree, pre, low, reply, node):
        
        pre[node] = pre[None]
        low[node] = pre[None]
        pre[None] = pre[None] + 1
        
        for each in self.graph[node]:
            if (each not in pre):
                spanning_tree[each] = node
                self._cut_dfs(spanning_tree, pre, low, reply, each)
                if (low[node] > low[each]):
                    low[node] = low[each]
                if (low[each] == pre[each]):
                    reply.append((node, each))
            elif (low[node] > pre[each] and spanning_tree[node] != each):
                low[node] = pre[each]


