'''
Created on Aug 22, 2018

@author: swagatam
'''
from math import floor
from math import sqrt

class Node:
    
    def __init__(self,state,parent,move,heuristic=None):
        self.state=state
        self.parent=parent
        self.move=move
        self.heuristic=heuristic
    
    def left(self,state1):
        state=state1.copy()
        pos=state.index(0)
        temp=int(pos%sqrt(len(state)))
        state[pos]=state[pos-1]
        state[pos-1]=0
        return state
    
    def right(self,state1):
        state=state1.copy()
        pos=state.index(0)
        #print("befor right",state)
        #temp=int(pos%sqrt(len(state)))
        state[pos]=state[pos+1]
        state[pos+1]=0
        #print("right",state)
        return state
        
    def up(self,state1):
        state=state1.copy()
        pos=state.index(0)
        #temp=int(floor(pos/sqrt(len(state))))
        state[pos]=state[pos-int(sqrt(len(state)))]
        state[pos-int(sqrt(len(state)))]=0
        return state
    
    def down(self,state1):
        state=state1.copy()
        pos=state.index(0)
        #temp=int(pos/sqrt(len(state)))
        #print("before down",state)
        #print("down var ",slen(state)))
        state[pos]=state[pos+int(sqrt(len(state)))]
        state[pos+int(sqrt(len(state)))]=0
        #print("down",state)
        return state
    
    
    def calculate_misplaced_tiles(self,initial,current):
        misplace=0
        for i in range(0,len(initial)):
            if initial[i] != current[i]:
                misplace=misplace+1
        return misplace
    
    def moves(self,node):
        moves=[]
        pos=0
        state=node.state
        pos=state.index(0)
        if int(pos/sqrt(len(node.state)))!=int(sqrt(len(node.state)))-1:
            t=int(pos/sqrt(len(node.state)))
            moves.append("down")
        if int(pos/sqrt(len(node.state)))!=0:
            moves.append("up")
        if pos%int(sqrt(len(node.state)))!=int(sqrt(len(node.state)))-1:
            moves.append("right")
        if pos%int(sqrt(len(node.state)))!=0:
            moves.append("left")
        return moves
        