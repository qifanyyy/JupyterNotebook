'''
Created on Aug 22, 2018

@author: swagatam
'''
import Node
import Searches
from Searches import bfs
from Searches import dfs
from Searches import astar
from Searches import idastar
#enter the input n/2 * n/2 format format with 0 for space
n=input("enter the value for n:")
n=int(n)
print("enter the input n/2 * n/2 format format with 0 for space")
initial=input().split()
initial=[int(i) for i in initial]
#print(initial)
goal=[]
for i in range(1,n+1):
    goal.append(i)
goal.append(0)
bfs(initial, goal)
dfs(initial, goal)
astar(initial,goal)
idastar(initial,goal)
#Searches.bfs(initial,goal)
