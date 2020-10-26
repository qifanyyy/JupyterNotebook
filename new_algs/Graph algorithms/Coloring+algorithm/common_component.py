import random
import sys
import pydot
import tempfile

from common.path import create_path
from four_color.ComplexEdgeColoring import EdgeColoring
from common.storage import *

class CommonComponent(object):
    
    def create_cycle_by_variable(self, var):
        (a,b) = var.get_endpoints()
        ca = var.link_color(a)
        cb = var.link_color(b)
        path = create_path(self.graph, a, b, cb, ca)
        return path
        
    def add_to_DB(self):
        failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
        
    def clear_colors(self):
        self.graph.clear_colors()

    def find_girth(self):
        """
            Find a face on the graph with girth edges
            return (face, cycle)
            face: the list of edge id
            cycle: the list of vertex id
        """
        girth = sys.maxint
        face = []
        vertices = list(self.graph.vertices)
        shift = random.randint(0,len(vertices)-1)
        vertices = vertices[shift:] + vertices[:shift]
        random.shuffle(vertices)
        
        for vertex in vertices:
            s = set() # set of explored edge id
            distance = {}
            distance[vertex.id] = 0
            father = {}
            father[vertex.id] = (None, None) # (a,b) a is v_id, b is edge id
            nodes = [vertex.id] # stack for the vertices to start with
            while len(nodes) > 0:
                node = nodes.pop(0)
                v_a = self.graph.get_vertex(node)
                nbrs = list(v_a.neighbors)
                random.shuffle(nbrs)
                for edge in nbrs:
                    if not edge.id in s:
                        another = edge.get_another_vertex(node)
                        if not distance.has_key(another):
                            nodes.append(another)
                            s.add(edge.id)
                            father[another] = (node, edge.id)
                            distance[another] = distance[node] + 1
                        elif distance[another] + distance[node] + 1 < girth:
                            girth = distance[another] + distance[node] + 1

                            face = list()
                            face.append(edge.id)
                            start = father[another]
                            while start[0] is not None:
                                face.append(start[1])
                                start = father[start[0]]
                            face.reverse()
                            start = father[node]
                            while start[0] is not None:
                                face.append(start[1])
                                start = father[start[0]]

        cycle = []
        edge0 = self.graph.get_edge(face[0])
        edge1 = self.graph.get_edge(face[1])
        (a, b) = edge0.get_endpoints()
        if a in edge1.get_endpoints():
            a, b = b, a
        for e in face:
            cycle.append(a)
            a = self.graph.get_edge(e).get_another_vertex(a)
        # logger.info("girth: %s",cycle)
        return (face, cycle)

    def factor_cycle(self, vertices, x, y):
        # vertices is the v_id list
        cycles = []
        paths = []
        while len(vertices) > 0:
            s = vertices[0]
            cycle1 = []
            path = create_path(self.graph, s, x, y)
            paths.append(path)
            assert path.is_closed(), "assert path.is_closed()"
            for v in path:
                cycle1.append(v)
                vertices.remove(v)
            cycles.append(list(cycle1))
        return paths

    def factor_graph(self, x, y):
        vid_list = self.graph.vid_list
        rc = list()
        while len(vid_list) > 0:
            v = random.choice(vid_list)
            temp = create_path(self.graph, v, x, y)
            for v in temp:
                if v in vid_list:
                    vid_list.remove(v)
            if temp.is_closed():
                rc.append(temp)
        return rc

    def edge_coloring(self):
        ec = EdgeColoring(self.graph)
        self.graph.random_color()
        if ec.another_run():
            return True
        return False

    def find_two_cycle(self):
        errors = []
        for edge in self.graph.errors:
            errors.append(edge)
        
        if len(errors) != 2:
            print "errors not equal 2, return false"
            return None

        (v1, v2) = errors[0].get_endpoints()
        (x1, y1) = self.graph._positions[v1]
        (x2, y2) = self.graph._positions[v2]
        mid1 = x1 + x2
        
        (v3, v4) = errors[1].get_endpoints()
        (x3, y3) = self.graph._positions[v3]
        (x4, y4) = self.graph._positions[v4]
        mid2 = x3 + x4

        if mid1 <= mid2:
            left = errors[0]
            right = errors[1]
        else:
            left = errors[1]
            right = errors[0]

        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        if la + lb != ra + rb:
            print "Two variable not same, return false"
            return None

        left_p = create_path(self.graph, v1, lb, la)
        if left_p.is_closed() != True:
            print "two variables are adjacent, return False"
            return None
        right_p = create_path(self.graph, v3, rb, ra)

        c = 6 - la - lb
        if c != 3:
            self.graph.swap_colors(c, 3)
            if left_p.c1 == 3:
                left_p.c1 = c;
            else:
                left_p.c2 = c;
            if right_p.c1 == 3:
                right_p.c1 = c;
            else:
                right_p.c2 = c;
        
        return (left_p, right_p)

    def prepare_highlight_data(self, add_edges = None):
        '''
        add_edges: list of (v_id1, v_id2)
        '''
        edges = dict()
        for p in self.highlighted:
            for v in p.edges:
                (a, b) = v.get_endpoints()
                edges[(a,b)] = True
        
        data = {}
        data['vertices'] = []
        data['edges'] = []
        for e in edges:
            data['edges'].append({
                'v1': e[0],
                'v2': e[1],
                'h1': True,
                'h2': True
                })

        if add_edges != None:
            for e in add_edges:
                data['edges'].append({
                    'v1': e[0],
                    'v2': e[1],
                    'h1': True,
                    'h2': True
                    })
        
        return data


############# to be modified #################

    def smooth(self):
        for v in self.graph.vertices:
            if len(self.graph._neighbors[v.id]) == 2:
                eid1, eid2 = self.graph._neighbors[v.id]
                edge1 = self.graph.get_edge(eid1)
                edge2 = self.graph.get_edge(eid2)
                vid1 = edge1.get_another_vertex(v.id)
                vid2 = edge2.get_another_vertex(v.id)
                c1 = edge1.get_link(vid1).color
                c2 = edge2.get_link(vid2).color
                neweid = self.graph.smooth_vertex(v.id)
                edge = self.graph.get_edge(neweid)
                edge.get_link(vid1).color = c1
                edge.get_link(vid2).color = c2
                path = create_path(self.graph, vid1, c2, c1)
                if not path.is_closed():
                    path.invert_colors()
        #if self.bicycle_algorithm():
        #    print "oh, success"
        #else:
        #    print "not success"

    def remove_one_edge(self, edge):
        e_id = edge.id
        self.graph.remove_edge(e_id)


   #### the following two method is obsolete

    def remove_edge(self):
        """Remove the first edge of the face.

        The removed edge and the original face are recorded in :attr:`removed`.

        face: the list of edge id
        cycle: the list of vertex id
        cycle[0] <--face[0]--> cycle[1]
        """
        (face, cycle) = self.find_girth()
        
        k = len(face)
        assert k >= 2, "length of face less than 2"

        e_id = face[0]
        self.graph.remove_edge(e_id)
        a = cycle[0]
        b = cycle[1]
        e1 = self.graph.smooth_vertex(a)
        #(x1, y1) = self.graph.get_edge(e1).get_endpoints()
        #removed_1st = (a, x1, y1)
        e2 = self.graph.smooth_vertex(b)
        #(x2, y2) = self.graph.get_edge(e2).get_endpoints()
        #removed_2nd = (b, x2, y2)
        #
        #   e1 = x --- a --- x
        #              |e_id
        #   e2 = x --- b --- x
        #
        #  (  (v_id1,(x1,y1)), (v_id2,(x1,y1))  )
        #self.edge_removed_info.append((removed_1st, removed_2nd))
        self.state = "initial"
        self.removed.append((e1, e2, cycle))
        #print "removed: ", (e1, e2, cycle)

    def easy_put_back(self):
        # check to see if there is edge removed.
        # if yes, simply put it back. And resolve the variables if it is easy.
        # return (k, Boolean)
        # k is the length of the cycle
        # Boolean is whether the variables are cleared up.
        if len(self.removed) > 0:
            e1, e2, cycle = self.removed.pop()
        else:
            print "nothing to put back"
            return

        colors = {1, 2, 3}
        k = len(cycle)
        #print "k: ", k
        a, b = tuple(cycle[:2])
        
        if k == 2:
            #          _
            # c -- a -/ \- b -- d
            #         \_/
            # e_1 = c -- b
            # e_2 = c -- d
            #
            edge = self.graph.get_edge(e2)
            x0 = edge.color
            x1, x2 = tuple(colors - {x0})
            (c, d) = edge.get_endpoints()
           
            self.graph.remove_edge(e2)
            self.graph.add_vertex(a)
            self.graph.add_vertex(b)
            f1 = self.graph.add_edge(a, b)
            f2 = self.graph.add_edge(a, b)
            f3 = self.graph.add_edge(a, c)
            f4 = self.graph.add_edge(b, d)
            self.graph.get_edge(f1).color = x1
            self.graph.get_edge(f2).color = x2
            self.graph.get_edge(f3).color = x0
            self.graph.get_edge(f4).color = x0
            self.state = "proper"
            return (k, True)
        
        edge_1 = self.graph.get_edge(e1)
        edge_2 = self.graph.get_edge(e2)
        
        if k == 3:
            # see p2
            x1 = edge_1.color
            x2 = edge_2.color
            x0 = 6 - x1 - x2
            v2 = cycle[2]
            v5 = edge_1.get_another_vertex(v2)
            v6 = edge_2.get_another_vertex(v2)
            self.graph.remove_edge(e1)
            self.graph.remove_edge(e2)
            self.graph.add_vertex(a)
            self.graph.add_vertex(b)
            f0 = self.graph.add_edge(a, b)
            f1 = self.graph.add_edge(a, v2)
            f2 = self.graph.add_edge(a, v5)
            f3 = self.graph.add_edge(b, v2)
            f4 = self.graph.add_edge(b, v6)
            self.graph.get_edge(f0).color = x0
            self.graph.get_edge(f1).color = x2
            self.graph.get_edge(f2).color = x1
            self.graph.get_edge(f3).color = x1
            self.graph.get_edge(f4).color = x2
            self.state = "proper"
            return (k, True)

        if k == 4:
            # see p3
            v2 = cycle[2]
            v1 = cycle[3]
            v5 = edge_1.get_another_vertex(v1)
            v6 = edge_2.get_another_vertex(v2)
            edge = self.graph.get_edge_by_endpoints(v1, v2)
            x0 = edge.color
            x1 = edge_1.color
            x2 = 6 - x0 - x1
            x3 = edge_2.color
            # case 0, different color, independent cycles
            if x3 != x1:
                # different color
                path = create_path(self.graph, v2, x3, x1)
                if not v1 in path: # independent cycle
                    path.swap_colors(x1, x3) # edge_1 and edge_2 should have the same color now
            x3 = edge_2.color # updated

            # put edges back
            self.graph.remove_edge(e1)
            self.graph.remove_edge(e2)
            self.graph.add_vertex(a)
            self.graph.add_vertex(b)
            f0 = self.graph.add_edge(a, b)
            f1 = self.graph.add_edge(a, v1)
            f2 = self.graph.add_edge(a, v5)
            f3 = self.graph.add_edge(b, v2)
            f4 = self.graph.add_edge(b, v6)

            # case 1, same color
            if x1 == x3:
                self.graph.get_edge(f0).color = x2
                self.graph.get_edge(f1).color = x0
                self.graph.get_edge(f2).color = x1
                self.graph.get_edge(f3).color = x0
                self.graph.get_edge(f4).color = x1
                edge.color = x1
            else: # case 2, different color, one cycle
                self.graph.get_edge(f0).color = x0
                self.graph.get_edge(f2).color = x1
                self.graph.get_edge(f4).color = x2
                self.graph.get_link(f1, v1).color = x1
                self.graph.get_link(f1, a).color = x2
                self.graph.get_link(f3, v2).color = x2
                self.graph.get_link(f3, b).color = x1
                path = create_path(self.graph, v1, x2, x1)
                path.swap_colors(x1, x2)
            self.state = "proper"
            return (k, True)

        if k == 5:
            v1, v2, v3, v4, v5 = tuple(cycle)
            v8 = edge_1.get_another_vertex(v5)
            v6 = edge_2.get_another_vertex(v3)
            x1 = edge_1.color
            x3 = edge_2.color
            self.graph.remove_edge(e1)
            self.graph.remove_edge(e2)
            self.graph.add_vertex(v1)
            self.graph.add_vertex(v2)
            f0 = self.graph.add_edge(v1, v2)
            f1 = self.graph.add_edge(v1, v5)
            f2 = self.graph.add_edge(v1, v8)
            f3 = self.graph.add_edge(v2, v3)
            f4 = self.graph.add_edge(v2, v6)

            if x1 == x3:
                # case (a, b)|(a, b)
                x2 = self.graph.get_edge_by_endpoints(v4, v5).color
                x0 = 6 - x1 - x2
                self.graph.get_edge(f0).color = x0
                self.graph.get_edge(f2).color = x1
                self.graph.get_edge(f4).color = x1
                self.graph.get_link(f1, v5).color = x1
                self.graph.get_link(f1, v1).color = x2
                self.graph.get_link(f3, v3).color = x1
                self.graph.get_link(f3, v2).color = x2
                path = create_path(self.graph, v2, x1, x2)
                if not path.is_closed(): # not blocked, two var cancelled
                    path.swap_colors(x1, x2)
                    self.state = "proper"
                    return (k, True)
            else:
                x2 = x3
                x0 = 6 - x1 - x2
                self.graph.get_edge(f0).color = x0
                self.graph.get_edge(f2).color = x1
                self.graph.get_edge(f4).color = x2
                self.graph.get_link(f1, v5).color = x1
                self.graph.get_link(f1, v1).color = x2
                self.graph.get_link(f3, v3).color = x2
                self.graph.get_link(f3, v2).color = x1
                path = create_path(self.graph, v2, x2, x1)
                path.swap_colors(x1, x2)
                if not path.is_closed(): # not blocked, two var cancelled
                    self.state = "proper"
                    return (k, True)

            # if var not cancelled, it is formatted as (x1, x2) | (x1, x2) type
            v7 = filter(lambda v: not v in [v1, v4], self.graph.get_vertex(v5).neighbor_vertices)[0]
            v9 = filter(lambda v: not v in [v3, v5], self.graph.get_vertex(v4).neighbor_vertices)[0]
            v10 = filter(lambda v: not v in [v2, v4], self.graph.get_vertex(v3).neighbor_vertices)[0]
            f5 = self.graph.get_edge_by_endpoints(v5, v7).id
            f6 = self.graph.get_edge_by_endpoints(v4, v9).id
            f7 = self.graph.get_edge_by_endpoints(v3, v10).id
            f8 = self.graph.get_edge_by_endpoints(v4, v5).id
            f9 = self.graph.get_edge_by_endpoints(v3, v4).id
            
            self.vertices = (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)
            self.edges = (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9)
            self.state = "petersen"
            return (k, False)

        return (k, False)
