__author__ = 'suhas subramanya'
import MapReduce
import re
import sys

mr=MapReduce.MapReduce()

def mapper(record):
    key=record[0]
    value=record[1]
    words = value.split()
    for w in words:
        if re.match('\w', w, flags=0)!=None:
            mr.emit_intermediate(w.lower(),key)


def reducer(key,list_of_values):
    dicts={}
    for each in list_of_values:
        if dicts.has_key(each):
            count=dicts.get(each)
            count+=1
            dicts[each]=count
        else:
            dicts[each]=1
    result=[]
    for keys,value in dicts.iteritems():
        doc=[]
        doc.append(keys)
        doc.append(value)
        result.append((doc))
    mr.emit((key,dicts.__len__(),result))


inputdata= open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)