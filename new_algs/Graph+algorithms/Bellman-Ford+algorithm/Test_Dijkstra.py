
# Import class droute from the Dijkstra.py in the same directory.
from Dijkstra import droute

# Test 1
A = [[0,2,0,1,0,0],[2,0,3,2,0,0],[0,3,0,3,1,5],[1,2,3,0,1,0],[0,0,1,1,0,2],[0,0,5,0,2,0]]
print("########################## TEST 1 ################################")
print("Test Dijkstra routing algorithm for graph A...")
print("Origin node: 3, Destination node: 6")
print("\n")
route1 = droute()
route1.dijkstra (A, 3, 6)
print("vector = " + str(route1.v))
print("cost = " + str(route1.c))
print("\n")


# Test 2
B = [[0,3,2,5,0,0],[3,0,0,1,2,0],[2,0,0,2,0,2],[5,1,2,0,3,0],[0,2,0,3,0,2],[0,0,2,0,2,0]]
print("########################## TEST 2 ################################")
print("Test Dijkstra routing algorithm for graph B...")
print("Origin node: 1, Destination node: 4")
print("\n")
route1 = droute()
route1.dijkstra (B, 1, 4)
print("vector = " + str(route1.v))
print("cost = " + str(route1.c))
print("\n")



