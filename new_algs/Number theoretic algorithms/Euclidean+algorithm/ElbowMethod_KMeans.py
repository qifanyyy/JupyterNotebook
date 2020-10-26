# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:31:17 2017

@author: Jyoti
"""
from scipy import cluster
import pandas as pd
import pylab as plt

#Elbow Method to determine value of K

def readData():
    """Read Data From csv files"""
    f = input("Enter the csv file name from which data is to be read : ")
    csv_data = pd.DataFrame.from_csv(f, index_col = None)
    number_of_attributes=input("Enter the number of attributes for kmeans clustering : ")
    number_of_attributes = int(number_of_attributes)
    attribute_arr=list()
    for i in range(0,number_of_attributes):
        attr = input("Enter the attribute name : ")
        attribute_arr.append(attr)
    attribute_list = csv_data[attribute_arr] 
    return attribute_list

def elbowMethod(data):
    initial = [cluster.vq.kmeans(data,i) for i in range(1,10)]
    plt.plot([var for (cent,var) in initial])
    plt.show()

def main():
    data = readData()
    elbowMethod(data)    

if __name__ == "__main__":
    main()    