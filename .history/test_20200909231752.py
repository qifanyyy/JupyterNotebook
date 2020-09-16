# import bs4
# import requests


# response = requests.get("https://en.wikipedia.org/wiki/List_of_algorithms")

# if response is not None:
#     html = bs4.BeautifulSoup(response.text, 'html.parser')

#     titles = html.select("h4")
#     print(len(titles))
#     paragraphs = html.select(".mw-headline")
#     for para in paragraphs:
#         if len(para.text)<50:
#             print(para.text)
#             subtitles= para.select("ul>li>a")
#             # print(subtitles.text)
import bs4
import requests
import pprint
from collections import defaultdict
from bs4 import BeautifulSoup

# response = requests.get("https://en.wikipedia.org/wiki/List_of_algorithms")

with open('algo_list(1).html', 'r') as f:

    contents = f.read()
    
    soup = BeautifulSoup(contents, 'lxml')
    # for i in range(100):
    #     if soup.h2!=  None:
    #         print(soup.h2)
    # print(soup.h2.text)
    # print(soup.li.text)
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
        # print(f'{tag.name}: {tag.text}')
    # root = soup.html
    # root_childs = [e.name for e in root.children if e.name is not None]
    # print(root_childs)
result2 = {}
for i, k in result.items():
    result2[i]=k    
for i, k in result.items():
    if len(k)==0:
        result2.pop(i)
# result2 = {}
# for i, k in result.items():
#     result2[i]=k
for i, k in result2.items():
    # pass
    print("key: "+i)
    for h in k:
        print ("   value: "+h)
    # if i == "Networking[edit]":
    #     print (result2["Networking[edit]"])
import os 
import shutil  
newpath ='/Users/yuqifan/Desktop/test'
# Source path  
source = ''
  
# Destination path  
destination = ''
for i in result2.keys():
    newpath1=newpath+"/"+i
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)    
# import os
for i,v in result2.items():
    for h in v:
        if any(x.startswith(h) for x in os.listdir('/Users/yuqifan/Desktop/test/')):
            source = newpath+"/"
            destination = newpath+"/"+i+"/"
            dest = shutil.move(source, destination) 
    