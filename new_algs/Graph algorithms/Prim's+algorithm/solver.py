# Put your solution here.

import networkx as nx
import random

def solve(client):
    client.end()
    client.start()

    graph = client.G
    print(list(graph.edges))

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    a = client.scout(random.choice(non_home), all_students)
    print(a)

    for _ in range(100):
        u, v = random.choice(list(client.G.edges()))
        client.remote(u, v)

    client.end()