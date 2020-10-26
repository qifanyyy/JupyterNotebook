import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#import pylab

import numpy as np
import heapq
import math
import time
import argparse
plt.ion()

def ObstacleMap():
    plot_x = []
    plot_y =[]
    obs_map = np.zeros((300,200))
    for x in range (0,300):    
        for y in range(0,200):
            #l1= 13*x - y - 140
            #l2= y - 185
            #l3= 7*x + 5*y - 1450
            #l4= 6*x - 5*y + 150
            #l5= 6*x + 5*y - 1050
            #l6= x - y +100
            l1= 13*x - y - 140
            l2= 7*x +5*y - 1110
            l3= x - y + 100
            l4 = 7*x - 5*y + 400
            l5 = 7*x + 5*y - 1450
            l6 = 6*x - 5*y + 150
            l7 = 6*x + 5*y - 1050
            l8 = y-185
            l9 = x -25
            l10 = x - 75
            l11 = y -150

            c = (x - 225)**2 + (y - 150)**2 - (25)**2
            e = 400*((x - 150)**2) + 1600*(y - 100)**2 - 640000
            
            rh1 = 3*x - 5*y -475
            rh2 = 3*x + 5*y -875
            rh3 = 3*x -5*y -625
            rh4 = 3*x + 5*y -725

            #rec1 = 8.66*x - 5*y +77.267
            rec1 = 1.732*x -y + 15.46
            #rec2 = x +2*y -177.37
            rec2 = 0.57*x + y - 96.13
            #rec3 = 8.66*x - 5*y -672.7
            rec3 = 1.732*x -y - 134.54
            rec4 = 0.57*x + y -84.15

            if (l1 >=0 and l2<=0 and l3<=0) or (l4>=0 and l5<=0 and l6<=0 and l7>=0) or (l8<=0 and l9>=0 and l10<=0 and l11>=0) or c<=0 or e<=0 or (rh1>=0 and rh2<=0 and rh3<=0 and rh4>=0) or (rec1>=0 and rec2<=0 and rec3<=0 and rec4>=0):
            #if (l1 >=0 and l2<=0 and l3<=0 and l4<=0 and l5>=0 and l6<=0):
                # print("x:", x)=
                # print("y:", y)
                obs_map[x][y] = 1
                plot_x.append(x)
                plot_y.append(y) 

    for i in range(300):
            plot_x.append(i)
            plot_y.append(0)
            obs_map[i][0] = 1
    for i in range(300):
            plot_x.append(i)
            plot_y.append(200)
            obs_map[i][199] = 1
    for i in range(200):
            plot_x.append(0)
            plot_y.append(i)
            obs_map[0][i] = 1
    for i in range(200):
            plot_x.append(300)
            plot_y.append(i)
            obs_map[299][i] = 1

    #pylab.plot(plot_x,plot_y,".k")
    #pylab.ylim((0,200))
    #pylab.xlim((0,300))
    #plt.plot(plot_x,plot_y,".k")
    #plt.ylim((0,200))
    #plt.xlim((0,300))
    #plt.show()
    return plot_x, plot_y, obs_map



# Defining actions along with their cost
def ActionModel():                
    actions = [[1,0,1], [0,1,1], [-1,0,1], [0,-1,1],
             [1,1,math.sqrt(2)], [1,-1,math.sqrt(2)],
             [-1,-1,math.sqrt(2)], [-1,1,math.sqrt(2)]]
    return actions


def DijkstraAlg(start_node,goal_node, obs_map):
    start = (0,start_node,None)       # cost, node, parent node
    goal = (0,goal_node,None)
    actions = ActionModel()
    
    nodes = []
    path_nodes = []
    heapq.heappush(nodes,(start))
    obs_map[start[1][0]][start[1][1]] = 1
    x_explored=[]
    y_explored=[]

    while len(nodes)>0:
       
        # print(nodes)
        current_node = heapq.heappop(nodes)
        heapq.heappush(path_nodes,current_node)
        x_explored.append(current_node[1][0])
        y_explored.append(current_node[1][1])
        # print("current node")
        # print(current_node)
        # print(path_nodes)

        #x_explored.append(current_node[1][0])
        #y_explored.append(current_node[1][1])

        for new_pos in actions:
            
            node = (current_node[1][0] + new_pos[0],
                             current_node[1][1] + new_pos[1])
            node_cost = current_node[0] + new_pos[2]
            
            
            node_parent = current_node[1]
            
            # Check within range
            #if node[0] > (len(obs_map) - 1) or node[0] < 0 or node[1] > (len(obs_map[0]) -1) or node[1] < 0:
                #continue
        
            if obs_map[node[0]][node[1]] != 0:
                continue
            
            obs_map[node[0]][node[1]] = 1
    
            new_node = (node_cost,node,node_parent)                
            heapq.heappush(nodes,(new_node))


        if current_node[1] == goal[1]:
            print('Goal reached')
            path = []
            #print(path_nodes)
            length = len(path_nodes)
            path.append(path_nodes[length-1][1])
            #print(path)
            parent = path_nodes[length-1][2]
            #print(parent)
            while parent != None: 
                for i in range(length):
                    X = path_nodes[i]
                    #print("xxxxxxxxxxxxxxxxxxxxxxx")
                    #print(X[1])
                    if X[1] == parent:
                        parent = X[2]
                        #print("yyyyyyyyyyyy")
                        #print(parent)
                        path.append(X[1])
            return path,x_explored,y_explored

        #if (len(x_explored))%500 == 0:
        #        #print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        #        plt.plot(x_explored,y_explored, "3c")
        #        plt.pause(0.00001)
    

def main():
    Parser = argparse.ArgumentParser()
    Parser.add_argument('--user_input')
    Parser.add_argument('--animation')
    
    Args = Parser.parse_args()
    user_input=int(Args.user_input)
    animation=int(Args.animation)
    #print(user_input)
    if user_input==1:
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        start_x = int(input('Enter the x-coordinate of start point: '))        
        start_y = int(input('Enter the y-coordinate of start point: '))        
        goal_x = int(input('Enter the x-coordinate of goal point: '))        
        goal_y = int(input('Enter the y-coordinate of goal point: '))        
    else: 
        start_x = 5
        start_y = 5
        goal_x = 295
        goal_y = 195

    start_time = time.time()
    start_node = (start_x, start_y)
    goal_node = (goal_x, goal_y)

    plot_x, plot_y,obs_map = ObstacleMap()

    if start_x < 0 or goal_x < 0 or start_x >300 or goal_x >300 or start_y < 0 or goal_y < 0 or start_y >200 or goal_y >200:
        print("Input values not in range.")
    elif start_node in zip(plot_x,plot_y):
        print('Start node is in obstacle space. Please give a different node')
    elif goal_node in zip(plot_x,plot_y) :    
        print('Goal node is in obstacle space. Please give a different node')
    else:
        rev_path,x_explored,y_explored = DijkstraAlg(start_node,goal_node, obs_map)  
        if rev_path == None:
            print("Path could not be found. Check inputs")
        else:
            path = rev_path[::-1]

            end_time = time.time()
            print('Time (in seconds) taken to find the path is: ',abs(end_time - start_time))

            #pylab.plot(plot_x,plot_y,".k")
            #pylab.plot(start_node[0], start_node[1], "Dw")
            #pylab.plot(goal_node[0], goal_node[1], "Dg") 

            plt.plot(plot_x,plot_y,".k")
            plt.plot(start_node[0], start_node[1], "Dw")
            plt.plot(goal_node[0], goal_node[1], "Dg") 

            x_path = [path[i][0] for i in range(len(path))]
            y_path = [path[i][1] for i in range(len(path))]
            
            #animation_start = time.time()
            if animation ==1:
	            for i in range(len(x_explored)):
	                #if (i%500) ==0:
	                #pylab.plot(x_explored[i], y_explored[i], "3c")
	                #pylab.pause(0.00000000000000000000000000000000000001)
	                plt.plot(x_explored[i], y_explored[i], "3c")
	                plt.pause(0.00000000000000000000000000000000000001)
            #animation_end = time.time()
            #print(abs(animation_end - animation_start))
      

            #pylab.plot(x_path,y_path,"-r")
            plt.plot(x_path,y_path,"-r")
            plt.show()
            plt.pause(3)
            plt.close('all')
            #pylab.show()
            #pylab.pause(2)
            #exit()
            #plt.show()
            #pylab.savfig('result.png')
        






if __name__ == '__main__':
    main()

