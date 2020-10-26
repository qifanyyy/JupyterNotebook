
# Steps to generate complete weighted tree

# disjoint sets (track completeness)
# linked list of vertices with their paired edges

# for n vertices
# create vertex in linked list
# generate random connection
# add vertex to disjoint set for linked vertex


# disjoint set structure
# dict for weights
# dict for parents
# set for each representatives members

# adding an item
# parents[item] = item
# weights[item] = item
# representatives[item] = set(item)

# linking item a to b
# parents[a] = b
# weights[b] = weights[b]++
# representatives[b] = b|a
# representatives[a].delete

# check if we're done
# if len(representatives) = 1

# access random set members to create new links
# for x in representatives: do stuff; break;

class UndirectedConnectedWeightedGraph:
    ''' Uses a disjoint set implementation to build a complete graph '''
    weights = {}
    parents = {}
    rep_members = {}

    def __init__(self, numvertices, numedges):
        ''' Create the graph '''
        print "initializing graph"

    def makeSet(self, x):
        ''' Creates an new set '''
        self.weights[x] = 0
        self.parents[x] = x
        self.rep_members[x] = set(x)

    def find(self, node):
        ''' Finds the representative of the specified vertex '''
        if self.parents[x] == x:
            return x
        else:
            return self.find(parents[x])

    def union(self, x, y):
        ''' Merges two sets '''
        xroot = self.find(x)
        yroot = self.find(y)
        if self.weights[xroot] > self.weights[yroot]:
            self.parents[yroot] = xroot
            self.weights[xroot] += 1
            self.rep_members[xroot] = self.rep_members[xroot] | self.rep_members[yroot]
            self.rep_members[yroot].pop()
        else:
            self.parents[xroot] = yroot
            self.weights[yroot] += 1
            self.rep_members[yroot] = self.rep_members[yroot] | self.rep_members[xroot]
            self.rep_members[xroot].pop()

    def done(self):
        return self.rep_members
