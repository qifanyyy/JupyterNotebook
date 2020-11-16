import numpy
import math
import random
import networkx as nx
# Change as necessary
#myfile = "Never.pvalued.csv"
#myfile = "corrP.csv"

# Number of iterations (change as necessary)
iters = 100000

# Distance when running the shortest path
def distance(a, b, adj):
   #if (adj[a][b] == 0):
   #   return 1
   #else:
   return -math.log(abs(adj[a][b]))

# Centrality function (subject to change)
# a is correlation with left neighbor
# b is correlation with right neighbor
def f(a, b):
   return (a+b)/2.0

def minSpanForest(m, n):
 #print dir(nx)
 G=nx.Graph()
 G.add_nodes_from((0,n-1))
 for i in range(n):
   for j in range(n):
     if (m[i][j] != 0):
        G.add_edge(i, j, weight=distance(i,j,m))
     elif (i == j):
        G.add_edge(i, j, weight=1)
        

 T=nx.minimum_spanning_tree(G)
 C=nx.connected_components(T)
 L= list(C)
 return L

def makeE(msf, originalM, n):
   def component(index):
      for i in range(k):
         if (index in msf[i]):
            return i
      return -1

   # Make a k x k matrix e
   k = len(msf)
   e = []
   for i in range(k):
      ec = []
      for j in range(k):
         ec.append(0)
      e.append(ec)

   totaledges = 0.0
   
   for i in range(n):
      for j in range(n):
         if (originalM[i][j] != 0):
            if (component(i) != -1 and component(j) != -1):
               e[component(i)][component(j)] += 1
            totaledges += 1

   for i in range(k):
      for j in range(k):
         e[i][j] /= totaledges
   return e

def makeQ(e):
   k = len(e)
   q = 0
   for i in range(k):
      ai = 0
      for j in range(k):
         ai += e[i][j]
      q += (e[i][i] - ai*ai)
   return q


class CommunityDetectionPlugin:
   def input(self, filename):
      filestuff = open(filename, 'r')

      # Get the first line (names)
      firstline = filestuff.readline()
      self.bacteria = firstline.split(',')
      if ('\"\"' in self.bacteria):
         self.bacteria.remove('\"\"')
      self.n = len(self.bacteria)
      #inf = float("infinity")
      # Make the identity matrix I
      # and the adjacency matrix A
      # and the positive matrix P
      # and the negative matrix N
      self.m = []
      for line in filestuff:
         mc = []
         contents = line.split(',')
         for i in range(1, self.n+1):
            value = float(contents[i])
            mc.append(value)
         self.m.append(mc)

      # Check to make sure all entries (i, i) are 0
      for i in range(self.n):
         self.m[i][i] = 0

      # Save the original for later
      self.originalM = []
      for i in range(self.n):
         originalMC = []
         for j in range(self.n):
            originalMC.append(self.m[i][j])
         self.originalM.append(originalMC)
 
      # Create removed edges adj matrix
      self.removedE = []
      for i in range(self.n):
         removedEC = []
         for j in range(self.n):
            removedEC.append(0)
         self.removedE.append(removedEC)  

   def run(self):
      # Shortest path table (updated by Dijkstra's Algorithm)
      lastQ = 0
      done = False
      while (not done):
       table = []
       marks = []
       through = []
       centrality = []
       for i in range(self.n):
         table.append([])
         for j in range(self.n):
            table[i].append(math.inf)
         marks.append(False)
         through.append([])
         for j in range(self.n):
            through[i].append(-1)
         # MODIFIED TMC 3/8/15
         #centrality.append(0)
         centrality.append([])
         for j in range(self.n):
            centrality[i].append(0)
      
      # Run Dijkstra for each node
       for i in range(self.n):
         # Set the first visited node to i
         node1 = i
      
         # Initialize all table entries to infinity for i
         # Unmark all vertices
         # Initialize all "through" vertices to -1 (none)
         for j in range(self.n):
            table[i][j] = math.inf
            marks[j] = False
            through[i][j] = -1
      
         table[i][node1] = 0  # Node has distance zero with itself
         while (True):
            # Mark the visited node
            marks[node1] = True
            # Run Dijkstra
      
            # Initialize a large minimum distance, and a negative minimum node
            mindist = math.inf
            minnode = -1
 
            # Look at all neighbors of the visited node
            # Any whose distance is less than what is in the table, update it
            for k in range(self.n):
               # If there is an edge from the visited node to k,
               # and the distance from the visited node to k plus i to the visited node is smaller
               # than the current minimum distance from i to k, update the table.
               if ((self.m[node1][k] != 0) and distance(node1, k, self.m)+table[i][node1] < table[i][k]):
                  table[i][k] = distance(node1, k, self.m)+table[i][node1]
                  through[i][k] = node1
      
            for k in range(self.n):
            	 if (marks[k] == False and table[i][k] < mindist):
                  mindist = table[i][k]
                  minnode = k
      
            # No more nodes to visit, jump out
            if (minnode == -1):
                break
      
            # Make this the new node
            node1 = minnode
       
      #############################################################


       # Zero edges
       zeroedge = []
       for i in range(self.n):
         zeroedge.append(True)
         for j in range(self.n):
            if (table[i][j] != math.inf and table[i][j] != 0):
               zeroedge[i] = False

       # At this point, all tables should be populated
       # Pick two random nodes, and get the shortest path between them
       # Increment the centrality of every node along the path
       for i in range(iters):
         node1 = random.randint(0, self.n-1)
         node2 = random.randint(0, self.n-1)
         if (not zeroedge[node1]):
          while (table[node1][node2] == math.inf or table[node1][node2] == 0):
            node2 = random.randint(0, self.n-1) 
            
          while (through[node1][node2] != node1):
               centrality[through[node1][node2]][node2] += abs(self.m[through[node1][node2]][node2])
               node2 = through[node1][node2]
          centrality[node1][node2] += abs(self.m[node1][node2])
      
      
       # Find the maximum edge
       done = True
       maxcent = 0
       maxI = -1
       maxJ = -1
       for i in range(self.n):
         for j in range(self.n):
            if (centrality[i][j] > maxcent):
               maxI = i
               maxJ = j
               maxcent = centrality[i][j]
               done = False
       # Print edge (i, j)
       #print "(", bacteria[maxI].strip(), ", ", bacteria[maxJ].strip(), "): ", maxcent

       # Remove edge (i, j)
       self.removedE[maxI][maxJ] = self.m[maxI][maxJ]
       self.m[maxI][maxJ] = 0
       self.m[maxJ][maxI] = 0

       # TMC 3/14
       # Minimum spanning forest
       # Should define the number of communities in our graph
       MSF = minSpanForest(self.m, self.n)
       E = makeE(MSF, self.originalM, self.n)
       Q = makeQ(E)
       #print Q
       # We break when Q hits a local max, indicating a good division
       #if (Q < lastQ):
       #   done = True
       #lastQ = Q

   def output(self, filename):
      g = open(filename, "w")

      # Write title line
      line = "\"Status\","
      for i in range(self.n-1):
         line += self.bacteria[i].strip() + ','
      line += self.bacteria[self.n-1].strip()
      g.write(line+"\n")

      # Write adjacency matrix
      for i in range(self.n):
         line = "\"Community\","
         for j in range(self.n-1):
            line += str(self.removedE[i][j]) + ","
         line += str(self.removedE[i][self.n-1])
         g.write(line+"\n")
