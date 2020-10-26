import random
import logging
import sys
import copy
import json
import itertools
import pydot
import tempfile
from subprocess import Popen, PIPE

from common.path import create_path
from common.multigraph import MultiGraph
from four_color.ComplexEdgeColoring import EdgeColoring


class LayoutComponent(object):
    
    def clear_state_data(self):
        pass

    def layout(self, width=600, height=600, margin=20):
        colors = ['red', 'green', 'blue', 'orange', 'cyan']

        def write_graph(g, f):
            graph = pydot.Dot(graph_type='graph')
            graph.set_prog('neato')
            node = pydot.Node()
            node.set_name('node')
            node.set('shape', 'point')
            graph.add_node(node)

            for e in g.edges:
                (l1, l2) = e.links
                (v1, v2) = e.vertices
                edge = pydot.Edge(str(v1.id), str(v2.id))
                if not e.is_error():
                    edge.set('color', colors[l1.color])
                graph.add_edge(edge)
            f.write(graph.to_string())

        def find_neato():
            cmds = pydot.find_graphviz()
            if cmds is not None:
                if cmds.has_key('neato'):
                    return cmds['neato']

        self.graph._positions = {}
        f = tempfile.NamedTemporaryFile(delete=False)
        write_graph(self.graph, f)
        f.close()
        filename = f.name

        neato_cmd = find_neato()
        if neato_cmd is None:
            logging.error('cannot find neato')
            raise Exception('cannot find neato, check graphviz installation')

        s = Popen([neato_cmd, '-Gepsilon=0.001', filename], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0]
        layout_f = tempfile.NamedTemporaryFile(delete=False)
        layout_f.write(s)
        layout_f.close()
        g = pydot.graph_from_dot_file(layout_f.name)

        vertices = []
        w = width - margin * 2.0
        h = height - margin * 2.0
        ratio = 1
        for v in g.get_nodes():
            name = v.get_name()
            if name == 'graph':
                if v.get_attributes().has_key('bb'):
                    bb = v.get_attributes()['bb']
                    bb = bb[1:-1].split(',')
                    w = float(bb[2])
                    h = float(bb[3])
                    ratio = min((width - margin * 2) / w, (height - margin * 2) / h)
            try:
                if int(name) > 0:
                    pos = v.get_pos()
                    xy = pos[1:-1].split(',')
                    x = float(xy[0])
                    y = float(xy[1])
                    vertices.append({'x': x, 'y': y, 'name': name})
            except:
                pass

        for vertex in vertices:
            x = int(vertex['x'] * ratio + margin)
            y = int(vertex['y'] * ratio + margin)
            v_id = int(vertex['name'])
            self.graph._positions[v_id] = (x, y)

############## state: two cycles ##################################
    def bicycle_layout(self, width=600, height=600, margin=20):
        if not hasattr(self, 'state') or self.state != "two cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "two cycles"
                self.left_p, self.right_p = cycles

        left_top = self.left_p.begin
        right_top = self.right_p.begin
        radius = width * 0.6
        import math
        rad = 2 * math.asin( 0.5 * float(height - 2 * margin) / radius )
        
        for index in range(0, len(self.left_p), 1):
            p_rad = index * rad / (len(self.left_p)-1)
            p_y = margin + (height - 2 * margin) / 2 - math.sin(rad / 2 - p_rad) * radius
            p_x = margin + math.cos(rad /2 - p_rad) * radius - math.cos(rad / 2) * radius
            self.graph._positions[self.left_p._vertices[index]] = (p_x, p_y)
       
        for index in range(0, len(self.right_p), 1):
            p_rad = index * rad / (len(self.right_p)-1)
            p_y = margin + (height - 2 * margin) /2 - math.sin(rad / 2 - p_rad) * radius
            p_x = width - margin - (math.cos(rad / 2 - p_rad) * radius - math.cos(rad / 2) * radius)
            self.graph._positions[self.right_p._vertices[index]] = (p_x, p_y)

        color_a = self.left_p.c1
        color_b = self.left_p.c2

        other_vertices = []
        for vertex in self.graph._vertices:
            if (vertex not in self.left_p) and (vertex not in self.right_p):
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
                x = x0 + math.cos(j * step_angle) * (width - 2 * margin)/6
                y = y0 + math.sin(j * step_angle) * (width - 2 * margin)/6
                self.graph._positions[cycle[i][j]] = (x,y)

        return True

    def move_left(self):
        if not hasattr(self, 'state') or self.state != "two cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "two cycles"
                self.left_p, self.right_p = cycles
    
        self.left_p.move_one_step()
    
    def back_left(self):
        if not hasattr(self, 'state') or self.state != "two cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "two cycles"
                self.left_p, self.right_p = cycles
    
        self.left_p.move_steps(-1)
         
    def move_right(self):
        if not hasattr(self, 'state') or self.state != "two cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "two cycles"
                self.left_p, self.right_p = cycles
        
        self.right_p.move_one_step()

    def back_right(self):
        if not hasattr(self, 'state') or self.state != "two cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "two cycles"
                self.left_p, self.right_p = cycles
        
        self.right_p.move_steps(-1)

############## state: ac cycles ###################################       
    def highlight_ac_cycles(self):
        if not hasattr(self, 'state') or self.state != "ac cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "ac cycles"
                left, right = cycles
                if left.c1 == 2:
                    path_ac = create_path(self.graph, left.begin, 3, 1)
                else:
                    path_ac = create_path(self.graph, left.end, 3, 1)

                v_ac = []
                for v in self.graph.vertices:
                    if v.id not in path_ac:
                        v_ac.append(v.id)

                self.ac_cycles = self.factor_cycle(v_ac, 1, 3)
        
        
        self.highlighted = []
        if len(self.ac_cycles) > 0:
            self.highlighted.append(self.ac_cycles[0])
            self.ac_cycles = self.ac_cycles[1:] + self.ac_cycles[0:1]
        
        return self.prepare_highlight_data()

############## state: bc cycles ###################################       
    def highlight_bc_cycles(self):
        if not hasattr(self, 'state') or self.state != "bc cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "bc cycles"
                left, right = cycles
                if left.c1 == 1:
                    path_bc = create_path(self.graph, left.begin, 3, 2)
                else:
                    path_bc = create_path(self.graph, left.end, 3, 2)

                v_bc = []
                for v in self.graph.vertices:
                    if v.id not in path_bc:
                        v_bc.append(v.id)

                self.bc_cycles = self.factor_cycle(v_bc, 2, 3)
        
        self.highlighted = []
        if len(self.bc_cycles) > 0:
            self.highlighted.append(self.bc_cycles[0])
            self.bc_cycles = self.bc_cycles[1:] + self.bc_cycles[0:1]
        
        return self.prepare_highlight_data()

############## state: ab cycles #################################### 
    def highlight_ab_cycles(self):
        if not hasattr(self, 'state') or self.state != "ab cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "ab cycles"
                left, right = cycles
                
                v_ab = []
                for v in self.graph.vertices:
                    if v.id not in left and v.id not in right:
                        v_ab.append(v.id)

                self.ab_cycles = self.factor_cycle(v_ab, 1, 2)
        
        self.highlighted = []
        if len(self.ab_cycles) > 0:
            self.highlighted.append(self.ab_cycles[0])
            self.ab_cycles = self.ab_cycles[1:] + self.ab_cycles[0:1]
        
        return self.prepare_highlight_data()

############## state: locking cycles ###############################
    def highlight_two_locking_cycles(self):
        if not hasattr(self, 'state') or self.state != "locking cycles":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "locking cycles"
                self.locking_cycles = cycles
        
        self.highlighted = self.locking_cycles
        return self.prepare_highlight_data()

############## state: exclusive chain #################################
    def highlight_ac_exclusive_chain(self):
        if not hasattr(self, 'state') or self.state != "exclusive chain":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "exclusive chain"
                if cycles[0].c1 == 1:
                    self.ac_chain = create_path(self.graph, cycles[0].end, 3, 1)
                    self.bc_chain = create_path(self.graph, cycles[0].begin, 3, 2)
                else:
                    self.ac_chain = create_path(self.graph, cycles[0].begin, 3, 1)
                    self.bc_chain = create_path(self.graph, cycles[0].end, 3, 2)
        
        self.highlighted = [self.ac_chain]
        return self.prepare_highlight_data()
    
    def highlight_bc_exclusive_chain(self):
        if not hasattr(self, 'state') or self.state != "exclusive chain":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "exclusive chain"
                if cycles[0].c1 == 1:
                    self.ac_chain = create_path(self.graph, cycles[0].end, 3, 1)
                    self.bc_chain = create_path(self.graph, cycles[0].begin, 3, 2)
                else:
                    self.ac_chain = create_path(self.graph, cycles[0].begin, 3, 1)
                    self.bc_chain = create_path(self.graph, cycles[0].end, 3, 2)
        
        self.highlighted = [self.bc_chain]
        return self.prepare_highlight_data()


############## state: deleted ##############################
    def delete_a_in_even_ab_cycles(self):
        if not hasattr(self, 'state') or self.state != "deleted":
            cycles = self.find_two_cycle()
            if cycles == None:
                print "not has two cycles"
                return False
            else:
                self.state = "deleted"
                left, right = cycles
                
                v_ab = []
                for v in self.graph.vertices:
                    if v.id not in left and v.id not in right:
                        v_ab.append(v.id)

                ab_cycles = self.factor_cycle(v_ab, 1, 2)
                deleted = []
                for p in ab_cycles:
                    for e in p.edges:
                        if e.color == 1:
                            deleted.append(e)
                
                for e in deleted:
                    self.graph.remove_edge(e.id)


    def highlight_pentagon(self):
        self.state = "girth"
        self.highlighted = []

        results = self.find_girth()
        data = {}
        data['vertices'] = results[1]
        temp = results[0]
        data['edges'] = []
        for eid in temp:
            edge = self.graph.get_edge(eid)
            (a, b) = edge.get_endpoints()
            data['edges'].append({
                'v1': a,
                'v2': b,
                'h1': True,
                'h2': True,
                })
        return data
    
    def invert_highlighted(self):
        if hasattr(self,'highlighted'):
            
            for path in self.highlighted:
                path.invert_colors()
            
            return self.prepare_highlight_data()


    def check_resolvable(self):
        errors = []
        for edge in self.graph.errors:
            errors.append(edge)
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
        
        if (la + lb) != (ra + rb):
            print "Two variable not same, return false"
            return False

        path_1 = create_path(self.graph, v1, lb, la)
        if path_1.is_closed() != True:
            print "Two variables are connected!"
            return True
        
        return self._sub_routine_for_resolve(path_1)

    def count_resolve(self):
        errors = []
        for edge in self.graph.errors:
            errors.append(edge)
        if len(errors) != 2:
            print "errors not equal 2, return false"
            return 

        left = errors[0]
        right = errors[1]
        (v1, v2) = left.get_endpoints()
        (v3, v4) = right.get_endpoints()
        la = left.link_color(v1)
        lb = left.link_color(v2)
        ra = right.link_color(v3)
        rb = right.link_color(v4)
        
        if la + lb != ra + rb:
            print "Two variable not same, return false"
            return

        left_p = create_path(self.graph, v1, lb, la)
        if left_p.is_closed() != True:
            print "Error: Two variables are connected!"
            return
        right_p = create_path(self.graph, v3, rb, ra)

        count = 0

        for i in range(0, 2 * len(left_p)):
            for j in range(0, 2 * len(right_p)):
                if self._sub_routine_for_resolve(left_p):
                    count = count + 1
                right_p.move_one_step()
            left_p.move_one_step()
        
        print "Total: ", 4, "*", len(left_p), "*", len(right_p),
        print " = ", 4 * len(left_p) * len(right_p)
        print "Solution #: ", count
        

    def count_resolve_with_even_ab(self):
        cycles = self.find_two_cycle()
        if cycles == None:
            print "not has two cycles"
            return False
        else:
            left, right = cycles
            v_ab = []
            for v in self.graph.vertices:
                if v.id not in left and v.id not in right:
                    v_ab.append(v.id)

            ab_cycles = self.factor_cycle(v_ab, 1, 2)
            self._sub_routine_for_count_resolve(ab_cycles)

    def _sub_routine_for_count_resolve(self, cycles):
        if len(cycles) == 0:
            self.count_resolve()
        else:
            cyc = cycles.pop()
            self._sub_routine_for_count_resolve(cycles)
            cyc.invert_colors()
            self._sub_routine_for_count_resolve(cycles)
            cyc.invert_colors()
            cycles.append(cyc)
    
        
    def _sub_routine_for_resolve(self, path1):
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



