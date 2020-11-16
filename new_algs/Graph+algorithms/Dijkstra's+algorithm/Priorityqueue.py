# Priority queue class where lowest key is removed and order of arc traversal is decided.


class PriorityQueue:

    def __init__(self):
        import sys as sy
        self.maxvalue = sy.maxsize  # constant declared here for use in code
        self.PQ = {}  # PQ stored in dictionary

    # Start node distance is 0 as distance a-a =0
    # All other nodes set to maxint so they may be updated to smaller values when shorter path to them is found.
    # Done as each node must already exist for algorithm to run, and so must have a default value larger than real value
    def setup_pq(self, nodes, start, end):
        for node in nodes:  # for each node
            if node == start:  # if its the start node (start user defined)
                self.PQ[node] = 0  #
            else:
                self.PQ[node] = self.maxvalue
        return self.PQ

    def lowest_value(self):  # Method returns the node of shortest value
        shortest_length = self.maxvalue
        priority_key = ""  # priority key will be one keys in graph , a string.
        for key in self.PQ:
            if self.PQ[key] < shortest_length:  # if length in pq less than current shortest length
                shortest_length = self.PQ[key]  # new shortest length now becomes shortest
                priority_key = key  # priority key is now node with shortest length
        del self.PQ[priority_key] # remove key from pq so next key can be used
        return priority_key
