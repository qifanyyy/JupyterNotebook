import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import subprocess


def execute():
    Algorithm = subprocess.Popen('java Main', stdout = subprocess.PIPE)
    resultList = []
    for line in Algorithm.stdout:
        if(line=='\n'):
            continue
        decode = line[:-2]
        resultList.append(decode.decode())
    return resultList

        
    

