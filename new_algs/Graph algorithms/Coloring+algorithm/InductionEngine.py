from common.storage import failed_graph_DB
from common.multigraph import MultiGraph

        
from four_color.P_matching_component import MatchingComponent
from four_color.common_component import CommonComponent
from four_color.cycles_component import InductionComponent
from four_color.layout_component import LayoutComponent

class InductionEngine(InductionComponent, MatchingComponent, CommonComponent, LayoutComponent):
    """
        Edge coloring algorithm by induction.
    """

    def __init__(self, graph):
        '''
            states list: initial, proper, petersen, unknown
        '''
        self.graph = graph
        self.removed = []
        self.removed_info = []
        self.state = "initial"
    
    def test_vertex_edge_merge(self, round):
        from four_color.GraphMerger import GraphMerger
        temp = self.graph
        content = self.graph.to_json()
        g1 = MultiGraph.from_json(content)
        g2 = MultiGraph.from_json(content)
        while round > 0:
            (g, elist) = GraphMerger.single_vertex_and_edge_merge(g1, g2)
            
            self.graph = g


            for eid in elist:
                xx, yy = eid
                edge = self.graph.get_edge_by_endpoints(xx, yy)
                self.remove_specified_edge(edge)

                if not self.edge_coloring():
                    raise Exception("Can not 3 coloring the induced graph")
                assert self.graph.num_errors == 0

                self.putback_the_last_deleted_edge(True)

                if not self.bicycle_algorithm():
                    xxx = edge.get_endpoints()
                    print "remove: ", xxx
                    failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
                    raise Exception("bicycle_algorithm not work!")
                
                assert self.graph.num_errors == 0
            
            round -= 1

    def test_merge_1(self, round):
        from four_color.GraphMerger import GraphMerger
        temp = self.graph
        content = self.graph.to_json()
        g1 = MultiGraph.from_json(content)
        g2 = MultiGraph.from_json(content)
        
        while round > 0:
            (g, elist) = GraphMerger.single_vertex_merge(g1, g2)
            self.graph = g
            for eid in elist:
                edge = self.graph.get_edge(eid)
                self.remove_specified_edge(edge)

                if not self.edge_coloring():
                    raise Exception("Can not 3 coloring the induced graph")
                assert self.graph.num_errors == 0

                self.putback_the_last_deleted_edge(True)

                if not self.bicycle_algorithm():
                    failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
                    raise Exception("bicycle_algorithm not work!")
                
                assert self.graph.num_errors == 0
            
            round -= 1

    def test_merge(self, round):
        from four_color.GraphMerger import GraphMerger
        temp = self.graph
        content = self.graph.to_json()
        g1 = MultiGraph.from_json(content)
        g2 = MultiGraph.from_json(content)
        
        while round > 0:
            (g, elist) = GraphMerger.single_vertex_merge(g1, g2)
            self.graph = g
            self.remove_edge_on_girth()
            
            if not self.edge_coloring():
                raise Exception("Can not 3 coloring the induced graph")
            assert self.graph.num_errors == 0

            self.putback_the_last_deleted_edge(True)

            if not self.bicycle_algorithm():
                failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
                raise Exception("bicycle_algorithm not work!")
            
            assert self.graph.num_errors == 0
            
            round -= 1


    def add_to_db(self):
        failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
        
    def test_main(self, round):
        while round > 0:
            if self.edge_coloring_by_perfect_matching():
                cycs = self.find_locking_cycles()
                if len(cycs) == 2:
                    if not self.bicycle_algorithm():
                        failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
                        raise Exception("bicycle_algorithm not work!")
                    
                    assert self.graph.num_errors == 0

            round -= 1

    def case_test(self, round):
        while round > 0:
            
            self.remove_edge_on_girth()
            #temp = self.graph.random_pick_a_edge()
            #self.remove_specified_edge(temp)
            
            if not self.edge_coloring():
                raise Exception("Can not 3 coloring the induced graph")
            assert self.graph.num_errors == 0

            self.putback_the_last_deleted_edge(True)

            if not self.bicycle_algorithm():
                failed_graph_DB.add_graph(self.graph.name,self.graph.to_json())
                raise Exception("bicycle_algorithm not work!")
            
            assert self.graph.num_errors == 0
            
            round -= 1


    def stat_test(self, rnd):
        count = 0
        sums = 0
        direct = 0
        total_rnd = rnd
        
        while rnd > 0:
            
            self.remove_edge_on_girth()
            #temp = self.graph.random_pick_a_edge()
            #self.remove_specified_edge(temp)
            
            if not self.edge_coloring():
                raise Exception("Can not 3 coloring the induced graph")
            assert self.graph.num_errors == 0

            self.putback_the_last_deleted_edge(True)

            # count the resolutions
            a = self.count_solutions()
            if a == False:
                print "some thing wrong"
                raise
            if a != -1:
                count += 1
                sums += a
            elif a == -1:
                direct = direct + 1

            rnd -= 1

        direct_rate = float(direct) / total_rnd
        
        if count != 0:
            tt = round(float(sums)/count * 100, 2)
        else:
            tt = "NA"
        return (direct_rate, tt)
