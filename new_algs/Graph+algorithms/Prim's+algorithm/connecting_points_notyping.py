# Uses python3
# from __future__ import annotations
import sys
import threading
# import math
# from typing import List, Union
sys.setrecursionlimit(10 ** 9)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


class GraphNode:
    # def __init__(self, x: int, y: int, cost: float, prev: Union[GraphNode, None] = None):
    def __init__(self, x: int, y: int, cost: float, prev = None):
        self.x = x
        self.y = y
        self.cost = cost
        self.prev = prev

    def __repr__(self):
        pass
        # return f"x={self.x}; y={self.y}; cost={self.cost}; prev={self.prev}\n"


class CityGraph:
    # def __init__(self, x: List[int], y: List[y]):
    def __init__(self, x, y):
        self.nodes = []
        self.init(x, y)

    # def init(self, x: List[int], y: [int]):
    def init(self, x, y: [int]):
        for counter in range(len(x)):
            node = GraphNode(x[counter], y[counter], float("inf"), None)
            self.nodes.append(node)


class PQNode:
    # def __init__(self, key: Union[int, float], point_num: int, prev_point_num: int):
    def __init__(self, key, point_num: int, prev_point_num: int):
        self.key = key  # cost
        self.point_num = point_num
        self.prev_point_num = prev_point_num

    def __repr__(self):
        pass
        # return f"key/weight={self.key}; point_num={self.point_num}; prev_point_num={self.prev_point_num}"


class PriorityQueue:
    def __init__(self, x_array):
        self.starting_input_size = len(x_array)
        self.size = 0
        self.max_size = self.starting_input_size * self.starting_input_size + 1
        self.pq_array = []
        self.init()
        self.not_visited = set(range(self.starting_input_size))
        # self.visited = [False for __ in range(len(x_array))]  # index is Node.point_num

    def init(self):
        for counter in range(self.starting_input_size):
            # pqnode = PQNode(float("inf"), counter)
            # self.insert(pqnode)
            self.insert(float("inf"), counter, None)
            # add node to self.pqnode_array
        # print(f"size={self.size}")

    def print_pq(self):
        print(self.pq_array[:self.size])

    def parent(self, pq_array_index: int):
        return (pq_array_index - 1) // 2  # index of parent in pq_array

    def left_child(self, pq_array_index: int):
        return 2 * pq_array_index + 1  # index of left child in pq_array

    def right_child(self, pq_array_index: int):
        return 2 * pq_array_index + 2  # index of right child in pq_array

    def sift_up(self, pq_array_index: int):
        # print(f"parent(pq_array_index)={self.parent(pq_array_index)}, pq_array_index={pq_array_index}")
        while pq_array_index > 0 and \
                self.pq_array[self.parent(pq_array_index)].key > self.pq_array[pq_array_index].key:
            self.pq_array[self.parent(pq_array_index)], self.pq_array[pq_array_index] = \
                self.pq_array[pq_array_index], self.pq_array[self.parent(pq_array_index)]
            pq_array_index = self.parent(pq_array_index)

    def sift_down(self, pq_array_index: int):
        # print("SIFT_DOWN BEGIN")
        # print(f"pq_array[:self.size]={self.pq_array[:self.size]}")
        # print(f"pq_array_index={pq_array_index}")
        # print(f"self.left_child(pq_array_index)={self.left_child(pq_array_index)}")
        # print(f"self.right_child(pq_array_index)={self.right_child(pq_array_index)}")
        min_index = pq_array_index
        left_index = self.left_child(pq_array_index)
        right_index = self.right_child(pq_array_index)

        if left_index < self.size and self.pq_array[left_index].key < self.pq_array[min_index].key:
            min_index = left_index
        if right_index < self.size and self.pq_array[right_index].key < self.pq_array[min_index].key:
            min_index = right_index

        if pq_array_index != min_index:
            self.pq_array[pq_array_index], self.pq_array[min_index] = self.pq_array[min_index], self.pq_array[pq_array_index]
            self.sift_down(min_index)
        # print("SIFT_DOWN END")
        # print(f"pq_array[:self.size]={self.pq_array[:self.size]}")
        # print(f"pq_array_index={pq_array_index}")
        # print(f"self.left_child(pq_array_index)={self.left_child(pq_array_index)}")
        # print(f"self.right_child(pq_array_index)={self.right_child(pq_array_index)}")

    # def insert(self, key: Union[int, float], point_num: int, prev_point_num: Union[int, None]):
    def insert(self, key, point_num: int, prev_point_num):
        pq_node = PQNode(key, point_num, prev_point_num)
        self.insert_node(pq_node)

    def insert_node(self, pq_node: PQNode):
        # print(f"size={self.size}; max_size={self.max_size}")
        if self.size == self.max_size:
            assert False
        # print(f"PRE-APPEND{self.pq_array}")
        self.pq_array.append(pq_node)
        # print(f"POST-APPEND{self.pq_array}")
        self.size += 1
        # print(f"INSERT PRE-SIFT UP pq_array{self.pq_array[:self.size]}")
        self.sift_up(self.size - 1)
        # print(f"INSERT POST-SIFT UP pq_array{self.pq_array[:self.size]}")

    def extract_min(self) -> PQNode:
        assert self.size > 0
        # print(f"extract before loop size={self.size}")
        result = None
        while self.size > 0:
            result = self.pq_array[0]
            # print(f"result={result}")
            # print(f"extract in loop size={self.size}")
            self.pq_array[0] = self.pq_array[self.size - 1]
            self.size -= 1
            self.pq_array.pop()
            self.sift_down(0)
            # print(f"extract in loop not_visited={self.not_visited}")
            if result.point_num in self.not_visited:
                self.not_visited.remove(result.point_num)
                # print(f"after removal not_visited={self.not_visited}")
                break
            # if self.visited[result.point_num] is False:
                # self.visited[result.point_num] = True
                # break
        return result

    def remove(self, pq_array_index: int):
        if pq_array_index >= self.size:
            assert False
        self.pq_array[pq_array_index].key = float("-inf")
        self.sift_up(pq_array_index)
        self.extract_min()

    def change_priority(self, pq_array_index: int, node_key: int):
        old_node_key = self.pq_array[pq_array_index].key
        self.pq_array[pq_array_index].key = node_key
        if node_key < old_node_key:
            self.sift_up(pq_array_index)
        else:
            self.sift_down(pq_array_index)

def get_edge_weight(city_graph: CityGraph, point_num: int, other_point_num: int):
    point_a = city_graph.nodes[point_num]
    point_b = city_graph.nodes[other_point_num]
    a_x = point_a.x
    a_y = point_a.y
    b_x = point_b.x
    b_y = point_b.y
    x_diff = a_x - b_x
    y_diff = a_y - b_y
    square_sum = x_diff * x_diff + y_diff * y_diff
    return square_sum ** 0.5


def minimum_distance(x, y) -> float:
    # result = 0.

    # print(f"x: {x}")
    # print(f"y: {y}")

    city_graph = CityGraph(x, y)

    # print(f"city_graph.nodes\n{city_graph.nodes}")

    pq = PriorityQueue(x)

    # print(f"PRE-INSERT of zero cost node 0 pq_array={pq.pq_array}")
    # print(pq.pq_array)

    city_graph.nodes[0].cost = 0
    pq.insert(0, 0, None)
    # print(f"POST-INSERT of zero cost node 0 pq_array={pq.pq_array}")

    # print(pq.pq_array)
    cum_cost = 0.0

    while len(pq.not_visited) > 0:
        # print("PRE-EXTRACT")
        # pq.print_pq()
        # print(f"pq.not_visited={pq.not_visited}")
        pq_node = pq.extract_min()
        # print("POST-EXTRACT")
        # pq.print_pq()
        # print(f"pq.not_visited={pq.not_visited}")
        pq_point_num = pq_node.point_num
        # print(f"pq_point_num={pq_point_num}; key/weight={pq_node.key}")
        cum_cost += pq_node.key
        if cum_cost == float("inf"):
            assert False
        # print(f"cum_cost={cum_cost}")
        for other_pq_point_num in pq.not_visited:
            edge_weight = get_edge_weight(city_graph, pq_point_num, other_pq_point_num)
            # print(f"other_pq_point_num={other_pq_point_num}; edge_weight={edge_weight}")
            # print(f"PRE-PRIORITY CHANGE city_graph.nodes={city_graph.nodes}")
            if city_graph.nodes[other_pq_point_num].cost > edge_weight:
                city_graph.nodes[other_pq_point_num].cost = edge_weight
                city_graph.nodes[other_pq_point_num].prev = pq_point_num
                pq.insert(edge_weight, other_pq_point_num, pq_point_num)
            # print(f"POST-PRIORITY CHANGE city_graph.nodes={city_graph.nodes}")


    return cum_cost

def main():
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))

if __name__ == '__main__':
    main()