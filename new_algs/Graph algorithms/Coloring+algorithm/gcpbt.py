import time

# starting time
start = time.time()

n=0
def is_safe(n, graph, colors, c):
    # Iterate trough adjacent vertices
    # and check if the vertex color is different from c
    for i in range(n):
        if graph[n][i] and c == colors[i]: return False
    return True

# n = vertex nb
def graphColoringUtil(graph, color_nb, colors, n):
    # Check if all vertices are assigned a color
    if color_nb+1 == n :
        return True

    # Trying differents color for the vertex n
    for c in range(1, color_nb+1):
        # Check if assignment of color c to n is possible
        if is_safe(n, graph, colors, c):
            # Assign color c to n
            colors[n] = c
            # Recursively assign colors to the rest of the vertices
            if graphColoringUtil(graph, color_nb, colors, n+1): return True
            # If there is no solution, remove color (BACKTRACK)
            colors[n] = 0
            colors[n] = 0
#We test the algorithm for the following graph and test whether it is 3 colorable:

#   (3)---(2)
#    |   / |
#    |  /  |
#    | /   |
#   (0)---(1)

vertex_nb = 5
# nb of colors
color_nb = 4
# Initiate vertex colors
colors = [0] * vertex_nb

graph = [
	[0,0,1,1,0],
	[0,0,0,1,1],
	[1,0,0,0,1],
	[1,1,0,0,0],
	[0,1,1,0,0],
]

#beginning with vertex 0
if graphColoringUtil(graph, color_nb, colors, 0):
    print()
else:
    print ("No solutions")

#sleeping for 1 second to get 10 seconds runtime
time.sleep(1)

# program body ends

# end time
end = time.time()

tt=end-start
# total time taken

print("Backtracking Algorithm : %f" %tt)
print()
