'''
* Author: Tomoya Tokunaga(mailto: ttokunag@ucsd.edu)
'''

class path_find(object):
    '''
    * a method which search a matrix structure to see if there exists
    * a path between the given two points in a matrix using BFS. returns 
    * True if there exists a path
    * @param grid: a matrix to be searched
    * @param start: start coordinate in the grid
    * @param dest: destination coordinate in the grid
    '''
    def bfs(grid, start=(0,0), dest=(len(grid)-1, len(grid[0])-1)):
        # nodes in visited are prevented from being re-visited
        visited = []
        queue = [start]

        while queue:
            node = queue.pop(0)
            # if a node unvisited search horizontal & vertical direction
            if node not in visited:
                if node[0]-1 >= 0 and grid[node[0]-1][node[1]] == 1:
                    queue.append((node[0]-1, node[1]))
                if node[0]+1 < len(grid) and grid[node[0]+1][node[1]] == 1:
                    queue.append((node[0]+1, node[1]))
                if node[1]-1 >= 0 and grid[node[0]][node[1]-1] == 1:
                    queue.append((node[0], node[1]-1))
                if node[1]+1 < len(grid[0]) and grid[node[0]][node[1]+1] == 1:
                    queue.append((node[0], node[1]+1))
                # the case reaching the destination coordinate
                if dest in queue:
                    return True
           visited.append(node)
        
        return False

    
    '''
    * a method which search a matrix structure to see if there exists
    * a path between the given two points in a matrix using DFS. returns 
    * True if there exists a path
    * @param grid: a matrix to be searched
    * @param start: start coordinate in the grid
    * @param dest: destination coordinate in the grid
    '''
    def dfs(grid, start=(0,0), dest=(len(grid)-1, len(grid[0])-1)):
        # nodes in visited are prevented from being re-visited
        visited = []
        stack = [start]

        while stack:
            node = stack.pop()
            if node not in visited:
                if node[0]-1 >= 0 and grid[node[0]-1][node[1]] == 1:
                    stack.append((node[0]-1, node[1]))
                if node[0]+1 < len(grid) and grid[node[0]+1][node[1]] == 1:
                    stack.append((node[0]+1, node[1]))
                if node[1]-1 >= 0 and grid[node[0]][node[1]-1] == 1:
                    stack.append((node[0], node[1]-1))
                if node[1]+1 < len(grid[0]) and grid[node[0]][node[1]+1] == 1:
                    stack.append((node[0], node[1]+1))
                # the case reaching the destination coordinate
                if dest in stack:
                    return True

            visited.append(node)

        return False
    
    
    
    
    
