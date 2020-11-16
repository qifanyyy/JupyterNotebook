# coding=utf-8
import time

import collections
from defines import *
from algorithms import MaxFlowAlgo


class Dinica(MaxFlowAlgo):
    def __init__(self, G, n, start, finish):
        super().__init__(G, n, start, finish)
        self.p = []
        self.d = []
        self._time_start = time.time()
        self.findMaxFlow()
        self.time = time.time() - self._time_start

    def __bfs(self):
        self.d = [INF for i in range(self.n)]
        self.d[self.start] = 0
        q = collections.deque()
        q.append(self.start)
        while q:
            u = q.popleft()
            for v in range(len(self.graph[u])):
                if self.graph[u][v].flow < self.graph[u][v].cup and self.d[v] == INF:
                    self.d[v] = self.d[u] + 1
                    q.append(v)
        return self.d[self.finish] != INF

    def __dfs(self, u, flow):
        if u == self.finish or flow == 0:
            return flow
        while self.p[u] < self.n:
            v = self.p[u]
            if self.d[v] == self.d[u] + 1:
                delta = self.__dfs(v, min(flow, self.graph[u][v].cup - self.graph[u][v].flow))
                if delta:
                    self.graph[u][v].flow += delta
                    self.graph[v][u].flow -= delta
                    return delta
            self.p[u] += 1
        return 0

    def findMaxFlow(self):
        while self.__bfs():
            self.p = [0 for i in range(self.n)]
            flow = self.__dfs(self.start, INF)
            while flow != 0:
                self.maxFlow += flow
                flow = self.__dfs(self.start, INF)
        return self.maxFlow

