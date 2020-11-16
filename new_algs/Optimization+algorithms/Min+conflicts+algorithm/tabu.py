"""tabu search algorithm compiled by Giannis Petrousov"""

import os
import copy
import random

def main():
    no_repeats = input("enter number of repeats ")
    tabu_size = input("enter tabu list size ")

    for filez in os.listdir('graphs'):
        #print os.listdir('graphs')j
        print ('solving ', filez)
        connection_graph, color_graph, max_color, tabu_list = create_graphs(filez, tabu_size) #will create the original graph
        print ('initial color_graph ', color_graph)
        if(solve(no_repeats, connection_graph, color_graph, max_color, tabu_list) == True):
            print ('solved')
            print ('final color graph ', color_graph)
        else:
            print ('impossibru')
        #break#this is just a test case, remove to test all filez

def solve(no_repeats, connection_graph, color_graph, max_color, tabu_list):
    no_changes = 0
    for repeat in range(no_repeats):
        no_total_collisions, colliding_nodes = find_total_collisions(connection_graph, color_graph)
        print('no_total_collisions ', no_total_collisions)
        if(no_total_collisions == 0):
            return True
        possible_moves = list() #[node, color, collisions]
        final_moves = list()
        for every_node in colliding_nodes: #else iterate every colliding node to find best solution
            t_colr_graph = copy.deepcopy(color_graph)
            for all_colors in range(0, max_color): #try every possible color
                print ('all_colors ', all_colors)
                t_colr_graph[every_node] = all_colors #change its color
                t_no_collisions = find_total_collisions(connection_graph, t_colr_graph)[0] #find collisions

                print ('t_no_collisions ', t_no_collisions)
                if(t_no_collisions <= no_total_collisions):
                    possible_moves.append([every_node, all_colors, t_no_collisions]) #store as possible move
                    no_total_collisions = t_no_collisions #new collisions number
        #after all nodes are examined
        for i in range(len(possible_moves)):
            if(no_total_collisions == possible_moves[i][2]):
                final_moves.append(possible_moves[i])
        if(len(final_moves) > 0):
            random_move = random.randint(0, len(final_moves) -1)
            #do something about tabu_list
            if(t_colr_graph[final_moves[random_move][0]] not in tabu_list[ final_moves[random_move][0] ]): #if current color not in list
                if(final_moves[random_move][1] in tabu_list[ final_moves[random_move][0] ]): #if new color in list
                    tabu_list[ final_moves[random_move][0] ][ tabu_list[ final_moves[random_move][0]].index(final_moves[random_move][1]) ] = t_colr_graph[final_moves[random_move][0]]# 
                else:
                    tabu_list[ final_moves[random_move][0] ][ random.randint(0,len(tabu_list[ final_moves[random_move][0]]) - 1) ] =  final_moves[random_move][1]#
            ########
            color_graph[final_moves[random_move][0]] = final_moves[random_move][1]#change color permanently
            no_changes += 1
            no_total_collisions = final_moves[random_move][2]
            if(no_total_collisions == 0):
                print ('number of changes ', no_changes)
                return True
        else:
            print ('no possible moves')
            print ('color_graph ', color_graph, '\nchanges ', no_changes)
            return False

                    #color_graph = copy.deepcopy(t_colr_graph)

                    #if(no_total_collisions == 0):
                    #    print 'final color graph ', color_graph
                    #    print 'final collisions ', find_total_collisions(connection_graph, color_graph)[0]
                    #    return True

def create_graphs(filez, tabu_size): #create the original graph
    fd = open('graphs/'+filez, 'r')
    max_color = int(fd.readline().split().pop(0)) #get colors
    #print 'max color ', max_color
    size = fd.readline() #returns tuple
    #print 'size ', size
    connection_graph = [[-1 for i in range(int(size))] for i in range(int(size))] #just another way to declare list 
    color_graph = list(-1 for i in range(int(size)))
    tabu_list = [[-1 for i in range(tabu_size)] for i in range(int(size))]#lines = nodes, rows = colors
    fd.readline() #miss the next one
    for l in fd:
        #print int(l.split()[0]), int(l.split()[1])
        connection_graph[int(l.split()[0])][int(l.split()[1])] = 1 #there is connection
    for i in range(len(color_graph)):
        color_graph[i] = random.randint(0, max_color) #input random color 
        for j in range(tabu_size):
            #input random colors in tabu_list
            ################prepei na mpei elegxos#######
            if(j > max_color): #all colors are in tabu  #
                break                                   #
            if(tabu_list[i][j] == -1):                  #
                rndc = random.randint(0, max_color)     ############################> DELETE IF DOES NoT WORK
                while(rndc in tabu_list[i]):            #
                    rndc = random.randint(0, max_color) #
                tabu_list[i][j] = rndc                  #
            #############################################

            #tabu_list[i][j] = random.randint(0, max_color)
    return connection_graph, color_graph, max_color, tabu_list

def find_total_collisions(connection_graph, color_graph):
    no_collisions = 0
    colliding = list()
    for node in range(len(color_graph) - 1):
        for j in range(node + 1, len(color_graph)):
            #print 'node=',node,'j=',j,'link=',connection_graph[node][j],'colornode=',color_graph[node],'colorJ=',color_graph[j]
            if(connection_graph[node][j] == 1):
                if(color_graph[node] == color_graph[j]):
                    no_collisions += 1
                    #print 'node ', node, 'collides with ',j
                    colliding.append(node) #nodes that collide
    return no_collisions, colliding

if __name__ == '__main__':
    main()
