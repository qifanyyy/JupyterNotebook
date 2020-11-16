
# Import class droute and broute (part 2) from the Assignment2.py in the same directory.
from Bellman import broute


# Test 1

A = [[0,2,0,1,0,0],[2,0,3,2,0,0],[0,3,0,3,1,5],[1,2,3,0,1,0],[0,0,1,1,0,2],[0,0,5,0,2,0]]
print("########################## TEST 1 ################################")
print("Test Bellman-ford routing algorithm for graph A...")
print("Origin node: 1, Destination node: 5")
print("\n")
route2 = broute()
route2.bellman_ford(A,1,5)
print("vector = " + str(route2.v))
print("cost = " + str(route2.c))
print("\n")


# Test 2
B = [[0,3,2,5,0,0],[3,0,0,1,2,0],[2,0,0,2,0,2],[5,1,2,0,3,0],[0,2,0,3,0,2],[0,0,2,0,2,0]]
print("########################## TEST 2 ################################")
print("Test Bellman-ford routing algorithm for graph B...")
print("Origin node: 4, Destination node: 4")
print("\n")
route2 = broute()
route2.bellman_ford(B, 4, 4)
print("vector = " + str(route2.v))
print("cost = " + str(route2.c))
print("\n")

