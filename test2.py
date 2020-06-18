import glob
import os
import zipfile
dir_name = "/Users/yuqifan/Documents/github/Jupyter-results/"
extension = ".zip"
import shutil
from shutil import copyfile

os.chdir(dir_name)  # change directory from working dir to dir with files
var = 0
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
