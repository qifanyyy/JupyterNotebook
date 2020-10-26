def inp():
#Method to get input in proper format
  ver = int(input("Enter Number of Vertex: "))
  #Number of Vertices is taken as input
  graph,cv,weight = [],[],[]
  for temp in range(ver): 
    con = int(input("Enter Number of Connections to 0th Vertex: "))
    #Number of Connections to 0th Vertex is taken as input
    y,z = [],[]
    for x in range(con):
      inpt = input().split()
      y.append(int(inpt[0]))
      z.append(int(inpt[1]))
    cv.append(y)
    weight.append(z)
    graph.append(cv)
    graph.append(weight)
    #Graph is a list containing both connected vertex and weight
  return graph



def dijkstra(graph,source):
#Method to implement dijkstra algorithm
  dist,Q = [],[]
  for v in range(len(graph[0])):
    dist.append(float("inf"))
    Q.append(v)
  dist[source]  = 0

  while len(Q) > 0:
  #While Q is not empty
    m = float("inf")
    u=0
    d = []
    #To find Minimum distance from nodes 
    for p in Q:
      d.append(dist[p])
    for p in Q:
      if(dist[p]==min(d)):
        u = p
    Q.remove(u)


    def leng(u,v):
      if (v not in graph[0][u]):
        return float("inf")
      else:
        g = graph[0][u].index(v)
        return graph[1][u][g]

    for v in graph[0][u]:
      alt = dist[u] + leng(u,v)
      #To find shorter path to v
      if alt < dist[v]:
        dist[v] = alt
  return dist

def bfs(graph,source):
#Method to implement Breadth First Traversal algorithm
  dist,Q, bfsl = [],[],[]
  for v in range(len(graph[0])):
    dist.append(float("inf"))
    Q.append(v)
  dist[source]  = 0
  qli = []
  qli.append(source)

  
  while len(qli) > 0:
  #while qli isnt empty
    m = float("inf")
    u= qli.pop(0)
    bfsl.append(u) #This can be returned if we want path instead of distance

    for v in graph[0][u]:
      if v in Q:
        qli.append(v)
        Q.remove(v) 
        dist[v] = dist[u] + graph[1][u][graph[0][u].index(v)]
      
  return dist #If we want to print path instead of distance we can return bsfl


"""
print(dijkstra(inp(),0))
print(bfs(inp(),0))
"""
