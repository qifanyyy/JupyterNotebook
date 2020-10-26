import random
import copy
from common.path import *

class SearchingComponent(object):
    

    def try_to_find(self):
        temp = self.exhaustive_matching()
        print "found matchings: ", len(temp)
        
        rnd = 10000
        while rnd > 0:
            rnd -= 1
            self.perfect_matching()
            ma = set()
            for edge in self.graph.edges:
                if edge.color == 3:
                    ma.add(edge.get_endpoints())

            if ma not in temp:
                print ma
                print temp
                return

        print "not found!!"

    def exhaustive_matching(self):
        # applied to snarks only
        self.found_list = list()
        self.subroutine()
        return self.found_list
        
    def subroutine(self):
        temp = set()
        for edge in self.graph.edges:
            if edge.color == 3:
                temp.add(edge.get_endpoints())

        if temp in self.found_list:
            return

        self.found_list.append(temp)

        errors = []
        for e in self.graph.errors:
            errors.append(e)
        
        if len(errors) != 2:
            print "errors not equal 2, return false"
            return False 

        left = errors[0]
        right = errors[1]
        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        if la + lb != ra + rb:
            raise Exception("Two variable not same, return false")
            
        path1 = create_path(self.graph, v1, lb, la)
        if path1.is_closed() != True:
            raise Exception("not snarks!!!!!!!!!")
        path2 = create_path(self.graph, v3, rb, ra)
        
        start_point = copy.deepcopy(self.graph._colors)

        len_left = len(path1)
        len_right = len(path2)

        for i in range(0, 2 * len_left):
            for j in range(0, 2 * len_right):
                self.graph._colors = copy.deepcopy(start_point)
                path1.move_steps(i)
                path2.move_steps(j)
                path1.validate()
                path2.validate()
                a, b = path1.c2, path1.c1
                v1 = path1.begin
                v2 = path1.end
             
                c = 6 - a - b
                path_ac = create_path(self.graph, v1, c, a)
                path_bc = create_path(self.graph, v2, c, b)
                #print "path ac: ", path_ac
                #print "path bc: ", path_bc
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
                    self.subroutine()
                    x.invert_colors()
                
                path1.move_steps(-i)
                path2.move_steps(-j)
        
        self.graph._colors  = copy.deepcopy(start_point)
                

    def exhaustive_search_simple_one(self):
        # dont use youyong cycles
        if self.graph._colors in self.coloring_stack:
            return False
        
        if self.try_to_reduce():
            return True
        
        self.coloring_stack.append(copy.deepcopy(self.graph._colors))
        
        current_coloring = copy.deepcopy(self.graph._colors)
            
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        a1 = self.graph.get_link(f3, v3).color
        b1 = self.graph.get_link(f3, v2).color
        assert {a, b} == {a1, b1}, "{a, b} == {c, d}"
        c = 6 - a - b

        if a == a1:
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_left_ab()
            if self.exhaustive_search_simple_one():
                return True
            
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_right_ab()
            if self.exhaustive_search_simple_one():
                return True

            self.graph._colors = copy.deepcopy(current_coloring) 
            self.graph.get_link(f1, v1).color = c
            self.graph.get_link(f3, v2).color = c
            self.graph.get_edge(f0).color = b
            if self.exhaustive_search_simple_one():
                return True

        else:
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_left_ab()
            if self.exhaustive_search_simple_one():
                return True

            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_right_ab()
            if self.exhaustive_search_simple_one():
                return True

        return False

    def exhaustive_search(self):
        if self.graph._colors in self.coloring_stack:
            return False
        if self.try_to_reduce():
            return True
        self.coloring_stack.append(copy.deepcopy(self.graph._colors))
        
        current_coloring = copy.deepcopy(self.graph._colors)
            
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        a1 = self.graph.get_link(f3, v3).color
        b1 = self.graph.get_link(f3, v2).color
        assert {a, b} == {a1, b1}, "{a, b} == {c, d}"
        c = 6 - a - b

        if a == a1:
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_left_ab()
            if self.exhaustive_search():
                return True
            
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_right_ab()
            if self.exhaustive_search():
                return True

            self.graph._colors = copy.deepcopy(current_coloring)
            
            self.graph.get_link(f1, v1).color = c
            self.graph.get_link(f3, v2).color = c
            self.graph.get_edge(f0).color = b
            if self.exhaustive_search():
                return True

            
            self.graph._colors = copy.deepcopy(current_coloring)
            path_bc = create_path(self.graph, v4, c, b)
            assert path_bc.is_closed(), "assert path_bc.is_closed()"
            v_bc = []
            for ve in self.graph.vertices:
                if ve.id not in path_bc and ve.id not in {v1, v2}:
                    v_bc.append(ve.id)
            bc_cycle = self.factor_cycle(v_bc, b, c)
            print "a1==a2, bc cycles: ", bc_cycle

            for i in range(0, len(bc_cycle), 1):
                bc_cycle[i].swap_colors(b, c)
                print "invert bc: ", bc_cycle[i]
        
                if self.exhaustive_search():
                    return True

                self.graph._colors = copy.deepcopy(current_coloring)
            

        else:
            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_left_ab()
            if self.exhaustive_search():
                return True

            self.graph._colors = copy.deepcopy(current_coloring)
            self.invert_right_ab()
            if self.exhaustive_search():
                return True

            
            self.graph._colors = copy.deepcopy(current_coloring)
            if self.graph.get_edge(f9).color == c:
                path_bc = create_path(self.graph, v3, c, b)
                v_bc = []
                for ve in self.graph.vertices:
                    if ve.id not in path_bc:
                        v_bc.append(ve.id)
                bc_cycle = self.factor_cycle(v_bc, b, c)
                print "a1!=a2, bc cycles: ", bc_cycle

                for i in range(0, len(bc_cycle), 1):
                    bc_cycle[i].swap_colors(b, c)
                    print "invert bc: ", bc_cycle[i]
                    if self.exhaustive_search():
                        return True
                    self.graph._colors = copy.deepcopy(current_coloring)

                
            elif self.graph.get_edge(f8).color == c:
                path_ac = create_path(self.graph, v5, c, a)
                v_ac = []
                for ve in self.graph.vertices:
                    if ve.id not in path_ac:
                        v_ac.append(ve.id)
                ac_cycle = self.factor_cycle(v_ac, a, c)
                print "a1!=a2, ac cycles: ", ac_cycle

                for i in range(0, len(ac_cycle), 1):
                    ac_cycle[i].swap_colors(a, c)
                    print "invert ac: ", ac_cycle[i]
                    if self.exhaustive_search():
                        return True
                    self.graph._colors = copy.deepcopy(current_coloring)
            


        return False

    def sub_routine_for_try_reduce_by_symmetry(self):
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        a1 = self.graph.get_link(f3, v3).color
        c = self.graph.get_link(f3, v2).color
        
        assert a == a1, "{a} == {a1}"
        assert a + b + c == 6, "assert a + b + c == 6"
        assert self.graph.get_edge(f8).color == b, "assert self.graph.get_edge(f8).color == b"
        assert self.graph.get_edge(f9).color == c, "assert self.graph.get_edge(f9).color == c"
        assert self.graph.get_link(f0, v1).color == c
        assert self.graph.get_link(f0, v2).color == b

        path_ac = create_path(self.graph, v5, c, a)
        path_ac.swap_colors(a, c)
        path_ab = create_path(self.graph, v3, b, a)
        if v5 not in path_ab:
            print "bravo!!~AA"
            path_ab.swap_colors(a, b)
            path_bc = create_path(self.graph, v5, b, c)
            path_bc.swap_colors(b, c)
            return True
        path_ac.swap_colors(a, c)

        path_ab = create_path(self.graph, v3, b, a)
        path_ab.swap_colors(a, b)
        path_ac = create_path(self.graph, v5, c, a)
        if v3 not in path_ac:
            print "bravo!!~BB"
            path_ac.swap_colors(a, c)
            path_bc = create_path(self.graph, v5, b, c)
            path_bc.swap_colors(b, c)
            return True
        path_ab.swap_colors(a, b)

        return False

    def try_to_reduce(self):
        """
            Check to see if the current coloring can be resolved properly.
            If yes, then do it.
            If no, the coloring should not be changed.
        """
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        a1 = self.graph.get_link(f3, v3).color
        b1 = self.graph.get_link(f3, v2).color
        assert {a, b} == {a1, b1}, "{a, b} == {c, d}"

        if a == a1: # ab, ab type
            # try two ab connected
            path_ab = create_path(self.graph, v1, a, b)
            if not path_ab.is_closed():
                path_ab.swap_colors(a, b)
                return True
        
            c = 6 - a - b
            self.graph.get_link(f1, v1).color = c
            self.graph.get_link(f3, v2).color = c
            self.graph.get_edge(f0).color = b

            # try two ac connected
            path_ac = create_path(self.graph, v1, a, c)
            if not path_ac.is_closed():
                path_ac.swap_colors(a, c)
                return True
        
            self.graph.get_link(f1, v1).color = b
            self.graph.get_link(f3, v2).color = b
            self.graph.get_edge(f0).color = c

            # try symmetry reduction
            if self.graph.get_edge(f9).color == c:
                self.graph.get_vertex(v2).swap_colors(b, c)
                if self.sub_routine_for_try_reduce_by_symmetry():
                    return True
                self.graph.get_vertex(v2).swap_colors(b, c)

            elif self.graph.get_edge(f8).color == c:
                self.graph.get_vertex(v1).swap_colors(b, c)
                if self.sub_routine_for_try_reduce_by_symmetry():
                    return True
                self.graph.get_vertex(v1).swap_colors(b, c)


        else: # ab, ba type
            # try two ab connected
            path_ab = create_path(self.graph, v1, a, b)
            if not path_ab.is_closed():
                path_ab.swap_colors(a, b)
                return True
        
            # try to resolve by swap ac cycle
            c = 6 - a - b        
            if self.graph.get_edge(f9).color == c:
                path_ac = create_path(self.graph, v3, a, c)
                if path_ac.is_closed():
                    path_ac.swap_colors(a, c)
                    temp = create_path(self.graph, v5, b, a)
                    temp.swap_colors(b, a)
                    return True
            elif self.graph.get_edge(f8).color == c:
                path_bc = create_path(self.graph, v5, b, c)
                if path_bc.is_closed():
                    path_bc.swap_colors(b, c)
                    temp = create_path(self.graph, v5, b, a)
                    temp.swap_colors(b, a)
                    return True

        return False
  