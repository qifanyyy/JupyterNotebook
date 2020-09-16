import bs4
import requests
import pprint
from collections import defaultdict
from bs4 import BeautifulSoup

with open('algo_list(1).html', 'r') as f:

    contents = f.read()
    
    soup = BeautifulSoup(contents, 'lxml')

    most_recent_key=""
    result=defaultdict(list)
    for tag in soup.find_all(['h3', 'li']):
        # if tag.name=="li":
        #     to_con= tag.text.split(':')[0]
        if tag.name=="h3":
            most_recent_key= tag.text.split('[')[0]
            if tag.text not in result:
                tags= tag.text.split('[')[0]
                result[tags]=[]
        elif tag.name!="h3":
            to_con= tag.text.split(':')[0].splitlines()
            for i in to_con:
                i=i.replace(" ", "+")
                result[most_recent_key].append(i)
result2 = {}
for i, k in result.items():
    result2[i]=k    
for i, k in result.items():
    if len(k)==0:
        result2.pop(i)
print(result2)



#####################
# put results in to dictionary
import os 
import shutil  
newpath ='/Users/yuqifan/Desktop/test'
source = ''
destination = ''
for i in result2.keys():
    newpath1=newpath+"/"+i
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)    
# import os
for i,v in result2.items():
    for h in v:
        if any(x.startswith(h) for x in os.listdir('/Users/yuqifan/Desktop/test/')):
            source = newpath+"/"+h+"/"
            destination = newpath+"/"+i+"/"
            dest = shutil.move(source, destination) 
    