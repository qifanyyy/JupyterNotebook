#!/usr/bin/python
#********************************************************************
# Name        : Jeffrey Allen
# Date        : 5/25/2016
# Description : Yoddle triangle puzzle
# 
# Write a program in a language of your choice to find the MAXIMUM 
# total from top to bottom in triangle.txt, a text file containing 
# a triangle with 100 rows. Send your solution and resume to 
# [123456 AT yodle dot com], replacing 123456 with the maximum sum 
# for the triangle.

# Bellman ford algorithm
# Purdy good explanation:
#   http://www.cs.cmu.edu/~avrim/451f13/lectures/lect1001.pdf

#********************************************************************
import os

rel_file_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(rel_file_path, "triangle.txt")) as f:
    triangle = [map(int, line.rstrip().split(' ')) for line in f]

for row in reversed(triangle):
    for index in range(0,len(row)):
        if max_val < row[index]:
            max_val = row[index]
            index = index


