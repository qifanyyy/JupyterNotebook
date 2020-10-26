from graph import Graph
from shortest_paths import *
from linked_stack import LinkedStack
railSystem = Graph()

eurail = open('eurail.txt','r')
cities = dict()
routes = set()

for line in eurail.readlines():
    s, d, w = line.split(',')
    hours = int(w.split(':')[0])
    minutes = int(w.split(':')[1])
    routes.add((s,d,hours*60+minutes))
    cities.setdefault(s)
    cities.setdefault(d)

# print(routes)

for city in cities:
    cities[city] = railSystem.insert_vertex(city)

# print(len(cities))

# for vertex in railSystem.vertices():
    # print(vertex)

for route in routes:
    s,d,D = route
    railSystem.insert_edge(cities[s],cities[d],D)

counts = 0
flag = False

for source in cities:
    for destination in cities:
        if source is destination:
            flag = True
        if flag and source is not destination :
            #print("(",source,destination)
            route = railSystem.get_edge(cities[source],cities[destination])
            # if route is not None:
            #     print(route)
            #     counts += 1
    flag = False

durations = shortest_path_lengths(railSystem,cities['London'])
paths = shortest_path_tree(railSystem,cities['London'],durations)
print(paths)

# counts = 0
# for city, duration in durations.items():
#     # if duration != float('inf'):
#         print(city.element(), str(duration//60)+'h', str(duration%60)+'m')
#         counts += 1
# print(counts)
# for city, route in paths.items():
#     print(city.element(), route.opposite(city).element())
#
# visual_graph = open('example.gv','w')
# path_cities = LinkedStack()
# current_stop = cities['Rhodes']
# path_cities.push(current_stop)
# while current_stop!=cities['London']:
#     current_stop = paths[current_stop].opposite(current_stop)
#     path_cities.push(current_stop)
#
# visual_graph.write('graph{\n')
# while not path_cities.is_empty() and path_cities.top() is not cities['Bari']:
#     current_stop = path_cities.pop()
#     next_stop = path_cities.top()
#     duration = railSystem.get_edge(current_stop, next_stop).element()
#     visual_graph.write(str(current_stop)+'--'+str(next_stop)+'[label="'+str(duration//60)+'h '+str(duration%60)+'m'+'", len=1.5]\n')
#
# visual_graph.write('}\n')

# for city, route in paths.items():
#     print(city.element(), route.opposite(city).element())
#print(railSystem)
#print(len(railSystem))