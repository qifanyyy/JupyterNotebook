import string
import fileinput
from heapq import heappush, heappop


class Graph:
  def __init__(self):
    lines = open('dict.txt').read().splitlines()
    self.dictionary = set(lines)
    self.graph = self.create_graph()

    for line in fileinput.input():
      split = line.split()
      start, target = split[0], split[1]
      print(self.dijkstra(start, target))

  def create_graph(self):
    graph = {}
    for element in self.dictionary:
      node = graph[element] = []
      self.insert(element, node)
      self.delete(element, node)
      self.twiddle(element, node)
      self.reversal(element, node)
    return graph

  def insert(self, word, node):
    for i in range(len(word) + 1):
      for j in string.ascii_lowercase:
        s = word[:i] + j + word[i:]
        if s in self.dictionary and s != word:
          node.append((1, s))

  def delete(self, word, node):
    for i in range(len(word)):
      s = word[:i] + word[(i+1):]
      if s in self.dictionary and s != word:
        node.append((3, s))

  def twiddle(self, word, node):
    for i in range(len(word) - 1):
      s = self.swap(word, i, i+1)
      if s in self.dictionary and s != word:
        node.append((2, s))

  def swap(self, s, i, j):
    temp = list(s)
    temp[i], temp[j] = temp[j], temp[i]
    return ''.join(temp)

  def reversal(self, word, node):
    reversed_word = word[::-1]
    if reversed_word in self.dictionary and word != reversed_word:
      node.append((len(word), reversed_word))

  def dijkstra(self, start, target):
    visited = set()
    distance = {start: 0}
    pq = [(0, start, '')]
    
    while pq:
      current_min = heappop(pq)
      dist, u, path = current_min
      if u in visited: continue
      path += u + ' '
      visited.add(u)
      if target == u:
        retval = str(dist) + ' ' + path
        return(retval[:-1])

      neighbors = self.graph.get(u, [])
      for neighbor in neighbors:
        delta, v = neighbor
        if v in visited: continue
        newdist = dist + delta
        if not distance.get(v) or distance[v] > newdist:
          distance[v] = newdist
          # Instead of decrease-key:
          # Using insert instead of decrease-key has
          # negligble effect on the performance of the 
          # algorithm, as studied in this paper:
          # http://www3.cs.stonybrook.edu/~rezaul/papers/TR-07-54.pdf
          heappush(pq, (newdist, v, path))
    return -1

Graph()
