import os

num_nodes = raw_input('Enter the number of nodes in the graph: ')
wgraph = raw_input('Enter the graph file: ')
weighted = raw_input('Do you want a weighted graph: ')

i = 0;

g = wgraph.split('_')

while i < int(num_nodes):
    fout = open('input/dijk/'+ g[1] + '/' + str(i) + '_' +  g[1] + '_' + weighted + '.txt' , 'wb')

    fout.write('d\n')
    fout.write(wgraph + '\n')
    fout.write(weighted + '\n')
    fout.write(str(i) + '\n')

    fout.close()

    i += 1
