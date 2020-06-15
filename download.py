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


#############
# Constants #
#############

URL = "https://api.github.com/search/repositories?q=" #The basic URL to use the GitHub API
# The personalized query (for instance, to get repositories from user 'rsain')
QUERY = "jupyternotebook&&extension:ipynb"
# Different subqueries if you need to collect more than 1000 elements
SUBQUERIES = ["+created%3A>%3D2020-01-1", "+created%3A<%3D2020-03-15"]
PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = 11 #The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = "/Users/yuqifan/Documents/GitHub/Jupyter-results/" #Folder where ZIP files will be stored
OUTPUT_CSV_FILE = "/Users/yuqifan/Documents/GitHub/JupyterNotebook/repositories.csv" #Path to the CSV file generated as output


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


########
# MAIN #
########

#To save the number of repositories processed
countOfRepositories = 0

#Output CSV file which will contain information about repositories
csvfile = open(OUTPUT_CSV_FILE, 'w')
repositories = csv.writer(csvfile, delimiter=',')

#Run queries to get information in json format and download ZIP file for each repository
for subquery in range(1, len(SUBQUERIES)+1):
    print( "Processing subquery " + str(subquery) + " of " + str(len(SUBQUERIES)) + " ...")
    #Obtain the number of pages for the current subquery (by default each page contains 100 items)
    url = URL + QUERY + str(SUBQUERIES[subquery-1]) + PARAMETERS
    # print("url = ", url)
    dataRead = simplejson.loads(getUrl(url))
    # print("dataread = ", dataRead)
    # print("dataRead.get('total_count') = ", dataRead.get('total_count'))
    numberOfPages = int(math.ceil(dataRead.get('total_count')/100.0))
    #Results are in different pages
    for currentPage in range(1, numberOfPages+1):
        print( "Processing page " + str(currentPage) + " of " + str(numberOfPages) + " ...")
        url = URL + QUERY + str(SUBQUERIES[subquery-1]) + PARAMETERS + "&page=" + str(currentPage)
        print("url = ", url)
        dataRead = simplejson.loads(getUrl(url))

        #Iteration over all the repositories in the current json content page
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
            wget.download(fileToDownload, out=OUTPUT_FOLDER + fileName)

            #Update repositories counter
            countOfRepositories = countOfRepositories + 1

    #A delay between different subqueries
    if (subquery < len(SUBQUERIES)):
        print( "Sleeping " + str(DELAY_BETWEEN_QUERYS) + " seconds before the new query ...")
        time.sleep(DELAY_BETWEEN_QUERYS)

print ("DONE! " + str(countOfRepositories) + " repositories have been processed.")
csvfile.close()

os.chdir(dir_name)  # change directory from working dir to dir with files

for item in os.listdir(dir_name):  # loop through items in dir
    if item.endswith(extension):  # check for ".zip" extension
        file_name = os.path.abspath(item)  # get full path of files
        zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
        zip_ref.extractall(dir_name)  # extract file to dir
        zip_ref.close()  # close file
        os.remove(file_name)  # delete zipped file

print("Sucessfully unzipped!")

for file in glob.glob("**/*.ipynb", recursive=True):
    copyfile(file, "/Users/qihongchen/desktop/notebooks/"+file.split('/')[-1])

for file in os.listdir():
    if os.path.isdir(file):
        shutil.rmtree(file)
