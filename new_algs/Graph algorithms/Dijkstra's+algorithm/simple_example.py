

class Node:
  def __init__(self, my_id):
    self.neighbors = None
    self.id = my_id
    self.curr_cost = float("inf")
    self.previous = None

  def __str__(self):
    return "Node "+str(self.id)+" Cost: "+self.curr_cost 

if __name__ == "__main__":

  # Setup the graph
  node_list = [Node(i) for i in range(1,7)]
  
  node_list[0].neighbors = [(node_list[1],7),
                            (node_list[2],9),
                            (node_list[5],14)]
  node_list[1].neighbors = [(node_list[0],7),
                            (node_list[2],10),
                            (node_list[3],15)]
  node_list[2].neighbors = [(node_list[0],9),
                            (node_list[1],10),
                            (node_list[3],11),
                            (node_list[5],2)]
  node_list[3].neighbors = [(node_list[1],15),
                            (node_list[2],11),
                            (node_list[4],1)]
  node_list[4].neighbors = [(node_list[3],1),
                            (node_list[5],9)]
  node_list[5].neighbors = [(node_list[0],14),
                            (node_list[2],2),
                            (node_list[4],9)]
  
  # Add all the items to the unevaluated list
  unevaluated = [node for node in node_list]
  evaluated = []
  # start at node 1
  node_list[0].curr_cost = 0
 
  print("Node 1 neighbors")
  print(node_list[0].neighbors)
 
  print("Running Dijkstra's")
  i = 0
  # Run Dijkstra's algorithm
  while len(unevaluated) > 0:
    min_node = min(unevaluated, key=lambda x: x.curr_cost)
    my_cost = min_node.curr_cost
    my_node = min_node
    for neighbor in my_node.neighbors:
      neighbor_node = neighbor[0]
      neighbor_cost = neighbor[1]
      if neighbor_node.curr_cost > my_cost+neighbor_cost:
        neighbor_node.curr_cost = my_cost+neighbor_cost
        neighbor_node.previous = my_node
    # Move this node to the evaluated list
    unevaluated.remove(min_node)
    evaluated.append(min_node)

    print("Unevaluated:")
    print(unevaluated)
    print("Evaluated:")
    print(evaluated)


  # Now that all of the nodes have been evaluated, unwind the stack
  curr_node = node_list[4]  # Node 5 is the end node
  path = []
  while curr_node != None:
    path.append(curr_node)
    curr_node = curr_node.previous

  # Get the order from start to end
  path.reverse()
  path_str = "Path: "
  for item in path:
    path_str+= str(item.id)  +", "
  print(path_str)
