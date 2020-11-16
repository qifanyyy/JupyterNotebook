from pyspark import SparkContext
import re
import sys
from operator import add



# def func
def bfs (root):
    with open(sys.argv[1]) as input:
        data = [re.findall(pattern="\w", string=line) for line in input]
    dict1 = dict()

    #start node
    dict1[root] = (0,1)

    # start layer
    cur_layer = [root]
    layer_index = 0
    edge = {}
    while cur_layer:
        layer_index += 1
        next_layer = []
        for parent_node in cur_layer:
            temp = []
            for i in range(len(data)):
                for ele in data:
                    if parent_node in ele:
                        for son_node in ele:
                            if son_node != parent_node and son_node not in cur_layer:
                                next_layer.append(son_node)
                                temp.append(son_node)
                        data.remove(ele)
            edge[parent_node] = temp

        for son_node in next_layer:
            if son_node in dict1:
                dict1[son_node] = (layer_index, dict1[son_node][1]+1)
            else:
                dict1[son_node] = (layer_index,1)
        cur_layer = next_layer

    layerIndex = layer_index-1
    score = {}
    edge_score = {}
    while layerIndex >= 0:
        for key, value in dict1.items():
            if value[0] == layerIndex:
                score[key] = 1
                for i in edge[key]:
                    score[key] += score[i] * dict1[key][1] / dict1[i][1]
                    edge_score[tuple(sorted((key, i)))] = score[i]
        layerIndex -= 1
    return edge_score


if __name__ == '__main__':

    with open(sys.argv[1]) as input:
        data = [re.findall(pattern="\w", string=line) for line in input]
    sc = SparkContext(appName="GNS")
    itemset = set([x for y in data for x in y])
    num = len(itemset)
    rootrdd = sc.parallelize(itemset, num)

    temp_result = rootrdd.map(lambda x: bfs(x)).collect()

    temp_result_list = []
    for i in temp_result:
        for j in i.items():
            temp_result_list.append(j)


    semi_final = sc.parallelize(temp_result_list)
    final_score = semi_final.reduceByKey(add).mapValues(lambda x: int(x) / 2).collect()

    with open(sys.argv[2], 'w') as file:
        for x in sorted(final_score):
            file.write(str(x)[1:-1].replace("'","")+ '\n')
