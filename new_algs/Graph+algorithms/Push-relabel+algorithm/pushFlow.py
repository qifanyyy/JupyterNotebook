import time

from algorithms import MaxFlowAlgo


class PushFlow(MaxFlowAlgo):

    def __init__(self, G, n, start, finish):
        super().__init__(G, n, start, finish)
        self.high = [0 for _ in range(n)]
        self.e = [0 for _ in range(n)]
        for i in range(0, self.n):
            self.graph[0][i].flow = self.graph[0][i].cup
            self.graph[i][0].flow = -self.graph[0][i].cup
            self.e[i] = self.graph[0][i].cup
            self.e[0] -= self.graph[0][i].cup
        self.high[0] = self.n
        self._time_start = time.time()
        self.findMaxFlow()
        self.time = time.time() - self._time_start

    def __push(self, u, v):
        d = min(self.e[u], self.graph[u][v].cup - self.graph[u][v].flow)
        self.graph[u][v].flow += d
        self.graph[v][u].flow = -self.graph[u][v].flow
        self.e[u] -= d
        self.e[v] += d

    def findMaxFlow(self):

        n = self.n
        while True:
            v = n
            for i in range(n - 1):
                if self.e[i] > 0:
                    v = i
                    break

            if v == n:
                break

            while self.e[v]:
                for i in range(0, n):
                    if self.graph[v][i].cup > self.graph[v][i].flow and self.high[v] > self.high[i]:
                        self.__push(v, i)

                if self.e[v] > 0:
                    self.high[v] += 1

        self.maxFlow = self.e[n - 1]
        return self.maxFlow
