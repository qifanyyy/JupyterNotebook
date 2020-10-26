# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:57:47 2017

@author: sachin
"""
import sys
import math
from DisjointSet import kruskal  ##Contains Kruskal Function which will calculate the MST
from Graph import load            ##Contains Load, Utilization, Hops and AverageDelay calculations

class Kurskalgo(object):
    
    def main(argv):

        nodelocationlist=[];x = [];y = [];node = [] #list containing X,Y direction and Node value
        #######################LOAD NODE LOCATIONS FROM THE FILE GIVEN################################
        with open("C:\\Users\\sachi\\Desktop\\KB\\assignment\\nodelocationsW17.txt") as f:
            for line in f:
                nodelocationlist.append([int(n) for n in line.strip().split()])
        for pair in nodelocationlist:
            node.append(pair[0]) ##store node values in Node list
            x.append(pair[1])    ##store x direction value in X list
            y.append(pair[2])    ##store y direction value in Y list
            
        src = [];dest = [];weight = []
        val_index_x=0;val_index_y=0
        while val_index_x<len(node): ##loop until for all node values
            index_x=0;index_y=0
            while index_x<len(node):
                value1 = float((x[index_x]-x[val_index_x])*(x[index_x]-x[val_index_x])) ##find x2 value
                value2 = float((y[index_y]-y[val_index_y])*(y[index_y]-y[val_index_y])) ##find y2 value
                weight.append(format(math.sqrt(value1+value2),'.2f'))    ##find the weight using pythagorean formula sqroot(x2+y2)
                src.append(val_index_x+1)
                dest.append(index_x+1)
                index_x+=1
                index_y+=1
            val_index_x+=1
            val_index_y+=1
        
        nodeweightlist = zip(src,dest,weight) # merging src,dest and weight into single list 
            
        ##########_____________KRUSKAL ALGORITHM________________#############
        ##STEP_1: Remove parallel lines from the List            
        rm_parallel_weightlist = []
        rm_parallel_weightlist = set((a,b,c) if a<=b else (b,a,c) for a,b,c in nodeweightlist)
        
        ##STEP_2: Remove loops from the List
        rm_loop_weightlist = []
        for pair in rm_parallel_weightlist:
            if pair[0] != pair[1]:
                rm_loop_weightlist.append(pair)
        
        ##STEP_3: Sort the List in Increasing Order (based on the weight)
        sortedweightlist = []
        sortedweightlist = sorted(rm_loop_weightlist,key=lambda x: float(x[2]))
            
        ##STEP_4: Create Minimal Spanning Tree with the Sorted List
        MST_Final = [];mst_src = [];mst_dest = [];mst_weight = [];final_weight = 0
        ##Call Kruskal Algorithm which will find the minimal spanning Tree
        MST_Final = kruskal(node,sortedweightlist) 
        ##Print MINIMAL SPANNING TREE
        print "Minimal Spanning Tree"
        print "Source\tdestination\tDistance"
        for pair in MST_Final:
            print pair[0],"\t",pair[1],"\t\t",pair[2],"Km"
            mst_src.append(pair[0])
            mst_dest.append(pair[1])
            mst_weight.append(pair[2])
            final_weight += float(pair[2])
        print "MST Weight = ",final_weight
        print
        ##Call Load Function which will find out the load and utilization of the MST
        ##Also print out the Average Hops and Average Delay
        load(zip(mst_src,mst_dest))
            
    if __name__ == "__main__":
        main(sys.argv)