'''
Created on Aug 22, 2018

@author: swagatam
'''
from Color_node_freq import Color_Node 

def color_bfs(initial):
    start_node=Color_Node(initial,None)
    visited=[]
    fringe=[]
    #visited.append(start_node.state)
    current_node=None
    fringe.append(start_node)
    c=0
    flag=0
    x_cord=0
    y_cord=0
    while fringe :
        moves=[]
        c=c+1
        current_node=fringe.pop(0)
        temp_current_node_state=current_node.state.copy()
        visited.append(temp_current_node_state)
        #print("before",visited)
        print("Node count",c,"current state is",current_node.state)
        if(Color_Node.goal_state_check(Color_Node,current_node.state)==0):
            flag=1
            print("goal state is \n")
            print(current_node.state)
            print("goal state reached \n")
            print("Max number of iterations: ",c)
            print("initial state: ",initial)
            break
        else:
            flag=0
            #print("before",current_node.state)
            i=0
            for i in range(0,len(current_node.state)-1):
                for j in range(0,len(current_node.state)-1):
                    if(current_node.state[i][j] == current_node.state[i][j+1]):
                        t1=Color_Node.moves(Color_Node,current_node.state,i,j+1)
                        flag=1 
                        for t in t1:
                            moves.append(t)
                        #print("after move",moves)
                    if(current_node.state[i][j]==current_node.state[i+1][j]) :
                        #print("here")
                        temp=Color_Node.moves(Color_Node,current_node.state,i+1,j)
                        flag=1
                        for t in temp:
                            moves.append(t)
                        #print("moves inn",moves)  
                    if flag==1:
                        break  
                           
                if(flag ==0 and current_node.state[i][len(current_node.state)-1] == current_node.state[i+1][len(current_node.state)-1]):
                    #print("here")
                    #print("prev move",moves)
                    #print("pos",i+1,len(current_node.state)-1)
                    flag=1
                    temp=Color_Node.moves(Color_Node,current_node.state,i+1,len(current_node.state)-1)
                    for t in temp:
                        moves.append(t)
                    break
                
                if flag==1:
                    break
                  
            if(flag==0):
                for j in range(0,len(current_node.state)-1):
                    if(current_node.state[len(current_node.state)-1][j]==current_node.state[len(current_node.state)-1][j+1]):
                        temp=Color_Node.moves(Color_Node,current_node.state,len(current_node.state)-1,j+1)
                    for t in temp:
                        moves.append(t)
                    break
                    
                #if(current_node.state[i][len(current_node.state)-1] == current_node.state[i+1][len(current_node.state)-1]):
                #    moves.append(Color_Node.moves(Color_Node,current_node.state,i,j)
            #print("moves are",moves)
            #print("mid",visited)
            children=[]
            for mv in moves:
                    children.append(Color_Node(mv,current_node))
            #moves=[]       
            for elem in children:
                            #print("visited",visited)
                            #print("state",elem.state)
                            if elem.state not in visited:
                                #print("here")
                                fringe.append(elem)
            #print(fringe)
    if flag==1:
        seq=[]
        #print(current_node.state)    
        while(current_node.parent is not None):
            seq.append(current_node.state)
            current_node=current_node.parent
        seq.reverse()
        #print(seq)
    else:
        print("goal state unreachable")
        
        
def color_dfs(initial):
    start_node=Color_Node(initial,None)
    visited=[]
    fringe=[]
    #visited.append(start_node.state)
    current_node=None
    fringe.append(start_node)
    c=0
    flag=0
    x_cord=0
    y_cord=0
    while fringe :
        moves=[]
        c=c+1
        current_node=fringe.pop()
        temp_current_node_state=current_node.state.copy()
        visited.append(temp_current_node_state)
        #print("before",visited)
        print("Node count",c,"current state is",current_node.state)
        if(Color_Node.goal_state_check(Color_Node,current_node.state)==0):
            flag=1
            print("goal state is \n")
            print(current_node.state)
            print("goal state reached \n")
            print("Max number of iterations: ",c)
            print("initial state: ",initial)
            break
        else:
            flag=0
            #print("before",current_node.state)
            i=0
            for i in range(0,len(current_node.state)-1):
                for j in range(0,len(current_node.state)-1):
                    if(current_node.state[i][j] == current_node.state[i][j+1]):
                        t1=Color_Node.moves(Color_Node,current_node.state,i,j+1)
                        flag=1 
                        for t in t1:
                            moves.append(t)
                        #print("after move",moves)
                    if(current_node.state[i][j]==current_node.state[i+1][j]) :
                        #print("here")
                        temp=Color_Node.moves(Color_Node,current_node.state,i+1,j)
                        flag=1
                        for t in temp:
                            moves.append(t)
                        #print("moves inn",moves)  
                    if flag==1:
                        break  
                           
                if(flag ==0 and current_node.state[i][len(current_node.state)-1] == current_node.state[i+1][len(current_node.state)-1]):
                    #print("here")
                    #print("prev move",moves)
                    #print("pos",i+1,len(current_node.state)-1)
                    flag=1
                    temp=Color_Node.moves(Color_Node,current_node.state,i+1,len(current_node.state)-1)
                    for t in temp:
                        moves.append(t)
                    break
                
                if flag==1:
                    break
                  
            if(flag==0):
                for j in range(0,len(current_node.state)-1):
                    if(current_node.state[len(current_node.state)-1][j]==current_node.state[len(current_node.state)-1][j+1]):
                        temp=Color_Node.moves(Color_Node,current_node.state,len(current_node.state)-1,j+1)
                    for t in temp:
                        moves.append(t)
                    break
                    
                #if(current_node.state[i][len(current_node.state)-1] == current_node.state[i+1][len(current_node.state)-1]):
                #    moves.append(Color_Node.moves(Color_Node,current_node.state,i,j)
            #print("moves are",moves)
            #print("mid",visited)
            children=[]
            for mv in moves:
                    children.append(Color_Node(mv,current_node))
            #moves=[]       
            for elem in children:
                            #print("visited",visited)
                            #print("state",elem.state)
                            if elem.state not in visited:
                                #print("here")
                                fringe.append(elem)
            #print(fringe)
    if flag==1:
        seq=[]
        #print(current_node.state)    
        while(current_node.parent is not None):
            seq.append(current_node.state)
            current_node=current_node.parent
        seq.reverse()
        #print(seq)
    else:
        print("goal state unreachable")