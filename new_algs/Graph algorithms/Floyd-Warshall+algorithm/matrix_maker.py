import random

'''
Script for generating random matrices 
for the Floyd-Warshall algorithm
'''

N = input("N = ")
f = open("matrix.txt", "w")
f.write(str(N) + "\n")
for i in range(N):
    for j in range(N):
        f.write(str(int(random.random() + .2) * random.randrange(1, 20)) + ' ')
    f.write("\n")
f.close()
