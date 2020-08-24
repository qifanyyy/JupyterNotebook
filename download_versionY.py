# #############
# # Libraries #
# #############

# from shutil import copyfile
# import shutil
# import wget
# import time
# import simplejson
# import csv
# import pycurl
# import math
# from io import BytesIO
# import io
# import glob
# import os
# import zipfile
# dir_name = "/Users/yuqifan/Documents/github/Jupyter-results/"
# extension = ".zip"


# #############
# # Constants #
# #############

# URL = "https://api.github.com/search/repositories?q=" #The basic URL to use the GitHub API
# # The personalized query (for instance, to get repositories from user 'rsain')
# QUERY = "jupyternotebook&&extension:ipynb"
# # Different subqueries if you need to collect more than 1000 elements
# SUBQUERIES = ["+created%3A>%3D2020-01-1", "+created%3A<%3D2020-03-15"]
# PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
# DELAY_BETWEEN_QUERYS = 11 #The time to wait between different queries to GitHub (to avoid be banned)
# OUTPUT_FOLDER = "/Users/yuqifan/Documents/GitHub/Jupyter-results/" #Folder where ZIP files will be stored
# OUTPUT_CSV_FILE = "/Users/yuqifan/Documents/GitHub/JupyterNotebook/repositories.csv" #Path to the CSV file generated as output


# #############
# # Functions #
# #############

# def getUrl (url) :
#     ''' Given a URL it returns its body '''
#     buffer = BytesIO()
#     c = pycurl.Curl()
#     c.setopt(c.URL, url)
#     c.setopt(c.WRITEDATA, buffer)
#     c.perform()
#     c.close()
#     body = buffer.getvalue()

#     return body


# ########
# # MAIN #
# ########

# #To save the number of repositories processed
# countOfRepositories = 0

# #Output CSV file which will contain information about repositories
# csvfile = open(OUTPUT_CSV_FILE, 'w')
# repositories = csv.writer(csvfile, delimiter=',')

# #Run queries to get information in json format and download ZIP file for each repository
# for subquery in range(1, len(SUBQUERIES)+1):
#     print( "Processing subquery " + str(subquery) + " of " + str(len(SUBQUERIES)) + " ...")
#     #Obtain the number of pages for the current subquery (by default each page contains 100 items)
#     url = URL + QUERY + str(SUBQUERIES[subquery-1]) + PARAMETERS
#     # print("url = ", url)
#     dataRead = simplejson.loads(getUrl(url))
#     # print("dataread = ", dataRead)
#     # print("dataRead.get('total_count') = ", dataRead.get('total_count'))
#     numberOfPages = int(math.ceil(dataRead.get('total_count')/100.0))
#     #Results are in different pages
#     for currentPage in range(1, numberOfPages+1):
#         print( "Processing page " + str(currentPage) + " of " + str(numberOfPages) + " ...")
#         url = URL + QUERY + str(SUBQUERIES[subquery-1]) + PARAMETERS + "&page=" + str(currentPage)
#         print("url = ", url)
#         dataRead = simplejson.loads(getUrl(url))

#         #Iteration over all the repositories in the current json content page
#         for item in dataRead['items']:
#             #Obtain user and repository names
#             user = item['owner']['login']
#             repository = item['name']
#             repositories.writerow([i.encode() for i in [user, repository]])

#             #Download the zip file of the current project
#             print ("Downloading repository '%s' from user '%s' ..." %(repository,user))
#             url = item['clone_url']
#             fileToDownload = url[0:len(url)-4] + "/archive/master.zip"
#             fileName = item['full_name'].replace("/","#") + ".zip"
#             wget.download(fileToDownload, out=OUTPUT_FOLDER + fileName)

#             #Update repositories counter
#             countOfRepositories = countOfRepositories + 1

#     #A delay between different subqueries
#     if (subquery < len(SUBQUERIES)):
#         print( "Sleeping " + str(DELAY_BETWEEN_QUERYS) + " seconds before the new query ...")
#         time.sleep(DELAY_BETWEEN_QUERYS)

# print ("DONE! " + str(countOfRepositories) + " repositories have been processed.")
# csvfile.close()

# os.chdir(dir_name)  # change directory from working dir to dir with files

# for item in os.listdir(dir_name):  # loop through items in dir
#     if item.endswith(extension):  # check for ".zip" extension
#         file_name = os.path.abspath(item)  # get full path of files
#         zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
#         zip_ref.extractall(dir_name)  # extract file to dir
#         zip_ref.close()  # close file
#         os.remove(file_name)  # delete zipped file

# print("Sucessfully unzipped!")

# for file in glob.glob("**/*.ipynb", recursive=True):
#     copyfile(file, "/Users/qihongchen/desktop/notebooks/"+file.split('/')[-1])

# for file in os.listdir():
#     if os.path.isdir(file):
#         shutil.rmtree(file)

# This script allows to crawl information and repositories from GitHub using the GitHub REST API (https://developer.github.com/v3/search/).
#
# Given a query, the script downloads for each repository returned by the query its ZIP file.
# In addition, it also generates a CSV file containing the list of repositories queried.
# For each query, GitHub returns a json file which is processed by this script to get information about repositories.
#
# The GitHub API limits the queries to get 100 elements per page and up to 1,000 elements in total.
# To get more than 1,000 elements, the main query should be splitted in multiple subqueries using different time windows through the constant SUBQUERIES (it is a list of subqueries).
#
# As example, constant values are set to get the repositories on GitHub of the user 'rsain'.


#############
# Libraries #
#############

import re
from shutil import copyfile
import shutil
import wget
import time
import simplejson
import csv
# import pycurl
import math
from io import BytesIO
import io
import glob
import os
import zipfile
import pathlib
dir_name = "/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/"
extension = ".zip"
import urllib
from urllib.request import urlopen
from http.client import IncompleteRead
#############
# Constants #
#############
def pre_processing():
    list_of_algos = []
    with open("/Users/yuqifan/Documents/GitHub/JupyterNotebook/list_of_algorithms.txt") as f:
        for lines in f.readlines():
            if lines[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                lines = lines[2:]
            if lines[:2] == "o ":
                lines = lines[2:]
            lines = lines.strip()
            for every_word in lines:
                if ":" in lines:
                    lines = lines.split(':')[0]
                if lines not in list_of_algos:
                    if lines[0] not in "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, a b c d e f g h i j k l m n o p q r s t u v w x y z":
                        lines = lines[2:]
                        if "edit" in lines:
                            lines = lines[:-6]
                        list_of_algos.append(lines)
                    else:
                        if "edit" in lines:
                            lines = lines[:-6]
                    if ("algorithm" not in lines) and ("Algorithm" not in lines):
                        lines += " algorithm"
                    list_of_algos.append(lines)

    for index in range(len(list_of_algos)):
        for every_word in list_of_algos[index]:
            if (every_word.isalnum() or every_word.isalpha()):
                if every_word.isascii() or every_word == "'" or every_word == "*":
                    continue
                else:
                    list_of_algos[index] = list_of_algos[index].replace(
                        every_word, ' ')
            else:
                if every_word != "'" and every_word != "*" and every_word != "-":
                    list_of_algos[index] = list_of_algos[index].replace(
                        every_word, ' ')

    # for i in list_of_algos:
    #     print(i)
    with open("output_of_algos.txt", "w") as output:
        output.write(str(list_of_algos))
    return list_of_algos

def write_result():
    print("writing out result...")
    with open("/Users/yuqifan/Documents/GitHub/JupyterNotebook/result.txt", "w") as output:
        for folder in os.listdir(dir_name):
            if os.path.isdir(dir_name + folder + '/'):
                length = len(os.listdir(dir_name + folder + '/'))
                print("alg = ", folder, " its length = ", length)
                output.write(folder + '-------->' + " " + str(length) + "\n")

SUBQUERIES = [
              ["+created%3A>%3D2009-01-1&created%3A<%3D2020-08-30"]]
URL = "https://api.github.com/search/repositories?q=" #The basic URL to use the GitHub API
# The personalized query (for instance, to get repositories from user 'rsain')

# Different subqueries if you need to collect more than 1000 elements
#SUBQUERIES = [["+created%3A>%3D2012-01-1&created%3A<%3D2012-12-31"],["+created%3A>%3D2013-01-1&created%3A<%3D2013-12-31"],["+created%3A>%3D2014-01-1&created%3A<%3D2014-12-31"],["+created%3A>%3D2015-01-1&created%3A<%3D2015-12-31"],["+created%3A>%3D2016-01-1&created%3A<%3D2016-12-31"],["+created%3A>%3D2017-01-1&created%3A<%3D2017-12-31"],["+created%3A>%3D2018-01-1&created%3A<%3D2018-12-31"],["+created%3A>%3D2019-01-1&created%3A<%3D2019-12-31"],["+created%3A>%3D2020-01-1&created%3A<%3D2020-12-31"]]
PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = 11 #The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = "/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/" #Folder where ZIP files will be stored
# OUTPUT_CSV_FILE = "/Users/qihongchen/desktop/JupyterNotebook/repositories.csv" #Path to the CSV file generated as output
downloads = 0

#############
# Functions #
#############
def build_name_list(folder_name):
    name1 = ""
    splitted_list = []
    if ' ' in folder_name:
        splitted_list = folder_name.split(' ')[:-1]
    elif '+' in folder_name:
        splitted_list = folder_name.split('+')[:-1]
    for i in splitted_list:
        if '-' not in i:
            for names in i:
                name1 += names[0]
                break
        else:
            for j in i.split('-'):
                name1 += j[0]
    print(name1)

    name2 = ""
    for i in splitted_list:
        for names in i:
            name2 += names
        name2 += '_'
    name2 = name2[:-1]
    print(name2)

    name3 = ""
    for i in splitted_list:
        for names in i:
            name3 += names
        name3 += '-'
    name3 = name3[:-1]
    print(name3)

    name4 = ""
    count = 0
    for i in splitted_list:
        for names in i:
            if count == 0:
                name4 += names.upper()
                count = 1
            else:
                name4 += names.lower()
        count = 0
    print(name4)
    return [name1, name2, name3, name4]

def getUrl (url) :
    ''' Given a URL it returns its body '''
    # buffer = BytesIO()
    # c = pycurl.Curl()
    # c.setopt(c.URL, url)
    # c.setopt(c.WRITEDATA, buffer)
    # c.perform()
    # c.close()
    # body = buffer.getvalue()
    # # print(body)
    # resp= urlopen(url).read().decode('utf-8')

    return urlopen(url).read().decode('utf-8')

def processing():
    for folder in os.listdir(dir_name):  # loop through folders in algorithms
        # folder = each algorithm
        each_alg = dir_name + folder + '/'
        print("each alg = ", each_alg)
        if os.path.isdir(each_alg):
            for file in os.listdir(each_alg):
                print("zip file handled = ", each_alg + file)
                if file.endswith(extension):  # check for ".zip" extension
                    file_name = each_alg + file  # get full path of files
                    print("file name = ", file_name)
                    try:
                        zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
                        zip_ref.extractall(each_alg+'/')  # extract file to dir
                        zip_ref.close()  # close file
                        # print("extracted already")
                        os.remove(file_name)  # delete zipped file
                    except:
                        os.remove(file_name)
                        pass
    print("Sucessfully unzipped!")
   

    for alg_folder in os.listdir(dir_name): # iterate through all each algs:
        alg_folder = dir_name + alg_folder + '/'
        print("folder = ", alg_folder)
        if os.path.isdir(alg_folder):
            os.chdir(alg_folder)
            for file in glob.glob("**/*.py", recursive=True):
                print('file = ', file)
                if "/" in file:
                    try:
                        print("move from ", os.getcwd()+file, " to ", alg_folder)
                        shutil.move(os.getcwd() + '/' + file, alg_folder)
                    except shutil.Error:
                        print("duplicate deleted...")
                        os.remove(file)
                        pass
    print("done processing 2nd part")
    

    for each_alg in os.listdir(dir_name):
        path = dir_name + each_alg + '/'
        if os.path.isdir(path):
            for thing in os.listdir(path):
                thing = path + thing
                if os.path.isdir(thing):
                    shutil.rmtree(thing)
                elif not thing.endswith(".py"):
                    os.remove(thing)
    print("done removing all non python files.")
    for each_alg in os.listdir(dir_name):
        alg_path = dir_name + each_alg + '/'
        if os.path.isdir(alg_path):
            for py_file in os.listdir(alg_path):
                try:
                    score = 0
                    print("opening file = ", os.path.join(alg_path, py_file))
                    with open(os.path.join(alg_path, py_file), 'r', encoding = 'latin1') as f:
                        content = f.read()
                        print("each_alg = ", each_alg)
                        new_name_list = build_name_list(each_alg)
                        print("new_name_list = ", new_name_list)
                        for name in new_name_list:
                            if name in content or "implementation" in content.lower() or "algorithm" in content.lower():
                                score += 1
                    if score == 0:
                        os.remove(alg_path+py_file)
                except IsADirectoryError:
                    pass

########
# MAIN #
########

#To save the number of repositories processed
countOfRepositories = 0

# #Output CSV file which will contain information about repositories
# csvfile = open(OUTPUT_CSV_FILE, 'w')
# repositories = csv.writer(csvfile, delimiter=',')

#Run queries to get information in json format and download ZIP file for each repository
terms = pre_processing()[0:3]
for term in terms:
    for subquery in range(1, len(SUBQUERIES)+1):
        downloads = 0
       # print("Processing subquery " + str(subquery) + " of " + str(len(SUBQUERIES)) + " ...")
        #Obtain the number of pages for the current subquery (by default each page contains 100 items)
       # print("building url")
        if ' ' in term:
            term = term.replace(' ', "+")
        QUERY = term+"&extension:py"
        # print("new qUERY = ",QUERY)
        url = URL + QUERY + str(SUBQUERIES[0]) + PARAMETERS
        # print("url = ", url)
        dataRead = simplejson.loads(getUrl(url))
        if dataRead.get('total_count') != None:
            numberOfPages = int(math.ceil(dataRead.get('total_count')/100.0))
            for currentPage in range(1, numberOfPages+1):
                time.sleep(5)
               # print( "Processing page " + str(currentPage) + " of " + str(numberOfPages) + " ...")
                url = URL + QUERY + str(SUBQUERIES[0]) + \
                    PARAMETERS + "&page=" + str(currentPage)
                dataRead = simplejson.loads(getUrl(url))

                #Iteration over all the repositories in the current json content page
                try:
                    for item in dataRead['items']:
                        #Obtain user and repository names
                        user = item['owner']['login']
                        repository = item['name']
                        # repositories.writerow([i.encode() for i in [user, repository]])

                        #Download the zip file of the current project
                        # print ("Downloading repository '%s' from user '%s' ..." %(repository,user))
                        url = item['clone_url']
                        fileToDownload = url[0:len(url)-4] + "/archive/master.zip"
                        fileName = item['full_name'].replace("/","#") + ".zip"
                        try:
                            if not os.path.exists("//Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/"):
                                os.mkdir("/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/")
                            if not os.path.exists("/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/" + str(term)+'/'):
                                os.mkdir("/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/" + str(term)+'/')
                            try:
                                wget.download(
                                    fileToDownload, out="/Users/yuqifan/Documents/GitHub/JupyterNotebook/algorithms/" + str(term)+'/')
                                downloads += 1
                            except IncompleteRead:
                                pass
                            # print("\nnow i ve downloaded zip = ", downloads)
                            if downloads == 1500:
                                break
                        except urllib.error.URLError:
                            pass
                        #Update repositories counter
                        countOfRepositories = countOfRepositories + 1
                except KeyError:
                    pass
                if downloads == 1500:
                    break

            #A delay between different subqueries
        time.sleep(5)






print("all downloaded zip....")

processing()
write_result()

