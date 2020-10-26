from sys import *
from numpy import *
import trackback
objec = trackback.matchSeq()
cols=objec.col
rows=objec.obj.rows
class graphFunc:
  
    print(objec.gap)
    def make_graph():
        cols=objec.col
        graph = {}
        for i in range(1, cols)[::-1]:
            graph[(i, 0)] = [(i-1, 0)]
            graph[(0, i)] = [(0, i-1)]
            for j in range(1, cols)[::-1]:
                graph[(i, j)] = []
                objec.score = objec.obj.a[i][j]
                objec.score_diag = objec.obj.a[i-1][j-1]
                objec.score_up = objec.obj.a[i][j-1]
                objec.score_left = objec.obj.a[i-1][j]
                if objec.score == objec.score_diag + objec.s[objec.obj.seq1[i-1] + objec.obj.seq2[j-1]]:
                    graph[(i, j)] += [(i-1, j-1)]
                if objec.score == objec.score_left + objec.gap:
                    graph[(i, j)] += [(i-1, j)]
                if objec.score == objec.score_up + objec.gap:
                    graph[(i, j)] += [(i, j-1)]
        return graph
    #back tracking algorithm 
    def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.__contains__(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    graph = make_graph()
    tracks = find_all_paths(graph, (cols-1, rows-1), (0, 0))
    baseqs1 = []
    baseqs2 = []
    for track in tracks:
        baseq1 = ''
        baseq2 = ''
        last_step = (objec.obj.cols-1, objec.obj.rows-1)
        for step in track:
            i, j = last_step
            if i == step[0]:
                baseq1 = '_' + baseq1
                baseq2 = objec.obj.seq2[j-1] + baseq2
            elif j == objec.obj.step[1]:
                baseq1 = objec.obj.seq1[i-1] + baseq1
                baseq2 = '_' + baseq2
            else:
                baseq1 = objec.obj.seq1[i-1] + baseq1
                baseq2 = objec.obj.seq2[j-1] + baseq2

            last_step = step
        baseqs1 += [baseq1]
        baseqs2 += [baseq2]
