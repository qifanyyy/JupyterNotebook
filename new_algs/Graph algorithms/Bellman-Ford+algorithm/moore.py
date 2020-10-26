#!/usr/bin/env python

def main():
    
    num_nodes = input("Enter the number of nodes: ");   #Taking input from user
    data = [[0 for x in range(num_nodes)] for x in range(num_nodes)]    #Declaring a dynamic matrix
    print("Enter d(j) values. NOTE: Enter 0 if not applicable.")
    
    for i in range(num_nodes):  #Nested for to input data into num_node dimensional matrix
        for j in range(i+1,num_nodes):
            statement = "From node-" + str(i+1) + " to node-" + str(j+1) + ": "  #Defining a print statement
            data[i][j] = input(statement)   #Taking input from user
            if i!=j:
                data[j][i] = data[i][j] #Defining all the elements of the symmetric matrix
    
    dnode = [999 for x in range(num_nodes)] # d(j) values for all the nodes
    address = [[0] for x in range(num_nodes)] # to store address values for all the nodes
    dnode[0] = 0
    address[0][0] = 1
    
    for i in range(num_nodes):  #Runs i from 0 to 5
        for j in range(num_nodes):  #since the matrix is symmetric j can be run from i+1
            if data[i][j] != 0:  #Skipping 0 values
                node_sum = dnode[i] + data[i][j]    #Algorithm
                if node_sum < dnode[j]:  #Algorithm
                    dnode[j] = node_sum  #Algorithm
                    for s in range(len(address[i])):
                        if len(address[i]) != len(address[j]):
                            diff = len(address[i]) - len(address[j])
                            zero_array = [0 for x in range(diff)]
                            address[j].append(zero_array)
                        address[j][s] = address[i][s]
                    address[j].append(j + 1)
                else: continue
            else: continue
    
    for i in range(1,num_nodes):
        print ("[Origin,Destination]= "+ "[1," + str(i+1) + "]" + \
               "\tRoute= " + str(address[i]) + "\tDistance= " + "[" + str(dnode[i]) + "]")
    
if __name__ == '__main__': main()
