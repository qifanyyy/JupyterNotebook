from Graph import *
import pdb
              

class graph_creationF(object):

    def __init__(self, weighted, wgraph):
        self.fname = wgraph
        self.wg = weighted
        self.g = Graph()
  
    def get_file(self, which_alg):
        self.g.alg = which_alg
        try:
            #self.fname = raw_input("Enter graph file: ")
            #self.wg = raw_input("Do you want to create a weighted Graph? ")

            file = open(self.fname, 'r')

            if self.wg[0] == 'y' or self.wg[0] == 'Y':
                for line in file:
                    s = line.split()
                    self.g.addEdge(s[0], s[1], int(s[2]))

            elif self.wg[0] == 'n' or self.wg[0] == 'N':
                for line in file:
                    s = line.split()
                    self.g.addEdge(s[0], s[1], 1)

            file.close()

            return self.g
        except:
            print "-----Graph File does not exist-----"
            #self.get_file(which_alg)
		

#get_file()
