'''
@author-name: Rishab Katta

Ford Fulkerson Max Flow Algorithm applied to Hospital Blood Supply-Demand Problem.
'''

import sys


class BloodSupplyDemand:

    def __init__(self, adj_matrix):
        self.dir_graph = adj_matrix
        self.matrix_row = len(self.dir_graph)
        self.matrix_col = len(self.dir_graph[0])

    def Breadth_First_Search(self, source, sink, parent_list):
        '''
        Returns True if there is a path from source to sink.
        :param source: starting point in the graph
        :param sink: ending point in the graph
        :param parent_list: array containing parents of nodes in the graph. used to store path.
        :return: True or False.
        '''

        visited_set = [False]*self.matrix_row #initially all vertices are not visited.
        bfs_queue=[]
        visited_set[source] = True
        bfs_queue.append(source)
        while len(bfs_queue)!=0:
            node = bfs_queue.pop(0)
            for index, value in enumerate(self.dir_graph[node]):
                if value>0 and visited_set[index]==False:
                    bfs_queue.append(index)
                    visited_set[index] = True
                    parent_list[index] = node
        if visited_set[sink]==True:
            return True
        return False
    def Ford_Fulkerson(self, source, sink):
        '''
        Ford Fulkerson Algorithm to determine max flow in a network.
        :param source: source node in the graph
        :param sink: sink node in the graph.
        :return: max flow in the graph.
        '''

        parent_list=[-1]*self.matrix_row
        max_flow = 0                    #initialize the max flow to 0.
        while self.Breadth_First_Search(source,sink,parent_list):
            current_flow = sys.maxsize
            s=sink
            while(s!=source):
                current_flow = min(current_flow, self.dir_graph[parent_list[s]][s])
                s=parent_list[s]
            max_flow +=current_flow
            v=sink
            while(v!=source):
                u = parent_list[v]
                self.dir_graph[u][v] = self.dir_graph[u][v] - current_flow
                self.dir_graph[v][u] = self.dir_graph[v][u] + current_flow
                v=parent_list[v]

        print(" ")
        print("The residual graph represented by the adjacency matrix: ")
        print(" ")
        for i in range(len(self.dir_graph)):
            print(self.dir_graph[i])
        print(" ")
        return max_flow



if __name__ == '__main__':
    i = sys.maxsize
    adj_matrix = [[0, 50, 36, 11, 8, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, i, i, i, i, 0],
                  [0, 0, 0, 0, 0, 0, i, 0, i, 0],
                  [0, 0, 0, 0, 0, 0, 0, i, i, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, i, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 45],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 42],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    bsd = BloodSupplyDemand(adj_matrix)
    source = 0
    sink = 9
    mf =bsd.Ford_Fulkerson(source, sink)
    print("The maximum flow in the given network is %d " %mf )






