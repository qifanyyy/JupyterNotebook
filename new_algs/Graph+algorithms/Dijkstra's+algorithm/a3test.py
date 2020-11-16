from a3 import *

assert dijkstra([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],0) == [0,5,3,8,9], "Dijkstra ERROR"
assert dijkstra([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],1) == [float("inf"),0,float("inf"),3,float("inf")], "Dijkstra ERROR"
assert dijkstra([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],2) == [float("inf"),2,0,5,6], "Dijkstra ERROR"
assert dijkstra([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],3) == [float("inf"),float("inf"),float("inf"),0,float("inf")], "Dijkstra ERROR"
assert dijkstra([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],4) == [float("inf"),float("inf"),float("inf"),1,0], "Dijkstra ERROR"



assert bfs([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],0) == [0,5,3,8,9], "BFS ERROR"
assert bfs([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],1) == [float("inf"),0,float("inf"),3,float("inf")], "BFS ERROR"
assert bfs([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],2) == [float("inf"),2,0,5,6], "BFS ERROR"
assert bfs([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],3) == [float("inf"),float("inf"),float("inf"),0,float("inf")], "BFS ERROR"
assert bfs([[[1, 2], [3], [1, 3, 4], [], [3]],[[5, 3], [3], [2, 5, 6], [], [1]]],4) == [float("inf"),float("inf"),float("inf"),1,0], "BFS ERROR"