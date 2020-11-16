class InductionEngine(object):
    def find_KaiXuanMen(self):
        ''' contaions only two variables of the same kind
            which are linked by a ceil edge
            and the two variables are in different kempe cycles
        '''
        errors = []
        for edge in self.graph.edges:
            if edge.is_error():
                errors.append(edge)
        if len(errors) != 2:
            err_msg = "errors not equal 2, return false"
            return (False, err_msg, None, None, None, None, None) 

        left = errors[0]
        right = errors[1]
        (la, lb) = left.links
        (ra, rb) = right.links
        if la.color + lb.color != ra.color + rb.color:
            err_msg = "Two variable not same, return false"
            return (False, err_msg, None, None, None, None, None)

        ceil = None
        (la, lb) = left.get_endpoints()
        (ra, rb) = right.get_endpoints()
        
        if self.graph.get_edge_by_endpoint(la, ra) != None:
            left_top, right_top = la, ra
            ceil = self.graph.get_edge_by_endpoint(left_top, right_top)

        if self.graph.get_edge_by_endpoint(la, rb) != None:
            left_top, right_top = la, rb
            ceil = self.graph.get_edge_by_endpoint(left_top, right_top)

        if self.graph.get_edge_by_endpoint(lb, ra) != None:
            left_top, right_top = lb, ra
            ceil = self.graph.get_edge_by_endpoint(left_top, right_top)

        if self.graph.get_edge_by_endpoint(lb, rb) != None:
            left_top, right_top = lb, rb
            ceil = self.graph.get_edge_by_endpoint(left_top, right_top)
            
        if ceil == None:
            err_msg = "format color failed! Two variable not adjacent, return false"
            return (False, err_msg, None, None, None, None, None)


        left_p = create_path(self.graph, left_top, left.link_color(left.get_another_vertex(left_top)), left.link_color(left_top))
        if left_p.is_closed() != True:
            err_msg = "left path not closed. Two variables are linked by kempe path, return false"
            return (False, err_msg, None, None, None, None, None)

        return (True, "", left, right, left_top, right_top, ceil)

    def format_location(self, kaixuanmen, width=600, height=600, margin=20):
        left, right, left_top, right_top, ceil = kaixuanmen
        radius = width
        import math
        rad = 2 * math.asin( 0.5 * float(height - 2 * margin) / radius )
        
        left_p = create_path(self.graph, left_top, left.link_color(left.get_another_vertex(left_top)), left.link_color(left_top))
        for index in range(0, len(left_p), 1):
            p_rad = index * rad / (len(left_p)-1)
            p_y = margin + (height - 2 * margin) / 2 - math.sin(rad / 2 - p_rad) * radius
            p_x = margin + math.cos(rad /2 - p_rad) * radius - math.cos(rad / 2) * radius
            self.graph._positions[left_p._vertices[index]] = (p_x, p_y)
       
        right_p = create_path(self.graph, right_top, right.link_color(right.get_another_vertex(right_top)), right.link_color(right_top))
        for index in range(0, len(right_p), 1):
            p_rad = index * rad / (len(right_p)-1)
            p_y = margin + (height - 2 * margin) /2 - math.sin(rad / 2 - p_rad) * radius
            p_x = width - margin - (math.cos(rad / 2 - p_rad) * radius - math.cos(rad / 2) * radius)
            self.graph._positions[right_p._vertices[index]] = (p_x, p_y)

        (la, lb) = left.links
        color_a = la.color
        color_b = lb.color

        other_vertices = []
        for vertex in self.graph._vertices:
            if (vertex not in left_p) and (vertex not in right_p):
                other_vertices.append(int(vertex))
         
        cycle = []
        while len(other_vertices) > 0:
            start = other_vertices[0]
            p = create_path(self.graph, start, color_a, color_b)
            for x in p._vertices:
                other_vertices.remove(int(x))
            cycle.append(p._vertices)

        x0 = width / 2
        step = (height - 2 * margin) / (len(cycle) + 1)
        for i in range(0,len(cycle),1):
            y0 = margin + (i + 1) * step
            step_angle = 2 * math.pi / len(cycle[i])
            for j in range(0, len(cycle[i]), 1):
                x = x0 + math.cos(j * step_angle) * (width - 2 * margin)/4
                y = y0 + math.sin(j * step_angle) * (width - 2 * margin)/4
                self.graph._positions[cycle[i][j]] = (x,y)

    def standard_format(self, width=600, height=600, margin=20):
        result, err_msg, left, right, left_top, right_top, ceil = self.find_KaiXuanMen()
        if result == False:
            print (err_msg)
            return False

        if ceil.color != 3:
            self.graph.swap_colors(ceil.color,3)

        if left.link_color(left_top) != 2:
            p = create_path(self.graph, left_top, 2, 1)
            p.swap_colors(1, 2)
        
        if right.link_color(right_top) != 2:
            p = create_path(self.graph, right_top, 2, 1)
            p.swap_colors(1, 2)

        kaixuanmen = (left, right, left_top, right_top, ceil)
        self.format_location(kaixuanmen, width, height, margin)
        return True
    
    def alternate_ceil(self, width=600, height=600, margin=20):
        result, err_msg, left, right, left_top, right_top, ceil = self.find_KaiXuanMen()
        if result == False:
            print (err_msg)
            return False
        
        cc = ceil.color
        bb = left.link_color(left_top)
        self.graph.get_vertex(left_top).swap_colors(cc,bb)
        self.graph.get_vertex(right_top).swap_colors(cc,bb)
        result, err_msg, left, right, left_top, right_top, ceil = self.find_KaiXuanMen()
        if result == False:
            print (err_msg)
            return False
        kaixuanmen = (left, right, left_top, right_top, ceil)
        self.format_location(kaixuanmen, width, height, margin)
        return True

    def invert_left_xy(self):
        result, err_msg, left, right, left_top, right_top, ceil = self.find_KaiXuanMen()
        left_bottom = left.get_another_vertex(left_top)
        path = create_path(self.graph, left_top, left.link_color(left_bottom), left.link_color(left_top))
        path.swap_colors(left.link_color(left_bottom), left.link_color(left_top))

    def invert_right_xy(self):
        result, err_msg, left, right, left_top, right_top, ceil = self.find_KaiXuanMen()
        right_bottom = right.get_another_vertex(right_top)
        path = create_path(self.graph, right_top, right.link_color(right_bottom), right.link_color(right_top))
        path.swap_colors(right.link_color(right_bottom), right.link_color(right_top))

    def invert_ceil(self):
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        assert self.graph.get_link(f3, v3).color == a, "asdwhr"
        assert self.graph.get_link(f3, v2).color == b, "woeaop"
        c = 6 - a - b
        self.graph.get_edge(f0).color = b
        self.graph.get_link(f1, v1).color = c
        self.graph.get_link(f3, v2).color = c

    def invert_left_ab(self):
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        path = create_path(self.graph, v1, a, b)
        assert path.is_closed(), "invert left ab"
        path.swap_colors(a, b)

    def invert_right_ab(self):
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f3, v3).color
        b = self.graph.get_link(f3, v2).color
        path = create_path(self.graph, v2, a, b)
        assert path.is_closed(), "aweofa;weigh"
        path.swap_colors(a, b)

    def invert_left_and_right_ab(self):
        (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10) = self.vertices
        (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = self.edges
        a = self.graph.get_link(f1, v5).color
        b = self.graph.get_link(f1, v1).color
        path = create_path(self.graph, v1, a, b)
        assert path.is_closed(), "left and right"
        path.swap_colors(a, b)
        a = self.graph.get_link(f3, v3).color
        b = self.graph.get_link(f3, v2).color
        path = create_path(self.graph, v2, a, b)
        assert path.is_closed(), "aowef;aisdf left and right"
        path.swap_colors(a, b)    

    
    # old code from Guan
    def put_back(self):
        """Put a removed edge back.

        :param e1: one of the endpoint of the removed edge is on ``e1``
        :param e2: one of the endpoint of the removed edge is on ``e2``
        :param cycle: the removed edge is on this cycle
        """
        if len(self.removed) > 0:
            e1, e2, cycle = self.removed.pop()
        else:
            print ("nothing to put back")
            return

        k = len(cycle)
        colors = {1, 2, 3}
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
            if x0 < 0:
                print ("error: in put_back, edge is error")
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
            return True
        

        edge_1 = self.graph.get_edge(e1)
        edge_2 = self.graph.get_edge(e2)

        if k == 3:
            # see p2
            edge_1 = self.graph.get_edge(e1)
            edge_2 = self.graph.get_edge(e2)
        
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
            return True

        if k == 4:
            # see p3
            v2 = cycle[2]
            v1 = cycle[3]
            v5 = edge_1.get_another_vertex(v1)
            v6 = edge_2.get_another_vertex(v2)
            edge = self.graph.get_edge_by_vertices(v1, v2)
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
            return True

        if k == 5:
            # see p4
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
                x2 = self.graph.get_edge_by_vertices(v4, v5).color
                x0 = 6 - x1 - x2
                self.graph.get_edge(f0).color = x0
                self.graph.get_edge(f2).color = x1
                self.graph.get_edge(f4).color = x1
                self.graph.get_link(f1, v5).color = x1
                self.graph.get_link(f1, v1).color = x2
                self.graph.get_link(f3, v3).color = x1
                self.graph.get_link(f3, v2).color = x2
                path = create_path(self.graph, v2, x1, x2)
                path.swap_colors(x1, x2)
                if not path.is_closed(): # single cycle, fixed
                  #  logger.info('Case 0.1')
                  #  logger.info('6 [x]')
                    return
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
                #path.swap_colors(x1, x2)
                if not path.is_closed(): # single cycle, fixed
                    path.swap_colors(x1, x2)
                    #logger.info('Case 0.1')
                    #logger.info('6 [x]')
                    return

            vertices = (v1, v2, v3, v4, v5, v6, v8)
            edges = (f0, f1, f2, f3, f4)
            #logger.info('6 BEGIN')
            if not self.check_five_block(vertices, edges):
              #  logger.info('6 [0]')
                return
            if not self.convert_ab(vertices, edges):
                #logger.info('6 [1]')
                return
            #logger.info('a<->b')
            if not self.check_five_block(vertices, edges):
                #logger.info('6 [1]')
                return
            self.convert_bc(vertices, edges)
            #logger.info('b<->c')
            if not self.check_five_block(vertices, edges):
                #logger.info('6 [2]')
                return
            if not self.convert_lr(vertices, edges):
                #logger.info('6 [3]')
                return
            if not self.check_five_block(vertices, edges):
               # logger.info('6 [3]')
                return
           # logger.info('l<->r')
            self.convert_bc(vertices, edges)
           # logger.info('b<->c')
            if not self.check_five_block(vertices, edges):
              #  logger.info('6 [4]')
                return
            if not self.convert_ab(vertices, edges):
               # logger.info('6 [5]')
                return
           # logger.info('a<->b')
            if not self.check_five_block(vertices, edges):
               # logger.info('6 [5]')
                return
        raise Exception("Case not handled.")

    def check_five_block(self, vertices, edges):
        v1, v2, v3, v4, v5, v6, v8 = vertices
        f0, f1, f2, f3, f4 = edges
        v7 = filter(lambda v: not v in [v1, v4], self.graph.get_vertex(v5).neighbor_vertices)[0]
        v9 = filter(lambda v: not v in [v3, v5], self.graph.get_vertex(v4).neighbor_vertices)[0]
        v10 = filter(lambda v: not v in [v2, v4], self.graph.get_vertex(v3).neighbor_vertices)[0]
        f5 = self.graph.get_edge_by_vertices(v5, v7).id
        f6 = self.graph.get_edge_by_vertices(v4, v9).id
        f7 = self.graph.get_edge_by_vertices(v3, v10).id
        f8 = self.graph.get_edge_by_vertices(v4, v5).id
        f9 = self.graph.get_edge_by_vertices(v3, v4).id
        if self.graph.get_edge(f6).color == self.graph.get_edge(f5).color:
            x1 = self.graph.get_edge(f8).color
            x2 = self.graph.get_edge(f6).color
            path = create_path(self.graph, v5, x1, x2)
            if not path.is_closed():
                #print "path: ", path
                #print v8, v10
                return True
            else:
                x0 = 6 - x1 - x2
                path.swap_colors(x1, x2)
                self.graph.get_vertex(v3).swap_colors(x0, x2)
                self.graph.get_vertex(v4).swap_colors(x0, x2)
                self.graph.get_vertex(v5).swap_colors(x0, x2)
                return False
        elif self.graph.get_edge(f6).color == self.graph.get_edge(f7).color:
            x1 = self.graph.get_edge(f9).color
            x2 = self.graph.get_edge(f6).color
            path = create_path(self.graph, v3, x1, x2)
            if not path.is_closed():
                return True
            else:
                x0 = 6 - x1 - x2
                path.swap_colors(x1, x2)
                self.graph.get_vertex(v3).swap_colors(x0, x2)
                self.graph.get_vertex(v4).swap_colors(x0, x2)
                self.graph.get_vertex(v5).swap_colors(x0, x2)
                return False
        raise Exception("check_five_block: Case not considered.")

    def convert_lr(self, vertices, edges):
        v1, v2, v3, v4, v5, v6, v8 = vertices
        f0, f1, f2, f3, f4 = edges
        v7 = filter(lambda v: not v in [v1, v4], self.graph.get_vertex(v5).neighbor_vertices)[0]
        v9 = filter(lambda v: not v in [v3, v5], self.graph.get_vertex(v4).neighbor_vertices)[0]
        v10 = filter(lambda v: not v in [v2, v4], self.graph.get_vertex(v3).neighbor_vertices)[0]
        f5 = self.graph.get_edge_by_vertices(v5, v7).id
        f6 = self.graph.get_edge_by_vertices(v4, v9).id
        f7 = self.graph.get_edge_by_vertices(v3, v10).id
        if self.graph.get_edge(f5).color == self.graph.get_edge(f6).color:
            # l -> r
            x1 = self.graph.get_link(f1, v1).color
            x2 = self.graph.get_link(f1, v5).color
            path = create_path(self.graph, v1, x2, x1)
            path.swap_colors(x1, x2)
            if not path.is_closed():
                return False
            x0 = 6 - x1 - x2
            path = create_path(self.graph, v5, x2, x0)
            path.swap_colors(x0, x2)
            path = create_path(self.graph, v3, x2, x1)
            path.swap_colors(x1, x2)
            if not path.is_closed():
                return False
        else:
            # r -> l
            x1 = self.graph.get_link(f3, v2).color
            x2 = self.graph.get_link(f3, v3).color
            path = create_path(self.graph, v2, x2, x1)
            path.swap_colors(x1, x2)
            if not path.is_closed():
                return False
            x0 = 6 - x1 - x2
            path = create_path(self.graph, v3, x2, x0)
            path.swap_colors(x0, x2)
            path = create_path(self.graph, v3, x2, x1)
            path.swap_colors(x1, x2)
            if not path.is_closed():
                return False
        return True

    def convert_ab(self, vertices, edges):
        # invert color of two ab-cycle
        v1, v2, v3, v4, v5, v6, v8 = vertices
        f0, f1, f2, f3, f4 = edges
        x1 = self.graph.get_link(f1, v1).color
        x2 = self.graph.get_link(f1, v5).color
        path = create_path(self.graph, v1, x2, x1)
        path.swap_colors(x1, x2)
        if not path.is_closed():
            return False
        x1 = self.graph.get_link(f3, v2).color
        x2 = self.graph.get_link(f3, v3).color
        path = create_path(self.graph, v2, x2, x1)
        path.swap_colors(x1, x2)
        return True

    def convert_bc(self, vertices, edges):
        v1, v2, v3, v4, v5, v6, v8 = vertices
        f0, f1, f2, f3, f4 = edges
        v7 = filter(lambda v: not v in [v1, v4], self.graph.get_vertex(v5).neighbor_vertices)[0]
        v9 = filter(lambda v: not v in [v3, v5], self.graph.get_vertex(v4).neighbor_vertices)[0]
        v10 = filter(lambda v: not v in [v2, v4], self.graph.get_vertex(v3).neighbor_vertices)[0]
        f5 = self.graph.get_edge_by_vertices(v5, v7).id
        f6 = self.graph.get_edge_by_vertices(v4, v9).id
        if self.graph.get_edge(f5).color == self.graph.get_edge(f6).color:
            # l -> r
            x1 = self.graph.get_link(f1, v1).color
            x2 = self.graph.get_link(f1, v5).color
            x0 = 6 - x1 - x2
            f8 = self.graph.get_edge_by_vertices(v4, v5).id
            path = create_path(self.graph, v5, x0, x2)
            path.swap_colors(x0, x2)
        else:
            # r -> l
            x1 = self.graph.get_link(f3, v2).color
            x2 = self.graph.get_link(f3, v3).color
            x0 = 6 - x1 - x2
            f9 = self.graph.get_edge_by_vertices(v4, v3).id
            path = create_path(self.graph, v3, x0, x2)
            path.swap_colors(x0, x2)
        return True
