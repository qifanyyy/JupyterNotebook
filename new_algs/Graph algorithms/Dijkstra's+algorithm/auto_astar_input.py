import os
import pdb


wgraph = raw_input("Enter a graph file: ")
weighted = raw_input("Do you want a weighted graph? ")

num_nodes = wgraph.split('_')
num_nodes = num_nodes[1]
num_nodes = num_nodes[1:]
num_nodes = int(num_nodes)

if weighted == 'y':
    w = 'w'
else:
    w = 'uw'


heur_count = 0

while heur_count < 16:
    init_node_count = 0
    while init_node_count < num_nodes - 1:
        goal_node_count = 0
        while goal_node_count < num_nodes:
            if init_node_count == goal_node_count:
                goal_node_count += 1
            
            files = os.listdir('input/astar')
            f = 'input/astar/n'+ str(num_nodes) + '/'  + str(init_node_count) + 'and' + str(goal_node_count)  + '_' + w + '_rr' + str(heur_count) + '.txt'
            
            if f in files:
                continue
            else:
                fout = open(f, 'wb')

                fout.write('a\n')
                fout.write(wgraph + '\n')
                fout.write(weighted + '\n')
                fout.write(str(init_node_count) + '\n')
                fout.write(str(goal_node_count) + '\n')
                #fout.write(str(heur_count))
                fout.write(str(heur_count) + '\n')

                fout.close()


            goal_node_count += 1
        
        init_node_count += 1

    heur_count += 1
