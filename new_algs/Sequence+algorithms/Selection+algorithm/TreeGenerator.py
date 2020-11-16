import numpy as np
import pandas as pd
import GraphSearch.featureTree as ft


class TreeGenerator(object):

    def __init__(self):
        pass

    def featureToTree(self, data,startIndex):
        columns = list(data.columns.values)
        columns.remove('diagnosis') #Computing all 30 features require large memory and time
        #columns = columns[startIndex:startIndex+10] #you can compute only 10 per time, and swap


        treeRoot = ft.featureTree(data=[])
        print("Tree generating")
        featuresTree = self.generateChild(treeRoot,columns,[])
        #featuresTree = self.generateChild(treeRoot, ['a','b','c','d'])

        return featuresTree

    def generateChild(self,Node,unUsedColumns,usedSets):
        children = []
        #print(unUsedColumns)
        for c in unUsedColumns:
            data = Node.data + [c]
            #print(data)
            data.sort()
            if(data not in usedSets):
                usedSets.append(data)
                childNode = ft.featureTree(data=data)
                temp = unUsedColumns[:] #cant use tem =unUsedColumns,lazy python just give temp the pointer to original data
                temp.remove(c)
                if(temp):
                    childs = self.generateChild(childNode,temp,usedSets)
                    children.append(childs)
                #print(childs.children)
                #print(len(children))


        Node.children = children
        return Node



