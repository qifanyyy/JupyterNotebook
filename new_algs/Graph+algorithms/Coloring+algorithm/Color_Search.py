'''
Created on Aug 22, 2018

@author: swagatam
'''
from Color_bfs import color_bfs
from Color_bfs import color_dfs


import random

print("enter the matrix dimension")
n=int(input())
print("enter 1 for BFS 2 for DFS")
c=int(input())
initial_state=[]
for  i in range(0,n):
    l=[]
    for j in range(0,n):
        l.append(random.randint(1,4))
    initial_state.append(l)

#print(initial_state)
#initial_state=[[1,2,2],[1,1,2],[1,1,2]]
#initial_State= [[3, 1, 4, 4], [1, 1, 1, 3], [2, 1, 4, 4], [1, 2, 3, 4]]
#initial_state=[[4, 2, 1, 3, 2], [4, 1, 3, 2, 4], [2, 3, 3, 2, 4], [1, 4, 2, 3, 4], [2, 2, 4, 1, 2]]
#print(len(initial_state))
#initial_state=[[3, 3, 4, 2, 1, 4, 1], [1, 3, 1, 2, 3, 1, 3], [2, 4, 3, 2, 3, 1, 4], [2, 4, 1, 3, 1, 2, 3], [3, 1, 2, 1, 3, 4, 4], [1, 2, 3, 1, 1, 2, 2], [2, 4, 2, 2, 2, 1, 4]]
#initial_state=[[3, 4, 1, 3, 2, 3], [2, 1, 1, 2, 4, 1], [3, 4, 3, 3, 2, 3], [2, 3, 4, 2, 2, 2], [1, 1, 4, 2, 1, 2], [2, 4, 4, 3, 4, 3]]
if c==1:
    color_bfs(initial_state)
else:
    color_dfs(initial_state)