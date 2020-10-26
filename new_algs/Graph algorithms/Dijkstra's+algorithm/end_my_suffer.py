from collections import defaultdict
from heapq import *

def search(roads, frm, to):
    # Initializing dictionary / adjacency matrix
    # Constructing clear data
    dictionary = defaultdict(list)
    for i, j, k in roads:
        dictionary[i].append((k, j))
        dictionary[j].append((k, i))
    # Heap queue
    # Taking records of each visited node and also distance
    # for the final (optimized) path
    q, visited, dist = [(0, frm,())], set(), {frm: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 in visited: continue

        visited.add(v1)
        path += (v1,)
        # if v1 (current node) is goal then return
        if v1 == to: return (cost, path)
    
        for c, v2 in dictionary.get(v1, ()):
            if v2 in visited: continue
            
            # Min - Max distance algorithm
            # to find the shortest path
            if v2 not in dist or cost+c < dist[v2]:
                dist[v2] = cost+c
                heappush(q, (cost+c, v2, path))

    return float("Infinity") # If there is no path available


if __name__ == "__main__":
    # Data for dictionary / adjacency matrix
    # (i,j,k)
    roads = [
        ("0", "1", 118),
        ("0", "5", 292),
        ("1", "5", 174),
        ("1", "6", 161),
        ("2", "3", 53),
        ("2", "4", 215),
        ("2", "5", 76),
        ("3", "4", 235),
        ("3", "5", 87),
        ("4", "5", 292),
        ("5", "6", 18)
    ]

    print("Welcome")
    place= ["0 - Aquaria Aquarium" ,
    "1 - Big Fish Natural Museum",
    "2 - City Hall",
    "3 - Deep Ones Movie Theater",
    "4 - Elder Park",
    "5 - Fhtagn Mall",
    "6 - Great Old Ones Concert Hall"]

    print(place)
    start=(input("Where are you?"))
    finish=(input("Where do you want to go?"))

    frm=str(start)
    to=str(finish)

    batuhan= search(roads, frm, to)
    print("The shortest path from {} to {} is [{}] with a distance of {} " .format(
        frm,
        to,
        batuhan[1],
        batuhan[0]
        )
    )