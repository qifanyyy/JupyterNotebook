#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:31:16 2018

@author: Lucas Magalhaes
"""
#Import square root calculator
from math import sqrt
#need to import pandas to manage and compute values for the data
import pandas as pd


"""
Writes the log of the clustering steps to a file called log.txt

Takes in the log list
"""
def write_to_file(log):
    FILE = open('log.txt','w')
    for x in log:
        FILE.write(x)
        FILE.write('\n')
    FILE.close
    return


"""
The open_file() function asks the user of the program to input a csv file of
the data. Then it turns the csv file into a pandas dataframe which is useful
to manage and manipulate the data.

Returns a pandas DataFrame with the data
"""
def open_file():
    #For debugging and programming purposes to not type in this every time
    filename = "/Users/Savannah/Documents/Lucas_HW/HW_AG_SHOPPING_CART_v512.csv"
    #Takes input csv file from the user
    #filename = input("place file path for the CSV data: ")
    #creates a pandas DataFrame from the csv file, which contains all data
    df = pd.DataFrame.from_csv(filename)
    #returns the DataFrame
    return df


"""
The cross_correlation() function calculates the cross correlation of all the
attributes of the data and then it parses through it and finds the highest
cross correlation of a specific attribute. This highest correlation value is
used to find 'useless' attributes, since low correlation attributes will not
help to cluster the data together.

Takes in a DataFrame with data
Returns the function clean_data() 
"""
def cross_correlation(dataframe):
    #computes the cross correlation of all the attributes of the data
    cross_corr = dataframe.corr()
    #empty list which will hold the attributes that are not sufficiently
    #correlated to anything else in the data and need to be deleted
    col_to_be_del = []
    
    #iterate all columns of the cross correlation DataFrame
    for x in cross_corr:
        #variable to hold the highest correlation of an attribute
        highest = 0.0
        #iterate over all correlation values of each attribute to another
        for y in cross_corr[x]:
            #if the correlation value is not 1.0, which should be itself and
            #should be skipped since all columns will have 1.0 as the highest
            #value
            if y != 1.0:
                #if highest of this attribute is less than current correlation
                #absolute value
                if highest < abs(y):
                    #Replace highest with the absolute value of the current 
                    #correlation value
                    highest = abs(y)
        #If the highest correlation absolute value of the current attribute 
        #is less than or equal to 0.5 then this attribute should be deleted
        
        #0.5 is an arbitrary value, and is data set dependent
        if highest <= 0.5:
            #Add attribute to the list which holds the names of the attributes
            #that should be deleted
            col_to_be_del.append(x)
    #returns clean_data function with the current DataFrame and the column
    #names that need to be deleted        
    return clean_data(dataframe, col_to_be_del)


"""
The clean_data() function deletes the attributes in the list passed in.

Takes in the DataFrame and a list that has the column names that need to be
dropped from the DataFrame.
Returns the DataFrame with the new set of columns
"""
def clean_data(dataframe, cols_del):
    #Iterate through the list of columns that need to be deleted
    for x in cols_del:
        #drops the columns from the dataframe
        dataframe.drop(x, inplace=True, axis=1)
    #returns the dataframe with the new set of columns
    return dataframe
    

"""
calculate_center_of_mass() function takes in a list of guest ids, which are 
part of the same cluster and the dataframe with the data and it calculates 
the new center of mass of this cluster.
 
Takes in a list of ids that are part of the same cluster and the dataframe that
has all the data
Returns the center of mass of the cluster
"""
def calculate_center_of_mass(ids, dataframe):
    #list that represents the center of mass of the cluster
    center_of_mass = []
    #loops through all the ids
    for x in range(len(ids)):
        #if it is the first iteration
        if x == 0:
            #Then the sum of all the inidividual data point's data is set to
            #the first id
            sum_total = dataframe.loc[ids[x]].tolist()
        #If not the first iteration
        else:
            #Grab the info of the data point
            current_data = dataframe.loc[ids[x]].tolist()
            #then add all the points data
            for y in range(len(sum_total)):
                sum_total[y] += current_data[y]
    #Go through all the dimension of the cluster center point
    for y in range(len(sum_total)):
        #divide all the dimension value by the bumber of data points in the
        #cluster
        center_of_mass.append((sum_total[y]/len(ids)))
    #return the center of mass
    return center_of_mass


"""
the euclidean_dist() function calculates the euclidean distance between two
data points.

Takes in two data points, both as a list that have the dimensions values
"""
def euclidean_dist(a, b):
    #initialize the distance between the two points as 0
    dist = 0
    #Check and make sure both data points have the same amount of dimensions
    if len(a) != len(b):
        raise Exception("Data points do not match")
    #Look through all the dimensions and calculate the euclidean distance
    for i in range(len(a)):
        dist += (a[i] - b[i])**2
    dist = sqrt(dist)
    #Return the distance value
    return dist


"""
The calculate_closest_two_clusters() function goes through the list of clusters
and finds the closest two clusters based on central linkage

Takes in a list of clusters
Returns a tuple with the index of the two closest clusters in the list
"""
def calculate_closest_two_clusters(clusters):
    #Initialize the two closest clusters to 0,0
    closest_two_clusters = (0,0)
    #initialize the closest dist to 0
    min_dist = 0
    #Goes through all the clusters list
    for x in range(len(clusters)):
        #Goes through all the combination of clusters, skipping the dist
        #between the same data point
        for y in range(x+1, len(clusters)):
            #dist is calculated using the euclidean_dist() function
            dist = euclidean_dist(clusters[x][1], clusters[y][1])
            #if it is the first combination, then set the min_dist and the
            #closest clusters to be the fist combination
            if closest_two_clusters == (0,0):
                min_dist = dist
                closest_two_clusters = (x,y)
            #if it is not the fisrt iteration
            else:
                #Check if the current combination has a smaller distance
                if min_dist > dist:
                    #if it does then current combination is set to be the
                    #closest clusters
                    min_dist = dist
                    closest_two_clusters = (x,y)
    #Return tuple with the index of the two closest clusters in the list
    return closest_two_clusters


"""
The clustering function performs the agglomerative clustering

Takes in the dataframe with all data points
"""
def clustering(dataframe):
    #Logs all clustering activity
    log = []
    #List of all clusters, now empty
    clusters = []
    #loops through the DataFrame to initialize all clusters
    for row in dataframe.iterrows():
        #saves the index and the data from a data point into variables
        initial_cluster, data = row
        #Appends the new singleton cluster to the cluster list
        #Each cluster is defined as a tuple:
        #   cluster = ([list of ID from data], [center of mass of cluster])
        clusters.append(([initial_cluster], data.tolist()))
    #Counter for logging purposes
    i = 1
    #While there is still more than one cluster    
    while len(clusters) != 1:
        current_log = str(i) + ". "
        #Find the two closest clusters
        closest_clusters = calculate_closest_two_clusters(clusters)
        #Get the index of the two closest clusters
        index_cluster1 = closest_clusters[0]
        index_cluster2 = closest_clusters[1]
        #pop the first cluster from the list
        cluster1 = clusters.pop(index_cluster1)[0]
        #pop the second cluster from the list, use minus 1 since popping the
        #first cluster will cause the list to have one less item in it
        cluster2 = clusters.pop(index_cluster2 - 1)[0]
        #Add activity to log
        current_log += "cluster " + str(index_cluster1+1) + " with size: " \
                                                + str(len(cluster1))
        current_log += " joined with cluster " + str(index_cluster2+1) + \
                                        " with size: " + str(len(cluster2))
        #Add the second cluster to the first cluster
        new_id_list = cluster1 + cluster2
        #Form the new cluster with the new center of mass
        new_cluster = (new_id_list, calculate_center_of_mass(new_id_list, 
                                                             dataframe))
        #Add center of mass of the new cluster
        current_log += " with center of mass: " + str(new_cluster[1])
        #Add the new cluster to the list of clusters
        clusters.insert(index_cluster1,new_cluster)
        #Add current log to log list
        log.append(current_log)
        #increase counter
        i += 1
    write_to_file(log)
    return

"""
Main function, controls the program flow
"""
def main():
    df = open_file()
    df = cross_correlation(df)
    clustering(df)  
#Calls the main function
main()
