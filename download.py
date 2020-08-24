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

from shutil import copyfile
import shutil
import wget
import time
import simplejson
import csv
import pycurl
import math
from io import BytesIO
import io
import glob
import os
import zipfile
dir_name = "/Users/yuqifan/Documents/github/Jupyter-results/"
extension = ".zip"
import urllib
var = 0
#############
# Constants #
#############
SUBQUERIES = [
            #   ["+created%3A>%3D2012-01-1&created%3A<%3D2012-03-30"],
            #   ["+created%3A>%3D2012-04-1&created%3A<%3D2012-06-30"],
            #   ["+created%3A>%3D2012-07-1&created%3A<%3D2012-12-31"],
            #   ["+created%3A>%3D2013-01-1&created%3A<%3D2013-03-31"],
            #   ["+created%3A>%3D2013-04-1&created%3A<%3D2013-06-30"],
            #   ["+created%3A>%3D2013-07-1&created%3A<%3D2013-09-30"],
            #   ["+created%3A>%3D2013-10-1&created%3A<%3D2013-12-31"],
            #   ["+created%3A>%3D2014-01-1&created%3A<%3D2014-03-31"],
            #   ["+created%3A>%3D2014-04-1&created%3A<%3D2014-06-30"],
            #   ["+created%3A>%3D2014-07-1&created%3A<%3D2014-09-30"],
            #   ["+created%3A>%3D2014-10-1&created%3A<%3D2014-12-31"],
            #   ["+created%3A>%3D2015-01-1&created%3A<%3D2015-03-31"],
            #   ["+created%3A>%3D2015-04-1&created%3A<%3D2015-06-30"],
            #   ["+created%3A>%3D2015-07-1&created%3A<%3D2015-09-30"],
            #   ["+created%3A>%3D2015-10-1&created%3A<%3D2015-12-31"],
            #   ["+created%3A>%3D2016-01-1&created%3A<%3D2016-03-31"],
            #   ["+created%3A>%3D2016-04-1&created%3A<%3D2016-06-30"],
            #   ["+created%3A>%3D2016-07-1&created%3A<%3D2016-09-30"],
            #   ["+created%3A>%3D2016-10-1&created%3A<%3D2016-12-31"],
            #   ["+created%3A>%3D2017-01-1&created%3A<%3D2017-03-31"],
            #   ["+created%3A>%3D2017-04-1&created%3A<%3D2017-06-30"],
            #   ["+created%3A>%3D2017-07-1&created%3A<%3D2017-09-30"],
            #   ["+created%3A>%3D2017-10-1&created%3A<%3D2017-12-31"],
            #   ["+created%3A>%3D2018-01-1&created%3A<%3D2018-01-30"],
            #   ["+created%3A>%3D2018-02-1&created%3A<%3D2018-02-30"]]
            #   ["+created%3A>%3D2018-03-1&created%3A<%3D2018-03-30"],
            #   ["+created%3A>%3D2018-04-1&created%3A<%3D2018-04-30"],
            #   ["+created%3A>%3D2018-05-1&created%3A<%3D2018-05-30"],
            #   ["+created%3A>%3D2018-06-1&created%3A<%3D2018-06-30"],
            #   ["+created%3A>%3D2018-07-1&created%3A<%3D2018-07-30"],
            #   ["+created%3A>%3D2018-08-1&created%3A<%3D2018-08-30"],
            #   ["+created%3A>%3D2018-09-1&created%3A<%3D2018-09-30"],
            #   ["+created%3A>%3D2018-10-1&created%3A<%3D2018-10-30"],
            #   ["+created%3A>%3D2018-11-1&created%3A<%3D2018-11-30"],
            #   ["+created%3A>%3D2018-12-1&created%3A<%3D2018-12-30"],
            #   ["+created%3A>%3D2019-01-1&created%3A<%3D2019-01-30"],
            #   ["+created%3A>%3D2019-02-1&created%3A<%3D2019-02-30"],
            #   ["+created%3A>%3D2019-03-1&created%3A<%3D2019-03-30"],
            #   ["+created%3A>%3D2019-04-1&created%3A<%3D2019-04-30"],
            #   ["+created%3A>%3D2019-05-1&created%3A<%3D2019-05-30"],
            #   ["+created%3A>%3D2019-06-1&created%3A<%3D2019-06-30"],
            #   ["+created%3A>%3D2019-07-1&created%3A<%3D2019-07-30"],
            #   ["+created%3A>%3D2019-08-1&created%3A<%3D2019-08-30"],
              ["+created%3A>%3D2019-09-1&created%3A<%3D2019-09-30"],
              ["+created%3A>%3D2019-10-1&created%3A<%3D2019-10-30"],
              ["+created%3A>%3D2019-11-1&created%3A<%3D2019-11-30"],
              ["+created%3A>%3D2019-12-1&created%3A<%3D2019-12-30"],
              ["+created%3A>%3D2020-01-1&created%3A<%3D2020-03-31"],
              ["+created%3A>%3D2020-04-1&created%3A<%3D2020-06-30"]]
URL = "https://api.github.com/search/repositories?q=" #The basic URL to use the GitHub API
# The personalized query (for instance, to get repositories from user 'rsain')
QUERY = "notebook&extension:ipynb"
# Different subqueries if you need to collect more than 1000 elements
#SUBQUERIES = [["+created%3A>%3D2012-01-1&created%3A<%3D2012-12-31"],["+created%3A>%3D2013-01-1&created%3A<%3D2013-12-31"],["+created%3A>%3D2014-01-1&created%3A<%3D2014-12-31"],["+created%3A>%3D2015-01-1&created%3A<%3D2015-12-31"],["+created%3A>%3D2016-01-1&created%3A<%3D2016-12-31"],["+created%3A>%3D2017-01-1&created%3A<%3D2017-12-31"],["+created%3A>%3D2018-01-1&created%3A<%3D2018-12-31"],["+created%3A>%3D2019-01-1&created%3A<%3D2019-12-31"],["+created%3A>%3D2020-01-1&created%3A<%3D2020-12-31"]]
PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = 11 #The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = "/Users/yuqifan/Documents/github/Jupyter-results/" #Folder where ZIP files will be stored
OUTPUT_CSV_FILE = "/Users/yuqifan/Documents/github//repositories.csv" #Path to the CSV file generated as output


#############
# Functions #
#############

def getUrl (url) :
    ''' Given a URL it returns its body '''
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()

    return body

def check_end():
    dirs = "/Users/yuqifan/Documents/github/Jupyter-results/"
    num_files = len(os.listdir(dirs))-1
    print("number files = ", num_files)
    if num_files >= 130000:
        return True
    else:
        return False
        
def processing():
    os.chdir(dir_name)  # change directory from working dir to dir with files
    global var
    for item in os.listdir(dir_name):  # loop through items in dir
        if item.endswith(extension):  # check for ".zip" extension
            file_name = os.path.abspath(item)  # get full path of files
            try:
                zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
                zip_ref.extractall(dir_name)  # extract file to dir
                zip_ref.close()  # close file
                os.remove(file_name)  # delete zipped file
            except:
                pass

    print("Sucessfully unzipped!")

    for file in glob.glob("**/*.ipynb", recursive=True):
        if "/" in file:
            try:
                shutil.move("/Users/yuqifan/Documents/github/Jupyter-results/"+file, "/Users/yuqifan/Documents/github/Jupyter-results/")
            except shutil.Error:
                print("duplicate")
                new_name = file.split('/')[1][:-4]+ "_"+str(var)+".ipynb"
                new_dir = "/Users/yuqifan/Documents/github/Jupyter-results/"+file.split('/')[0] + '/' + new_name
                print("new_dir = ", new_dir)
                os.rename("/Users/yuqifan/Documents/github/Jupyter-results/" + file, new_name)
                print('after rename...')
                var += 1
                try:
                    shutil.move(new_dir, "/Users/yuqifan/Documents/github/Jupyter-results/")
                except shutil.Error:
                    pass

    for file in os.listdir():
        if os.path.isdir(file):
            shutil.rmtree(file)
        elif not file.endswith(".ipynb"):
            os.remove(file)

########
# MAIN #
########

#To save the number of repositories processed
countOfRepositories = 0

#Output CSV file which will contain information about repositories
csvfile = open(OUTPUT_CSV_FILE, 'w')
repositories = csv.writer(csvfile, delimiter=',')

#Run queries to get information in json format and download ZIP file for each repository
for i in SUBQUERIES:
    print("running subquery = ", i[0])
    for subquery in range(1, len(i)+1):
        print( "Processing subquery " + str(subquery) + " of " + str(len(i)) + " ...")
        #Obtain the number of pages for the current subquery (by default each page contains 100 items)
        url = URL + QUERY + str(i[subquery-1]) + PARAMETERS
        # print("url = ", url)
        dataRead = simplejson.loads(getUrl(url))
        # print("dataread = ", dataRead)
        # print("dataRead.get('total_count') = ", dataRead.get('total_count'))
        if dataRead.get('total_count') != None:
            numberOfPages = int(math.ceil(dataRead.get('total_count')/100.0))
            #Results are in different pages
            for currentPage in range(1, numberOfPages+1):
                print( "Processing page " + str(currentPage) + " of " + str(numberOfPages) + " ...")
                url = URL + QUERY + str(i[subquery-1]) + PARAMETERS + "&page=" + str(currentPage)
                dataRead = simplejson.loads(getUrl(url))

                #Iteration over all the repositories in the current json content page
                try:
                    for item in dataRead['items']:
                        #Obtain user and repository names
                        user = item['owner']['login']
                        repository = item['name']
                        repositories.writerow([i.encode() for i in [user, repository]])

                        #Download the zip file of the current project
                        print ("Downloading repository '%s' from user '%s' ..." %(repository,user))
                        url = item['clone_url']
                        fileToDownload = url[0:len(url)-4] + "/archive/master.zip"
                        fileName = item['full_name'].replace("/","#") + ".zip"
                        try:
                            wget.download(fileToDownload, out=OUTPUT_FOLDER + fileName)
                        except urllib.error.URLError:
                            pass
                        #Update repositories counter
                        countOfRepositories = countOfRepositories + 1
                except KeyError:
                    pass

            #A delay between different subqueries
            if (subquery < len(i)):
                print( "Sleeping " + str(DELAY_BETWEEN_QUERYS) + " seconds before the new query ...")
                time.sleep(DELAY_BETWEEN_QUERYS)
        time.sleep(50)
    processing()
    if (check_end()):
        exit(0);


print ("DONE! " + str(countOfRepositories) + " repositories have been processed.")
csvfile.close()


