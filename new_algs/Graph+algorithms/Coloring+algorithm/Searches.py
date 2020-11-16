'''
Created on Aug 22, 2018

@author: swagatam
'''
from Node import Node
from test.test_typing import Founder

def bfs(initial,goal):
    #print(goal)
    start_node=Node(initial,None,None)
    visited=[]
    fringe=[]
    #visited.append(start_node.state)
    current_node=None
    fringe.append(start_node)
    c=0
    flag=0
    while fringe:
        moves=[]
        c=c+1
        current_node=fringe.pop(0)
        visited.append(current_node.state)
        #print(c)
        print("Node count",c,"current state is",current_node.state)
        if(current_node.state==goal):
            flag=1
            print("goal state reached \n")
            print("total number of iterations: ",c)
            break
        else:
            #print(current_node)
            moves=Node.moves(Node,current_node)
            #print(moves)
            children=[]
            for mv in moves:
                if mv=="left":
                    state=Node.left(Node,current_node.state)
                    left_child=Node(state,current_node,"left")
                    children.append(left_child)
                if mv=="right":
                    state=Node.right(Node,current_node.state)
                    right_child=Node(state,current_node,"right")
                    children.append(right_child)
                if mv=="up":
                    state=Node.up(Node,current_node.state)
                    up_child=Node(state,current_node,"up")
                    children.append(up_child)
                if mv=="down":
                    state=Node.down(Node,current_node.state)
                    down_child=Node(state,current_node,"down")
                    children.append(down_child)
            #break
            for elem in children:
                #print(elem.state)
                if elem.state not in visited:
                    fringe.append(elem)
    if flag==1:
        seq=[]    
        while(current_node.parent is not None):
            seq.append(current_node.move)
            current_node=current_node.parent
        seq.reverse()
        print("goal state sequence: ",seq)
        print("Maximum depth reached: ",len(seq))
    else:
        print("goal state unreachable")
        
def dfs(initial,goal):
    #print(goal)
    start_node=Node(initial,None,None)
    visited=[]
    fringe=[]
    #visited.append(start_node.state)
    current_node=None
    fringe.append(start_node)
    c=0
    flag=0
    while fringe:
        moves=[]
        c=c+1
        current_node=fringe.pop()
        visited.append(current_node.state)
        #print(c)
        print("Node count",c,"current state is",current_node.state)
        if(current_node.state==goal):
            flag=1
            print("goal state reached \n")
            print("total number of iterations: ",c)
            break
        else:
            #print(current_node)
            moves=Node.moves(Node,current_node)
            #print(moves)
            children=[]
            for mv in moves:
                if mv=="left":
                    state=Node.left(Node,current_node.state)
                    left_child=Node(state,current_node,"left")
                    children.append(left_child)
                if mv=="right":
                    state=Node.right(Node,current_node.state)
                    right_child=Node(state,current_node,"right")
                    children.append(right_child)
                if mv=="up":
                    state=Node.up(Node,current_node.state)
                    up_child=Node(state,current_node,"up")
                    children.append(up_child)
                if mv=="down":
                    state=Node.down(Node,current_node.state)
                    down_child=Node(state,current_node,"down")
                    children.append(down_child)
            #break
            for elem in children:
                #print(elem.state)
                if elem.state not in visited:
                    fringe.append(elem)
    if flag==1:
        seq=[]    
        while(current_node.parent is not None):
            seq.append(current_node.move)
            current_node=current_node.parent
        seq.reverse()
        print("here")
        print(seq)
        print("Maximum depth reached: ",len(seq))
    else:
        print("goal state unreachable")
        
def astar(initial,goal):
    #print(goal)
    start_node=Node(initial,None,None,0)
    visited=[]
    fringe=[]
    #visited.append(start_node.state)
    current_node=None
    fringe.append(start_node)
    c=0
    flag=0
    while fringe:
        moves=[]
        c=c+1
        #print(fringe.pop().heuristic)
        fringe.sort(key= lambda x: x.heuristic, reverse=False)
        current_node=fringe.pop(0)
        visited.append(current_node.state)
        #print(c)
        print("Node count",c,"current state is",current_node.state)
        if(current_node.state==goal):
            flag=1
            print("goal state reached \n")
            print("total number of iterations: ",c)
            break
        else:
            #print(current_node)
            moves=Node.moves(Node,current_node)
            #print(moves)
            children=[]
            for mv in moves:
                if mv=="left":
                    state=Node.left(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    left_child=Node(state,current_node,"left",heuristic)
                    children.append(left_child)
                if mv=="right":
                    state=Node.right(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    right_child=Node(state,current_node,"right",heuristic)
                    children.append(right_child)
                if mv=="up":
                    state=Node.up(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    up_child=Node(state,current_node,"up",heuristic)
                    children.append(up_child)
                if mv=="down":
                    state=Node.down(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    down_child=Node(state,current_node,"down",heuristic)
                    children.append(down_child)
            #break
            #children.sort(key=Node.heuristic, reverse=False)
            for elem in children:
                #print(elem.state)
                if elem.state not in visited:
                    fringe.append(elem)
    if flag==1:
        seq=[]    
        while(current_node.parent is not None):
            seq.append(current_node.move)
            current_node=current_node.parent
        seq.reverse()
        print("goal state sequence: ",seq)
        print("Maximum depth reached: ",len(seq))
    else:
        print("goal state unreachable")
 
     
def idastar(initial,goal):
    global flag
    flag=0
    threshold=Node.calculate_misplaced_tiles(Node,initial,goal)
    count=0
    start_node=Node(initial,None,None,0)
    
    def search(current_node,g,threshold,goal,count):
        global flag
        heuristic=g + Node.calculate_misplaced_tiles(Node,current_node.state,goal)
        if heuristic > threshold:
            return heuristic
        if current_node.state==goal:
            seq=[]
            while(current_node.parent is not None):
                seq.append(current_node.move)
                current_node=current_node.parent
            seq.reverse()
            print("total number of iterations: ",count)
            print(" goal state sequence is",seq)
            print("Maximum depth reached: ",len(seq))
            return "found"
        min=99999
        moves=Node.moves(Node,current_node)
        children=[]
        for mv in moves:
                if mv=="left":
                    state=Node.left(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    left_child=Node(state,current_node,"left",heuristic)
                    children.append(left_child)
                if mv=="right":
                    state=Node.right(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    right_child=Node(state,current_node,"right",heuristic)
                    children.append(right_child)
                if mv=="up":
                    state=Node.up(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    up_child=Node(state,current_node,"up",heuristic)
                    children.append(up_child)
                if mv=="down":
                    state=Node.down(Node,current_node.state)
                    heuristic = Node.calculate_misplaced_tiles(Node,current_node.state,state) + Node.calculate_misplaced_tiles(Node,state,goal)
                    down_child=Node(state,current_node,"down",heuristic)
                    children.append(down_child)
        
        for elem in children:
            count=count+1
            print("Node count is",count,"node state is :",elem.state)
            t=search(elem, g + Node.calculate_misplaced_tiles(Node,current_node.state,elem.state), threshold, goal,count)
            if t == "found" :
                #print(elem.state)
                #if flag==0:
                #    seq=[]
                #    while(elem.parent is not None):
                #        seq.append(elem.move)
                #        elem=elem.parent
                #    seq.reverse()
                #    print(" goal state sequence is",seq)
                #    flag=1
                return "found"
            if t< min:
                min=t
        return min
    
    while True:
        t= search(start_node,0,threshold,goal,count=count+1)
        if t== "found":
            print("goal state reached at threshold value :",threshold)
            #print("No of iterations: ",count)
            break
        if t==-1:
            print("gaol state unrechable")
            break
        threshold=t
    
    
    
        
        

        