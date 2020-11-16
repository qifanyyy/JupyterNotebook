from typing import List, TypeVar
import math


class BellmanFordPOE:

    num2curr = {0: "chaos", 1: "exalted", 2: "fusing"}

    class POEEdge:
        """ An implementation of a graph edge that is used to determine if there are any profitable exchanges 
        in POE currency. It is able to attain this utalizing Bellman Ford Algorithm with negative cycles 
        """

        def __init__(self, u: int, v: int, w: int):
            """ A POEEdge is shows the exchange rate for two different currencies

            Args:
                param1 (int): u, the currency that is being sold or what you have
                param2 (int): v, the currency that is being bought or what you want
                param3 (int): w, the exchange rate from trading in your currency u and getting currency v
            """
            self.u = u
            self.v = v
            self.w = w

    def bellmanFord(self, edges: List[POEEdge], V: int, start: int) -> List:
        # initialize the whole list to be infinity except for start which is 0
        dist = [math.inf] * V
        dist[start] = 0

        # a bool checker to see if we need to do all v-1 loops of relaxing
        # relaxed_an_edge = True

        for i in range(V-1):
            # relaxed_an_edge = False
            for edge in edges:
                if dist[edge.u] + edge.w < dist[edge.v]:
                    dist[edge.v] = dist[edge.u] + edge.w
                    # relaxed_an_edge = True

        # we will run the algorithm a second tiem to detect any negative cyles
        # relaxed_an_edge = True
        for i in range(V-1):
            # relaxed_an_edge = False
            for edge in edges:
                if dist[edge.u] + edge.w < dist[edge.v]:
                    print(
                        f"going from {num2curr[edge.u]} to {num2curr[edge.v]} gave a neg cycle")
                    dist[edge.v] = -math.inf
                    # relaxed_an_edge = True

        return dist
