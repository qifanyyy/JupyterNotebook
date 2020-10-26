import random
import json
import itertools
from subprocess import Popen, PIPE

from common.path import create_path
from common.multigraph import MultiGraph
from common.storage import failed_graph_DB
from four_color.ComplexEdgeColoring import EdgeColoring


class SnarkComponent(object):
    
    def find_petersen_subdivision(self):
        if not hasattr(self, 'left_p'):
            if not self.find_two_cycle():
                print "not has two cycles"
                return False

        left_list = []
        for x in self.left_p:
            left_list.append(x)

        right_list = []
        for x in self.right_p:
            right_list.append(x)

        print "left_list and right_list: "
        print left_list
        print right_list

        edge_set = list()

        for x in self.left_p:
            for y in self.right_p:
                if self.graph.multiplicity(x, y) > 0:
                    edge_set.append((x, y))
        
        for com in itertools.combinations(edge_set, 5):
            per = dict()
            for x in com:
                per[left_list.index(x[0])] = right_list.index(x[1])
            if self.check_petersen_permutation(per):
                print "petersen: ", com
                data = self.prepare_highlight_data([self.left_p, self.right_p], list(com))
                #print data
                return data

        return False

    def check_petersen_permutation(self, pa):
        if len(pa) != 5:
            return False
        petersen1 = {1:1, 2:3, 3:5, 4:2, 5:4}
        petersen2 = {1:1, 2:4, 3:2, 4:5, 5:3}
        if self.check_same_permutation(pa, petersen1):
            return True
        if self.check_same_permutation(pa, petersen2):
            return True

        return False

    def check_same_permutation(self, pa, pb):
        # pa and pb are both dict()
        len_a = len(pa)
        len_b = len(pb)
        if len_a != len_b:
            return False
        length = len_a
            
        a_key = list()
        a_value = list()
        for x in pa:
            a_key.append(x)
            a_value.append(pa[x])
        a_key.sort()
        a_value.sort()

        b_key = list()
        b_value = list()
        for x in pb:
            b_key.append(x)
            b_value.append(pb[x])
        b_key.sort()
        b_value.sort()
        
        for i in range(0, length, 1):
            a_index = a_value.index(pa[a_key[i]])
            b_index = b_value.index(pb[b_key[i]])
            if a_index != b_index:
                return False

        return True
      
    def check_critical(self):
        checked = []
        while True:
            edge = None
            for e in self.graph.edges:
                (a, b) = e.get_endpoints()
                if ((a, b) not in checked) and ((b, a) not in checked):
                    edge = e
                    break
            if edge == None:
                break
            checked.append(edge.get_endpoints())
            self.remove_specified_edge(edge)
            if not self.edge_coloring():
                print "edge: ", edge.get_endpoints(), " not critical"
            self.putback_for_specified_edge()
