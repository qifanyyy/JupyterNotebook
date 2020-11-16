#!/usr/bin/python3.7
# coding: utf-8

#Library
import numpy as np
import pandas as pd
import time
import os

#Execution time initialization
start_time = time.time()

name = [
    'dsjc125.1.col','dsjc125.5.col','dsjc125.9.col',
    'dsjc250.1.col','dsjc250.5.col','dsjc250.9.col','dsjc256.1.col',
    'dsjc500.1.col','dsjc500.5.col','dsjc500.9.col',
    'dsjc1000.1.col','dsjc1000.5.col','dsjc1000.9.col'
]

for l in range(0,len(name)) :
        
    #Data path
    data_path = "./Pb/" + name[l]

    #Init color data
    data = pd.read_fwf(data_path,names = ['X1', 'X2']) #Load data
    data = data[ data["X1"] == "e"]                  #Only keep e rows

    #Get each rows values
    p = data["X2"].str.split(" ", n = 1, expand = True)
    p = p.values

    summit_number = int (p[:,0][len(p[:,0]) - 1 ])            #Get summit number
    summit_list = [str(i) for i in range (1,summit_number+1)] #List all summit

    #list all links between summit
    link=[]
    for summit in summit_list:
        linked_summit=[]
        for i in range (len(p[:,0])):
            if (p[:,0][i] == summit):
                linked_summit.append(p[:,1][i])
            if (p[:,1][i] == summit):
                linked_summit.append(p[:,0][i])
        link.append(linked_summit)

    #List all connections between all summits in a matrix, 1=linked, 0=not linked
    mat=[]
    for i in range (len(summit_list)):
        row = summit_number * [0]
        for summit in link[i]:
            row[int(summit) - 1] = 1
        mat.append(row)      
    mat = np.array(mat)
    g = mat

    #FUNCTION DEFINITION

    #Return the degree of a given summit
    def deg(summit):
        return(sum(g[summit]))

    #Sort by degree 
    def sort_degree(b):
        summit_list=[i for i in range(len(g))]
        return(sorted(summit_list,key=deg,reverse=b))

    #Main function  
    def dsatur():
        n = np.shape(g)[0]
        color = n*[0]
        
        #List all summits by decreasing degree
        summits_ord = sort_degree(True)
        
        #While there are summits without color    
        while 0 in color:
    
            #Search for summit to draw with the maximum saturation degree
            dsat = n*[0]
            degre_sat_max = 0
            choosed_summit = summits_ord[0]
            
            for i in summits_ord:
                
                #If the summit i is undrawn
                if color[i]==0:
                    vois = link[i]
                
                    #Calculate degree of saturation of summit i
                    neigh_color = []
                    for k in vois:
                        if color[int(k)-1]>0:
                            neigh_color = neigh_color+[color[int(k)-1]]
                    dsat[i] = len(np.unique(neigh_color))
                    
                    #Has i summit the maximum degree of saturation ?
                    if dsat[i]>degre_sat_max :
                        degre_sat_max = dsat[i]
                        choosed_summit = i
            
            #Color of choosed neighbour summit 
            neigh_summit = link[choosed_summit] 
            summit_neigh_color = []    
            for k in neigh_summit:
                summit_neigh_color = summit_neigh_color+[color[int(k)-1]]        
            
            #Choose the smallest color who doesn't still exist in neighbourhood from choosed summit
            j=1
            while j in summit_neigh_color:
                j=j+1
                
            #coloration du summit choisi avec la couleur trouvée ci-dessus
            color[choosed_summit]=j
        
        #print(color)
        print("Minimum number of color for {} is : {}".format(name[l],max(color)))

        #Create solution file for each file
        sol= open("./Sol/sol_"+name[l]+".txt","w+") #create each file
        compt = 1
        
        for y in color:
            sol.write(str(y) + "\n" )
            compt += 1
        sol.close() 


    #Call main function
    dsatur()

#End time of execution
print("--- %s seconds ---" % (time.time() - start_time)) #Almost 30 min to execute the program (1740s with quad 1.9GHz intel i3 CPU)

#Minimum number of color for dsjc125.1.col is : 6
#Minimum number of color for dsjc125.5.col is : 22
#Minimum number of color for dsjc125.9.col is : 51
#Minimum number of color for dsjc250.1.col is : 10
#Minimum number of color for dsjc250.5.col is : 37
#Minimum number of color for dsjc250.9.col is : 92
#Minimum number of color for dsjc256.1.col is : 23
#Minimum number of color for dsjc500.1.col is : 16
#Minimum number of color for dsjc500.5.col is : 65
#Minimum number of color for dsjc500.9.col is : 170
#Minimum number of color for dsjc1000.1.col is : 27
#Minimum number of color for dsjc1000.5.col is : 115
#Minimum number of color for dsjc1000.9.col is : 299
#--- 2094.3220422267914 seconds ---
