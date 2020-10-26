import random
import sys

#sys.argv[1] could be -u which means 'user'

try:
  if sys.argv[1] == '-u':
    #resp = raw_input("How many iterations would you like to do? ")
    walg = raw_input("Which algorithm will you be using? ")
    wgraph = raw_input("Enter graph file: ")
    weighted = raw_input("Do you want to create a weighted graph? ")
    init_node = raw_input("Starting Node: ")

    if walg[0] == 'a':
      goal_node = raw_input("Goal Node: ")
      random_range = raw_input("Enter the random range: ")

except:
  random.seed()

  #resp = str(1000)
  wgraph = "graphs/gr_n40_d2.txt"
  weighted = 'n'
  walg = 'd'
  init_node = str(random.randint(0, 40))

  if walg[0] == 'a':
    goal_node = str(random.randint(0, 40))

    while goal_node == init_node:
      goal_node = str(random.randint(0, 40))

#for now, with an unweighted graph, 2 is double the weight. 
#  We are planning on using the average of the hop counts

#Then we hopefully will be able to translate that math into the weighted graphs.
    if weighted == 'y':
      random_range = '10'
    else:
      random_range = '2'

#i = 0
#w = ''

gr = wgraph.split("_")
if weighted == 'y':
  w = 'w'
else:
  w = 'uw'

if walg == 'a':
  fout = open("input/astar/" + init_node + "and" + goal_node + "_" + gr[1] + "_" + w + "_rr" + random_range + ".txt", 'wb')
  #fout.write(resp + '\n')

  #while i < int(resp):
  fout.write(walg + '\n')
  fout.write(wgraph + '\n')
  fout.write(weighted + '\n')
  fout.write(init_node + '\n')
  fout.write(goal_node + '\n')
  fout.write(random_range + '\n')
  
  fout.close()

elif walg == 'd':
  fout = open("input/dijk/" + init_node+ "_" + gr[1] + "_" + w  + ".txt", 'wb')
  #fout.write(resp + '\n')

  #while i < int(resp):
  fout.write(walg + '\n')
  fout.write(wgraph + '\n')
  fout.write(weighted + '\n')
  fout.write(str(init_node) + '\n')
  
  fout.close()

else:
  print 'Unrecognizable algorithm\n'
