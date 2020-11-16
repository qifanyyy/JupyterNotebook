import time
from input_values import neighbors, colors, nodes
# n = int(input("Enter number of colours : "))
# colors = []
# for i in range(0, n):
#     print("Enter the %d color:" % (i+1))
#     ele = input()
#     colors.append(ele)
# print(colors)
# x = int(input("Enter number of nodes : "))
# nodes = []
# for i in range(0, x):
#     print("Enter the %d node " % (i+1))
#     ele = int(input())
#     nodes.append(ele)
# print(nodes)
# neighbors = {}
# for i in range(0, x):
#     key = nodes[i]
#     print("Enter the number of connections for {%d}:" % key)
#     z = int(input())
#     my_list = []
#     for state in range(0, z):
#         ele = int(input())
#         my_list.append(ele)
#     neighbors.update({key: my_list})
start = time.time()
colors_of_states = {}


def promising(state, color):
    for neighbor in neighbors.get(state):
        color_of_neighbor = colors_of_states.get(neighbor)
        if color_of_neighbor == color:
            return False
    return True


def get_color_for_state(state):
    for color in colors:
        if promising(state, color):
            return color


def main():
    for state in nodes:
        colors_of_states[state] = get_color_for_state(state)
    print()
    print("------------------------------------------")
    print("This is the final colored output graph :: ")
    print(colors_of_states)


main()
time.sleep(1)
end = time.time()
tt = end-start
print()
print("------------------------------------------------")
print("Total time taken to solve the entered graph is :")
print("------------------------------------------------")
print()
print("Greedy Algorithm : %f" % tt)
print()
