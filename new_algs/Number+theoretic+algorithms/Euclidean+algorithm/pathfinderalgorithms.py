from queue import Queue, PriorityQueue
import Heuristic as hs

path_list=[]
def traverseback(came_from,end_key,start_pos):
    if came_from[end_key] != start_pos:
        path_list.append(came_from[end_key])
        traverseback(came_from,came_from[end_key],start_pos)
    else:
        return path_list.reverse()
        
def bfs(graph, start, end):
    frontier = Queue()
    frontier.put(start)
    explored = []
    came_from={}

    while True:
        if frontier.empty():
            raise Exception("Queue Downflow")
        current_node = frontier.get()
        explored.append(current_node)

        if current_node == end: #End Mi?
            return came_from

        for node in graph[current_node]:
            if node not in explored:
                came_from[node]=current_node
                frontier.put(node)


def dfs(graph, start, end):
    frontier = [start]
    explored = []
    came_from={}

    while True:
        if len(frontier) == 0:
            raise Exception("Stack Downflow")
        current_node = frontier.pop()
        explored.append(current_node)

        if current_node == end:
            return came_from


        for node in reversed(graph[current_node]):
            if node not in explored:
                came_from[node]=current_node
                frontier.append(node)


def ucs_weight(from_node, to_node, weights=None):

   return weights.get((from_node, to_node), 10e100) if weights else 1


def ucs(graph, start, end, weights=None):
    frontier = PriorityQueue()
    frontier.put((0, start))  
    explored = []
    came_from={}

    while True:
        if frontier.empty():
            raise Exception("Priority Queue Downflow")

        ucs_w, current_node = frontier.get()
        explored.append(current_node)

        if current_node == end:
            return came_from


        for node in graph[current_node]:
            if node not in explored:
                came_from[node]=current_node
                frontier.put((
                    ucs_w + ucs_weight(current_node, node, weights),
                    node
                ))

def aStar(graph, start,end,sxy,exy):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cost_so_far = {}
    came_from = {}
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        
        if current == end:
            break
        
        for next in graph[current]:
            new_cost = cost_so_far[current] + hs.ManhattanDis(sxy[0],sxy[1],exy[0],exy[1]) #2 Different Algortihm
            # new_cost = cost_so_far[current] + hs.EuclideanDis(sxy[0],sxy[1],exy[0],exy[1])


            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + hs.ManhattanDis(sxy[0],sxy[1],exy[0],exy[1]) #2 Different Algorithm
                #priority = new_cost + hs.EuclideanDis(sxy[0],sxy[1],exy[0],exy[1])

                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from