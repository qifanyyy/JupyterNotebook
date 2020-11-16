import random
import logging
import sys
import copy
import json

from common.path import create_path, Path
from common.multigraph import MultiGraph
from common.storage import failed_graph_DB, count_utility
from four_color.ComplexEdgeColoring import EdgeColoring


class InductionComponent(object):

    def find_locking_cycles(self, standard = True):
        etype = None
        variables = []
        for edge in self.graph.errors:
            variables.append(edge)
            if etype == None:
                etype = edge.edge_type
            elif edge.edge_type != etype:
                print ("Not homogeneous configuration!")
                return False # different variables found
        
        if standard == True:
            if etype == "ac":
                self.graph.swap_colors(1, 3)
            elif etype == "bc":
                self.graph.swap_colors(2, 3)

        cycles = []
        while len(variables) > 0:
            edge = variables.pop()
            (a, b) = edge.get_endpoints()
            ca = edge.link_color(a)
            cb = edge.link_color(b)
            temp = create_path(self.graph, a, cb, ca)
            if temp.is_closed() == True:
                cycles.append(temp)
            else:
                end = temp.end
                temp.invert_colors()
                for xx in variables:
                    if end in xx:
                        variables.remove(xx)
                        break
        return cycles
    
    def bicycle_algorithm(self):
        errors = []
        for e in self.graph.errors:
            errors.append(e)
        
        if len(errors) != 2:
            print ("errors not equal 2, return false")
            return False 

        left = errors[0]
        right = errors[1]
        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        a, b = la, lb
        if (la, lb) == (ra, rb):
            pass
        elif (la, lb) == (rb, ra):
            v3, v4 = v4, v3
        else:
            print ("Two variable not same, return false")
            return False

        left_p = create_path(self.graph, v1, b, a)
        if left_p.is_closed() != True:
            count_utility.count(-1)
            left_p.swap_colors(b, a)
            return True
        
        right_p = create_path(self.graph, v3, b, a)
        
        
        len_left = len(left_p)
        len_right = len(right_p)
        
        steps = 0

        for i in range(0, 2 * len_left):
            for j in range(0, 2 * len_right):
                if self.sub_routine_for_bicycle_algorithm(left_p, right_p):
                    count_utility.count(steps)
                    return True
                right_p.move_one_step()
                steps = steps + 1
            left_p.move_one_step()
        
        return False

    def false_algorithm_1(self):
        errors = []
        for e in self.graph.errors:
            errors.append(e)
        
        if len(errors) != 2:
            print ("errors not equal 2, return false")
            return False 

        left = errors[0]
        right = errors[1]
        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        a, b = la, lb
        if (la, lb) == (ra, rb):
            pass
        elif (la, lb) == (rb, ra):
            v3, v4 = v4, v3
        else:
            print ("Two variable not same, return false")
            return False

        left_p = create_path(self.graph, v1, b, a)
        if left_p.is_closed() != True:
            left_p.swap_colors(b, a)
            return True
        
        if self.graph.multiplicity(v1, v3) == 1:
            x, y = v1, v3
        elif self.graph.multiplicity(v1, v4) == 1:
            x, y = v1, v4
        elif self.graph.multiplicity(v2, v3) == 1:
            x, y = v2, v3
        elif self.graph.multiplicity(v2, v4) == 1:
            x, y = v2, v4
        else:
            raise Exception("weriuhgas")

        xx = v1 + v2 - x
        yy = v3 + v4 - y

        vid_x = self.graph.neighbor_vid_list(x)
        vid_y = self.graph.neighbor_vid_list(y)
        vid_x.remove(y)
        vid_y.remove(x)

        x1, x2 = vid_x
        y1, y2 = vid_y

        def list_to_set(li):
            ss = set()
            for x in li:
                ss.add(x)
            return ss

        temp1 = self.graph.neighbor_vid_list(x1)

        ###################

        right_p = create_path(self.graph, v3, b, a)
        
        
        len_left = len(left_p)
        len_right = len(right_p)
        
        steps = 0

        for i in range(0, 2 * len_left):
            for j in range(0, 2 * len_right):
                if self.sub_routine_for_bicycle_algorithm(left_p, right_p):
                    count_utility.count(steps)
                    return True
                right_p.move_one_step()
                steps = steps + 1
            left_p.move_one_step()
        
        return False

    def xxx(self):
        (face, cycle) = self.find_girth()        
        e_id = random.choice(face)
        edge = self.graph.get_edge(e_id)
        self.remove_specified_edge(edge)
        while not self.edge_coloring():
            pass
        assert self.graph.num_errors == 0
        self.putback_for_specified_edge(True)
        

        cycles = self.find_two_cycle()
        if cycles != None:
            left, right = cycles
            v_ab = []
            for v in self.graph.vertices:
                if v.id not in left and v.id not in right:
                    v_ab.append(v.id)
                    break
            if len(v_ab) == 0:
                self.add_to_db()
                return
        
        self.xxx()

    def sub_routine_for_bicycle_algorithm(self, path1, path2):
        a, b = path1.c2, path1.c1
        v1 = path1.begin
        v2 = path1.end
     
        c = 6 - a - b
        path_ac = create_path(self.graph, v1, c, a)
        path_bc = create_path(self.graph, v2, c, b)
        v_ac = []
        v_bc = []
        for ve in self.graph.vertices:
            if ve.id not in path_ac:
                v_ac.append(ve.id)
            if ve.id not in path_bc:
                v_bc.append(ve.id)
        ac_cycle = self.factor_cycle(v_ac, a, c)
        bc_cycle = self.factor_cycle(v_bc, b, c)
        cycles = ac_cycle + bc_cycle

        for x in cycles:
            x.invert_colors()
            temp = create_path(self.graph, v1, b, a)
            if temp.is_closed() != True:
                temp.invert_colors()
                return True
            x.invert_colors()
        return False


    
    def find_end_matching(self, storage):
        errors = []
        for e in self.graph.errors:
            errors.append(e)
        
        for err in errors:
            path = self.create_cycle_by_variable(err)
            if path.is_closed() == False:
                continue
            lgth = len(path)
            i = 0
            vmap = dict()
            for v in path:
                i += 1
                vmap[v] = i

    def sub_end_matching(self, path):
        lgth = len(path)
        i = 0
        vmap = dict()
        for v in path:
            i += 1
            vmap[v] = i

        mlist = set()
        for i in range(0,lgth):
            begin = path.begin
            end = path.end
            beginc = path.c2
            endc = path.c1
            
            p1 = Path(self.graph, 3, beginc)
            p.add_vertex(begin)
            
            va = begin
            vertex = multigraph.get_vertex(va)
            color = 3
            alt_color = beginc

            while True:
                edge = vertex.get_neighbor_edge_by_color(color)
                if edge is None:
                    break

                vb = edge.get_another_vertex(va)
                if vb not in path:
                    break

                p.add_vertex(vb)
                va = vb
                vertex = self.graph.get_vertex(va)
                color, alt_color = alt_color, color

            p2 = Path(self.graph, 3, endc)
            p.add_vertex(end)
            
            va = end
            vertex = multigraph.get_vertex(va)
            color = 3
            alt_color = endc

            while True:
                edge = vertex.get_neighbor_edge_by_color(color)
                if edge is None:
                    break

                vb = edge.get_another_vertex(va)
                if vb not in path:
                    break

                p.add_vertex(vb)
                va = vb
                vertex = self.graph.get_vertex(va)
                color, alt_color = alt_color, color
            

################ remove and putback part ################################

    def remove_specified_edge(self, edge):
        e_id = edge.id
        (a, b) = edge.get_endpoints()
        
        self.graph.remove_edge(e_id)
        
        loc_a = self.graph.get_position(a)
        e1 = self.graph.smooth_vertex(a)
        (x1, y1) = self.graph.get_edge(e1).get_endpoints()
        removed_1st = (a, x1, y1, loc_a)
        
        loc_b = self.graph.get_position(b)
        e2 = self.graph.smooth_vertex(b)
        (x2, y2) = self.graph.get_edge(e2).get_endpoints()
        removed_2nd = (b, x2, y2, loc_b)
        self.removed_info.append((removed_1st, removed_2nd))

    def remove_edge_on_girth(self):
        (face, cycle) = self.find_girth()        
        e_id = random.choice(face)
        edge = self.graph.get_edge(e_id)
        self.remove_specified_edge(edge)

    def putback_the_last_deleted_edge(self, try_to_color = False):
        if len(self.removed_info) == 0:
            print ("nothing to putback")
            return

        removed_1st, removed_2nd = self.removed_info.pop()
        (a, x1, y1, loc_a) = removed_1st
        (b, x2, y2, loc_b) = removed_2nd
    
        self._add_vertex_and_color(removed_2nd, try_to_color)
        self._add_vertex_and_color(removed_1st, try_to_color)
        self._add_edge_and_color(a, b, try_to_color)

    def putback_for_specified_edge(self, try_to_color = False):
        while len(self.removed_info) > 0:
            self.putback_the_last_deleted_edge(try_to_color)

    def _add_vertex_and_color(self, removed_info, try_to_color = True):
        '''
            requisite: The underlaying graph must be properly colored
        '''
        (a, x, y, loc_a) = removed_info
        
        edge = self.graph.get_edge_by_endpoints(x, y)
        xc = edge.link_color(x)
        yc = edge.link_color(y)
        
        self.graph.remove_edge(edge.id)
        
        self.graph.add_vertex(a, loc_a)
        xa = self.graph.add_edge(x, a)
        ya = self.graph.add_edge(y, a)

        if try_to_color == False:
            return

        if xc not in [1, 2, 3] or yc not in [1, 2, 3]:
            print ("edge is not colored")
            return

        used_color = set()
        used_color.add(xc)
        used_color.add(yc)
        
        if xc == yc:
            temp = self.graph.get_edge(ya)
            temp.color = yc
            temp = self.graph.get_edge(xa)
            temp.get_link(x).color = xc
            temp.get_link(a).color = xc % 3 + 1
        else:
            temp = self.graph.get_edge(ya)
            temp.color = yc
            temp = self.graph.get_edge(xa)
            temp.color = xc

    def _add_edge_and_color(self, vid1, vid2, try_to_color = True):
        assert len(self.graph._neighbors[vid1]) == 2
        assert len(self.graph._neighbors[vid2]) == 2
        
        if try_to_color == False:
            self.graph.add_edge(vid1, vid2)
            return
            
        vertex1 = self.graph.get_vertex(vid1)
        vertex2 = self.graph.get_vertex(vid2)

        var1 = None
        cst1 = None
        var2 = None
        cst2 = None
        
        for e in vertex1.neighbors:
            if e.is_error():
                var1 = e
            else:
                cst1 = e
        
        for e in vertex2.neighbors:
            if e.is_error():
                var2 = e
            else:
                cst2 = e
        
        assert var1.another_link_color(vid1) == cst1.color
        assert var2.another_link_color(vid2) == cst2.color
        
        eid = self.graph.add_edge(vid1, vid2)
        
        if cst1.color == cst2.color:
            cc = cst1.color
            var1.get_link(vid1).color = cc % 3 + 1
            var2.get_link(vid2).color = cc % 3 + 1
            self.graph.get_edge(eid).color = (cc + 1) % 3 + 1
        else:
            c1 = cst1.color
            c2 = cst2.color
            var1.get_link(vid1).color = c2
            var2.get_link(vid2).color = c1
            self.graph.get_edge(eid).color = 6 - c1 - c2

############## end of remove and putback part ###########################

    def count_solutions(self):
        errors = []
        for e in self.graph.errors:
            errors.append(e)
        
        if len(errors) != 2:
            return False 

        left = errors[0]
        right = errors[1]
        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        a, b = la, lb
        if (la, lb) == (ra, rb):
            pass
        elif (la, lb) == (rb, ra):
            v3, v4 = v4, v3
        else:
            return False

        left_p = create_path(self.graph, v1, b, a)
        if left_p.is_closed() != True:
            return -1
        
        right_p = create_path(self.graph, v3, b, a)
        
        len_left = len(left_p)
        len_right = len(right_p)
        
        count = 0

        for i in range(0, 2 * len_left):
            for j in range(0, 2 * len_right):
                if self._sub_routine_for_count(left_p):
                    count = count + 1
                right_p.move_one_step()
            left_p.move_one_step()
        
        return float(count) / (4 * len_left * len_right)

    def _sub_routine_for_count(self, path1):
        a, b = path1.c2, path1.c1
        v1 = path1.begin
        v2 = path1.end
     
        c = 6 - a - b
        path_ac = create_path(self.graph, v1, c, a)
        path_bc = create_path(self.graph, v2, c, b)
        v_ac = []
        v_bc = []
        for ve in self.graph.vertices:
            if ve.id not in path_ac:
                v_ac.append(ve.id)
            if ve.id not in path_bc:
                v_bc.append(ve.id)
        
        ac_cycle = self.factor_cycle(v_ac, a, c)
        bc_cycle = self.factor_cycle(v_bc, b, c)
        cycles = ac_cycle + bc_cycle

        for x in cycles:
            x.invert_colors()
            temp = create_path(self.graph, v1, b, a)
            if temp.is_closed() != True:
                x.invert_colors()
                return True
            x.invert_colors()
        
        return False


########################
    def not_finished_cycles_algorithm(self):
        cycles = self.find_locking_cycles()
        if cycles == False:
            return
        while len(cycles) > 0:
            cyc1 = random.choice(cycles)
 
            a, b = cyc1.c2, cyc1.c1
            v1 = cyc1.begin
            v2 = cyc1.end
            c = 6 - a - b

            ac_cycle = self.factor_graph(a, c)
            bc_cycle = self.factor_graph(b, c)
            resolutions = ac_cycle + bc_cycle
            
            for x in resolutions:
                x.invert_colors()
                temp = create_path(self.graph, v1, b, a)
                if temp.is_closed() != True:
                    temp.invert_colors()
                    for cc in cycles:
                        if temp.end in cc:
                            cycles.remove(cc)
                    print ("resolve two variables")
                    break
                x.invert_colors()

            return False

        return True
