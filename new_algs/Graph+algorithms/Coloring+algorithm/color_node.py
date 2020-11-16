'''
Created on Aug 22, 2018

@author: swagatam
'''
import copy

class Color_Node:
    
    def __init__(self,state,parent):
        self.state=state
        self.parent=parent
        
    def moves(self,state1,x_cord,y_cord):
        moves=[]
        #print(x_cord,y_cord)
        state = [[i for i in row] for row in state1]
        color=state[x_cord][y_cord]
        #print(color)
        #if(x_cord==1 and y_cord==1):
        #    print(state[x_cord][y_cord])
        for i in range(1,5):
            state = [[i for i in row] for row in state1]
            if(color != i):
                state[x_cord][y_cord]=i
                #for j in range(0,len(state)):
                #    for k in range(0,len(state)):
                #        if state[j][k]==i and j !=x_cord and k !=y_cord :
                #            temp=[[m for m in row] for row in state]
                #            temp[j][k]=color
                moves.append(state)
        #print("in moves",moves)
        #if(x_cord==1 and y_cord==1):
        #    print(state[x_cord][y_cord])
        return moves
    
        
    def goal_state_check(self,state):
        flag=0
        for i in range(0,len(state)-1):
            for j in range(0,len(state)-1):
                if(state[i][j]== state[i][j+1] or state[i][j]== state[i+1][j]):
                    flag=1
                    break;
            if state[i][len(state)-1]== state[i+1][len(state)-1]:
                flag=1
                break
        for j in range(0,len(state)-1):
            if state[len(state)-1][j] == state[len(state)-1][j+1]:
                flag=1
                break
        #print(flag)
        return flag
        