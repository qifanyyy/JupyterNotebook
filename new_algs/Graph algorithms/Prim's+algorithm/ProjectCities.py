from copy import deepcopy as dc
import requests as rs
from cmath import sqrt
import json
import folium
from folium.plugins import MarkerCluster


def max_of_list_in_list(Graph):
    maxElement = int(-100)
    for i in range(len(Graph)):
        if max(Graph[i])>maxElement:
            maxElement = max(Graph[i])
    return maxElement

#########################################################################################

def searchMin_Prims(Graph, visited):                             # Prims start
    min = max_of_list_in_list(Graph)
    for i in visited:
        graph_temp = enumerate(Graph[i])
        for j, elem in graph_temp:
            if elem<min and j not in visited:
                min = elem
                index_res = j
    return [min, index_res]

def Prims(Graph):
    visitPlan = list()
    for i in range(1, len(Graph)):
        visitPlan.append(i)
    visited, result = [0], [0]
    for i in visitPlan:
        weight, j = searchMin_Prims(Graph, visited)
        result.append(weight)
        visited.append(j)
    return result                                                  # Prims End

#########################################################################################

def Kruskal(Graph):                     #as input i get already sorted Graph in form of list [index_1, index_2, Distance]. Graph is sorted by Distance
    result=list()
    visitPlan = dict()
    for i in range(0, len(Graph)):
        visitPlan[i] = set([i])
    for i in range(len(Graph)):
        edge_start, edge_end = Graph[i][0], Graph[i][1]
        check = visitPlan[edge_start].intersection(visitPlan[edge_end])
        if not check:
            temp = visitPlan[edge_start].union(visitPlan[edge_end])
            visitPlan[edge_start], visitPlan[edge_end] = temp, temp
            result.append([edge_start, edge_end])
            for i in visitPlan[edge_end]:
                visitPlan[i] = temp
    return result

#########################################################################################

paa={'country':'UK','maxRows':'300', 'type':'json', 'username':"premium", 'cities':'cities1000'}
r =rs.get('http://api.geonames.org/search?', paa)
list_of_cities = list(list())
file_json = open('data_cities.json', 'w')
file_json.write(r.text)                                  #json with cities and inf ab them
data = r.json()                                          #creating all needed lists and files
data_temp = dc(data)


for i in data['geonames']:                               # list of cities with alt and lng
    list_temp = list()
    list_temp.append(i['toponymName'])
    list_temp.append(i['lat'])
    list_temp.append(i['lng'])
    list_of_cities.append(list_temp)

#########################################################################################

    map = folium.Map([53.139499, -1.685177], zoom_start=8, tiles='CartoDBdark_matter')              # doing all the map stuff
    marker_cluster = MarkerCluster().add_to(map)
    for i in data['geonames']:
        coor_temp = list()
        coor_temp.append(i['lat'])
        coor_temp.append(i['lng'])
        folium.CircleMarker(location=coor_temp, popup=i['toponymName'], radius=7, fill_color='ffa8af', color='white', icon=folium.Icon(color='gray')).add_to(marker_cluster)

#########################################################################################
                                                                                                    # If Prims Algorithm this part
Graph_prim = list(list())                                                                           # just preparations such as creating graph of distances
for i in data['geonames']:
    row_temp = list()
    for j in data_temp['geonames']:
        row_temp.append(float(((float(i['lat'])-float(j['lat']))**2 + (float(i['lng']) - float(j['lng']))**2)**.5))
    Graph_prim.append(row_temp)
result_prim = Prims(Graph_prim)

for i in range(len(Graph_prim)):                                                                    # using the obtained data in creating roads between cities
    for j in range(len(Graph_prim[i])):                                                             # exactly Prim
        if Graph_prim[i][j] in result_prim:
            points_to_connect_temp = list(list())
            temp_point_1 = (float(list_of_cities[i][1]), float(list_of_cities[i][2]))
            temp_point_2 = (float(list_of_cities[j][1]), float(list_of_cities[j][2]))
            coords_for_line  = [temp_point_1, temp_point_2]
            folium.PolyLine(locations = coords_for_line).add_to(map)

#########################################################################################

# Graph_Kruskal = list(list())                                                        #Kruskal's Algorithm Preparation(creating needed as input graph.)
# i_temp = int(0)
# for i in data['geonames']:
#     j_temp = int(0)
#     for j in data_temp['geonames']:
#         temp_list = list()
#         temp_list.append(i_temp)
#         temp_list.append(j_temp)
#         temp_list.append(float(((float(i['lat'])-float(j['lat']))**2 + (float(i['lng']) - float(j['lng']))**2)**.5))
#         Graph_Kruskal.append(temp_list)
#         j_temp+=1
#     i_temp+=1
# Graph_Kruskal.sort(key = lambda x:x[2])
# result_Kruskal = Kruskal(Graph_Kruskal)


map.save('map.html')
file_json.close()
